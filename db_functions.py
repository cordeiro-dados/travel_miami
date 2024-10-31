import psycopg2
import streamlit as st
from dotenv import load_dotenv
import os
from databricks import sql

load_dotenv()
DB_SERVER_HOSTNAME = os.getenv("DB_SERVER_HOSTNAME")
DB_HTTP_PATH = os.getenv("DB_HTTP_PATH")
DB_ACCESS_TOKEN = os.getenv("DB_ACCESS_TOKEN")

def conectar():
    return sql.connect(
        server_hostname=DB_SERVER_HOSTNAME,
        http_path=DB_HTTP_PATH,
        access_token=DB_ACCESS_TOKEN
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

def visualizar_dados(query, params=None):
    try:
        conn = conectar()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
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
