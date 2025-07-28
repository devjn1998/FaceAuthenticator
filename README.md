# 🚀 Autenticação Facial com IA

Bem-vindo ao projeto de Autenticação Facial, uma aplicação web completa construída com Python, Flask e YOLO. Este sistema permite que usuários se registrem usando a webcam e, posteriormente, se autentiquem em tempo real com reconhecimento facial.

![Demonstração da Interface](https://i.imgur.com/URL_DA_SUA_IMAGEM.gif) 
*Substitua o link acima por um GIF ou screenshot da sua aplicação em funcionamento.*

---

## ✨ Funcionalidades Principais

- **Página de Entrada Moderna:** Interface de boas-vindas com um design limpo e links para as seções principais.
- **Registro de Rosto Inteligente:**
    - **Guia em Tempo Real:** Uma moldura oval na tela ajuda o usuário a posicionar o rosto corretamente.
    - **Feedback Instantâneo:** Dicas como "Aproxime-se", "Afaste-se" e "Centralize o rosto" são exibidas para garantir uma captura de alta qualidade.
    - **Validação de Posição:** O botão de registro só é ativado quando o rosto está perfeitamente enquadrado.
- **Autenticação em Tempo Real:**
    - **Análise Contínua:** O sistema analisa a webcam em tempo real para encontrar um rosto na posição correta.
    - **Autenticação Automática:** Assim que o rosto está bem posicionado, a autenticação é disparada, e a moldura muda de cor para indicar sucesso (verde) ou falha (vermelho).
- **Backend Robusto com IA:**
    - **Detecção com YOLO:** Utiliza o modelo `yolov8n-face` para uma detecção de rostos rápida e precisa.
    - **Reconhecimento Facial:** Usa a biblioteca `face_recognition` para comparar e identificar os rostos.
    - **API com Flask:** Construído com Flask para servir a interface e gerenciar as requisições de forma eficiente.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:**
    - ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
    - ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
    - ![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
- **Inteligência Artificial:**
    - ![Ultralytics](https://img.shields.io/badge/YOLO-Ultralytics-4F46E5?style=for-the-badge)
    - `face_recognition`
    - `dlib`
    - `OpenCV`
- **Frontend:**
    - ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
    - ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
    - ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

---

## 🚀 Como Executar Localmente

Siga os passos abaixo para rodar o projeto em sua máquina local.

### 1. Pré-requisitos
- Python 3.8+
- `pip` (gerenciador de pacotes do Python)
- `git` (sistema de controle de versão)

### 2. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 3. Crie e Ative um Ambiente Virtual
É altamente recomendado usar um ambiente virtual para isolar as dependências.

```bash
# Criar o ambiente
python3 -m venv venv

# Ativar o ambiente (Linux/Mac)
source venv/bin/activate

# Ativar o ambiente (Windows)
.\\venv\\Scripts\\activate
```

### 4. Instale as Dependências
As dependências de sistema para `dlib` e `opencv` podem ser necessárias. Em sistemas baseados em Debian/Ubuntu:
```bash
sudo apt-get update && sudo apt-get install -y cmake libsm6 libxext6
```

Depois, instale as dependências Python:
```bash
pip install -r requirements.txt
```

### 5. Inicie a Aplicação
```bash
python3 app.py
```

Abra seu navegador e acesse `http://127.0.0.1:5000`.

---

## ☁️ Deploy

Este projeto está configurado para deploy na plataforma [Render](https://render.com) utilizando o plano gratuito. Os seguintes arquivos garantem um processo de build suave:
- **`requirements.txt`**: Lista as dependências Python.
- **`Procfile`**: Especifica o comando para iniciar o servidor web com `gunicorn`.
- **`build.sh`**: Instala as dependências de sistema (`cmake`, etc.) antes de instalar os pacotes Python, prevenindo erros de build.

---
