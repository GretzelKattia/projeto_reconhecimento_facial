# Documentação Técnica - Sistema de Registro e Login com Reconhecimento Facial

Este documento oferece uma análise técnica detalhada do sistema, explicando seu propósito, arquitetura, fluxo de dados e os componentes de código mais relevantes.

## 1. Visão Geral do Projeto

O propósito central deste projeto é implementar um sistema web em Django que oferece um método de **autenticação duplo**:

1.  **Autenticação Tradicional:** Login com nome de usuário e senha.
2.  **Autenticação Biométrica:** Login através de reconhecimento facial em tempo real, utilizando a webcam do usuário.

O fluxo principal para o usuário é:

-   **Cadastro:** Um novo funcionário se registra fornecendo seus dados pessoais e uma foto nítida do seu rosto.
-   **Processamento:** O sistema analisa a foto, detecta o rosto e gera uma **"assinatura facial"** (um vetor numérico de 128 dimensões, conhecido como *encoding*), que é armazenada de forma segura no banco de dados.
-   **Login Facial:** Na tela de login, o usuário pode ativar a câmera. O sistema captura um frame, gera um novo *encoding* do rosto detectado e o compara com as assinaturas salvas. Se uma correspondência for encontrada, o usuário é autenticado e logado.

## 2. Arquitetura e Estrutura de Arquivos

-   `manage.py`: Script de linha de comando padrão do Django para tarefas administrativas.
-   `gestao/`: Diretório de configuração do projeto Django.
    -   `settings.py`: Define todas as configurações do projeto, como `INSTALLED_APPS`, banco de dados, caminhos de arquivos estáticos (`STATIC_URL`) e de mídia (`MEDIA_URL`).
    -   `urls.py`: Arquivo de roteamento principal que direciona as requisições para as URLs do aplicativo `registro`.
-   `registro_recognition/registro/`: O aplicativo Django que contém a lógica principal do sistema.
    -   `views.py`: O cérebro da aplicação. Contém as funções que processam as requisições HTTP e implementam a lógica de negócio.
    -   `models.py`: (Não fornecido, mas define os modelos `Funcionario` e `ColetaDeFaces`, que estruturam como os dados são salvos no banco).
    -   `forms.py`: Define os formulários Django para validação e coleta de dados do usuário (`UserForm`, `FuncionarioForm`, `ColetaDeFacesForm`).
    -   `templates/registro/`: Contém os arquivos HTML que renderizam a interface do usuário (`login.html`, `dashboard.html`, `cadastro.html`).
-   `static/`: Contém arquivos estáticos como CSS e JavaScript globais.
-   `media/`: Diretório onde as imagens de perfil enviadas pelos usuários são armazenadas.

---

## 3. Blocos de Código Mais Relevantes

Estes são os trechos de código que formam o núcleo funcional do sistema de reconhecimento facial.

### Bloco 1: Geração da Assinatura Facial no Cadastro

Este trecho, localizado na view `cadastro_view`, é executado quando um novo usuário envia o formulário de registro com sua foto. Ele é responsável por processar a imagem e extrair o *encoding* facial.

📍 **Arquivo:** `registro_recognition/registro/views.py`

```python
# ... dentro da função cadastro_view ...

try:
    # 1. Abre a imagem enviada pelo usuário com a biblioteca Pillow
    img_pil = Image.open(coleta.image)
    img_rgb = img_pil.convert('RGB') # Garante que a imagem está no formato de cor correto (RGB)
    
    # 2. Converte a imagem para um array NumPy, o formato esperado pela biblioteca face_recognition
    imagem_carregada = np.array(img_rgb)
    
    # 3. A função principal: detecta rostos e gera os encodings
    encodings = face_recognition.face_encodings(imagem_carregada)

    if encodings:
        # 4. Se um rosto foi encontrado, pega o primeiro encoding (assumindo uma pessoa por foto)
        encoding_list = encodings[0].tolist()
        
        # 5. Converte o array NumPy para uma lista Python e depois para uma string JSON para salvar no banco
        coleta.encoding = json.dumps(encoding_list)
        coleta.save() # Salva o objeto ColetaDeFaces com a imagem e o encoding
        
        return redirect('login')
    else:
        # Se nenhum rosto for detectado, adiciona um erro ao formulário
        coleta_form.add_error('image', 'Nenhum rosto foi detectado na imagem. Por favor, envie outra foto.')

except Exception as e:
    coleta_form.add_error('image', f'Erro ao processar a imagem: {e}')
```

**Importância:** Este bloco é a fundação do sistema. Sem a geração e armazenamento correto do *encoding*, o reconhecimento facial no login seria impossível.

### Bloco 2: Reconhecimento Facial em Tempo Real

Esta é a API chamada pelo frontend durante o login facial. Ela recebe uma imagem da webcam, processa-a e a compara com todos os registros no banco de dados.

📍 **Arquivo:** `registro_recognition/registro/views.py`

```python
def reconhecer_rosto(request):
    if request.method == 'POST':
        try:
            # ... (decodifica a imagem em base64 recebida do frontend)
            # ...

            # 1. Gera o encoding do rosto capturado pela webcam
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings_rosto_atual = face_recognition.face_encodings(rgb_img)

            if not encodings_rosto_atual:
                return JsonResponse({'success': False, 'message': 'Nenhum rosto detectado na captura.'})

            encoding_rosto_atual = encodings_rosto_atual[0]

            # 2. Busca todos os encodings conhecidos do banco de dados
            faces_conhecidas = ColetaDeFaces.objects.all()
            encodings_conhecidos = [json.loads(face.encoding) for face in faces_conhecidas]
            
            # 3. Compara o rosto atual com todos os rostos conhecidos
            # A tolerância (tolerance=0.5) define o quão estrita é a comparação. Valores menores são mais estritos.
            matches = face_recognition.compare_faces(encodings_conhecidos, encoding_rosto_atual, tolerance=0.5)

            if True in matches:
                # 4. Se encontrou uma correspondência, identifica o usuário e realiza o login
                first_match_index = matches.index(True)
                face_encontrada = faces_conhecidas[first_match_index]
                user = face_encontrada.funcionario.user
                
                login(request, user) # Usa o sistema de autenticação do Django para logar o usuário
                return JsonResponse({'success': True, 'user': user.username})

            return JsonResponse({'success': False, 'message': 'Rosto não reconhecido.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro no servidor: {str(e)}'})
```

**Importância:** Este é o motor da funcionalidade de login facial. Ele executa a comparação biométrica e integra-se diretamente com o sistema de autenticação do Django para garantir o acesso seguro.

### Bloco 3: Interação com a Câmera no Frontend

Este script JavaScript na página de login gerencia a interação com o usuário, o acesso à câmera, a captura da imagem e a comunicação assíncrona com o backend Django.

📍 **Arquivo:** `registro_recognition/registro/templates/registro/login.html`

```javascript
async function captureAndRecognize() {
    // ... (verifica se a câmera está ativa)

    // 1. Desenha o frame atual do vídeo da câmera em um <canvas> invisível
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

    // 2. Converte a imagem do canvas para o formato base64 (string de texto)
    const imageDataUrl = canvas.toDataURL('image/jpeg');

    try {
        // 3. Envia a imagem para a API no backend usando fetch()
        const response = await fetch(reconhecerRostoUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // Token de segurança do Django
            },
            body: JSON.stringify({ image: imageDataUrl }) // Envia a imagem no corpo da requisição
        });

        const result = await response.json(); // Aguarda a resposta do servidor

        // 4. Atualiza a interface do usuário com base no sucesso ou falha do reconhecimento
        if (result.success) {
            statusMessage.textContent = `Bem-vindo, ${result.user}! Redirecionando...`;
            setTimeout(() => { window.location.href = dashboardUrl; }, 1500);
        } else {
            statusMessage.textContent = result.message || 'Rosto não reconhecido. Tente novamente.';
        }
    } catch (error) {
        statusMessage.textContent = 'Erro de comunicação com o servidor.';
    }
}
```

**Importância:** Este código conecta a experiência do usuário no navegador com a lógica poderosa do backend. Ele demonstra como capturar mídia do hardware do cliente e enviá-la para processamento no servidor de forma assíncrona, criando uma experiência de usuário fluida e moderna.