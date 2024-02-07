from flask import Flask, jsonify, request

app = Flask(__name__)
host = 'localhost'
port = 8080

cancoes = [
    {
        'cancao': ' abc',
        'estilo': 'rock'
    },
    {
        'cancao': ' cdf',
        'estilo': 'classico'
    },
    {
        'cancao': ' ghe',
        'estilo': 'jazz'
    },
    {
        'cancao': ' flm',
        'estilo': 'blues'
    },
    {
        'cancao': ' nop',
        'estilo': 'metal'
    },
]

@app.route('/cancoes', methods=['GET'])
def obter_cancoes():
    return jsonify(cancoes)

@app.route('/cancoes/<int:indice>', methods=['GET'])
def obter_cancao(indice):
    try:
        if cancoes[indice] is not None:
            return jsonify(cancoes[indice])
        
    except:
        return ('nao existe essa cancao')



app.run(port=port, host=host, debug=True) 