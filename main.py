import requests
from flask import Flask, jsonify, redirect, request
from models import Clientes, Ordem_de_servicos, Veiculos, banco_session
from sqlalchemy import select, create_engine
from flask_pydantic_spec import FlaskPydanticSpec
from sqlalchemy.exc import SQLAlchemyError


@app.route('/cadastrar_nv', methods=['POST'])
def cadastrar_nv():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        telefone = request.form.get('telefone')
        endereco = request.form.get('endereco')

        cpf_cadastrado = select(Clientes)
        cpf_cadastrado = banco_session.execute(cpf_cadastrado.filter_by(CPF=cpf)).first()
        if cpf_cadastrado:
            return jsonify({"error": 'CPF ja cadastrado'})

        endereco_cadastrado = select(Clientes)
        endereco_cadastrado = banco_session.execute(endereco_cadastrado.filter_by(endereco=endereco)).first()
        if endereco_cadastrado:
            return jsonify({"error": 'endereco ja cadastrado'})
        if not nome:
            return jsonify({"error": 'campo nome vazio'}), 400
        if not cpf:
            return jsonify({"error": 'campo cpf vazio'}, 400)
        if not endereco:
            return jsonify({"error": 'campo endereco vazio'}, 400)
        if not telefone:
            return jsonify({"error": 'campo endereco vazio'}, 400)
        else:
            try:
                usuario_salvo = Clientes(nome=nome,
                                           CPF=cpf,
                                           telefone=telefone,
                                           endereco=endereco)
                usuario_salvo.save()
                return jsonify({
                    'nome': usuario_salvo.nome,
                    'cpf': usuario_salvo.CPF,
                    'tefone': usuario_salvo.telefone,
                    'endereco': usuario_salvo.endereco})
            except IntegrityError as e:
                return jsonify({'error': str(e)})

@app.route('/consultar_cliente')
def consultar_clientes():
    try:
        lista_servicos = select(Clientes)
        lista_servicos = banco_session.execute(lista_servicos).scalars()
        result = []
        for servicos in lista_servicos:
            result.append(servicos.get_usuario())
        banco_session.close()

        return jsonify({'usuarios': result})


    except IntegrityError as e:
        return jsonify({'error': str(e)})

@app.route('/cadastrar_veiculo_nv',methods=['POST'])
def cadastrar_veiculo_nv():
    if request.method == 'POST':
        cliente_associados = request.form.get('cliente_associados')
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        placa = request.form.get('placa')
        ano_de_fabricacao = request.form.get('ano_de_fabricacao')
        placa_registrada = select(Veiculos)
        placa_buscada = banco_session.execute(placa_registrada.filter_by(placa=placa)).first()
        if placa_buscada:
            return jsonify({"error": 'Placa ja cadastrado'})
        else:
            try:
                cliente_associados = int(cliente_associados)
                placa = int(placa)
                veiculo = Veiculos(cliente_associados=cliente_associados,
                                   marca=marca,
                                   modelo=modelo,
                                   placa=placa,
                                   ano_de_fabricacao=ano_de_fabricacao)
                veiculo.save()
                return jsonify({'cliente_associados': cliente_associados},
                               {'marca': marca},
                               {'modelo': modelo},
                               {'placa': placa},
                               {'ano_de_fabricacao': ano_de_fabricacao}
                               )
            except IntegrityError as e:
                return jsonify({'error': str(e)})

@app.route('/registrar_servico', methods=['POST'])
def registrar_servicos():
    if request.method == 'POST':
        veiculo_associados = request.form.get('veiculo_associados')
        data_abertura = request.form.get('data_abertura')
        descricao_servico = request.form.get('descricao_servico')
        status = request.form.get('status')
        valor_estimado = request.form.get('valor_estimado')
        try:
            veiculo_associados = int(veiculo_associados)
            status = int(status)
            valor_estimado = float(valor_estimado)
            serivco = Ordem_de_servicos(veiculo_associados=veiculo_associados,
                                        data_de_abertura=data_abertura,
                                        descricao_do_servicos=descricao_servico,
                                        status=status,
                                        valor_estimado=valor_estimado)
            serivco.save()
            return jsonify({'veiculo': serivco.veiculo_associados},
                           {'data de abertura':serivco.data_de_abertura},
                           {'descricao do servico':serivco.descricao_do_servicos},
                           {'status': serivco.status},
                           {'valor estimado': serivco.valor_estimado}
                           )
        except IntegrityError as e:
            return jsonify({'error': str(e)})




@app.route('/consulta_veiculo_por_cliente/<id_cliente>')
def consulta_veiculo_cliente(id_cliente):
    try:
        id_cliente = int(id_cliente)
        cliente_associ = select(Veiculos)
        veiculos_encontrado = banco_session.execute(cliente_associ.filter_by(cliente_associados=id_cliente)).scalar()

        if veiculos_encontrado:
            return jsonify({'veiculo': veiculos_encontrado.placa},
                           {'marca': veiculos_encontrado.marca},
                           {'modelo': veiculos_encontrado.modelo},
                           {'placa': veiculos_encontrado.placa},
                           {'ano de fabricacao': veiculos_encontrado.ano_de_fabricacao},
                           {'cliente_associados': veiculos_encontrado.cliente_associados}
                           )
        else:
            return jsonify({'nao a veiculos no nome desse cliente'})
    except IntegrityError as e:
        return jsonify({'error': str(e)})

@app.route('/consulta_servicos_por_cliente/<status>')
def consulta_servicos_por_cliente(status):
    try:
        status = int(status)
        servico_por_status = select(Ordem_de_servicos)
        if status == 0:
            pendente = banco_session.execute(servico_por_status.filter_by(status=status)).scalar()
            return jsonify({'id do veiculo': pendente.veiculo_associados},
                           {'data de abertura': pendente.data_de_abertura},
                           {'descricao do servico': pendente.descricao_do_servicos},
                           {'valor estimado': pendente.valor_estimado}
                           )
        elif status == 1:
            pendente = banco_session.execute(servico_por_status.filter_by(status=status)).scalar()
            return jsonify({'id do veiculo': pendente.veiculo_associados},
                           {'data de abertura': pendente.data_de_abertura},
                           {'descricao do servico': pendente.descricao_do_servicos},
                           {'valor estimado': pendente.valor_estimado}
                           )
        else:
            pendente = banco_session.execute(servico_por_status.filter_by(status=status)).scalar()
            return jsonify({'id do veiculo': pendente.veiculo_associados},
                           {'data de abertura': pendente.data_de_abertura},
                           {'descricao do servico': pendente.descricao_do_servicos},
                           {'valor estimado': pendente.valor_estimado}
                           )
    except IntegrityError as e:
        return jsonify({'error': str(e)})


@app.route('/atualizar_cliente/<id>', methods=['POST'])
def atualizar_cliente(id):
    if request.method == 'PUT':
        id_cliente = int(id)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)