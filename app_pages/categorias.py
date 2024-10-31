import streamlit as st
import uuid
from db_functions import inserir_dados, visualizar_dados, atualizar_dados, deletar_dados

def app():
    st.title("Gerenciamento de Categorias")

    # Escolher a ação desejada
    acao = st.selectbox("Escolha a ação", ["Inserir", "Alterar", "Deletar"])

    if acao == "Inserir":
        # Carregar locais e cidades
        locais = visualizar_dados("SELECT local_id, cidade FROM data_collect.db_datatv.locais")
        locais_dict = {local[0]: local[1] for local in locais}  # Mapeia 'local_id' para 'cidade'

        # Selecionar o local exibindo o nome da cidade
        local_id = st.selectbox("Selecione a Cidade", [local[0] for local in locais], format_func=lambda x: locais_dict.get(x, ""))
        tipo_categoria = st.text_input("Tipo da Categoria (ex: Aéreo, Carro, Hotel)")
        
        if st.button("Salvar Categoria"):
            categoria_id = str(uuid.uuid4())  # Gerar UUID para categoria_id
            inserir_dados(
                "INSERT INTO data_collect.db_datatv.categorias (categoria_id, local_id, tipo) VALUES (?, ?, ?)",
                (categoria_id, local_id, tipo_categoria)
            )

    elif acao == "Alterar":
        # Selecionar categoria para editar
        categorias = visualizar_dados("SELECT * FROM data_collect.db_datatv.categorias")
        categoria_id = st.selectbox("Selecione a Categoria", [cat[0] for cat in categorias])

        if categoria_id:
            # Carregar locais e cidades
            locais = visualizar_dados("SELECT local_id, cidade FROM data_collect.db_datatv.locais")
            locais_dict = {local[0]: local[1] for local in locais}

            # Pegar os valores da categoria selecionada para exibir no formulário
            categoria_selecionada = next((cat for cat in categorias if cat[0] == categoria_id), None)
            if categoria_selecionada:
                local_id = st.selectbox(
                    "Selecione a Cidade",
                    [local[0] for local in locais],
                    index=[local[0] for local in locais].index(categoria_selecionada[1]),
                    format_func=lambda x: locais_dict.get(x, "")
                )
                tipo_categoria = st.text_input("Tipo da Categoria", value=categoria_selecionada[2])

                if st.button("Atualizar Categoria"):
                    atualizar_dados(
                        "UPDATE data_collect.db_datatv.categorias SET local_id=?, tipo=? WHERE categoria_id=?",
                        (local_id, tipo_categoria, categoria_id)
                    )

    elif acao == "Deletar":
        # Selecionar categoria para deletar
        categorias = visualizar_dados("SELECT * FROM data_collect.db_datatv.categorias")
        categoria_id = st.selectbox("Selecione a Categoria para Deletar", [cat[0] for cat in categorias])

        if st.button("Deletar Categoria"):
            deletar_dados("DELETE FROM data_collect.db_datatv.categorias WHERE categoria_id=?", (categoria_id,))
