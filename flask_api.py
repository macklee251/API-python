from flask import Flask, jsonify, request

app = Flask(__name__)
host = 'localhost'
port = 8080

postagens = [
    {
        'titulo': 'minha história',
        'autor': 'Lee. M'
    },
    {
        'titulo': 'Novo dispositivo sone',
        'autor': 'Allison'
    },
    {
        'titulo': 'Lançamento do ano',
        'autor': 'Eduardo'
    }
]

# Rota padrao
@app.route('/')
def obter_postagens():
    return jsonify(postagens)

# Get com ID
@app.route('/postagem/<int:indice>', methods=['GET'])
def obter_postagens_por_indice(indice):
    return jsonify(postagens[indice])

# Port
@app.route('/postagem', methods=['POST'])
def nova_postagem():
    postagem = request.get_json()
    postagens.append(postagem)
    
    return jsonify(postagem, 200)

# Put
@app.route('/postagem/<int:indice>', methods=['PUT'])
def alterar_postagem(indice):
    postagem_alterada = request.get_json()
    postagens[indice].update(postagem_alterada)
    
    return jsonify(postagens[indice], 200)

# Delete
@app.route('/postagem/<int:indice>', methods=['DELETE'])
def excluir_postagem(indice):
    try:
        if postagens[indice] is not None :
            del postagens[indice]
            return jsonify(f'postagem {postagens[indice]} excluida', 200 )
    except:
        return jsonify('Não foi possível encontrar a postagem para exclusão', 404)

app.run(port=port, host=host, debug=True) 