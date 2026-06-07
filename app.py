from flask import Flask, request, jsonify
from helpdesk_JORDAN_VINICIUS_MARI import (
    CentralDeSupporte,
    ChamadoNaoEncontradoException,
    CapacidadeExcedidaException,
    TransicaoInvalidaException,
)

app = Flask(__name__)
central = CentralDeSupporte("Ciesa Solutions")


@app.route('/chamados', methods=['POST'])
def criar_chamado():
    try:
        dados = request.get_json()
        chamado = central.abrir_chamado(
            dados['titulo'],
            dados['descricao'],
            dados['cliente'],
            dados['prioridade'],
        )
        return jsonify(chamado.to_dict()), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except KeyError as e:
        return jsonify({'erro': f"Campo obrigatorio ausente: {e}"}), 400


@app.route('/chamados', methods=['GET'])
def listar_chamados():
    status = request.args.get('status')
    chamados = list(central.chamados.values())
    if status:
        chamados = [c for c in chamados if c.status == status]
    return jsonify([c.to_dict() for c in chamados]), 200


@app.route('/chamados/em-atraso', methods=['GET'])
def listar_em_atraso():
    chamados = central.listar_em_atraso()
    return jsonify([c.to_dict() for c in chamados]), 200


@app.route('/chamados/<int:numero>', methods=['GET'])
def buscar_chamado(numero):
    try:
        chamado = central.buscar_chamado(numero)
        return jsonify(chamado.to_dict()), 200
    except ChamadoNaoEncontradoException as e:
        return jsonify({'erro': str(e)}), 404


@app.route('/chamados/<int:numero>/status', methods=['PATCH'])
def alterar_status(numero):
    try:
        dados = request.get_json()
        chamado = central.buscar_chamado(numero)
        chamado.alterar_status(dados['novo_status'], dados['responsavel'])
        return jsonify(chamado.to_dict()), 200
    except ChamadoNaoEncontradoException as e:
        return jsonify({'erro': str(e)}), 404
    except TransicaoInvalidaException as e:
        return jsonify({'erro': str(e)}), 400
    except KeyError as e:
        return jsonify({'erro': f"Campo obrigatorio ausente: {e}"}), 400


@app.route('/chamados/<int:numero>/resolver', methods=['PATCH'])
def resolver_chamado(numero):
    try:
        dados = request.get_json()
        central.resolver_chamado(numero, dados['id_tecnico'], dados['descricao_solucao'])
        chamado = central.buscar_chamado(numero)
        return jsonify(chamado.to_dict()), 200
    except ChamadoNaoEncontradoException as e:
        return jsonify({'erro': str(e)}), 404
    except PermissionError as e:
        return jsonify({'erro': str(e)}), 403
    except (TransicaoInvalidaException, ValueError) as e:
        return jsonify({'erro': str(e)}), 400
    except KeyError as e:
        return jsonify({'erro': f"Campo obrigatorio ausente: {e}"}), 400


@app.route('/tecnicos', methods=['POST'])
def criar_tecnico():
    try:
        dados = request.get_json()
        capacidade = dados.get('capacidade_maxima', 5)
        tecnico = central.registrar_tecnico(dados['nome'], dados['especialidades'], capacidade)
        return jsonify(tecnico.to_dict()), 201
    except KeyError as e:
        return jsonify({'erro': f"Campo obrigatorio ausente: {e}"}), 400


@app.route('/tecnicos', methods=['GET'])
def listar_tecnicos():
    disponivel = request.args.get('disponivel')
    tecnicos = list(central.tecnicos.values())
    if disponivel == 'true':
        tecnicos = [t for t in tecnicos if t.disponivel]
    elif disponivel == 'false':
        tecnicos = [t for t in tecnicos if not t.disponivel]
    return jsonify([t.to_dict() for t in tecnicos]), 200


@app.route('/atribuicao/automatica', methods=['POST'])
def atribuicao_automatica():
    atribuidos = central.atribuicao_automatica()
    chamados = [c.to_dict() for c in central.chamados.values() if c.status == 'em_atendimento']
    return jsonify({'atribuidos': atribuidos, 'chamados': chamados}), 200


@app.route('/painel', methods=['GET'])
def painel():
    return jsonify(central.painel_operacional()), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
