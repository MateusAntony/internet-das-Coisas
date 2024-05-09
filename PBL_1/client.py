import requests
import json
import time
import os

API_URL = "http://"+os.getenv('ip')+":8080" 

# Função para reiniciar um dispositivo específico
def reiniciar_dispositivo(device_id):
    url = f"{API_URL}/reiniciar-dispositivo/{device_id}"
    response = requests.post(url)
    content = response.json()

    if 'success' in content and 'message' in content:
        print(content['success'])
        print(content['message'])

# Função para listar os dispositivos disponíveis e selecionar um
def selecionar_dispositivo():
    url = f"{API_URL}/listar-dispositivos"
    response = requests.get(url)
    devices = response.json()
    print("Dispositivos disponíveis:")
    for device in devices:
        print(f"ID: {device['device_id']}")
    selected_device_id = input("Digite o ID do dispositivo que deseja selecionar: ")
    return selected_device_id

# Função para ligar um dispositivo selecionado
def ligar_dispositivo(device_id):
    url = f"{API_URL}/ligar-device/{device_id}"
    response = requests.post(url)
    content = response.json()

    if 'success' in content and 'message' in content:
        print(content['success'])
        print(content['message'])

# Função para desligar um dispositivo selecionado
def desligar_dispositivo(device_id):
    url = f"{API_URL}/desligar-device/{device_id}"
    response = requests.post(url)
    content = response.json()

    if 'success' in content and 'message' in content:
        print(content['success'])
        print(content['message'])

# Função para notificar o broker sobre a conexão de um cliente
def notify_broker():
    client_id = input("Digite o ID do cliente: ")
    url = f"{API_URL}/client-conectado"
    data = {'client_id': client_id}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Client conectado ao broker com sucesso.")
        else:
            print("Erro ao conectar client ao broker.")
    except requests.ConnectionError:
        print("Erro de conexão.")
    return client_id

# Função para desconectar um cliente do broker
def desconectar_cliente(client_id):
    url = f"{API_URL}/client-desconectado/{client_id}"
    try:
        response = requests.delete(url)
        if response.status_code == 200:
            print("Cliente desconectado com sucesso.")
        else:
            print("Erro ao desconectar cliente.")
    except requests.ConnectionError:
        print("Erro de conexão ao desconectar cliente.")

if __name__ == "__main__":
    client_id = notify_broker()  # Notifica o broker sobre a conexão do cliente
    try:
        while True:
            print("1. Selecionar dispositivo")
            print("2. Ligar dispositivo")
            print("3. Desligar dispositivo")
            print("4. Sair")
            print("5. Reiniciar dispositivo")

            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                device_id = selecionar_dispositivo()  # Seleciona um dispositivo disponível
                print(f"Dispositivo selecionado: {device_id}")
            elif escolha == "2":
                if 'device_id' not in locals():
                    print("Nenhum dispositivo selecionado. Selecione um dispositivo primeiro.")
                else:
                    for x in range(5):
                        ligar_dispositivo(device_id)  # Liga o dispositivo selecionado
            elif escolha == "3":
                if 'device_id' not in locals():
                    print("Nenhum dispositivo selecionado. Selecione um dispositivo primeiro.")
                else:
                    desligar_dispositivo(device_id)  # Desliga o dispositivo selecionado
            elif escolha == "4":
                desconectar_cliente(client_id)  # Desconecta o cliente do broker e encerra o programa
                break
            elif escolha == "5":
                if 'device_id' not in locals():
                    print("Nenhum dispositivo selecionado. Selecione um dispositivo primeiro.")
                else:
                    reiniciar_dispositivo(device_id)  # Reinicia o dispositivo selecionado
            else:
                print("Opção inválida. Tente novamente.")
    finally:
        desconectar_cliente(client_id)  # Certifica-se de desconectar o cliente do broker mesmo em caso de erro ou interrupção
