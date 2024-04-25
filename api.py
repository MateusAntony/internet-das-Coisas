from flask import Flask, request, jsonify
from broker import BrokerService  # Importe a classe do broker
import threading

app = Flask(__name__)
broker = BrokerService(host="127.0.0.1", port=55555)  # Crie uma instância do broker

def start_broker():
    print("Starting broker...")
    broker.start()

broker_thread = threading.Thread(target=start_broker)  # Inicie o broker em uma thread separada
broker_thread.start()

devices = {}

@app.route('/devices/<device_id>/command', methods=['POST'])
def send_command(device_id):
    command = request.json.get('command')
    if command:
        # Envie o comando para o broker usando a função do broker
        response = broker.send_to_device(device_id, command)
        return jsonify({'response': response}), 200
    else:
        return jsonify({'error': 'No command provided'}), 400

@app.route('/devices/<device_id>/status', methods=['GET'])
def get_device_status(device_id):
    if device_id in devices:
        # Envie o comando para o broker para obter o status do dispositivo
        response = broker.send_to_device(device_id, 'STATUS')
        return jsonify({'status': response}), 200
    else:
        return jsonify({'error': 'Device not found'}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)