import psycopg2
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

def conectar():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def inserir_dados(query, data):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        st.success("Dados inseridos com sucesso!")
    except Exception as e:
        st.error(f"Erro ao inserir dados: {e}")
    finally:
        cursor.close()
        conn.close()

def visualizar_dados(query):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        st.error(f"Erro ao visualizar dados: {e}")
    finally:
        cursor.close()
        conn.close()

def atualizar_dados(query, data):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        st.success("Dados atualizados com sucesso!")
    except Exception as e:
        st.error(f"Erro ao atualizar dados: {e}")
    finally:
        cursor.close()
        conn.close()

def deletar_dados(query, data):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        st.success("Dados deletados com sucesso!")
    except Exception as e:
        st.error(f"Erro ao deletar dados: {e}")
    finally:
        cursor.close()
        conn.close()
