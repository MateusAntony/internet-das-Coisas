import socket
import time
import threading
import random

class ElectricFenceDevice:
    def __init__(self, device_id, broker_host, broker_port):
        # Inicialização do dispositivo de cerca elétrica
        self.device_id = device_id
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Criação de um socket TCP/IP
        self.connected = False  # Estado de conexão com o broker
        self.running = False  # Estado de operação da cerca elétrica
        self.voltage = 0  # Valor da voltagem simulada
        self.lock = threading.Lock()  # Lock para garantir acesso seguro a recursos compartilhados

    def connect_broker(self):
        # Método para conectar ao broker
        try:
            self.socket.connect((self.broker_host, self.broker_port))  # Conexão ao broker
            self.connected = True  # Define o estado de conexão como True
            print(f"Conectado no broker: {self.broker_host}:{self.broker_port}")
        except socket.error as e:
            print(f'Erro ao conectar no broker: {e}')

    def start(self):
        # Método para iniciar o dispositivo
        if not self.connected:
            self.connect_broker()  # Conecta ao broker, se ainda não estiver conectado
        if self.connected:
            self.running = True  # Define o estado de operação como True
            threading.Thread(target=self.receive_commands).start()  # Inicia uma thread para receber comandos do broker

    def send_data(self):
        # Método para enviar dados simulados ao broker (não utilizado neste exemplo)
        while self.running:
            with self.lock:
                self.voltage = random.randint(1000, 5000)
                data = f'Voltagem:{self.voltage}V'
                try:
                    self.socket.sendall(data.encode())  # Envio dos dados de voltagem ao broker
                except socket.error as e:
                    print(f"Erro ao enviar dados! {e}")
            time.sleep(5)

    def receive_commands(self):
        # Método para receber comandos do broker
        while self.running:
            try:
                command = self.socket.recv(1024).decode()  # Recebe comandos do broker
                print(command)
                if command:
                    self.handle_command(command)  # Chama o método para lidar com o comando recebido
            except socket.error as e:
                print(f"Erro ao receber o comando! {e}")

    def handle_command(self, command):
        # Método para lidar com os comandos recebidos do broker
        with self.lock:
            if command == "ON" and self.running == False:
                print(f"Comando recebido: {command}")
                self.running = True  # Liga a cerca elétrica
                print(f"Cerca elétrica ligada\nVoltagem: {self.voltage}V")
            elif command == "OFF" and self.running == True:
                print(f"Comando recebido: {command}")
                self.running = False  # Desliga a cerca elétrica
                print("Cerca elétrica desligada")


if __name__ == "__main__":
    # Configurações para as duas cercas elétricas pré-cadastradas
    devices_config = [
        {'id': '1', 'broker_host': '127.0.0.1', 'broker_port': 123},
        {'id': '2', 'broker_host': '127.0.0.1', 'broker_port': 123}
    ]

    # Criar e iniciar as duas cercas elétricas
    devices = []
    for config in devices_config:
        device = ElectricFenceDevice(config['id'], config['broker_host'], config['broker_port'])
        device.start()  # Inicia cada dispositivo
        devices.append(device)  # Adiciona o dispositivo à lista de dispositivos