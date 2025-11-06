from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Funcionario, ColetaDeFaces
from django.contrib.auth.models import User
from .forms import FuncionarioForm, UserForm, ColetaDeFacesForm
import base64
from django.db import transaction
import cv2
import numpy as np
from PIL import Image
import face_recognition
import json
import os

def login_view(request):
    """Página de login com usuário/senha e reconhecimento facial."""
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'registro/login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'registro/login.html')

@login_required
def dashboard(request):
    """Dashboard do usuário após o login."""
    try:
        funcionario = request.user.funcionario
        face_data = ColetaDeFaces.objects.get(funcionario=funcionario)
    except Funcionario.DoesNotExist:
        funcionario = None
        face_data = None
    except ColetaDeFaces.DoesNotExist:
        face_data = None

    # Calcular tamanho da imagem em MB
    mb_image = None
    if face_data and face_data.image:
        path = face_data.image.path
        if os.path.exists(path):
            size_bytes = os.path.getsize(path)
            size_mb = size_bytes / (1024 * 1024)
            mb_image = round(size_mb, 2)  # duas casas decimais

    return render(request, 'registro/dashboard.html', {
        'funcionario': funcionario,
        'face_data': face_data,
        'mb_image': mb_image,
    })

@login_required
def logout_view(request):
    """Faz o logout do usuário."""
    logout(request)
    return redirect('login')

def reconhecer_rosto(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data['image'].split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image_np = np.frombuffer(image_bytes, dtype=np.uint8)
            img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings_rosto_atual = face_recognition.face_encodings(rgb_img)

            if not encodings_rosto_atual:
                return JsonResponse({'success': False, 'message': 'Nenhum rosto detectado na captura.'})

            encoding_rosto_atual = encodings_rosto_atual[0]
            faces_conhecidas = ColetaDeFaces.objects.all()
            if not faces_conhecidas.exists():
                return JsonResponse({'success': False, 'message': 'Nenhum rosto cadastrado no sistema.'})

            encodings_conhecidos = [json.loads(face.encoding) for face in faces_conhecidas]
            matches = face_recognition.compare_faces(encodings_conhecidos, encoding_rosto_atual, tolerance=0.5)

            if True in matches:
                first_match_index = matches.index(True)
                face_encontrada = faces_conhecidas[first_match_index]
                user = face_encontrada.funcionario.user
                login(request, user)
                return JsonResponse({'success': True, 'user': user.username})

            return JsonResponse({'success': False, 'message': 'Rosto não reconhecido.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro no servidor: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Método inválido'})

@transaction.atomic
def cadastro_view(request):
    if request.method != 'POST':
        user_form = UserForm()
        funcionario_form = FuncionarioForm()
        coleta_form = ColetaDeFacesForm()
        return render(request, 'registro/cadastro.html', {
            'user_form': user_form,
            'funcionario_form': funcionario_form,
            'coleta_form': coleta_form
        })

    user_form = UserForm(request.POST)
    funcionario_form = FuncionarioForm(request.POST)
    coleta_form = ColetaDeFacesForm(request.POST, request.FILES)

    if user_form.is_valid() and funcionario_form.is_valid() and coleta_form.is_valid():
        username = user_form.cleaned_data['username']
        password = user_form.cleaned_data['password']
        user = User.objects.create_user(username=username, password=password)

        funcionario = funcionario_form.save(commit=False)
        funcionario.user = user
        funcionario.save()

        coleta = ColetaDeFaces(funcionario=funcionario)
        coleta.image = coleta_form.cleaned_data['image']

        try:
            img_pil = Image.open(coleta.image)
            img_rgb = img_pil.convert('RGB')
            imagem_carregada = np.array(img_rgb)
            encodings = face_recognition.face_encodings(imagem_carregada)

            if encodings:
                encoding_list = encodings[0].tolist()
                coleta.encoding = json.dumps(encoding_list)
                coleta.save()
                return redirect('login')
            else:
                coleta_form.add_error('image', 'Nenhum rosto foi detectado na imagem. Por favor, envie outra foto.')
        except Exception as e:
            coleta_form.add_error('image', f'Erro ao processar a imagem: {e}')

    return render(request, 'registro/cadastro.html', {
        'user_form': user_form,
        'funcionario_form': funcionario_form,
        'coleta_form': coleta_form
    })
