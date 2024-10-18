from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Diccionario que mapea los textos a las imágenes
images = {
    "banana": "banana.png",
    "papel": "papel.png",
    "manzana": "manzana.png",
    "botella": "botella.png"
}
messages = {
    "banana": "Caneca verde",
    "papel": "Caneca blanca",
    "manzana": "Caneca verde",
    "botella": "Caneca azul"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_image', methods=['POST'])
def get_image():
    data = request.json
    text = data.get('text', '').lower()

    if text in images:
        image = images[text]
        message = messages[text]
    else:
        image = "default.png"
        message = "Imagen no encontrada."

    # Emitir evento de actualización de imagen a través de WebSocket
    socketio.emit('update_image', {'image': image, 'message': message})

    return jsonify({'success': True}), 200

if __name__ == '__main__':
    socketio.run(app, debug=True)
