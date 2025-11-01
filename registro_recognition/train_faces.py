# train_faces.py
# Script para gerar encodings.pkl a partir do modelo ColetaDeFaces
import os, django, pickle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()
from registro.models import ColetaDeFaces
import face_recognition

def treinar_faces():
    encodings, nomes, niveis = [], [], []
    coletas = ColetaDeFaces.objects.all()
    for coleta in coletas:
        try:
            imagem_path = coleta.imagem.path
        except Exception as e:
            print('⚠ Não foi possível obter o caminho da imagem para', coleta.nome, e)
            continue
        img = face_recognition.load_image_file(imagem_path)
        faces = face_recognition.face_encodings(img)
        if faces:
            encodings.append(faces[0])
            nomes.append(coleta.nome)
            niveis.append(coleta.nivel)
        else:
            print('⚠ Nenhum rosto detectado em:', coleta.nome)

    with open('encodings.pkl', 'wb') as f:
        pickle.dump((encodings, nomes, niveis), f)
    print('✅ Treinamento concluído. encodings.pkl salvo.')

if __name__ == '__main__':
    treinar_faces()
