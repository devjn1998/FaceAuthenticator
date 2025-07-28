import cv2
import numpy as np
import face_recognition
import os
from ultralytics import YOLO

# Carregar o modelo YOLO pré-treinado
model = YOLO('yolov8n-face.pt')

# Carregar as imagens conhecidas e seus encodings
known_faces_dir = 'known_faces'
known_face_encodings = []
known_face_names = []

print("Carregando rostos conhecidos...")
for filename in os.listdir(known_faces_dir):
    if filename.endswith(('.jpg', '.png', '.jpeg')):
        image_path = os.path.join(known_faces_dir, filename)
        name = os.path.splitext(filename)[0]
        
        # Carregar a imagem e encontrar os encodings faciais
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        
        if face_encodings:
            encoding = face_encodings[0]
            known_face_encodings.append(encoding)
            known_face_names.append(name)
            print(f"Rosto de {name} carregado.")
        else:
            print(f"Nenhum rosto encontrado em {filename}.")

if not known_face_encodings:
    print("Nenhum rosto conhecido foi carregado. Adicione imagens em 'known_faces'.")
    exit()

# inicia a webcam
video_capture = cv2.VideoCapture(0)

print("Iniciando captura de vídeo...")
while True:
    # Capturar um único frame de vídeo
    ret, frame = video_capture.read()
    if not ret:
        break

    # Redimensionar o frame para um processamento mais rápido
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    
    # Converter a imagem de BGR (OpenCV) para RGB (YOLO e face_recognition)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detectar rostos no frame usando YOLO
    results = model(rgb_small_frame)
    
    face_locations = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # A biblioteca face_recognition espera (top, right, bottom, left)
            face_locations.append((y1, x2, y2, x1))

    # Obter os encodings dos rostos detectados
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # Verificar se o rosto corresponde a algum rosto conhecido
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Desconhecido"

        # Usar o rosto conhecido com a menor distância para o novo rosto
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        face_names.append(name)

    # Exibir os resultados
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Escalar de volta as localizações dos rostos para o tamanho original do frame
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # Calcular o centro e os eixos para a elipse
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2
        axis_x = (right - left) // 2
        axis_y = (bottom - top) // 2

        # Definir a cor: verde para autenticado, vermelho para não autenticado
        color = (0, 255, 0) if name != "Desconhecido" else (0, 0, 255)
        
        # Desenhar uma elipse ao redor do rosto com linha mais grossa
        cv2.ellipse(frame, (center_x, center_y), (axis_x, axis_y), 0, 0, 360, color, thickness=2)

    # Exibir a imagem resultante
    cv2.imshow('Video', frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a captura de vídeo e fechar janelas
video_capture.release()
cv2.destroyAllWindows() 