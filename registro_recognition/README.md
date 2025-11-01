Registro - Reconhecimento Facial (estrutura pronta)
================================================
Conteúdo:
- registro/ (app Django pronto: models, views, urls, templates, static)
- train_faces.py (script para gerar encodings.pkl)
- requirements.txt (dependências principais)

Instruções rápidas:
1) Extraia esta pasta dentro da raiz do seu projeto Django (onde está manage.py)
2) Adicione 'registro' em INSTALLED_APPS no settings.py
3) Rode migrações se quiser usar o modelo: python manage.py makemigrations registro && python manage.py migrate
4) Cadastre imagens pelo admin (ou diretamente no banco) usando o modelo ColetaDeFaces (nome, nível, imagem)
5) Gere encodings com: python train_faces.py
6) Rode o servidor e acesse /reconhecimento/ (adicione a rota principal no urls do projeto se necessário)

Observações:
- Este pacote usa a biblioteca face_recognition (que depende de dlib). Em sistemas Windows/Linux, a instalação pode requerer ferramentas adicionais.
- Para testar a câmera ao vivo, abra /reconhecimento/ no navegador e clique em "Iniciar Reconhecimento". O browser pedirá permissão para usar a webcam.
- Se quiser, substituo cores/estética ou ajusto a frequência de envio de frames.
