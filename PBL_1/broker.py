import socket
import threading
import time
from flask import Flask, request, jsonify
from queue import Queue

# Classe que define o serviço de Broker
class BrokerService:
    def __init__(self, port):
        # Inicialização da instância do BrokerService
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.devices = {}  # Dicionário para rastrear dispositivos conectados
        self.lock = threading.Lock() # Lock para sincronização de threads
        self.counter = 1  # Contador para identificar os dispositivos
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket UDP para receber dados
        self.udp_socket.bind((self.host, self.port)) # Ligação do socket UDP ao host e porta especificados
        self.message_queue = Queue() # Fila para armazenar mensagens recebidas

    # Método para iniciar o serviço de Broker
    def start(self):
        # Configuração do socket TCP/IP para aceitar conexões de dispositivos
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Broker iniciado em {self.host}:{self.port}")
        
        # Inicia uma thread para receber dados via UDP
        udp_thread = threading.Thread(target=self.receive_from_device)
        udp_thread.start()

        # Loop principal para aceitar conexões de dispositivos
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Nova conexão de {client_address}")

            # Adiciona o cliente à lista de dispositivos conectados
            with self.lock:
                self.devices[self.counter] = client_socket  # Usando o contador como ID do dispositivo
                self.counter += 1  # Incrementa o contador

            # Inicia uma thread para lidar com a comunicação com o cliente
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    # Método para lidar com a comunicação com um cliente específico
    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                self.broadcast(data, client_socket) # Transmite a mensagem recebida para todos os dispositivos conectados
            except OSError as e:
                print(f"Erro ao lidar com o cliente: {e}")
                self.remove_client(client_socket) # Remove o cliente da lista de dispositivos conectados
                break

    # Método para receber dados de dispositivos via UDP
    def receive_from_device(self):
        while True:
            try:
                data, address = self.udp_socket.recvfrom(1024)
                print(f"Dados recebidos via UDP de {address}: {data.decode()}")
                self.message_queue.put(data.decode()) # Adiciona a mensagem recebida à fila
            except socket.error as e:
                print(f"Erro ao receber dados UDP: {e}")

    # Método para enviar uma mensagem para um dispositivo específico
    def send_to_device(self, device_id, message):
        with self.lock:
            if device_id in self.devices:
                client_socket = self.devices[device_id]
                try:
                    client_socket.sendall(message.encode())
                    print(f'Mensagem enviada para o dispositivo {device_id}: {message}')
                except ConnectionResetError:
                    self.remove_client(client_socket) # Remove o dispositivo da lista de dispositivos conectados em caso de erro
            else:
                print(f"Dispositivo {device_id} não está conectado.")

    # Método para listar os dispositivos conectados
    def list_devices(self):
        with self.lock:
            devices = [{'device_id': str(client_address), 'status': 'connected'} for client_address in self.devices.keys()]
            return devices

    # Método para remover um cliente da lista de dispositivos conectados
    def remove_client(self, client_socket):
        with self.lock:
            for client_address, sock in list(self.devices.items()):
                if sock == client_socket:
                    sock.close()
                    del self.devices[client_address]
                    print(f"Device {client_address} desconectado.")

# Configuração da aplicação Flask
app = Flask(__name__)
broker_inst = BrokerService(port=5555) # Instância do BrokerService
broker_thread = threading.Thread(target=broker_inst.start) # Thread para iniciar o serviço de Broker
broker_thread.start() # Inicia a thread

# Rotas da API RESTful para interagir com o serviço de Broker

#Rota para reiniciar device
@app.route('/reiniciar-dispositivo/<device_id>', methods=['POST'])
def reiniciar_dispositivo(device_id):
    broker_inst.send_to_device(int(device_id), "RESTART")  # Envia comando para reiniciar o dispositivo
    if not broker_inst.message_queue.empty():  # Verifica se a fila de mensagens não está vazia
        last_message = broker_inst.message_queue.get()  # Obtém a última mensagem da fila
        voltagem = last_message.split(',')[0].split(':')[1]  # Obtém a voltagem da mensagem
        return jsonify({'success': 'Estado: Dispositivo Reiniciado', 'message':f'Voltagem: {voltagem}'}), 200  # Retorna resposta JSON com sucesso e mensagem

    
#Rota para conectar cliente 
@app.route('/client-conectado', methods=['POST'])
def client_conectado():
    client_id = request.json.get('client_id')  # Obtém o ID do cliente da solicitação JSON
    print(f"Client {client_id} conectado ao broker.")  
    return jsonify({'success': True}), 200  

#Rota para ligar um device
@app.route('/ligar-device/<device_id>', methods=['POST'])
def ligar_device(device_id):
    broker_inst.send_to_device(int(device_id), "ON")  # Envia comando para ligar o dispositivo
    time.sleep(3)  # Aguarda 3 segundos para receber a resposta
    if not broker_inst.message_queue.empty():  # Verifica se a fila de mensagens não está vazia
        last_message = broker_inst.message_queue.get()  # Obtém a última mensagem da fila
        voltagem = last_message.split(',')[0].split(':')[1]  # Obtém a voltagem da mensagem
        return jsonify({'success': 'Estado: Ligado', 'message':f'Voltagem: {voltagem}'}), 200  
    else:
        return jsonify({'success': False, 'message': 'Nenhuma mensagem recebida'}), 404  


#Rota para desligar um device
@app.route('/desligar-device/<device_id>', methods=['POST'])
def desligar_device(device_id):
    broker_inst.send_to_device(int(device_id), "OFF")  # Envia comando para desligar o dispositivo
    return jsonify({'success': 'Estado: Desligado', 'message': 'Dispositivo desligado com sucesso'}), 200  


#Rota para listar todos os devices
@app.route('/listar-dispositivos', methods=['GET'])
def listar_dispositivos():
    devices = broker_inst.list_devices()  # Obtém a lista de dispositivos conectados
    return jsonify(devices), 200  


#Rota para desconectar o cliente
@app.route('/client-desconectado/<client_id>', methods=['DELETE'])
def client_desconectado(client_id):
    print(f"Cliente {client_id} desconectado.")  # Exibe mensagem no console
    return jsonify({'success': True}), 200  

# Inicia a execução da aplicação Flask
if __name__ == '__main__':
    app.run(host= broker_inst.host, port=6000)
