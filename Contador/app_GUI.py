import tkinter as tk
import time
import threading

class ContadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contador Infinito")
        self.root.geometry("200x200")

        # Configura para a janela ficar sempre por cima das outras
        self.root.attributes("-topmost", True)

        self.contador = 0  # contador em segundos
        self.contando = False

        # Cor inicial da janela (usando uma cor mais genérica, como branco)
        self.root.configure(bg='white')

        # Label para mostrar o contador no formato HH:MM:SS
        self.label = tk.Label(root, text=self.format_time(self.contador), font=("Helvetica", 20))
        self.label.pack(pady=20)

        # Botão para Start/Stop
        self.botao = tk.Button(root, text="Start", command=self.toggle_contador)
        self.botao.pack()

        # Botão para Resetar o contador
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_contador)
        self.reset_button.pack(pady=10)

        # Inicia o ciclo de troca de cor de fundo baseado no contador
        self.check_color_change()

    def toggle_contador(self):
        """Inicia ou para o contador."""
        if self.contando:
            self.contando = False
            self.botao.config(text="Start")
        else:
            self.contando = True
            self.botao.config(text="Stop")
            threading.Thread(target=self.contador_infinito, daemon=True).start()

    def contador_infinito(self):
        """Função do contador que aumenta de um segundo em segundo."""
        while self.contando:
            time.sleep(1)
            self.contador += 1
            # Atualiza o contador com o formato HH:MM:SS
            self.label.config(text=self.format_time(self.contador))
            self.root.update_idletasks()  # Atualiza a GUI

            # Verifica se precisa mudar a cor do fundo a cada segundo
            self.check_color_change()

    def format_time(self, seconds):
        """Converte o tempo em segundos para o formato HH:MM:SS."""
        horas = seconds // 3600
        minutos = (seconds % 3600) // 60
        segundos = seconds % 60
        return f"{horas:02}:{minutos:02}:{segundos:02}"

    def check_color_change(self):
        """Verifica se o contador atingiu um múltiplo de 20 segundos e muda a cor."""
        # Se o número de segundos for um múltiplo de 20
        if self.contador % 20 == 0:
            self.change_to_red()

    def change_to_red(self):
        """Muda a cor de fundo para vermelho por 2 segundos."""
        self.root.configure(bg='red')  # Muda o fundo para vermelho
        # Depois de 2 segundos, restaura a cor original
        self.root.after(2000, self.restore_color)

    def restore_color(self):
        """Restaura a cor de fundo para o padrão."""
        self.root.configure(bg='white')  # Restaura a cor de fundo para branco

    def reset_contador(self):
        """Reseta o contador para 0 e reinicia a cor de fundo."""
        self.contador = 0  # Reseta o contador
        self.label.config(text=self.format_time(self.contador))  # Atualiza a label para 00:00:00
        self.root.configure(bg='white')  # Restaura a cor de fundo para branco
        if self.contando:
            self.contando = False
            self.botao.config(text="Start")  # Se estava rodando, para o contador

# Criação da janela principal
root = tk.Tk()
app = ContadorApp(root)
root.mainloop()
