import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import sqlite3

# === Banco de Dados ===
conn = sqlite3.connect('trabalhos.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS registos (
        data TEXT PRIMARY KEY,
        horas_normais REAL,
        valor_hora REAL,
        horas_extra REAL,
        valor_extra REAL
    )
''')
conn.commit()

# === Carregar dados do DB ===
dias_trabalhados = {}

def carregar_registos():
    cursor.execute('SELECT * FROM registos')
    for linha in cursor.fetchall():
        data_r, h, vh, he, ve = linha
        dias_trabalhados[data_r] = {
            "horas": h,
            "valor_hora": vh,
            "extra": he,
            "valor_extra": ve
        }

carregar_registos()

# === Funções principais ===
def adicionar_dia():
    hoje = date.today().isoformat()

    if hoje in dias_trabalhados:
        messagebox.showwarning("Dia já registado", f"Já registaste o dia de hoje ({hoje}).")
        return

    trabalhou = var_trabalhou.get()
    try:
        horas_normais = float(entry_horas_normais.get())
        valor_hora = float(entry_valor_hora.get())
        horas_extra = float(entry_horas_extra.get())
        valor_extra = float(entry_valor_extra.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira apenas valores numéricos.")
        return

    if trabalhou == "sim":
        horas = horas_normais
        extras = horas_extra
    else:
        horas = 0
        extras = 0

    # Inserir no dicionário
    dias_trabalhados[hoje] = {
        "horas": horas,
        "valor_hora": valor_hora,
        "extra": extras,
        "valor_extra": valor_extra
    }

    # Salvar no DB
    cursor.execute('''
        INSERT INTO registos (data, horas_normais, valor_hora, horas_extra, valor_extra)
        VALUES (?, ?, ?, ?, ?)
    ''', (hoje, horas, valor_hora, extras, valor_extra))
    conn.commit()

    atualizar_resultado()

def atualizar_resultado():
    total_normais = sum(d["horas"] * d["valor_hora"] for d in dias_trabalhados.values())
    total_extras = sum(d["extra"] * d["valor_extra"] for d in dias_trabalhados.values())
    total_geral = total_normais + total_extras
    total_dias = len(dias_trabalhados)

    resultado.set(f"""
📅 Dias registados: {total_dias}
💼 Total horas normais: {total_normais:.2f} €
⏱️ Total horas extra: {total_extras:.2f} €
💰 Total a receber: {total_geral:.2f} €
""")

# === Interface Gráfica ===
janela = tk.Tk()
janela.title("Gestor de Horas de Trabalho (com DB)")
janela.geometry("500x550")
janela.resizable(False, False)

var_trabalhou = tk.StringVar(value="sim")
resultado = tk.StringVar()
resultado.set("📆 Nenhum registo hoje ainda.")

# Inputs
frame_inputs = ttk.LabelFrame(janela, text="📥 Registo do Dia de Trabalho")
frame_inputs.pack(padx=10, pady=10, fill="x")

ttk.Label(frame_inputs, text=f"Trabalhou hoje ({date.today().isoformat()})?").pack(anchor="w", padx=10, pady=(5, 0))
ttk.Radiobutton(frame_inputs, text="Sim", variable=var_trabalhou, value="sim").pack(anchor="w", padx=20)
ttk.Radiobutton(frame_inputs, text="Não", variable=var_trabalhou, value="nao").pack(anchor="w", padx=20)

ttk.Label(frame_inputs, text="Horas normais trabalhadas (padrão: 8):").pack(anchor="w", padx=10, pady=(10, 0))
entry_horas_normais = ttk.Entry(frame_inputs)
entry_horas_normais.insert(0, "8")
entry_horas_normais.pack(fill="x", padx=10)

ttk.Label(frame_inputs, text="Valor por hora normal (€):").pack(anchor="w", padx=10, pady=(10, 0))
entry_valor_hora = ttk.Entry(frame_inputs)
entry_valor_hora.insert(0, "6.25")
entry_valor_hora.pack(fill="x", padx=10)

ttk.Label(frame_inputs, text="Horas extra (se houver):").pack(anchor="w", padx=10, pady=(10, 0))
entry_horas_extra = ttk.Entry(frame_inputs)
entry_horas_extra.insert(0, "0")
entry_horas_extra.pack(fill="x", padx=10)

ttk.Label(frame_inputs, text="Valor por hora extra (€):").pack(anchor="w", padx=10, pady=(10, 0))
entry_valor_extra = ttk.Entry(frame_inputs)
entry_valor_extra.insert(0, "0")
entry_valor_extra.pack(fill="x", padx=10)

ttk.Button(janela, text="Adicionar Dia", command=adicionar_dia).pack(pady=10)

# Totais
frame_resultado = ttk.LabelFrame(janela, text="📊 Total acumulado")
frame_resultado.pack(padx=10, pady=10, fill="both", expand=True)

label_resultado = tk.Label(frame_resultado, textvariable=resultado, justify="left", anchor="nw", bg="#f7f7f7", font=("Arial", 10), wraplength=460)
label_resultado.pack(padx=10, pady=10, fill="both", expand=True)

# Mostrar valores iniciais
atualizar_resultado()

# Iniciar GUI
janela.mainloop()

