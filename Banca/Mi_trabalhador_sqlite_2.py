import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

# Banco de dados SQLite
conn = sqlite3.connect('trabalho_horas_2.db')
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

def atualizar_resultado():
    total_horas = sum(d["horas"] for d in dias_trabalhados.values())
    total_valor_horas = sum(d["horas"] * d["valor_hora"] for d in dias_trabalhados.values())
    total_horas_extra = sum(d["extra"] for d in dias_trabalhados.values())
    total_valor_extra = sum(d["extra"] * d["valor_extra"] for d in dias_trabalhados.values())
    total_global = total_valor_horas + total_valor_extra

    label_total_horas.config(text=f"Total Horas Normais: {total_horas:.2f} h")
    label_total_valor.config(text=f"Valor Horas Normais: {total_valor_horas:.2f} €")
    label_total_extra.config(text=f"Total Horas Extra: {total_horas_extra:.2f} h")
    label_total_valor_extra.config(text=f"Valor Horas Extra: {total_valor_extra:.2f} €")
    label_total_geral.config(text=f"Total a Receber: {total_global:.2f} €")

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

def adicionar_dia():
    data_r = cal.get_date().strftime("%Y-%m-%d")
    if data_r in dias_trabalhados:
        messagebox.showerror("Erro", "Já existe um registro para esse dia.")
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

    dias_trabalhados[data_r] = {
        "horas": h_normais,
        "valor_hora": v_hora,
        "extra": h_extra,
        "valor_extra": v_extra
    }
    salvar_dia(data_r, h_normais, v_hora, h_extra, v_extra)
    atualizar_resultado()
    atualizar_historico()
    messagebox.showinfo("Sucesso", f"Dia {data_r} adicionado com sucesso.")

# --- Configuração da janela ---
janela = tk.Tk()
janela.title("Gestor de Horas de Trabalho")
janela.geometry("700x700")
janela.resizable(False, False)

# Entradas
frame_entrada = ttk.LabelFrame(janela, text="📅 Registrar dia de trabalho")
frame_entrada.pack(padx=10, pady=10, fill="x")

ttk.Label(frame_entrada, text="Data:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
cal = DateEntry(frame_entrada, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
cal.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_entrada, text="Horas Normais:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_horas = ttk.Entry(frame_entrada)
entry_horas.insert(0, "8")
entry_horas.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_entrada, text="Valor €/hora:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_valor_hora = ttk.Entry(frame_entrada)
entry_valor_hora.insert(0, "6.25")
entry_valor_hora.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame_entrada, text="Horas Extra:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_horas_extra = ttk.Entry(frame_entrada)
entry_horas_extra.insert(0, "0")
entry_horas_extra.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(frame_entrada, text="Valor €/hora Extra:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
entry_valor_extra = ttk.Entry(frame_entrada)
entry_valor_extra.insert(0, "0")
entry_valor_extra.grid(row=4, column=1, padx=5, pady=5)

btn_adicionar = ttk.Button(frame_entrada, text="Adicionar dia", command=adicionar_dia)
btn_adicionar.grid(row=5, column=0, columnspan=2, pady=10)

# Seção de totais
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

# Histórico de dias trabalhados
frame_historico = ttk.LabelFrame(janela, text="📜 Histórico de Dias Trabalhados")
frame_historico.pack(padx=10, pady=10, fill="both", expand=True)

colunas = ("data", "horas", "valor_hora", "extra", "valor_extra", "total")
tree = ttk.Treeview(frame_historico, columns=colunas, show='headings', height=10)

tree.heading("data", text="📅 Data")
tree.heading("horas", text="⏱️ Horas")
tree.heading("valor_hora", text="💶 €/Hora")
tree.heading("extra", text="🕒 Extra")
tree.heading("valor_extra", text="💸 €/Extra")
tree.heading("total", text="💰 Total (€)")

for col in colunas:
    tree.column(col, anchor="center", width=100)

tree.pack(fill="both", expand=True, padx=10, pady=10)

# Carregar dados ao iniciar
carregar_dados()
atualizar_resultado()
atualizar_historico()

janela.mainloop()

# Fechar conexão ao fechar o app
conn.close()

