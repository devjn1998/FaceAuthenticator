# -*- coding: utf-8 -*-
import cv2
import numpy as np
import face_recognition
import os
from ultralytics import YOLO
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
from PIL import Image
import io

app = Flask(__name__, static_folder='web')
CORS(app)

model = YOLO('yolov8n-face.pt')

KNOWN_FACES_DIR = 'known_faces'
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

def get_known_faces():
    """Carrega os rostos conhecidos do diretório."""
    known_face_encodings = []
    known_face_names = []
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(KNOWN_FACES_DIR, filename)
            name = os.path.splitext(filename)[0]
            try:
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_face_encodings.append(encodings[0])
                    known_face_names.append(name)
            except Exception as e:
                print(f"Erro ao carregar a imagem {filename}: {e}")
    return known_face_encodings, known_face_names

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/register_page')
def register_page():
    return send_from_directory(app.static_folder, 'register.html')

@app.route('/authenticate_page')
def authenticate_page():
    return send_from_directory(app.static_folder, 'authenticate.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(os.path.join(app.static_folder, 'static'), path)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    image_data = data['image']  

    if not name or not image_data:
        return jsonify({'status': 'error', 'message': 'Nome e imagem são obrigatórios.'}), 400

    try:
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        frame = np.array(image)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detectar rosto
        results = model(rgb_frame)
        face_locations = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                face_locations.append((int(y1), int(x2), int(y2), int(x1)))

        if not face_locations:
            return jsonify({'status': 'error', 'message': 'Nenhum rosto detectado na imagem.'}), 400
        
        if len(face_locations) > 1:
            return jsonify({'status': 'error', 'message': 'Múltiplos rostos detectados. Por favor, envie uma foto com apenas um rosto.'}), 400

        # Salvar a imagem do rosto
        filename = f"{name}.jpg"
        filepath = os.path.join(KNOWN_FACES_DIR, filename)
        image.save(filepath, 'JPEG')
        
        return jsonify({'status': 'success', 'message': f'Rosto de {name} registrado com sucesso.'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    image_data = data['image']

    if not image_data:
        return jsonify({'status': 'error', 'message': 'Imagem é obrigatória.'}), 400

    try:
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        frame = np.array(image)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Carregar rostos conhecidos
        known_face_encodings, known_face_names = get_known_faces()
        if not known_face_encodings:
            return jsonify({'status': 'unauthenticated', 'message': 'Nenhum rosto cadastrado.'})

        # Detectar rostos na imagem recebida
        results = model(rgb_frame)
        face_locations = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                face_locations.append((int(y1), int(x2), int(y2), int(x1)))
        
        if not face_locations:
            return jsonify({'status': 'unauthenticated', 'message': 'Nenhum rosto detectado.'})

        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Retornaremos as informações do primeiro rosto que corresponder
        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Desconhecido"
            status = 'unauthenticated'
            
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    status = 'authenticated'
            
            # Retorna as coordenadas junto com o status da primeira detecção
            # O frontend precisa das coordenadas no formato (left, top, right, bottom)
            top, right, bottom, left = face_location
            return jsonify({
                'status': status, 
                'name': name,
                'box': {'top': top, 'right': right, 'bottom': bottom, 'left': left}
            })

        # Se o loop terminar e não houver correspondência (improvável, mas seguro)
        return jsonify({'status': 'unauthenticated', 'name': 'Desconhecido'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/analyze_frame', methods=['POST'])
def analyze_frame():
    data = request.get_json()
    image_data = data['image'] # Base64 string

    if not image_data:
        return jsonify({'status': 'error', 'message': 'Imagem é obrigatória.'}), 400

    try:
        # Decodificar a imagem
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        frame = np.array(image)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detectar rosto
        results = model(rgb_frame)
        face_locations = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                face_locations.append((int(y1), int(x2), int(y2), int(x1)))

        # Lógica de feedback
        if not face_locations:
            return jsonify({'status': 'NO_FACE', 'message': 'Nenhum rosto detectado.'})
        
        if len(face_locations) > 1:
            return jsonify({'status': 'MULTIPLE_FACES', 'message': 'Múltiplos rostos detectados.'})

        # Analisar a posição do único rosto detectado
        top, right, bottom, left = face_locations[0]
        
        img_height, img_width, _ = rgb_frame.shape
        
        # Área ideal do rosto (baseado no oval do frontend: 45% da largura, 75% da altura)
        ideal_face_area = (img_width * 0.45) * (img_height * 0.75)
        face_area = (right - left) * (bottom - top)

        area_ratio = face_area / ideal_face_area
        
        if area_ratio > 1.4: # Rosto ocupa mais de 140% da área ideal
            return jsonify({'status': 'TOO_CLOSE', 'message': 'Afaste-se um pouco.'})
        if area_ratio < 0.7: # Rosto ocupa menos de 70% da área ideal
            return jsonify({'status': 'TOO_FAR', 'message': 'Aproxime-se um pouco.'})
            
        # Posição ideal do rosto
        ideal_center_x = img_width / 2
        ideal_center_y = img_height / 2
        
        face_center_x = left + (right - left) / 2
        face_center_y = top + (bottom - top) / 2
        
        # Distância do centro
        distance = np.sqrt((face_center_x - ideal_center_x)**2 + (face_center_y - ideal_center_y)**2)
        
        # Se a distância for maior que 10% da largura da imagem
        if distance > (img_width * 0.10):
            return jsonify({'status': 'OFF_CENTER', 'message': 'Centralize o rosto.'})

        return jsonify({'status': 'GOOD_POSITION', 'message': 'Posição ideal!'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run() 