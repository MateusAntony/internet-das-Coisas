import socket
import threading
import time
from flask import Flask, request, jsonify

class BrokerService:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {}  # Dicionário para rastrear dispositivos conectados
        self.lock = threading.Lock()
        self.counter = 1 
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((self.host, self.port))

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Broker iniciado em {self.host}:{self.port}")
        
        udp_thread = threading.Thread(target=self.receive_from_device)
        udp_thread.start()  # Inicia a thread para receber dados via UDP

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Nova conexão de {client_address}")

            with self.lock:
                self.clients[self.counter] = client_socket  # Usando o contador como ID do dispositivo
                self.counter += 1  # Incrementa o contador

            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

        
    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                self.broadcast(data, client_socket)
            except OSError as e:
                print(f"Erro ao lidar com o cliente: {e}")
                self.remove_client(client_socket)
                break

    def receive_from_device(self):
        while True:
            try:
                data, address = self.udp_socket.recvfrom(1024)
                print(f"Dados recebidos via UDP de {address}: {data.decode()}")
            except socket.error as e:
                print(f"Erro ao receber dados UDP: {e}")

    def send_to_device(self, device_id, message):
        with self.lock:
            if device_id in self.clients:
                client_socket = self.clients[device_id]
                try:
                    client_socket.sendall(message.encode())
                    print(f'Mensagem enviada para o dispositivo {device_id}: {message}')
                except ConnectionResetError:
                    self.remove_client(client_socket)
            else:
                print(f"Dispositivo {device_id} não está conectado.")

    def list_devices(self):
        with self.lock:
            devices = [{'device_id': str(client_address), 'status': 'connected'} for client_address in self.clients.keys()]
            return devices

    def broadcast(self, message, sender_socket):
        for client_address, client_socket in self.clients.items():
            if client_socket != sender_socket:
                try:
                    client_socket.sendall(message)
                except ConnectionResetError:
                    self.remove_client(client_socket)

    def remove_client(self, client_socket):
        with self.lock:
            for client_address, sock in list(self.clients.items()):
                if sock == client_socket:
                    sock.close()
                    del self.clients[client_address]
                    print(f"Cliente {client_address} desconectado.")

app = Flask(__name__)
broker_inst = BrokerService(host="127.0.0.1", port=5555)
broker_thread = threading.Thread(target=broker_inst.start)
broker_thread.start()


@app.route('/ligar-device/<device_id>', methods=['POST'])
def ligar_device(device_id):
    broker_inst.send_to_device(int(device_id), "ON")
    return jsonify({'success': True, 'message': 'Dispositivo ligado com sucesso'}), 200

@app.route('/desligar-device/<device_id>', methods=['POST'])
def desligar_device(device_id):
    broker_inst.send_to_device(int(device_id), "OFF")
    return jsonify({'success': True, 'message': 'Dispositivo desligado com sucesso'}), 200

@app.route('/enviar-mensagem/<device_id>', methods=['POST'])
def enviar_mensagem(device_id):
    data = request.get_json()
    message = data.get('mensagem')
    if message:
        broker_inst.send_to_device(int(device_id), str(message))
        return jsonify({'success': True, 'message': 'Mensagem enviada com sucesso'}), 200
    else:
        return jsonify({'success': False, 'message': 'Parâmetro "mensagem" ausente'}), 400

@app.route('/listar-dispositivos', methods=['GET'])
def listar_dispositivos():
    devices = broker_inst.list_devices()
    return jsonify(devices), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
