import os
import sys

# Adicione o caminho para o diretório raiz do seu projeto
root_path = '/home/ubuntu/projetos/Plano_Real-APP'
sys.path.insert(0, root_path)

# Atualize o nome do módulo do seu aplicativo
from core.wsgi import wsgi

