import requests

API_URL = "http://localhost:5000"  # Substitua pelo URL da sua API

def selecionar_dispositivo():
    url = f"{API_URL}/listar-dispositivos"
    response = requests.get(url)
    devices = response.json()
    print("Dispositivos disponíveis:")
    for device in devices:
        print(f"ID: {device['device_id']}")
    selected_device_id = input("Digite o ID do dispositivo que deseja selecionar: ")
    return selected_device_id

def ligar_dispositivo(device_id):
    url = f"{API_URL}/ligar-device/{device_id}"
    response = requests.post(url)
    print(response.json())

def desligar_dispositivo(device_id):
    url = f"{API_URL}/desligar-device/{device_id}"
    response = requests.post(url)
    print(response.json())

if __name__ == "__main__":
    while True:
        print("1. Selecionar dispositivo")
        print("2. Ligar dispositivo")
        print("3. Desligar dispositivo")
        print("4. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            device_id = selecionar_dispositivo()
            print(f"Dispositivo selecionado: {device_id}")
        elif escolha == "2":
            if 'device_id' not in locals():
                print("Nenhum dispositivo selecionado. Selecione um dispositivo primeiro.")
            else:
                ligar_dispositivo(device_id)
        elif escolha == "3":
            if 'device_id' not in locals():
                print("Nenhum dispositivo selecionado. Selecione um dispositivo primeiro.")
            else:
                desligar_dispositivo(device_id)
        elif escolha == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")