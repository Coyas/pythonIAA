import os
import networkx as nx
import matplotlib.pyplot as plt

# Função para listar diretórios e subdiretórios
def listar_diretorios(pasta):
    G = nx.DiGraph()  # Grafo direcionado
    for dirpath, dirnames, filenames in os.walk(pasta):
        for dirname in dirnames:
            # Adiciona a aresta no grafo (diretório pai -> subdiretório)
            G.add_edge(dirpath, os.path.join(dirpath, dirname))
    return G

# Função para plotar a árvore de diretórios
def plotar_estrutura_árvore(G):
    plt.figure(figsize=(12, 12))
    
    # Desenhar a árvore
    pos = nx.spring_layout(G, seed=42)  # Layout para espaçar os nós
    nx.draw(G, pos, with_labels=True, node_size=5000, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray")

    plt.title("Árvore de Diretórios e Subdiretórios")
    plt.tight_layout()
    plt.show()

# Defina o caminho da pasta a ser analisada
pasta = '/home/coyas/Documents/zebraTests'  # Substitua com o caminho desejado

# Obter a estrutura de diretórios
grafo = listar_diretorios(pasta)

# Plotar gráfico
plotar_estrutura_árvore(grafo)

