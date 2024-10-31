# pages/home.py
import streamlit as st

def app():
    st.title("Aplicativo de Gerenciamento de Viagem")
    st.write("""
    Bem-vindo ao sistema de gerenciamento de viagem.
    
    Use o menu na barra lateral para acessar as seções de Locais, Atividades, Categorias, e Descrições de Categorias.

    Cada seção permite inserir, atualizar ou deletar registros para facilitar a organização da viagem.
    """)
