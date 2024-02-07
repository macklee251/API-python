from flask import Flask, jsonify, request, make_response
from estrutura_banco_de_dados import Autor, Postagem, app, db
import json, jwt
from datetime import datetime, timedelta

host = 'localhost'
port = 8080

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Login invalido', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    usuario = Autor.query.filter_by(nome=auth.username).first()
    if not usuario:
        return make_response('Login invalido', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if auth.password == usuario.senha:
        token = jwt.enconde({'id_autor':usuario.id_autor, 'exp':datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return make_response('Login invalido', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


# Rota padrão - GET https://localhost:8080
@app.route('/')
def obter_postagens():
    postagens = Postagem.query.all()
    postagens_list = []
    for postagem in postagens:
        postagem_atual = {}
        postagem_atual['id_postagem'] = postagem.id_postagem
        postagem_atual['titulo'] = postagem.titulo
        postagem_atual['id_autor'] = postagem.id_autor
        postagens_list.append(postagem_atual)        
    return jsonify('postagens', postagens_list)

# Obter postagem por id - GET https://localhost:8080/postagem/1
@app.route('/postagem/<int:id_postagem>', methods=['GET'])
def obter_postagem_por_indice(id_postagem):
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    postagem_atual = {}
    try:
        postagem_atual['titulo'] = postagem.titulo
    except:
        pass
    postagem_atual['id_autor'] = postagem.id_autor

    return jsonify({'postagens': postagem_atual})

# Criar uma nova postagem - POST https://localhost:8080/postagem
@app.route('/postagem', methods=['POST'])
def nova_postagem():
    nova_postagem = request.get_json()
    postagem = Postagem(
        titulo=nova_postagem['titulo'], id_autor=nova_postagem['id_autor'])
    db.session.add(postagem)
    db.session.commit()

    return jsonify({'mensagem': 'Postagem criada com sucesso'})

# Alterar uma postagem existente - PUT https://localhost:8080/postagem/1
@app.route('/postagem/<int:id_postagem>', methods=['PUT'])
def alterar_postagem(id_postagem):
    postagem_alterada = request.get_json()
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    try:
        postagem.titulo = postagem_alterada['titulo']
    except:
        pass
    try:
        postagem.id_autor = postagem_alterada['id_autor']
    except:
        pass

    db.session.commit()
    return jsonify({'mensagem': 'Postagem alterada com sucessso'})

# Excluir uma postagem - DELETE - https://localhost:8080/postagem/1
@app.route('/postagem/<int:id_postagem>', methods=['DELETE'])
def excluir_postagem(id_postagem):
    postagem_a_ser_excluida = Postagem.query.filter_by(
        id_postagem=id_postagem).first()
    if not postagem_a_ser_excluida:
        return jsonify({'mensagem': 'Não foi encontrado uma postagem com este id'})
    db.session.delete(postagem_a_ser_excluida)
    db.session.commit()

    return jsonify({'mensagem': 'Postagem excluída com sucesso!'})


@app.route('/autores/<int:id_autor>',methods=['GET'])
def obter_autor_por_id(id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify('autor não encontrado')
    autor_atual = {}
    try:
        autor_atual['id_autor'] = autor.id_autor
    except:
        pass
    try:
        autor_atual['nome'] = autor.nome
    except:
        pass
    try:
        autor_atual['email'] = autor.email
    except:
        pass
    return jsonify(f'Você buscou pelo autor: {autor_atual}')


@app.route('/autores',methods=['POST'])
def novo_autor():
    novo_autor = request.get_json()
    autor = Autor(nome = novo_autor['nome'],
                  email = novo_autor['email'], 
                  senha = novo_autor['senha'])
    db.session.add(autor)
    db.session.commit()
    return jsonify({'Mensagem': f'Usuario criado com sucesso'}, 200)


@app.route('/autores/<int:id_autor>',methods=['PUT'])
def alterar_autor(id_autor):
    usuario_alterar = request.get_json()
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify(f'autor não encontrado')
    try:
        if usuario_alterar['nome']:
            autor.nome = usuario_alterar['nome']
    except:
        pass
    try:
        if usuario_alterar['email']:
            autor.email = usuario_alterar['email']
    except:
        pass
    try:
        if usuario_alterar['senha']:
            autor.senha = usuario_alterar['senha']
    except:
        pass
    try:
        if usuario_alterar['admin']:
            autor.admin = usuario_alterar['admin']
    except:
        pass
        db.session.commit()
        return jsonify({'Mensagem': f'Usuario alterado com sucesso'}, 200)

@app.route('/autores/<int:id_autor>',methods=['DELETE'])
def excluir_autor(id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify(f'autor não encontrado')
    db.session.delete(autor)
    db.session.commit()
    return jsonify({'Mensagem': f'Usuario excluido com sucesso'}, 200)


app.run(port=port, host=host, debug=True) 