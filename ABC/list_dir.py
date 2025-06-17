import os
import matplotlib.pyplot as plt

# Função para listar diretórios e subdiretórios
def listar_diretorios(pasta):
    estrutura = {}
    for dirpath, dirnames, filenames in os.walk(pasta):
        estrutura[dirpath] = len(dirnames)  # Conta o número de subdiretórios
    return estrutura

# Função para plotar gráfico
def plotar_grafico(estrutura):
    # Extrai os dados para o gráfico
    diretorios = list(estrutura.keys())
    subdiretorios = list(estrutura.values())

    # Plotando o gráfico
    plt.figure(figsize=(10, 6))
    plt.barh(diretorios, subdiretorios, color='skyblue')
    plt.xlabel('Número de Subdiretórios')
    plt.title('Distribuição de Diretórios e Subdiretórios')
    plt.tight_layout()
    plt.show()

# Defina o caminho da pasta a ser analisada
pasta = '/home/coyas/Documents/zebraTests'  # Substitua com o caminho desejado

# Obter a estrutura de diretórios
estrutura = listar_diretorios(pasta)

# Plotar gráfico
plotar_grafico(estrutura)

