import streamlit as st
import uuid
from db_functions import inserir_dados, visualizar_dados, atualizar_dados, deletar_dados  # Funções CRUD

def app():
    st.title("Gerenciamento de Locais")

    # Selecione a ação desejada
    acao = st.selectbox("Escolha a ação", ["Inserir", "Alterar", "Deletar"])

    if acao == "Inserir":
        st.subheader("Inserir Novo Local")
        nome_local = st.text_input("Nome do Local")
        img_url = st.text_input("URL da Imagem")
        cidade = st.text_input("Cidade")
        pais = st.text_input("País")
        if st.button("Salvar Local"):
            local_id = str(uuid.uuid4())  # Gerar UUID para local_id
            inserir_dados(
                "INSERT INTO data_collect.db_datatv.locais (local_id, nome, img_url, cidade, pais) VALUES (?, ?, ?, ?, ?)",
                (local_id, nome_local, img_url, cidade, pais)
            )

    elif acao == "Alterar":
        st.subheader("Alterar Local Existente")
        locais = visualizar_dados("SELECT * FROM data_collect.db_datatv.locais")
        local_id = st.selectbox("Selecione o Local", [local[0] for local in locais])

        # Encontrar o local selecionado e preencher o formulário com os dados existentes
        if local_id:
            local_selecionado = next((local for local in locais if local[0] == local_id), None)
            
            if local_selecionado:
                nome_local = st.text_input("Nome do Local", value=local_selecionado[1])
                img_url = st.text_input("URL da Imagem", value=local_selecionado[2])
                cidade = st.text_input("Cidade", value=local_selecionado[3])
                pais = st.text_input("País", value=local_selecionado[4])
                
                if st.button("Atualizar Local"):
                    atualizar_dados(
                        "UPDATE data_collect.db_datatv.locais SET nome=?, img_url=?, cidade=?, pais=? WHERE local_id=?",
                        (nome_local, img_url, cidade, pais, local_id)
                    )
            else:
                st.warning("Local selecionado não encontrado. Por favor, tente novamente.")

    elif acao == "Deletar":
        st.subheader("Deletar Local")
        locais = visualizar_dados("SELECT * FROM data_collect.db_datatv.locais")
        local_id = st.selectbox("Selecione o Local para Deletar", [local[0] for local in locais])
        if st.button("Deletar Local"):
            deletar_dados("DELETE FROM data_collect.db_datatv.locais WHERE local_id=?", (local_id,))
