import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

class Banco:
    def __init__(self):
        self.conn = sqlite3.connect("banco.db")
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


class BancoGUI:
    def __init__(self, root):
        self.banco = Banco()
        self.root = root
        self.root.title("💰 Banco Supreme Deluxe 💰")
        self.root.geometry("800x600")

        style = ttk.Style(theme='cyborg')  # Tema dark chique

        self.notebook = ttk.Notebook(root, bootstyle="info")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.criar_tab_contas()
        self.criar_tab_transferencia()
        self.criar_tab_consulta()

        self.atualizar_lista()

    def criar_tab_contas(self):
        self.tab_contas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_contas, text="🏦 Gerenciar Contas")

        frame = ttk.Frame(self.tab_contas, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nome:", bootstyle="info").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.nome_entry = ttk.Entry(frame, width=30)
        self.nome_entry.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Saldo Inicial (€):", bootstyle="info").grid(row=1, column=0, sticky="e", padx=5)
        self.saldo_entry = ttk.Entry(frame, width=30)
        self.saldo_entry.grid(row=1, column=1)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="💼 Criar Conta", bootstyle="success-outline", command=self.criar_conta).pack(side=LEFT, padx=10)
        ttk.Button(btn_frame, text="🗑️ Apagar Conta", bootstyle="danger-outline", command=self.apagar_conta).pack(side=LEFT)

        self.lista_contas = ttk.Treeview(frame, columns=("Nome", "Saldo"), show='headings', height=12, bootstyle="info")
        self.lista_contas.heading("Nome", text="Nome")
        self.lista_contas.heading("Saldo", text="Saldo (€)")
        self.lista_contas.column("Nome", anchor="center", width=200)
        self.lista_contas.column("Saldo", anchor="center", width=100)
        self.lista_contas.grid(row=3, column=0, columnspan=2, pady=15)

    def criar_tab_transferencia(self):
        self.tab_transfer = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_transfer, text="🔄 Transferências")

        frame = ttk.Frame(self.tab_transfer, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="De:", bootstyle="info").grid(row=0, column=0, sticky="e", pady=5)
        self.transf_de = ttk.Entry(frame, width=30)
        self.transf_de.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Para:", bootstyle="info").grid(row=1, column=0, sticky="e", pady=5)
        self.transf_para = ttk.Entry(frame, width=30)
        self.transf_para.grid(row=1, column=1, padx=5)

        ttk.Label(frame, text="Valor (€):", bootstyle="info").grid(row=2, column=0, sticky="e", pady=5)
        self.transf_valor = ttk.Entry(frame, width=30)
        self.transf_valor.grid(row=2, column=1, padx=5)

        ttk.Button(frame, text="💸 Transferir", bootstyle="warning-outline", command=self.transferir).grid(row=3, column=0, columnspan=2, pady=10)

    def criar_tab_consulta(self):
        self.tab_consulta = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_consulta, text="📊 Consultar Saldo")

        frame = ttk.Frame(self.tab_consulta, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nome da Conta:", bootstyle="info").grid(row=0, column=0, sticky="e", pady=5)
        self.consulta_entry = ttk.Entry(frame, width=30)
        self.consulta_entry.grid(row=0, column=1, padx=5)

        ttk.Button(frame, text="🔍 Consultar", bootstyle="primary-outline", command=self.consultar_saldo).grid(row=1, column=0, columnspan=2, pady=10)

        self.resultado = ttk.Label(frame, text="", font=("Helvetica", 16), bootstyle="success")
        self.resultado.grid(row=2, column=0, columnspan=2, pady=20)

    def criar_conta(self):
        nome = self.nome_entry.get()
        try:
            saldo = int(self.saldo_entry.get() or 0)
        except ValueError:
            messagebox.showerror("Erro", "Saldo inválido")
            return
        if self.banco.criar_conta(nome, saldo):
            messagebox.showinfo("Criado", f"Conta '{nome}' criada com {saldo}€")
        else:
            messagebox.showwarning("Existente", "Conta já existe")
        self.atualizar_lista()

    def apagar_conta(self):
        nome = self.nome_entry.get()
        status = self.banco.apagar_conta(nome)
        if status == "Conta apagada":
            messagebox.showinfo("Sucesso", "Conta apagada com sucesso")
        else:
            messagebox.showerror("Erro", status)
        self.atualizar_lista()

    def transferir(self):
        de = self.transf_de.get()
        para = self.transf_para.get()
        try:
            valor = int(self.transf_valor.get())
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido")
            return
        resultado = self.banco.transferir(de, para, valor)
        if resultado == "Transferência realizada":
            messagebox.showinfo("Feito", resultado)
        else:
            messagebox.showerror("Erro", resultado)
        self.atualizar_lista()

    def consultar_saldo(self):
        nome = self.consulta_entry.get()
        saldo = self.banco.mostrar_saldo(nome)
        if saldo is not None:
            self.resultado.config(text=f"Saldo de {nome}: {saldo}€")
        else:
            self.resultado.config(text="Conta não encontrada")

    def atualizar_lista(self):
        for i in self.lista_contas.get_children():
            self.lista_contas.delete(i)
        contas = self.banco.listar_contas()
        for nome, saldo in contas:
            self.lista_contas.insert("", "end", values=(nome, saldo))


if __name__ == "__main__":
    app = ttk.Window(themename="cyborg")  # ou flatly, darkly, morph, etc.
    BancoGUI(app)
    app.mainloop()

