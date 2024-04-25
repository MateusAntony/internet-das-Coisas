import requests

API_URL = "http://localhost:5000"  # Substitua pelo URL da sua API

def send_command(device_id, command):
    url = f"{API_URL}/devices/{device_id}/command"
    data = {"command": command}
    response = requests.post(url, json=data)
    print(response.json())

def get_device_status(device_id):
    url = f"{API_URL}/devices/{device_id}/status"
    response = requests.get(url)
    print(response.json())

if __name__ == "__main__":
    while True:
        print("1. Enviar comando para dispositivo")
        print("2. Obter status do dispositivo")
        print("3. Sair")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            device_id = input("Digite o ID do dispositivo: ")
            command = input("Digite o comando a ser enviado: ")
            send_command(device_id, command)
        elif choice == "2":
            device_id = input("Digite o ID do dispositivo: ")
            get_device_status(device_id)
        elif choice == "3":
            break
        else:
            print("Opção inválida. Tente novamente.")