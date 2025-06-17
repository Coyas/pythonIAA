import sqlite3

class Banco:
    def __init__(self):
        # Conectando ao banco de dados (cria o arquivo .db caso não exista)
        self.conn = sqlite3.connect('banco_b1.db')
        self.cursor = self.conn.cursor()
        
        # Criando a tabela de contas, se não existir
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contas (
                nome TEXT PRIMARY KEY,
                saldo INTEGER
            )
        ''')
        self.conn.commit()

    def apagar_conta(self, nome):
        # Verificando se a conta existe antes de apagar
        self.cursor.execute('SELECT * FROM contas WHERE nome = ?', (nome,))
        if not self.cursor.fetchone():
            print(f"\nConta de {nome} não encontrada.")
            return
        # Verificando se o saldo é zero antes de apagar
        self.cursor.execute('SELECT saldo FROM contas WHERE nome = ?', (nome,))
        saldo = self.cursor.fetchone()
        if saldo[0] != 0:
            print(f"\nConta de {nome} não pode ser apagada, saldo não é zero.")
            return
        # Apagando a conta
        self.cursor.execute('DELETE FROM contas WHERE nome = ?', (nome,))
        self.conn.commit()
        print(f"\nConta de {nome} apagada com sucesso.")
        # Exibindo as contas restantes
        self.cursor.execute('SELECT * FROM contas')
        contas_restantes = self.cursor.fetchall()
        if contas_restantes:
            print("\nContas restantes:")
            for conta in contas_restantes:
                print(f"Nome: {conta[0]}, Saldo: {conta[1]}")
        else:
            print("\nNenhuma conta restante.")
        # Exibindo o saldo atualizado
        self.mostrar_saldo(nome)    


    def criar_conta(self, nome, saldo_inicial=0):
        # Inserindo uma nova conta no banco de dados
        try:
            self.cursor.execute('''
                INSERT INTO contas (nome, saldo) VALUES (?, ?)
            ''', (nome, saldo_inicial))
            self.conn.commit()
            print(f"\nConta de {nome} criada com sucesso!")
        except sqlite3.IntegrityError:
            print(f"\nConta de {nome} já existe.")

    def transferir(self, de, para, valor):
        # Verificando saldos e realizando a transferência
        self.cursor.execute('SELECT saldo FROM contas WHERE nome = ?', (de,))
        saldo_de = self.cursor.fetchone()
        
        self.cursor.execute('SELECT saldo FROM contas WHERE nome = ?', (para,))
        saldo_para = self.cursor.fetchone()
        
        if not saldo_de:
            print(f"\nConta {de} não existe.")
            return
        if not saldo_para:
            print(f"\nConta {para} não existe.")
            return
        if saldo_de[0] < valor:
            print(f"\nSaldo insuficiente na conta {de}.")
            return
        
        # Atualizando os saldos
        self.cursor.execute('''
            UPDATE contas SET saldo = saldo - ? WHERE nome = ?
        ''', (valor, de))
        
        self.cursor.execute('''
            UPDATE contas SET saldo = saldo + ? WHERE nome = ?
        ''', (valor, para))
        
        self.conn.commit()
        print(f"\nTransferência de {valor} de {de} para {para} realizada com sucesso.")

    def mostrar_saldo(self, nome):
        # Exibindo o saldo de uma conta
        self.cursor.execute('SELECT saldo FROM contas WHERE nome = ?', (nome,))
        saldo = self.cursor.fetchone()
        
        if saldo:
            print(f"\nSaldo de {nome}: {saldo[0]}")
        else:
            print(f"\nConta {nome} não encontrada.")

    def fechar_conexao(self):
        # Fechando a conexão com o banco de dados
        self.conn.close()


# Criando um banco
banco = Banco()

# Criando contas iniciais
banco.criar_conta("sandra", 0)
banco.criar_conta("bebe", 1000)
banco.criar_conta("sonia", 1000)
banco.criar_conta("maria", 200)
banco.criar_conta("lenira", 700)

def ListarContas():
    # Listando todas as contas e seus saldos
    banco.cursor.execute('SELECT * FROM contas')
    contas = banco.cursor.fetchall()
    if contas:
        print("\nContas e seus saldos:")
        for conta in contas:
            print(f"Nome: {conta[0]}, Saldo: {conta[1]}")
    else:
        print("\nNenhuma conta encontrada.")
    
def mostrar_saldo_conta():
    # Função para mostrar o saldo de uma conta específica
    nome_conta = input("\nDigite o nome da conta para mostrar o saldo: ")
    banco.mostrar_saldo(nome_conta)            

# Função para mostrar o menu e processar a escolha do usuário
def menu():
    while True:
        print("\nSelecione uma opção:")
        print("1. Listar contas")
        print("2. Realizar transferência")
        print("3. Criar conta")
        print("4. Mostrar saldo de uma conta")
        print("0. Eliminar conta")
        print("-1. Sair")

        opcao = input("\nDigite o número da opção desejada: ")

        if opcao == '1':
            # listando as contas
            ListarContas()            
        
        elif opcao == '2':
            # Executando as transferências
            executar_transferencia()

        elif opcao == '3':
            # Criando uma nova conta
            nome_conta = input("\nDigite o nome da nova conta: ")
            saldo_inicial = int(input("Digite o saldo inicial (padrão é 0): ") or 0)
            banco.criar_conta(nome_conta, saldo_inicial)
        elif opcao == '4':
            # Mostrando o saldo de uma conta específica
            mostrar_saldo_conta()
        elif opcao == '-1':
            print("Saindo...")
            banco.fechar_conexao()
            break
        elif opcao == '0':
            # Apagando uma conta
            nome_conta = input("\nDigite o nome da conta a ser apagada: ")
            banco.apagar_conta(nome_conta)
        else:
            print("Opção inválida. Tente novamente.")

# Função para executar transferências via terminal
def executar_transferencia():
    while True:
        try:
            comando = input("\nDigite a transferência no formato 'manda {valor} de {origem} pa {destino}' ou 'sair' para encerrar: ")
            
            if comando.lower() == 'sair':
                break

            # Verificando a sintaxe do comando
            if comando.lower().startswith("manda"):
                partes = comando.split()
                
                # Verificando a quantidade correta de partes na entrada
                if len(partes) != 6 or partes[2].lower() != 'de' or partes[4].lower() != 'pa':
                    print("Comando mal formatado. Tente novamente.")
                    continue
                
                valor = int(partes[1])  # Valor a ser transferido
                origem = partes[3]  # Conta de origem
                destino = partes[5]  # Conta de destino
                
                # Realizando a transferência
                banco.transferir(origem, destino, valor)
        
        except Exception as e:
            print(f"Erro ao processar comando: {e}")

# Iniciando o menu
menu()
