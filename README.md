# Sistema de Registro com Reconhecimento Facial

Este é um sistema de registro de funcionários com reconhecimento facial desenvolvido em Django.

## Configuração do Ambiente

### Pré-requisito: Instalar o Miniconda

Antes de começar, você precisa ter o **Miniconda** instalado em sua máquina.

**Por que usar Miniconda/Conda?**
Este projeto utiliza a biblioteca `dlib` para o reconhecimento facial, que possui dependências complexas (C++) difíceis de instalar com o `pip` padrão do Python. O `conda` é um gerenciador de pacotes e ambientes que instala versões pré-compiladas dessas bibliotecas, tornando a configuração simples e livre de erros.

- **Baixe o instalador do Miniconda para o seu sistema operacional aqui**

Após a instalação, você poderá usar os comandos `conda` no seu terminal.

### 1. Criar e Ativar o Ambiente Conda

Primeiro, crie um ambiente Conda com Python 3.9:
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

### 3. Verificar a Instalação

Para verificar se o face_recognition foi instalado corretamente:
```bash
python -c "import face_recognition; print('Face Recognition instalado com sucesso!')"
```

### 4. Configurar o Django

Aplique as migrações do banco de dados:
```bash
python manage.py makemigrations registro
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

O projeto usa:
- Django para o backend e templates
- SQLite como banco de dados
- face_recognition para reconhecimento facial
- OpenCV para processamento de imagens
- Pillow para manipulação de imagens
