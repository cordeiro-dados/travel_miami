import streamlit as st
from multiapp import MultiApp  # Gerenciador para múltiplos apps
import sys
import os

# Adicione o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app_pages import home, locais, atividades, categorias, desccategorias



app = MultiApp()

# Adicionar cada página ao aplicativo
app.add_app("Home", home.app)
app.add_app("Gerenciar Locais", locais.app)
app.add_app("Gerenciar Atividades", atividades.app)
app.add_app("Gerenciar Categorias", categorias.app)
app.add_app("Gerenciar Descrições de Categorias", desccategorias.app)

# Executar o aplicativo
app.run()
