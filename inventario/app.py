from flask import Flask, render_template, send_file
import csv
from io import StringIO

app = Flask(__name__)

# Dados de exemplo para o inventário
produtos = [
    {
        'id': 1,
        'tipo': 'Simples',
        'sku': 'PROD-001',
        'nome': 'Sapato Clássico Castanho',
        'publicado': 'Sim',
        'emDestaque': 'Sim',
        'visibilidade': 'Visível',
        'precoNormal': 100,
        'precoPromocional': 90,
        'qtdEstoque': 50,
        'categorias': 'Eletrônicos',
        'tags': 'Tecnologia, Inovação',
        'imagens': 'https://exemplo.com/imagem.jpg',
    },
    {
        'id': 2,
        'tipo': 'Simples',
        'sku': 'PROD-002',
        'nome': 'Tênis Casual Preto',
        'publicado': 'Sim',
        'emDestaque': 'Não',
        'visibilidade': 'Catalogo',
        'precoNormal': 150,
        'precoPromocional': 120,
        'qtdEstoque': 30,
        'categorias': 'Moda',
        'tags': 'Verão, Desconto',
        'imagens': 'https://exemplo.com/imagem2.jpg',
    },
]

# Rota para a página principal
@app.route('/')
def index():
    return render_template('index.html', produtos=produtos)

# Rota para exportar os dados em CSV
@app.route('/exportar_csv')
def exportar_csv():
    # Criação do arquivo CSV
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        'id', 'tipo', 'sku', 'nome', 'publicado', 'emDestaque', 'visibilidade',
        'precoNormal', 'precoPromocional', 'qtdEstoque', 'categorias', 'tags', 'imagens'
    ])
    
    writer.writeheader()
    for produto in produtos:
        writer.writerow(produto)
    
    output.seek(0)  # Volta para o início do StringIO

    # Enviar o arquivo CSV para download
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='inventario.csv')

if __name__ == '__main__':
    app.run(debug=True)
