#!/usr/bin/env bash
# exit on error
set -o errexit

# Instala dependências de sistema para OpenCV e Dlib
apt-get update && apt-get install -y cmake libsm6 libxext6 libxrender-dev

# Instala as dependências Python
pip install -r requirements.txt 