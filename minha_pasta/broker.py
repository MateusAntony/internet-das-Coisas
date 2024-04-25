from flask import Flask, request, jsonify
import socket
import threading

app = Flask(__name__)

class BrokerService:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {}  # Dicionário para armazenar clientes conectados (ID: socket)
        self.device_data = {}  # Dicionário para armazenar dados de dispositivos (device_id: data)
        self.client_id_counter = 0  # Contador de IDs de cliente
        self.lock = threading.Lock()  # Lock para garantir acesso seguro aos recursos compartilhados
        self.condition = threading.Condition()  # Condição para sinalizar atualização do dicionário de clientes
    
    def start(self):
        # Inicia o servidor socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)  # Permite até 5 conexões pendentes
        print(f"Broker iniciado em {self.host}:{self.port}")

        while True:
            # Aceita novas conexões de clientes e inicia uma nova thread para cada cliente
            client_socket, client_address = server_socket.accept()
            print(f"Nova conexão de {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        with self.lock:
            # Adiciona o novo cliente ao dicionário com um ID incremental
            self.clients[self.client_id_counter] = client_socket
            print(f"Novo cliente adicionado. ID: {self.client_id_counter}")
            self.client_id_counter += 1
        
        # Sinaliza que o dicionário de clientes foi atualizado
        with self.condition:
            self.condition.notify_all()

        # Inicia uma nova thread para lidar com esse cliente
        threading.Thread(target=self.client_handler, args=(client_socket,)).start()

    def client_handler(self, client_socket):
        # Lida com as mensagens recebidas do cliente e transmite para os outros clientes
        while True:
            try:
                data = client_socket.recv(1024)  # Recebe dados do cliente
                if not data:
                    break
                self.broadcast(data, client_socket)  # Transmite dados recebidos para outros clientes
            except ConnectionResetError:
                self.remove_client(client_socket)  # Remove cliente em caso de erro de conexão

    def send_to_device(self, device_id, message):
        # Envia mensagem para um dispositivo específico
        print(f'Aguardando dicionário de clientes atualizar...')
        with self.condition:
            self.condition.wait(timeout=5)  # Aguarda atualização do dicionário de clientes
        
        with self.lock:
            if device_id in self.clients:
                client_socket = self.clients[device_id]
                print(f'Enviando mensagem para o dispositivo {device_id}: {message}')
                try:
                    client_socket.sendall(message.encode())
                except ConnectionResetError:
                    pass
            else:
                print(f'Dispositivo {device_id} não encontrado.')
                print(self.clients)

    def broadcast(self, message, sender_socket):
        # Transmite mensagem para todos os clientes, exceto o remetente
        with self.lock:
            for client_address, client_socket in self.clients.items():
                if client_socket != sender_socket:
                    try:
                        client_socket.sendall(message)
                    except ConnectionResetError:
                        pass

    def remove_client(self, client_socket):
        # Remove cliente desconectado do dicionário de clientes
        with self.lock:
            for client_address, socket in self.clients.items():
                if socket == client_socket:
                    del self.clients[client_address]
                    print(f"Cliente {client_address} desconectado.")

    def get_connected_devices(self):
        # Retorna uma lista de IDs de dispositivos conectados
        with self.lock:
            return list(self.clients.keys())
    
    def get_device_data(self, device_id):
        # Retorna os dados do dispositivo com o ID especificado
        with self.lock:
            return self.device_data.get(device_id)

broker = BrokerService(host="127.0.0.1", port=123)
threading.Thread(target=broker.start).start()

@app.route('/broker/send_command/<device_id>', methods=['POST'])
def send_command(device_id):
    # Rota para enviar um comando para um dispositivo específico
    command = request.json.get('command')
    if command:
        broker.send_to_device(device_id, command)
        return jsonify({'response': 'Command sent successfully'}), 200
    else:
        return jsonify({'error': 'No command provided'}), 400

@app.route('/broker/devices', methods=['GET'])
def get_devices():
    # Rota para obter a lista de dispositivos conectados
    devices = broker.get_connected_devices()
    return jsonify({'devices': devices}), 200

@app.route('/broker/receive_data/<device_id>', methods=['GET'])
def receive_data(device_id):
    # Rota para receber dados de um dispositivo específico
    device_data = broker.get_device_data(device_id)
    if device_data:
        return jsonify({'data': device_data}), 200
    else:
        return jsonify({'error': 'No data available for this device'}), 404
    
if __name__ == "__main__":
    app.run(debug=True, port=5002)  # Inicia o servidor Flask