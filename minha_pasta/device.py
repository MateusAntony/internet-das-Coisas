import socket
import time
import threading
import random

class ElectricFenceDevice:
    def __init__(self, device_id, broker_host, broker_port):
        self.device_id = device_id
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.running = False
        self.voltage = 0
        self.lock = threading.Lock()

    def connect_broker(self):
        try:
            self.socket.connect((self.broker_host, self.broker_port))
            self.connected = True
            print(f"Conectado no broker: {self.broker_host}:{self.broker_port}")
        except socket.error as e:
            print(f'Erro ao conectar no broker: {e}')

    def start(self):
        if not self.connected:
            self.connect_broker()
        if self.connected:
            self.running = True
            #threading.Thread(target=self.send_data).start()
            threading.Thread(target=self.receive_commands).start()

    def send_data(self):
        while self.running:
            with self.lock:
                self.voltage = random.randint(1000, 5000)
                data = f'Voltagem:{self.voltage}V'
                try:
                    self.socket.sendall(data.encode())  # Correção aqui
                except socket.error as e:
                    print(f"Erro ao enviar dados! {e}")
            time.sleep(5)

    def receive_commands(self):
            try:
                command = self.socket.recv(1024).decode()
                print(command)
                if command:
                    self.handle_command(command)
            except socket.error as e:
                print(f"Erro ao receber o comando! {e}")

    def handle_command(self, command):
        with self.lock:
            if command == "ON" and  self.running:
                print(f"Comando recebido: {command}")
                self.running = True
                print(f"Cerca elétrica ligada\nVoltagem: {self.voltage}V")
            elif command == "OFF" and self.running:
                print(f"Comando recebido: {command}")
                self.running = False
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
        device.start()
        devices.append(device)



