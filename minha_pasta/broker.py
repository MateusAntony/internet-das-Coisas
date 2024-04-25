from flask import Flask, request, jsonify
import socket
import threading

app = Flask(__name__)

class BrokerService:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {}
        self.client_id_counter = 0  # Inicializando o contador de IDs de cliente
        self.lock = threading.Lock()
        self.condition = threading.Condition()  # Condição para sinalizar que o dicionário de clientes foi atualizado
    
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Broker iniciado em {self.host}:{self.port}")

        while True:
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
        print(self.clients)

    def client_handler(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                self.broadcast(data, client_socket)
            except ConnectionResetError:
                self.remove_client(client_socket)

    def send_to_device(self, device_id, message):
        print(f'Aguardando dicionário de clientes atualizar...')
        with self.condition:
            # Aguarda até que o dicionário de clientes tenha sido atualizado
            self.condition.wait(timeout=5)
        
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
        with self.lock:
            for client_address, client_socket in self.clients.items():
                if client_socket != sender_socket:
                    try:
                        client_socket.sendall(message)
                    except ConnectionResetError:
                        pass

    def remove_client(self, client_socket):
        with self.lock:
            for client_address, socket in self.clients.items():
                if socket == client_socket:
                    del self.clients[client_address]
                    print(f"Cliente {client_address} desconectado.")

broker = BrokerService(host="127.0.0.1", port=123)
threading.Thread(target=broker.start).start()

@app.route('/broker/send_command/<device_id>', methods=['POST'])
def send_command(device_id):
    command = request.json.get('command')
    if command:
        broker.send_to_device(device_id, command)
        return jsonify({'response': 'Command sent successfully'}), 200
    else:
        return jsonify({'error': 'No command provided'}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5002)
