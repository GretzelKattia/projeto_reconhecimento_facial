# Sistema de Registro e Login com Reconhecimento Facial

Este é um sistema web desenvolvido em Django que permite o registro de funcionários e oferece dois métodos de autenticação:
1.  **Login Tradicional:** Utilizando nome de usuário e senha.
2.  **Login Facial:** Utilizando a webcam para reconhecimento facial em tempo real.

## Visão Geral

O projeto demonstra um fluxo completo de autenticação biométrica em um ambiente web:

-   **Cadastro:** O usuário preenche seus dados (nome, CPF, etc.) e envia uma foto de seu rosto. O sistema processa essa foto para extrair uma "assinatura facial" (um vetor de 128 números, conhecido como *encoding*), que é armazenada no banco de dados.
-   **Autenticação:** Na tela de login, o usuário pode optar por usar a câmera. Ao capturar uma imagem, o sistema gera um novo *encoding* e o compara com todos os *encodings* armazenados. Se uma correspondência for encontrada com um grau de similaridade aceitável, o login é efetuado.
-   **Dashboard:** Após o login, o usuário é direcionado para um painel que exibe suas informações de perfil.

## Tecnologias Utilizadas

-   **Backend:** Django
-   **Banco de Dados:** SQLite (padrão do Django para desenvolvimento)
-   **Reconhecimento Facial:** `face_recognition`
-   **Processamento de Imagem:** `OpenCV-Python`, `Pillow`
-   **Frontend:** HTML, CSS, JavaScript (para interação com a câmera e comunicação com o backend)
-   **Gerenciamento de Ambiente:** Conda (para facilitar a instalação de dependências complexas como o `dlib`)

## Como Funciona

1.  **Geração da Assinatura Facial (Encoding):** Durante o cadastro, a imagem enviada é processada pela função `face_recognition.face_encodings()`. Ela localiza o rosto na imagem e gera um vetor numérico que o representa de forma única. Esse vetor é convertido para uma string JSON e salvo no banco de dados, associado ao funcionário.
2.  **Comparação de Rostos:** Durante o login facial, a função `face_recognition.compare_faces()` é usada. Ela recebe uma lista de *encodings* conhecidos (buscados do banco de dados) e o *encoding* do rosto capturado pela webcam. A função retorna `True` para os rostos que correspondem, com base em um limiar de tolerância (`tolerance=0.5`).
3.  **Integração Django:** As views do Django (`cadastro_view`, `reconhecer_rosto`) orquestram todo o processo, desde receber os dados do formulário e da câmera até interagir com o banco de dados e autenticar o usuário com o sistema de sessões nativo do Django.
## Configuração do Ambiente

### Pré-requisito: Instalar o Miniconda

Antes de começar, é essencial ter o **Miniconda** instalado.

**Por que usar Miniconda/Conda?**
Este projeto utiliza a biblioteca `dlib` para o reconhecimento facial, que possui dependências complexas (C++) difíceis de instalar com o `pip` padrão do Python. O `conda` é um gerenciador de pacotes e ambientes que instala versões pré-compiladas dessas bibliotecas, tornando a configuração simples e livre de erros.

**Baixe o instalador do Miniconda para o seu sistema operacional aqui**.

Após a instalação, você poderá usar os comandos `conda` no seu terminal.

### Passo 1: Criar e Ativar o Ambiente Conda

Primeiro, ativar um ambiente Conda:
```bash
conda CAMINHO_PARA_MINICONDA/miniconda3/Scripts/activate base
```

Depois, crie um ambiente Conda com Python 3.9:
```bash
conda create -n homologado39 python=3.9
```

Para ativar o ambiente:
```bash
conda activate homologado39
```

### 2. Instalar Dependências

A forma mais segura de instalar as dependências é usando o arquivo `requirements.txt`, que contém as versões exatas e compatíveis dos pacotes.

1.  **Instale o `dlib` via Conda:** Esta biblioteca é um pré-requisito para o reconhecimento facial e sua instalação é mais estável via Conda.
    ```bash
    conda install -c conda-forge dlib
    ```

2.  **Instale todas as outras dependências com `pip`:** Este comando instalará todas as bibliotecas Python necessárias de uma só vez.
    ```bash
    pip install -r registro_recognition/requirements.txt
    ```

> **Alternativa (Instalação Manual):** Se preferir instalar manualmente, esteja ciente de que o `pip` pode baixar versões mais recentes dos pacotes que podem causar conflitos.
> ```bash
> pip install django "face-recognition<1.4.0" "opencv-python<4.10" pillow
> ```

<!-- ### 3. Verificar a Instalação

Para verificar se o face_recognition foi instalado corretamente:
```bash
python -c "import face_recognition; print('Face Recognition instalado com sucesso!')"
``` -->

### 4. Configurar o Django

Aplique as migrações do banco de dados:
```bash
# python manage.py makemigrations registro
python manage.py migrate
```

### 5. Rodar o Servidor

Para iniciar o servidor de desenvolvimento:
```bash
python manage.py runserver
```

## Comandos Úteis

### Gerenciamento do Ambiente Conda

- Listar ambientes: `conda env list`
- Ativar ambiente: `conda activate homologado39`
- Desativar ambiente: `conda deactivate`
- Ver pacotes instalados: `conda list`

### Dicas Importantes

1. Sempre use o terminal (Git Bash ou PowerShell) com o ambiente `homologado39` ativado
2. O ambiente foi criado com Python 3.9 por ser uma versão estável compatível com dlib e face_recognition
3. Se houver problemas com o dlib, certifique-se de instalá-lo via Conda e não pip
4. Para desenvolvimento, mantenha o servidor rodando com `python manage.py runserver`

## Solução de Problemas

Se encontrar problemas:

1. Verifique se o ambiente está ativado (`conda env list`)
2. Confirme que todas as dependências estão instaladas (`conda list`)
3. Certifique-se que o dlib foi instalado via Conda
4. Verifique se as migrações foram aplicadas corretamente

### Erros de Banco de Dados (ex: `OperationalError: no such column`)

Se você encontrar erros como `OperationalError: table ... has no column named ...`, isso indica que o banco de dados (`db.sqlite3`) está dessincronizado com os modelos do Django (`models.py`). Em um ambiente de desenvolvimento, a forma mais simples de corrigir isso é recriando o banco de dados.

**Atenção:** Este processo apagará todos os dados existentes (usuários, funcionários, etc.).

1.  **Pare o servidor Django** (pressione `CTRL + C` no terminal).

2.  **Exclua o arquivo do banco de dados** na raiz do projeto:
    ```bash
    rm db.sqlite3
    ```

3.  **Crie e aplique as novas migrações** para construir o banco de dados do zero:
    ```bash
    python manage.py makemigrations registro
    python manage.py migrate
    ```

4.  **Inicie o servidor novamente** e o erro estará resolvido:
    ```bash
    python manage.py runserver
    ```

## Estrutura do Projeto

### Tecnologias Utilizadas
- **Django**: Framework web para backend e templates
- **SQLite**: Banco de dados relacional
- **face_recognition**: Biblioteca principal para reconhecimento facial
- **OpenCV**: Processamento de imagens e captura da webcam
- **Pillow**: Manipulação de imagens
- **NumPy**: Processamento numérico e arrays

### Componentes Principais

#### 1. Módulo de Registro (`registro/views.py`, `registro/models.py`)
- **Funcionario**: Modelo para armazenar dados dos funcionários (nome, CPF, nível de acesso)
- **ColetaDeFaces**: Modelo para armazenar imagens e encodings faciais
- **Cadastro**: View para registrar novos funcionários com foto

#### 2. Sistema de Autenticação
- Login tradicional com usuário/senha
- Login por reconhecimento facial usando webcam
- Proteção de rotas com `@login_required`

#### 3. Dashboard (`templates/registro/dashboard.html`)
- Visualização de dados do funcionário
- Exibição do nível de acesso
- Dados do reconhecimento facial (foto e encoding)

#### 4. Processamento de Imagens (`views.py`)
- Captura de imagem via webcam (JavaScript)
- Conversão de imagem para RGB
- Geração de encodings faciais (128 medidas faciais)
- Comparação de rostos em tempo real

#### 5. Interface (`static/css/`)
- Design responsivo e moderno
- Estilização específica para formulários e dashboard
- Feedback visual para ações do usuário

### Fluxo de Funcionamento

1. **Cadastro de Funcionário**:
   - Criação de usuário no sistema
   - Registro de informações pessoais
   - Upload de foto facial
   - Geração e armazenamento do encoding facial

2. **Autenticação por Reconhecimento**:
   - Captura de imagem via webcam
   - Geração do encoding da imagem capturada
   - Comparação com encodings armazenados
   - Login automático em caso de match

3. **Níveis de Acesso**:
   - Nível 1: Acesso geral
   - Nível 2: Acesso de diretores
   - Nível 3: Acesso exclusivo do ministro

### Segurança
- Senha hasheada pelo Django
- Proteção CSRF em formulários
- Validação de imagens enviadas
- Sessões seguras
- Autorização baseada em decorators

### Arquivos Importantes

```
projeto_reconhecimento_facial/
├── gestao/                    # Configurações do projeto
│   ├── settings.py           # Configurações Django
│   └── urls.py              # URLs principais
├── registro_recognition/
│   └── registro/
│       ├── models.py        # Modelos de dados
│       ├── views.py         # Lógica de negócio
│       ├── forms.py         # Formulários
│       └── templates/       # Templates HTML
├── static/
│   ├── css/                # Estilos
│   └── js/                 # JavaScript
└── media/                  # Arquivos enviados
    └── faces/             # Fotos dos funcionários
```