import requests
import os
import socket
import threading 

port = int(os.getenv('portApi', 1234))
endereco_ip = socket.gethostbyname(socket.gethostname())
ip= os.getenv('ip', endereco_ip)

base_url = f"http://{ip}:{port}"


def criar_conta_pf():
    numero = input("Número da conta: ")
    saldo = float(input("Saldo inicial: "))
    senha = input("Senha: ")
    cpf = input("CPF: ")
    url = f"{base_url}/criar-conta-fisica"
    payload = {
        "numero": numero,
        "saldo": saldo,
        "senha": senha,
        "cpf": cpf
    }
    response = requests.post(url, json=payload)
    print(response.json())

def criar_conta_pj():
    numero = input("Número da conta: ")
    saldo = float(input("Saldo inicial: "))
    senha = input("Senha: ")
    cnpj = input("CNPJ: ")
    url = f"{base_url}/criar-conta-PJ"
    payload = {
        "numero": numero,
        "saldo": saldo,
        "senha": senha,
        "cnpj": cnpj
    }
    response = requests.post(url, json=payload)
    print(response.json())

def criar_conta_conjunta():
    numero = input("Número da conta: ")
    saldo = float(input("Saldo inicial: "))
    senha = input("Senha: ")
    cpf1 = input("CPF do primeiro titular: ")
    cpf2 = input("CPF do segundo titular: ")
    url = f"{base_url}/criar-conta-conjunta"
    payload = {
        "numero": numero,
        "saldo": saldo,
        "senha": senha,
        "cpf1": cpf1,
        "cpf2": cpf2
    }
    response = requests.post(url, json=payload)
    print(response.json())

def login():
    cpf = input("CPF: ")
    senha = input("Senha: ")
    numero = input("Número da conta: ")
    url = f"{base_url}/login"
    payload = {
        "cpf": cpf,
        "senha": senha,
        "numero": numero
    }
    session = requests.Session()
    response = session.post(url, json=payload)
    print(response.json())
    return session

def exibir_conta(session):
    url = f"{base_url}/exibir-conta"
    response = session.get(url)
    print(response.json())

def add_saldo():
    cpf = input("CPF: ")
    numero = input("Número da conta: ")
    valor = float(input("Valor a adicionar: "))
    url = f"{base_url}/add"
    payload = {
        "cpf": cpf,
        "numero": numero,
        "valor": valor
    }
    response = requests.post(url, json=payload)
    print(response.json())

def retirada():
    cpf = input("CPF: ")
    numero = input("Número da conta: ")
    valor = float(input("Valor a retirar: "))
    url = f"{base_url}/retirada"
    payload = {
        "cpf": cpf,
        "numero": numero,
        "valor": valor
    }
    response = requests.post(url, json=payload)
    print(response.json())

def transferencia_mult(session):
    contas_origem = []
    while True:
        cpf = input("CPF da conta de origem: ")
        numero = input("Número da conta de origem: ")
        valor = float(input("Valor a transferir: "))
        print("Nome do banco de origem: ")
        print("1. banco_a")
        print("2. banco_b")
        print("3. banco_c")
        escolha = input("Escolha uma opção (1/2/3): ")
        if escolha == '1':
            nome_banco = 'banco_a'
        elif escolha == '2':
            nome_banco = 'banco_b'
        elif escolha == '3':
            nome_banco = 'banco_c'
        contas_origem.append({"cpf": cpf, "numero": numero, "valor": valor, "nome_banco": nome_banco})
        cont = input("Deseja adicionar outra conta de origem? (s/n): ")
        if cont.lower() != 's':
            break
    cpf_destino = input("CPF do destinatário: ")
    numero_destino = input("Número da conta de destino: ")
    print("Nome do banco de destino: ")
    print("1. banco_a")
    print("2. banco_b")
    print("3. banco_c")
    escolha = input("Escolha uma opção (1/2/3): ")
    if escolha == '1':
        nome_banco_destino = 'banco_a'
    elif escolha == '2':
        nome_banco_destino = 'banco_b'
    elif escolha == '3':
        nome_banco_destino = 'banco_c'

    status = status()    
    if status == False:
        print('banco off')
    else:
        url = f"{base_url}/transferencia"
        payload = {
            "contas_origem": contas_origem,
            "cpf_destino": cpf_destino,
            "numero_destino": numero_destino,
            "nome_banco_destino": nome_banco_destino
        }
        response = session.post(url, json=payload)
        print(response.json())
    
def exibir_todas_contas():
    url = f"{base_url}/exibir-contas-cpf"
    cpf = input("CPF: ")
    payload = {
        "cpf": cpf
    }
    response = requests.get(url, json=payload)
    print(response.json())

def sub_menu(session):
    while True:
        on=status()
        print("1. Exibir conta logada")
        print("2. Exibir todas as contas")
        print("3. Transferência")
        print("4. Pagamento")
        print("5. Deposito")
        print("6. Transferencia concorrente")
        print("7. Voltar")
        
        escolha = input("Escolha uma opção: ")
        if escolha == '7':
            break
        if on == False:
            escolha= '0'
        if escolha == '1':
            if session:
                exibir_conta(session)
            else:
                print("Você precisa fazer login primeiro.")
            
        elif escolha == '2':
            exibir_todas_contas()
        elif escolha == '3':
            if session:
                transferencia_mult(session)
            else:
                print("Você precisa fazer login primeiro.")
        elif escolha == '4':
            if session:
                transferencia_mult(session)
            else:
                print("Você precisa fazer login primeiro.")
        elif escolha == '5':
            if session:
                transferencia_mult(session)
            else:
                print("Você precisa fazer login primeiro.")
        elif escolha == '6':
            if session:
                transferencia_concorrente(session)
            else:
                print("Você precisa fazer login primeiro.")
        

def transferencia(session, cpf_origem, numero_origem, cpf_destino, numero_destino, valor, nome_banco_origem, nome_banco_destino):
    url = f"{base_url}/transferencia"
    payload = {
        "contas_origem": [{"cpf": cpf_origem, "numero": numero_origem, "valor": valor, "nome_banco": nome_banco_origem}],
        "cpf_destino": cpf_destino,
        "numero_destino": numero_destino,
        "nome_banco_destino": nome_banco_destino
    }
    response = session.post(url, json=payload)
    print(response.json())


def transferencia_concorrente(session):
    cpf_origem = input("CPF da conta de origem: ")
    numero_origem = input("Número da conta de origem: ")
    valor = float(input("Valor a transferir (por transferência): "))
    print("Nome do banco de origem: ")
    print("1. banco_a")
    print("2. banco_b")
    print("3. banco_c")
    escolha = input("Escolha uma opção (1/2/3): ")
    if escolha == '1':
        nome_banco_origem = 'banco_a'
    elif escolha == '2':
        nome_banco_origem = 'banco_b'
    elif escolha == '3':
        nome_banco_origem = 'banco_c'
    
    cpf_destino1 = input("CPF do destinatário 1: ")
    numero_destino1 = input("Número da conta de destino 1: ")
    print("Nome do banco de destino 1: ")
    print("1. banco_a")
    print("2. banco_b")
    print("3. banco_c")
    escolha = input("Escolha uma opção (1/2/3): ")
    if escolha == '1':
        nome_banco_destino1 = 'banco_a'
    elif escolha == '2':
        nome_banco_destino1 = 'banco_b'
    elif escolha == '3':
        nome_banco_destino1 = 'banco_c'
    
    cpf_destino2 = input("CPF do destinatário 2: ")
    numero_destino2 = input("Número da conta de destino 2: ")
    print("Nome do banco de destino 2: ")
    print("1. banco_a")
    print("2. banco_b")
    print("3. banco_c")
    escolha = input("Escolha uma opção (1/2/3): ")
    if escolha == '1':
        nome_banco_destino2 = 'banco_a'
    elif escolha == '2':
        nome_banco_destino2 = 'banco_b'
    elif escolha == '3':
        nome_banco_destino2 = 'banco_c'

    threads = [
        threading.Thread(target=transferencia, args=(session, cpf_origem, numero_origem, cpf_destino1, numero_destino1, valor, nome_banco_origem, nome_banco_destino1)),
        threading.Thread(target=transferencia, args=(session, cpf_origem, numero_origem, cpf_destino2, numero_destino2, valor, nome_banco_origem, nome_banco_destino2))
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

def status():
    try:
        url = f"{base_url}/status"
        response = requests.get(url)
        if response.status_code == 200:
            print("Banco online")
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False


def main():
    session = None
    while True:
        on=status()
        print("\n--- Menu ---")
        print("1. Criar conta PF")
        print("2. Criar conta PJ")
        print("3. Criar conta conjunta")
        print("4. Login")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")
        if escolha == '5':
            break
        if on == False:
            escolha= '0'
        elif escolha == '1':
            criar_conta_pf()
        elif escolha == '2':
            criar_conta_pj()
        elif escolha == '3':
            criar_conta_conjunta()
        elif escolha == '4':
            session = login()
            sub_menu(session)
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()