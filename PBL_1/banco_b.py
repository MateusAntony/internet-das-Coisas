from banco import Banco
from flask import Flask, request, jsonify, session
import requests
import os
import socket
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
nome_banco = os.getenv('NOME_BANCO', 'banco_b')
app = Flask(nome_banco)
banco = Banco(nome_banco)
app.secret_key = 'secret_key'  # Chave secreta para assinatura da sessão
endereco_ip = socket.gethostbyname(socket.gethostname())
ip_a = os.getenv('ipa', endereco_ip)
ip_c = os.getenv('ipc', endereco_ip)
bancos = {'banco_a': f"http://{ip_a}:1234", 'banco_c': f"http://{ip_c}:4567"}

@app.route('/criar-conta-fisica', methods=['POST'])
def criar_contaFisica():
    data = request.json
    numero = data.get('numero')
    saldo = float(data.get('saldo'))
    senha = data.get('senha')
    cpf = data.get('cpf')
    try:
        conta = banco.criar_contaPF(numero, saldo, senha, cpf)
        if conta == False:
            return jsonify({'mensagem': 'Cliente já existe no cadastro do banco'}),400
        return jsonify({'numero': conta.numero, 'saldo': conta.saldo, 'cpf': conta.cpf, 'mensagem': 'Conta criada com sucesso'}), 200
    except:
        return jsonify({"mensagem": "Erro ao criar conta"}), 400

@app.route('/criar-conta-PJ', methods=['POST'])
def criar_contaPJ():
    data = request.json
    numero = data.get('numero')
    saldo = float(data.get('saldo'))
    cnpj = data.get('cnpj')
    senha = data.get('senha')
    try:
        conta = banco.criar_contaPJ(numero, saldo, senha, cnpj)
        if conta == False:
            return jsonify({'mensagem': 'Cliente já existe no cadastro do banco'}), 400
        return jsonify({'numero': conta.numero, 'saldo': conta.saldo, 'cnpj': conta.cnpj, 'mensagem': 'Conta criada com sucesso'}), 200
    except:
        return jsonify({"mensagem": "Erro ao criar conta"}), 400

@app.route('/criar-conta-conjunta', methods=['POST'])
def criar_contaConjunta():
    data = request.json
    numero = data.get('numero')
    saldo = float(data.get('saldo'))
    cpf1 = data.get('cpf1')
    cpf2 = data.get('cpf2')
    senha = data.get('senha')
    try:
        conta = banco.criar_contaConjunta(numero, saldo, senha, cpf1, cpf2)
        if conta == False:
            return jsonify({'mensagem': 'Um dos clientes já possui conta'}),400
        return jsonify({'numero': conta.numero, 'saldo': conta.saldo, 'cpf1': conta.cpf1, 'cpf2': conta.cpf2, 'mensagem': 'Conta criada com sucesso'}), 200
    except:
        return jsonify({'mensagem': 'Erro ao criar conta'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    cpf = data.get('cpf')
    senha = data.get('senha')
    numero = data.get('numero')
    if banco.verificar_credenciais(cpf, senha, numero):
        session['logged_in'] = True
        session['cpf'] = cpf
        session['numero'] = numero
        return jsonify({"mensagem": "Login realizado com sucesso"}), 200
    return jsonify({"mensagem": "Cpf, senha ou número da conta inválidos"}), 401

@app.route('/exibir-conta', methods=['GET'])
def exibir_conta_do_login():
    cpf = session.get('cpf')  
    numero = session.get('numero') # Obtém o CPF do usuário logado da sessão
    conta = banco.get_conta(cpf,numero)  # Obtém os detalhes da conta do banco
    if conta:
        return jsonify(conta), 200
    else:
        return jsonify({"mensagem": "Conta não encontrada"}), 404
    
@app.route('/exibir-contas-banco', methods=['GET'])
def exibir_conta_do_banco():
    cpf = request.args.get('cpf')
    contas = banco.get_conta_por_cpf(cpf)
    if contas:
        return jsonify(contas), 200
    else:
        return jsonify({"mensagem": "Conta não encontrada"}), 404

@app.route('/add', methods=['POST'])
def add_saldo():
    data = request.json
    cpf = data.get('cpf')
    numero = data.get('numero')
    valor = float(data.get('valor'))
    conta = banco.get_conta(cpf,numero)  # Obtém os detalhes da conta do banco
    if conta:
        conta = banco.add(cpf,numero,valor)
        return jsonify({"mensagem": "Valor adicionado na conta"}), 200    
    else:
        return jsonify({"mensagem": "Conta não encontrada"}), 404

@app.route('/retirada', methods=['POST'])
def retirada():
    data = request.json
    cpf = data.get('cpf')
    numero = data.get('numero')
    valor = float(data.get('valor'))
    conta = banco.get_conta(cpf,numero)  # Obtém os detalhes da conta do banco
    if conta:
        conta = banco.retirada(cpf,numero, valor)
        return jsonify({"mensagem": "Valor retirado da conta"}), 200
    else:
        return jsonify({"mensagem": "Conta não encontrada"}), 404

@app.route('/preparar', methods=['POST'])
def preparar():
    data = request.json
    cpf = data.get('cpf')
    numero = data.get('numero')
    valor = float(data.get('valor'))
    try:
        preparado = banco.preparar(cpf, numero, valor)
        if preparado:
            return jsonify({"preparado": preparado}), 200
        else:
            return jsonify({"preparado": preparado}), 500  
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao preparar transferência: {str(e)}"}), 500

@app.route('/confirmar', methods=['POST'])
def confirmar():
    data = request.json
    numero = data.get('numero')
    cpf = data.get('cpf')
    try:
        confirmado = banco.confirmar(numero, cpf)
        if confirmado:
            return jsonify({"confirmado": confirmado}), 200 
        else:
            return jsonify({"confirmado": confirmado}), 500             
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao confirmar transferência: {str(e)}"}), 500


@app.route('/rollback', methods=['POST'])
def rollback():
    data = request.json
    numero = data.get('numero')
    cpf = data.get('cpf')
    try:
        rollback = banco.rollback(numero, cpf)
        if rollback:
            return jsonify({"rollback": rollback}), 200 
        else: 
            return jsonify({"rollback": rollback}),500
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao reverter transferência: {str(e)}"}), 500

@app.route('/transferencia', methods=['POST'])
def transferencia_mult():
    if session.get('logged_in'):
        data = request.json
        contas_origem = data.get('contas_origem')  # Lista de contas de origem, cada conta é um dicionário com 'cpf', 'numero', 'valor', 'nome_banco'
        cpf_destino = data.get('cpf_destino')
        numero_destino = data.get('numero_destino')
        nome_banco_destino = data.get('nome_banco_destino')
        valor_total = sum([float(conta['valor']) for conta in contas_origem])

        transacoes_preparadas = []

        if nome_banco_destino in bancos:
            url_banco_origem = bancos[nome_banco_destino]
            if verificar_status_banco(url_banco_origem) == False:
                return jsonify({f"mensagem": "Banco destino temporariamente indisponível"}), 503

        for conta in contas_origem:
            nome_banco_origem = conta['nome_banco']
            if nome_banco_origem in bancos:
                url_banco_origem = bancos[nome_banco_origem]
                if verificar_status_banco(url_banco_origem) == False:
                    return jsonify({f"mensagem": "Um dos Bancos temporariamente indisponível"}), 503
            
        try:
            # Preparar retiradas
            for conta in contas_origem:
                nome_banco_origem = conta['nome_banco']
                cpf_origem = conta['cpf']
                numero_origem = conta['numero']
                valor = float(conta['valor'])

                logger.debug(f"Preparando retirada para conta: {conta}")

                if nome_banco_origem == nome_banco:  # Mesma instituição
                    if banco.preparar(cpf_origem, numero_origem, valor):
                        transacoes_preparadas.append((cpf_origem, numero_origem, valor))
                        logger.debug(f"Retirada preparada para conta local: {conta}")
                    else:
                        raise Exception("Falha ao preparar retirada")

                elif nome_banco_origem in bancos:  # Outra instituição
                    url_banco_origem = bancos[nome_banco_origem]
                    payload_preparar_origem = {
                        "cpf": cpf_origem,
                        "numero": numero_origem,
                        "valor": valor
                    }
                    response_preparar = requests.post(f"{url_banco_origem}/preparar", json=payload_preparar_origem)
                    logger.debug(f"Resposta da preparação no banco origem {nome_banco_origem}: {response_preparar.json()}")
                    if response_preparar.status_code == 200 and response_preparar.json().get('preparado'):
                        transacoes_preparadas.append((cpf_origem, numero_origem, valor))
                        logger.debug(f"Retirada preparada para conta externa: {conta}")
                    else:
                        raise Exception("Falha ao preparar retirada em banco origem")

            # Confirmar retiradas
            for cpf_origem, numero_origem, valor in transacoes_preparadas:
                nome_banco_origem = next((conta['nome_banco'] for conta in contas_origem if conta['cpf'] == cpf_origem and conta['numero'] == numero_origem), None)
                logger.debug(f"Confirmando retirada para conta: {cpf_origem}, {numero_origem}")

                if nome_banco_origem == nome_banco:
                    if not banco.confirmar(numero_origem, cpf_origem):
                        raise Exception("Falha ao confirmar retirada")
                    logger.debug(f"Retirada confirmada para conta local: {cpf_origem}, {numero_origem}")

                elif nome_banco_origem in bancos:
                    url_banco_origem = bancos[nome_banco_origem]
                    payload_confirmar_origem = {
                        "cpf": cpf_origem,
                        "numero": numero_origem
                    }
                    response_confirmar = requests.post(f"{url_banco_origem}/confirmar", json=payload_confirmar_origem)
                    logger.debug(f"Resposta da confirmação no banco origem {nome_banco_origem}: {response_confirmar.json()}")
                    if response_confirmar.status_code != 200:
                        raise Exception("Falha ao confirmar retirada em banco origem")
                    logger.debug(f"Retirada confirmada para conta externa: {cpf_origem}, {numero_origem}")

            # Adicionar valor no destino
            if nome_banco_destino == nome_banco:
                banco.add(cpf_destino, numero_destino, valor_total)
                logger.debug(f"Valor adicionado na conta destino local: {cpf_destino}, {numero_destino}, valor: {valor_total}")
            elif nome_banco_destino in bancos:
                url_banco_destino = bancos[nome_banco_destino]
                payload_destino = {
                    "cpf": cpf_destino,
                    "numero": numero_destino,
                    "valor": valor_total
                }
                response_destino = requests.post(f"{url_banco_destino}/add", json=payload_destino)
                logger.debug(f"Resposta da adição de valor no banco destino {nome_banco_destino}: {response_destino.json()}")
                if response_destino.status_code != 200:
                    raise Exception("Falha ao adicionar valor no banco destino")
                logger.debug(f"Valor adicionado na conta destino externa: {cpf_destino}, {numero_destino}, valor: {valor_total}")

            return jsonify({"mensagem": f"Transferência de R${valor_total:.2f} realizada com sucesso"}), 200

        except Exception as e:
            # Rollback em caso de erro
            logger.error(f"Erro na transferência: {str(e)}")
            for cpf_origem, numero_origem, valor in transacoes_preparadas:
                nome_banco_origem = next((conta['nome_banco'] for conta in contas_origem if conta['cpf'] == cpf_origem and conta['numero'] == numero_origem), None)
                if nome_banco_origem == nome_banco:
                    banco.rollback(cpf_origem, numero_origem)
                    logger.debug(f"Rollback realizado para conta local: {cpf_origem}, {numero_origem}")
                elif nome_banco_origem in bancos:
                    url_banco_origem = bancos[nome_banco_origem]
                    payload_rollback = {
                        "cpf": cpf_origem,
                        "numero": numero_origem
                    }
                    requests.post(f"{url_banco_origem}/rollback", json=payload_rollback)
                    logger.debug(f"Rollback solicitado para conta externa: {cpf_origem}, {numero_origem}")

            return jsonify({"mensagem": f"Erro ao realizar transferência: {str(e)}"}), 500
    else:
        return jsonify({"mensagem": "Usuário não está logado"}), 401

    
@app.route('/pagamento', methods=['POST'])
def pagamento():
    if session.get('logged_in'):
        data = request.json
        contas_origem = data.get('contas_origem')  # Lista de contas de origem, cada conta é um dicionário com 'cpf', 'numero', 'valor', 'nome_banco'
        cpf_destino = data.get('cpf_destino')
        numero_destino = data.get('numero_destino')
        nome_banco_destino = data.get('nome_banco_destino')
        valor_total = sum([float(conta['valor']) for conta in contas_origem])

        transacoes_preparadas = []

        if nome_banco_destino in bancos:
            url_banco_origem = bancos[nome_banco_destino]
            if verificar_status_banco(url_banco_origem) == False:
                return jsonify({f"mensagem": "Banco destino temporariamente indisponível"}), 503

        for conta in contas_origem:
            nome_banco_origem = conta['nome_banco']
            if nome_banco_origem in bancos:
                url_banco_origem = bancos[nome_banco_origem]
                if verificar_status_banco(url_banco_origem) == False:
                    return jsonify({f"mensagem": "Um dos Bancos temporariamente indisponível"}), 503

        try:
            # Preparar retiradas
            for conta in contas_origem:
                nome_banco_origem = conta['nome_banco']
                cpf_origem = conta['cpf']
                numero_origem = conta['numero']
                valor = float(conta['valor'])

                logger.debug(f"Preparando retirada para conta: {conta}")

                if nome_banco_origem == nome_banco:  # Mesma instituição
                    if banco.preparar(cpf_origem, numero_origem, valor):
                        transacoes_preparadas.append((cpf_origem, numero_origem, valor))
                        logger.debug(f"Retirada preparada para conta local: {conta}")
                    else:
                        raise Exception("Falha ao preparar retirada")

                elif nome_banco_origem in bancos:  # Outra instituição
                    url_banco_origem = bancos[nome_banco_origem]
                    payload_preparar_origem = {
                        "cpf": cpf_origem,
                        "numero": numero_origem,
                        "valor": valor
                    }
                    response_preparar = requests.post(f"{url_banco_origem}/preparar", json=payload_preparar_origem)
                    logger.debug(f"Resposta da preparação no banco origem {nome_banco_origem}: {response_preparar.json()}")
                    if response_preparar.status_code == 200 and response_preparar.json().get('preparado'):
                        transacoes_preparadas.append((cpf_origem, numero_origem, valor))
                        logger.debug(f"Retirada preparada para conta externa: {conta}")
                    else:
                        raise Exception("Falha ao preparar retirada em banco origem")

            # Confirmar retiradas
            for cpf_origem, numero_origem, valor in transacoes_preparadas:
                nome_banco_origem = next((conta['nome_banco'] for conta in contas_origem if conta['cpf'] == cpf_origem and conta['numero'] == numero_origem), None)
                logger.debug(f"Confirmando retirada para conta: {cpf_origem}, {numero_origem}")

                if nome_banco_origem == nome_banco:
                    if not banco.confirmar(numero_origem, cpf_origem):
                        raise Exception("Falha ao confirmar retirada")
                    logger.debug(f"Retirada confirmada para conta local: {cpf_origem}, {numero_origem}")

                elif nome_banco_origem in bancos:
                    url_banco_origem = bancos[nome_banco_origem]
                    payload_confirmar_origem = {
                        "cpf": cpf_origem,
                        "numero": numero_origem
                    }
                    response_confirmar = requests.post(f"{url_banco_origem}/confirmar", json=payload_confirmar_origem)
                    logger.debug(f"Resposta da confirmação no banco origem {nome_banco_origem}: {response_confirmar.json()}")
                    if response_confirmar.status_code != 200:
                        raise Exception("Falha ao confirmar retirada em banco origem")
                    logger.debug(f"Retirada confirmada para conta externa: {cpf_origem}, {numero_origem}")

            # Adicionar valor no destino
            if nome_banco_destino == nome_banco:
                banco.add(cpf_destino, numero_destino, valor_total)
                logger.debug(f"Valor adicionado na conta destino local: {cpf_destino}, {numero_destino}, valor: {valor_total}")
            elif nome_banco_destino in bancos:
                url_banco_destino = bancos[nome_banco_destino]
                payload_destino = {
                    "cpf": cpf_destino,
                    "numero": numero_destino,
                    "valor": valor_total
                }
                response_destino = requests.post(f"{url_banco_destino}/add", json=payload_destino)
                logger.debug(f"Resposta da adição de valor no banco destino {nome_banco_destino}: {response_destino.json()}")
                if response_destino.status_code != 200:
                    raise Exception("Falha ao adicionar valor no banco destino")
                logger.debug(f"Valor adicionado na conta destino externa: {cpf_destino}, {numero_destino}, valor: {valor_total}")

            return jsonify({"mensagem": f"Transferência de R${valor_total:.2f} realizada com sucesso"}), 200

        except Exception as e:
            # Rollback em caso de erro
            logger.error(f"Erro na transferência: {str(e)}")
            for cpf_origem, numero_origem, valor in transacoes_preparadas:
                nome_banco_origem = next((conta['nome_banco'] for conta in contas_origem if conta['cpf'] == cpf_origem and conta['numero'] == numero_origem), None)
                if nome_banco_origem == nome_banco:
                    banco.rollback(cpf_origem, numero_origem)
                    logger.debug(f"Rollback realizado para conta local: {cpf_origem}, {numero_origem}")
                elif nome_banco_origem in bancos:
                    url_banco_origem = bancos[nome_banco_origem]
                    payload_rollback = {
                        "cpf": cpf_origem,
                        "numero": numero_origem
                    }
                    requests.post(f"{url_banco_origem}/rollback", json=payload_rollback)
                    logger.debug(f"Rollback solicitado para conta externa: {cpf_origem}, {numero_origem}")

            return jsonify({"mensagem": f"Erro ao realizar transferência: {str(e)}"}), 500
    else:
        return jsonify({"mensagem": "Usuário não está logado"}), 401

    

@app.route('/deposito', methods=['POST'])
def deposito():
    if session.get('logged_in'):
        data = request.json
        contas_origem = data.get('contas_origem')  # Lista de contas de origem, cada conta é um dicionário com 'cpf', 'numero', 'valor', 'nome_banco'
        cpf_destino = data.get('cpf_destino')
        numero_destino = data.get('numero_destino')
        nome_banco_destino = data.get('nome_banco_destino')
        valor_total = sum([float(conta['valor']) for conta in contas_origem])

        transacoes_preparadas = []

        if nome_banco_destino in bancos:
            url_banco_origem = bancos[nome_banco_destino]
            if verificar_status_banco(url_banco_origem) == False:
                return jsonify({f"mensagem": "Banco destino temporariamente indisponível"}), 503

        for conta in contas_origem:
            nome_banco_origem = conta['nome_banco']
            if nome_banco_origem in bancos:
                url_banco_origem = bancos[nome_banco_origem]
                if verificar_status_banco(url_banco_origem) == False:
                    return jsonify({f"mensagem": "Um dos Bancos temporariamente indisponível"}), 503

        try:
            # Preparar retiradas
            for conta in contas_origem:
                nome_banco_origem = conta['nome_banco']
                cpf_origem = conta['cpf']
                numero_origem = conta['numero']
                valor = float(conta['valor'])

                logger.debug(f"Preparando retirada para conta: {conta}")

                if nome_banco_origem == nome_banco:  # Mesma instituição
                    if banco.preparar(cpf_origem, numero_origem, valor):
                        transacoes_preparadas.append((cpf_origem, numero_origem, valor))
                        logger.debug(f"Retirada preparada para conta local: {conta}")
                    else:
                        raise Exception("Falha ao preparar retirada")

                elif nome_banco_origem in bancos:  # Outra instituição
                    url_banco_origem = bancos[nome_banco_origem]
                    payload_preparar_origem = {
                        "cpf": cpf_origem,
                        "numero": numero_origem,
                        "valor": valor
                    }
                    response_preparar = requests.post(f"{url_banco_origem}/preparar", json=payload_preparar_origem)
                    logger.debug(f"Resposta da preparação no banco origem {nome_banco_origem}: {response_preparar.json()}")
                    if response_preparar.status_code == 200 and response_preparar.json().get('preparado'):
                        transacoes_preparadas.append((cpf_origem, numero_origem, valor))
                        logger.debug(f"Retirada preparada para conta externa: {conta}")
                    else:
                        raise Exception("Falha ao preparar retirada em banco origem")

            # Confirmar retiradas
            for cpf_origem, numero_origem, valor in transacoes_preparadas:
                nome_banco_origem = next((conta['nome_banco'] for conta in contas_origem if conta['cpf'] == cpf_origem and conta['numero'] == numero_origem), None)
                logger.debug(f"Confirmando retirada para conta: {cpf_origem}, {numero_origem}")

                if nome_banco_origem == nome_banco:
                    if not banco.confirmar(numero_origem, cpf_origem):
                        raise Exception("Falha ao confirmar retirada")
                    logger.debug(f"Retirada confirmada para conta local: {cpf_origem}, {numero_origem}")

                elif nome_banco_origem in bancos:
                    url_banco_origem = bancos[nome_banco_origem]
                    payload_confirmar_origem = {
                        "cpf": cpf_origem,
                        "numero": numero_origem
                    }
                    response_confirmar = requests.post(f"{url_banco_origem}/confirmar", json=payload_confirmar_origem)
                    logger.debug(f"Resposta da confirmação no banco origem {nome_banco_origem}: {response_confirmar.json()}")
                    if response_confirmar.status_code != 200:
                        raise Exception("Falha ao confirmar retirada em banco origem")
                    logger.debug(f"Retirada confirmada para conta externa: {cpf_origem}, {numero_origem}")

            # Adicionar valor no destino
            if nome_banco_destino == nome_banco:
                banco.add(cpf_destino, numero_destino, valor_total)
                logger.debug(f"Valor adicionado na conta destino local: {cpf_destino}, {numero_destino}, valor: {valor_total}")
            elif nome_banco_destino in bancos:
                url_banco_destino = bancos[nome_banco_destino]
                payload_destino = {
                    "cpf": cpf_destino,
                    "numero": numero_destino,
                    "valor": valor_total
                }
                response_destino = requests.post(f"{url_banco_destino}/add", json=payload_destino)
                logger.debug(f"Resposta da adição de valor no banco destino {nome_banco_destino}: {response_destino.json()}")
                if response_destino.status_code != 200:
                    raise Exception("Falha ao adicionar valor no banco destino")
                logger.debug(f"Valor adicionado na conta destino externa: {cpf_destino}, {numero_destino}, valor: {valor_total}")

            return jsonify({"mensagem": f"Transferência de R${valor_total:.2f} realizada com sucesso"}), 200

        except Exception as e:
            # Rollback em caso de erro
            logger.error(f"Erro na transferência: {str(e)}")
            for cpf_origem, numero_origem, valor in transacoes_preparadas:
                nome_banco_origem = next((conta['nome_banco'] for conta in contas_origem if conta['cpf'] == cpf_origem and conta['numero'] == numero_origem), None)
                if nome_banco_origem == nome_banco:
                    banco.rollback(cpf_origem, numero_origem)
                    logger.debug(f"Rollback realizado para conta local: {cpf_origem}, {numero_origem}")
                elif nome_banco_origem in bancos:
                    url_banco_origem = bancos[nome_banco_origem]
                    payload_rollback = {
                        "cpf": cpf_origem,
                        "numero": numero_origem
                    }
                    requests.post(f"{url_banco_origem}/rollback", json=payload_rollback)
                    logger.debug(f"Rollback solicitado para conta externa: {cpf_origem}, {numero_origem}")

            return jsonify({"mensagem": f"Erro ao realizar transferência: {str(e)}"}), 500
    else:
        return jsonify({"mensagem": "Usuário não está logado"}), 401

@app.route('/exibir-contas-cpf', methods=['GET'])
def exibir_contas_cpf():
    data = request.json
    cpf = data.get('cpf')
    contas_encontradas = []

    # Obtém contas do banco local (banco próprio)
    contas_locais = banco.get_conta_por_cpf(cpf)
    if contas_locais:
        for conta in contas_locais:
            conta['banco'] = nome_banco  # Adiciona o nome do banco
        contas_encontradas.extend(contas_locais)
    
    # Itera sobre bancos externos
    for nome_banco_externo, url_banco in bancos.items():
        try:
            response = requests.get(f"{url_banco}/exibir-contas-banco", params={'cpf': cpf})
            if response.status_code == 200:
                contas_externas = response.json()
                if isinstance(contas_externas, list):
                    for conta in contas_externas:
                        conta['banco'] = nome_banco_externo  # Adiciona o nome do banco
                    contas_encontradas.extend(contas_externas)
                else:
                    print(f"Resposta inválida do banco {nome_banco_externo}: {contas_externas}")
            else:
                print(f"Erro ao recuperar contas do banco {nome_banco_externo}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Erro ao recuperar contas do banco {nome_banco_externo}: {str(e)}")

    return jsonify(contas_encontradas), 200
    
@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "online"}),200    

def criar_conta_inicial():
    conta1 = banco.criar_contaPF('123', 1000, '123', '123')
    conta_conjunta = banco.criar_contaConjunta('1234',3000,'123','123','321')
    conta2 = banco.criar_contaPF('12345', 200, '123', '987')

def verificar_status_banco(url):
    try:
        response = requests.get(url + '/status')
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

if __name__ == '__main__':
    criar_conta_inicial()
    port = int(os.getenv('portApi', 4321))
    f"http://{endereco_ip}:{port}"
    app.run(debug=True, host=endereco_ip, port=port)
