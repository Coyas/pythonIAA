import tkinter as tk
from tkinter import ttk, messagebox

# Criar janela principal
janela = tk.Tk()
janela.title("Simulador de Crédito Pessoal")
janela.geometry("520x800")
janela.resizable(False, False)

# Função de cálculo
def calcular_credito():
    try:
        montante = float(entry_montante.get())
        prazo = int(entry_prazo.get())
        tan = float(entry_tan.get()) / 100  # converter para decimal

        if montante <= 0 or prazo <= 0 or tan <= 0:
            raise ValueError("Os valores devem ser positivos.")

        # Cálculo da prestação mensal
        mensal = (montante * tan / 12) / (1 - (1 + tan / 12) ** -prazo)
        mensal = round(mensal, 2)

        # Imposto do selo (estimado 0.532%)
        imposto_selo = round(montante * 0.00532, 2)

        # Montante total imputado ao consumidor
        mtic = round(mensal * prazo + imposto_selo, 2)

        # TAEG aproximada
        taeg = ((mtic / montante - 1) / (prazo / 12)) * 100
        taeg = round(taeg, 2)

        texto_resultado = (
            f"📊 Resultados:\n\n"
            f"• Prestação mensal: {mensal} €\n"
            f"• Imposto do selo (estimado): {imposto_selo} €\n"
            f"• Montante total a pagar (MTIC): {mtic} €\n"
            f"• TAEG estimada: {taeg} %\n"
        )

        # Atualiza o widget Text
        text_resultado.config(state='normal')  # ativa edição
        text_resultado.delete('1.0', tk.END)   # limpa conteúdo anterior
        text_resultado.insert(tk.END, texto_resultado)  # insere novo texto
        text_resultado.config(state='disabled')  # desativa edição para o usuário

    except ValueError:
        messagebox.showerror("Erro", "Insere apenas valores numéricos válidos e positivos.")

# Instruções
frame_info = ttk.LabelFrame(janela, text="ℹ️ Instruções")
frame_info.pack(padx=10, pady=10, fill="x")

info_label = tk.Label(frame_info, justify="left", anchor="w", text="""
1. Introduz o valor do crédito (1.000 € - 30.000 €)
2. Define o prazo (em meses, até 84)
3. Introduz a TAN (ex: 6.29)

TAN típica: 6.29% a 12.00%
TAEG típica: 7.7% a 14.5%
""")
info_label.pack(anchor="w", padx=10, pady=5)

# Entradas
frame_inputs = ttk.LabelFrame(janela, text="📥 Parâmetros do Crédito")
frame_inputs.pack(padx=10, pady=5, fill="x")

ttk.Label(frame_inputs, text="Montante (€):").pack(pady=5, anchor="w", padx=10)
entry_montante = ttk.Entry(frame_inputs)
entry_montante.pack(padx=10, fill="x")

ttk.Label(frame_inputs, text="Prazo (em meses):").pack(pady=5, anchor="w", padx=10)
entry_prazo = ttk.Entry(frame_inputs)
entry_prazo.pack(padx=10, fill="x")

ttk.Label(frame_inputs, text="TAN (%):").pack(pady=5, anchor="w", padx=10)
entry_tan = ttk.Entry(frame_inputs)
entry_tan.pack(padx=10, fill="x", pady=(5, 10))

# Botão
ttk.Button(janela, text="Calcular Crédito", command=calcular_credito).pack(pady=15)

# Resultados
frame_resultado = ttk.LabelFrame(janela, text="📉 Resultado da Simulação")
frame_resultado.pack(padx=10, pady=10, fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame_resultado)
scrollbar.pack(side='right', fill='y')

text_resultado = tk.Text(frame_resultado, wrap='word', yscrollcommand=scrollbar.set, font=("Arial", 10), bg="#f7f7f7")
text_resultado.pack(padx=10, pady=10, fill='both', expand=True)
text_resultado.config(state='disabled')  # inicializa como não editável

scrollbar.config(command=text_resultado.yview)

# Mensagem inicial
text_resultado.config(state='normal')
text_resultado.insert(tk.END, "📝 Introduza os dados e clique em 'Calcular Crédito'.")
text_resultado.config(state='disabled')

# Iniciar GUI
janela.mainloop()
