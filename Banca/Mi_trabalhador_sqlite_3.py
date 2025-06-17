import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
import sqlite3

# Banco de dados SQLite
conn = sqlite3.connect('trabalho_horas.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS dias (
    data TEXT PRIMARY KEY,
    horas_normais REAL,
    valor_hora REAL,
    horas_extra REAL,
    valor_hora_extra REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS carteira (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    total_retirado REAL DEFAULT 0
)
''')
cursor.execute("INSERT OR IGNORE INTO carteira (id, total_retirado) VALUES (1, 0)")
conn.commit()

# Dados carregados do DB
dias_trabalhados = {}

def carregar_dados():
    cursor.execute('SELECT * FROM dias')
    rows = cursor.fetchall()
    for data_r, h_normais, v_hora, h_extra, v_extra in rows:
        dias_trabalhados[data_r] = {
            "horas": h_normais,
            "valor_hora": v_hora,
            "extra": h_extra,
            "valor_extra": v_extra
        }

def salvar_dia(data_r, h_normais, v_hora, h_extra, v_extra):
    cursor.execute('''
        INSERT OR REPLACE INTO dias (data, horas_normais, valor_hora, horas_extra, valor_hora_extra)
        VALUES (?, ?, ?, ?, ?)
    ''', (data_r, h_normais, v_hora, h_extra, v_extra))
    conn.commit()

def obter_total_retirado():
    cursor.execute('SELECT total_retirado FROM carteira WHERE id = 1')
    return cursor.fetchone()[0]

def atualizar_total_retirado(novo_valor):
    cursor.execute('UPDATE carteira SET total_retirado = ? WHERE id = 1', (novo_valor,))
    conn.commit()

def atualizar_resultado():
    total_horas = sum(d["horas"] for d in dias_trabalhados.values())
    total_valor_horas = sum(d["horas"] * d["valor_hora"] for d in dias_trabalhados.values())
    total_horas_extra = sum(d["extra"] for d in dias_trabalhados.values())
    total_valor_extra = sum(d["extra"] * d["valor_extra"] for d in dias_trabalhados.values())
    total_global = total_valor_horas + total_valor_extra

    total_retirado = obter_total_retirado()
    saldo_restante = total_global - total_retirado

    label_total_horas.config(text=f"Total Horas Normais: {total_horas:.2f} h")
    label_total_valor.config(text=f"Valor Horas Normais: {total_valor_horas:.2f} €")
    label_total_extra.config(text=f"Total Horas Extra: {total_horas_extra:.2f} h")
    label_total_valor_extra.config(text=f"Valor Horas Extra: {total_valor_extra:.2f} €")
    label_total_geral.config(text=f"Total a Receber: {total_global:.2f} €")
    label_total_retirado.config(text=f"💸 Já Retirado: {total_retirado:.2f} €")
    label_saldo_restante.config(text=f"💼 Saldo Restante: {saldo_restante:.2f} €")

def atualizar_historico():
    for item in tree.get_children():
        tree.delete(item)
    for data_r, dados in sorted(dias_trabalhados.items()):
        total_dia = dados["horas"] * dados["valor_hora"] + dados["extra"] * dados["valor_extra"]
        tree.insert('', 'end', values=(
            data_r,
            f"{dados['horas']:.2f}",
            f"{dados['valor_hora']:.2f}",
            f"{dados['extra']:.2f}",
            f"{dados['valor_extra']:.2f}",
            f"{total_dia:.2f}"
        ))

def limpar_campos():
    entry_horas.delete(0, tk.END)
    entry_horas.insert(0, "8")
    entry_valor_hora.delete(0, tk.END)
    entry_valor_hora.insert(0, "6.25")
    entry_horas_extra.delete(0, tk.END)
    entry_horas_extra.insert(0, "0")
    entry_valor_extra.delete(0, tk.END)
    entry_valor_extra.insert(0, "0")
    cal.set_date(date.today())
    btn_adicionar.config(text="Adicionar dia")
    tree.selection_remove(tree.selection())

def adicionar_ou_atualizar_dia():
    data_r = cal.get_date().strftime("%Y-%m-%d")
    data_atual = date.today()
    data_obj = cal.get_date()

    if data_obj > data_atual:
        messagebox.showerror("Erro", "Não é possível registrar dias futuros.")
        return

    try:
        h_normais = float(entry_horas.get())
        v_hora = float(entry_valor_hora.get())
        h_extra = float(entry_horas_extra.get())
        v_extra = float(entry_valor_extra.get())
        if h_normais < 0 or v_hora < 0 or h_extra < 0 or v_extra < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos e não negativos.")
        return

    if h_normais == 0 and h_extra == 0:
        messagebox.showinfo("Info", "Nenhuma hora trabalhada para este dia.")
        return

    selecionado = tree.selection()
    if selecionado:
        salvar_dia(data_r, h_normais, v_hora, h_extra, v_extra)
        dias_trabalhados[data_r] = {
            "horas": h_normais,
            "valor_hora": v_hora,
            "extra": h_extra,
            "valor_extra": v_extra
        }
        messagebox.showinfo("Sucesso", f"Dia {data_r} atualizado com sucesso.")
    else:
        if data_r in dias_trabalhados:
            messagebox.showerror("Erro", "Já existe um registro para esse dia. Se quiser editar, selecione ele na tabela.")
            return
        dias_trabalhados[data_r] = {
            "horas": h_normais,
            "valor_hora": v_hora,
            "extra": h_extra,
            "valor_extra": v_extra
        }
        salvar_dia(data_r, h_normais, v_hora, h_extra, v_extra)
        messagebox.showinfo("Sucesso", f"Dia {data_r} adicionado com sucesso.")

    atualizar_resultado()
    atualizar_historico()
    limpar_campos()

def on_selecionar_item(event):
    selecionado = tree.selection()
    if not selecionado:
        return
    item = tree.item(selecionado[0])
    data_r, h_normais, v_hora, h_extra, v_extra, _ = item['values']
    cal.set_date(datetime.strptime(data_r, "%Y-%m-%d").date())
    entry_horas.delete(0, tk.END)
    entry_horas.insert(0, h_normais)
    entry_valor_hora.delete(0, tk.END)
    entry_valor_hora.insert(0, v_hora)
    entry_horas_extra.delete(0, tk.END)
    entry_horas_extra.insert(0, h_extra)
    entry_valor_extra.delete(0, tk.END)
    entry_valor_extra.insert(0, v_extra)
    btn_adicionar.config(text="Atualizar dia")

def retirar_dinheiro():
    try:
        valor = float(entry_retirada.get())
        if valor <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Insira um valor válido e positivo para retirar.")
        return

    total_retirado = obter_total_retirado()
    total_receber = sum(
        d["horas"] * d["valor_hora"] + d["extra"] * d["valor_extra"]
        for d in dias_trabalhados.values()
    )

    if valor > (total_receber - total_retirado):
        messagebox.showerror("Erro", "Saldo insuficiente para esta retirada.")
        return

    atualizar_total_retirado(total_retirado + valor)
    messagebox.showinfo("Sucesso", f"{valor:.2f} € retirado da carteira com sucesso.")
    atualizar_resultado()

# --- GUI ---
janela = tk.Tk()
janela.title("Gestor de Horas de Trabalho")
janela.geometry("750x800")
janela.resizable(False, False)

frame_entrada = ttk.LabelFrame(janela, text="📅 Registrar dia de trabalho")
frame_entrada.pack(padx=10, pady=10, fill="x")

# Entradas
labels = ["Data:", "Horas Normais:", "Valor €/hora:", "Horas Extra:", "Valor €/hora Extra:"]
widgets = []

for i, text in enumerate(labels):
    ttk.Label(frame_entrada, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="w")

cal = DateEntry(frame_entrada, width=12, background='darkblue', foreground='white', borderwidth=2,
                date_pattern='yyyy-mm-dd', maxdate=date.today())
cal.grid(row=0, column=1, padx=5, pady=5)

entry_horas = ttk.Entry(frame_entrada)
entry_horas.insert(0, "8")
entry_horas.grid(row=1, column=1, padx=5, pady=5)

entry_valor_hora = ttk.Entry(frame_entrada)
entry_valor_hora.insert(0, "6.25")
entry_valor_hora.grid(row=2, column=1, padx=5, pady=5)

entry_horas_extra = ttk.Entry(frame_entrada)
entry_horas_extra.insert(0, "0")
entry_horas_extra.grid(row=3, column=1, padx=5, pady=5)

entry_valor_extra = ttk.Entry(frame_entrada)
entry_valor_extra.insert(0, "0")
entry_valor_extra.grid(row=4, column=1, padx=5, pady=5)

btn_adicionar = ttk.Button(frame_entrada, text="Adicionar dia", command=adicionar_ou_atualizar_dia)
btn_adicionar.grid(row=5, column=0, columnspan=2, pady=10)

# Totais
frame_totais = ttk.LabelFrame(janela, text="💰 Totais")
frame_totais.pack(padx=10, pady=10, fill="x")

label_total_horas = ttk.Label(frame_totais, text="Total Horas Normais: 0.00 h")
label_total_horas.pack(anchor="w", padx=10, pady=2)
label_total_valor = ttk.Label(frame_totais, text="Valor Horas Normais: 0.00 €")
label_total_valor.pack(anchor="w", padx=10, pady=2)
label_total_extra = ttk.Label(frame_totais, text="Total Horas Extra: 0.00 h")
label_total_extra.pack(anchor="w", padx=10, pady=2)
label_total_valor_extra = ttk.Label(frame_totais, text="Valor Horas Extra: 0.00 €")
label_total_valor_extra.pack(anchor="w", padx=10, pady=2)
label_total_geral = ttk.Label(frame_totais, text="Total a Receber: 0.00 €", font=("Arial", 12, "bold"))
label_total_geral.pack(anchor="w", padx=10, pady=5)

# Carteira
frame_carteira = ttk.LabelFrame(janela, text="💼 Minha Carteira")
frame_carteira.pack(padx=10, pady=10, fill="x")

label_total_retirado = ttk.Label(frame_carteira, text="💸 Já Retirado: 0.00 €")
label_total_retirado.pack(anchor="w", padx=10, pady=2)
label_saldo_restante = ttk.Label(frame_carteira, text="💼 Saldo Restante: 0.00 €", font=("Arial", 11, "bold"))
label_saldo_restante.pack(anchor="w", padx=10, pady=2)

frame_retirar = ttk.Frame(frame_carteira)
frame_retirar.pack(padx=10, pady=5, fill="x")

entry_retirada = ttk.Entry(frame_retirar, width=10)
entry_retirada.pack(side="left", padx=5)
entry_retirada.insert(0, "0")

btn_retirar = ttk.Button(frame_retirar, text="Retirar", command=retirar_dinheiro)
btn_retirar.pack(side="left", padx=5)

# Histórico
frame_historico = ttk.LabelFrame(janela, text="📜 Histórico de Dias Trabalhados")
frame_historico.pack(padx=10, pady=10, fill="both", expand=True)

colunas = ("data", "horas", "valor_hora", "extra", "valor_extra", "total")
tree = ttk.Treeview(frame_historico, columns=colunas, show='headings', height=10)
for col in colunas:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor="center", width=100)
tree.pack(fill="both", expand=True, padx=10, pady=10)
tree.bind("<<TreeviewSelect>>", on_selecionar_item)

# Inicializar tudo
carregar_dados()
atualizar_resultado()
atualizar_historico()

janela.mainloop()
conn.close()
