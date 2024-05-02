import socket
import time
import threading
import random

class ElectricFenceDevice:
    def __init__(self, broker_host, broker_port):
        # Inicialização do dispositivo de cerca elétrica
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Criação de um socket TCP/IP
        self.connected = False  # Estado de conexão com o broker
        self.running = False  # Estado de operação da cerca elétrica
        self.voltage = 0  # Valor da voltagem simulada
        self.lock = threading.Lock()  # Lock para garantir acesso seguro a recursos compartilhados
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
            
    def send_broker(self,data):
    # Método para enviar dados simulados ao broker (UDP)
        if self.running:
            try:
                message = ",".join(data)  # Concatenando os elementos da lista em uma única string
                print(f"Mensagem enviada ao broker: {message}")
                self.udp_socket.sendto(message.encode(), (self.broker_host, self.broker_port))  # Envio dos dados ao broker
            except socket.error as e:
                print(f"Erro ao enviar dados! {e}")
            time.sleep(5)
            
            
    def receive_commands(self):
    # Método para receber comandos do broker
        while True:
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
                if command == "ON":
                    print(f"Comando recebido: {command}")
                    self.running = True  # Liga a cerca elétrica
                    self.voltage = random.randint(200, 300)
                    data = [f'Voltagem:{self.voltage}V', str(self.running)]
                    self.send_broker(data)
                    print(f"Cerca elétrica ligada\nVoltagem: {self.voltage}V")
                elif command == "OFF":
                    print(f"Comando recebido: {command}")
                    self.running = False  # Desliga a cerca elétrica
                    data=[str(self.running)]
                    self.send_broker(data)
                    print("Cerca elétrica desligada")


if __name__ == "__main__":
    device = ElectricFenceDevice('127.0.0.1', 5555)
    device2 = ElectricFenceDevice( '127.0.0.1', 5555)
    device.start()  # Inicia cada dispositivo
    device2.start()