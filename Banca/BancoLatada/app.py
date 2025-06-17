import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Lógica de banco
class Banco:
    def __init__(self):
        self.conn = sqlite3.connect('banco_app.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contas (
                nome TEXT PRIMARY KEY,
                saldo INTEGER
            )
        ''')
        self.conn.commit()

    def criar_conta(self, nome, saldo=0):
        try:
            self.cursor.execute('INSERT INTO contas (nome, saldo) VALUES (?, ?)', (nome, saldo))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def apagar_conta(self, nome):
        self.cursor.execute('SELECT saldo FROM contas WHERE nome = ?', (nome,))
        row = self.cursor.fetchone()
        if not row:
            return "Conta não existe"
        if row[0] != 0:
            return "Saldo não é zero"
        self.cursor.execute('DELETE FROM contas WHERE nome = ?', (nome,))
        self.conn.commit()
        return "Conta apagada"

    def transferir(self, de, para, valor):
        self.cursor.execute('SELECT saldo FROM contas WHERE nome = ?', (de,))
        saldo_de = self.cursor.fetchone()
        self.cursor.execute('SELECT saldo FROM contas WHERE nome = ?', (para,))
        saldo_para = self.cursor.fetchone()
        if not saldo_de or not saldo_para:
            return "Conta de origem ou destino não existe"
        if saldo_de[0] < valor:
            return "Saldo insuficiente"
        self.cursor.execute('UPDATE contas SET saldo = saldo - ? WHERE nome = ?', (valor, de))
        self.cursor.execute('UPDATE contas SET saldo = saldo + ? WHERE nome = ?', (valor, para))
        self.conn.commit()
        return "Transferência realizada"

    def listar_contas(self):
        self.cursor.execute('SELECT * FROM contas')
        return self.cursor.fetchall()

    def mostrar_saldo(self, nome):
        self.cursor.execute('SELECT saldo FROM contas WHERE nome = ?', (nome,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def fechar(self):
        self.conn.close()


# Interface gráfica
class App:
    def __init__(self, root):
        self.banco = Banco()
        self.root = root
        self.root.title("Banco Fancy 💳")
        self.root.geometry("650x500")
        self.root.configure(bg="#f0f2f5")

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=1, fill="both")

        self.criar_gui_contas()
        self.criar_gui_transferencia()
        self.criar_gui_consulta()

        self.atualizar_lista()

    def criar_gui_contas(self):
        self.tab_contas = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_contas, text="💼 Contas")

        frame = ttk.Frame(self.tab_contas, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="e")
        self.nome_entry = ttk.Entry(frame)
        self.nome_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Saldo Inicial:").grid(row=1, column=0, sticky="e")
        self.saldo_entry = ttk.Entry(frame)
        self.saldo_entry.grid(row=1, column=1)

        ttk.Button(frame, text="Criar Conta", command=self.criar_conta).grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Apagar Conta", command=self.apagar_conta).grid(row=3, column=0, columnspan=2)

        self.lista_contas = tk.Text(frame, height=15, width=60, state="disabled", bg="#fafafa")
        self.lista_contas.grid(row=4, column=0, columnspan=2, pady=10)

    def criar_gui_transferencia(self):
        self.tab_transferencia = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_transferencia, text="🔄 Transferência")

        frame = ttk.Frame(self.tab_transferencia, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="De:").grid(row=0, column=0, sticky="e")
        self.entry_de = ttk.Entry(frame)
        self.entry_de.grid(row=0, column=1)

        ttk.Label(frame, text="Para:").grid(row=1, column=0, sticky="e")
        self.entry_para = ttk.Entry(frame)
        self.entry_para.grid(row=1, column=1)

        ttk.Label(frame, text="Valor:").grid(row=2, column=0, sticky="e")
        self.entry_valor = ttk.Entry(frame)
        self.entry_valor.grid(row=2, column=1)

        ttk.Button(frame, text="Transferir", command=self.transferir).grid(row=3, column=0, columnspan=2, pady=10)

    def criar_gui_consulta(self):
        self.tab_consulta = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_consulta, text="📊 Consultar Saldo")

        frame = ttk.Frame(self.tab_consulta, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nome da Conta:").grid(row=0, column=0, sticky="e")
        self.consulta_nome = ttk.Entry(frame)
        self.consulta_nome.grid(row=0, column=1)

        ttk.Button(frame, text="Consultar", command=self.consultar_saldo).grid(row=1, column=0, columnspan=2, pady=10)

        self.resultado_saldo = tk.Label(frame, text="", font=("Arial", 12), fg="blue")
        self.resultado_saldo.grid(row=2, column=0, columnspan=2)

    def criar_conta(self):
        nome = self.nome_entry.get()
        try:
            saldo = int(self.saldo_entry.get() or 0)
        except ValueError:
            messagebox.showerror("Erro", "Saldo inválido.")
            return
        if self.banco.criar_conta(nome, saldo):
            messagebox.showinfo("Sucesso", f"Conta de {nome} criada.")
            self.atualizar_lista()
        else:
            messagebox.showwarning("Aviso", "Conta já existe.")

    def apagar_conta(self):
        nome = self.nome_entry.get()
        status = self.banco.apagar_conta(nome)
        if status == "Conta apagada":
            messagebox.showinfo("Sucesso", f"Conta de {nome} apagada.")
        elif status == "Saldo não é zero":
            messagebox.showerror("Erro", "A conta tem saldo diferente de zero.")
        else:
            messagebox.showerror("Erro", "Conta não encontrada.")
        self.atualizar_lista()

    def transferir(self):
        de = self.entry_de.get()
        para = self.entry_para.get()
        try:
            valor = int(self.entry_valor.get())
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")
            return
        resultado = self.banco.transferir(de, para, valor)
        if resultado == "Transferência realizada":
            messagebox.showinfo("Sucesso", resultado)
        else:
            messagebox.showerror("Erro", resultado)
        self.atualizar_lista()

    def consultar_saldo(self):
        nome = self.consulta_nome.get()
        saldo = self.banco.mostrar_saldo(nome)
        if saldo is not None:
            self.resultado_saldo.config(text=f"Saldo de {nome}: {saldo} €")
        else:
            messagebox.showerror("Erro", "Conta não encontrada.")
            self.resultado_saldo.config(text="")

    def atualizar_lista(self):
        contas = self.banco.listar_contas()
        self.lista_contas.config(state="normal")
        self.lista_contas.delete(1.0, "end")
        if contas:
            for nome, saldo in contas:
                self.lista_contas.insert("end", f"{nome}: {saldo} €\n")
        else:
            self.lista_contas.insert("end", "Nenhuma conta registrada.")
        self.lista_contas.config(state="disabled")


# Execução do app
if __name__ == "__main__":
    root = tk.Tk()
    estilo = ttk.Style(root)
    estilo.theme_use('clam')  # usar tema moderno
    App(root)
    root.mainloop()
