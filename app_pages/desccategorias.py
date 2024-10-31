import streamlit as st
import uuid
from db_functions import inserir_dados, visualizar_dados, atualizar_dados, deletar_dados

def app():
    st.title("Gerenciamento de Descrições de Categorias")

    # Escolher a ação desejada
    acao = st.selectbox("Escolha a ação", ["Inserir", "Alterar", "Deletar"])

    if acao == "Inserir":
        categorias = visualizar_dados("SELECT categoria_id, tipo FROM data_collect.db_datatv.categorias")
        categoria_id = st.selectbox("Selecione a Categoria", [cat[0] for cat in categorias], format_func=lambda x: dict(categorias)[x])
        tipo_desc = st.text_input("Tipo de Descrição")
        preco_diaria = st.number_input("Preço por Diária", min_value=0.0)
        preco_total = st.number_input("Preço Total", min_value=0.0)
        total_dias = st.number_input("Total de Dias", min_value=0)
        img_cat = st.text_input("URL da Imagem da Categoria")
        link_url = st.text_input("Link URL para mais informações")

        if st.button("Salvar Descrição da Categoria"):
            desc_id = str(uuid.uuid4())  # Gerar UUID para desc_id
            inserir_dados(
                "INSERT INTO data_collect.db_datatv.desccategorias (desc_id, categoria_id, tipo, preco_diaria, preco_total, total_dias, img_cat, link_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (desc_id, categoria_id, tipo_desc, preco_diaria, preco_total, total_dias, img_cat, link_url)
            )

    elif acao == "Alterar":
        # Carregar categorias para o selectbox
        categorias = visualizar_dados("SELECT categoria_id, tipo FROM data_collect.db_datatv.categorias")
        
        # Selecionar descrição de categoria para editar
        desccategorias = visualizar_dados("SELECT * FROM data_collect.db_datatv.desccategorias")
        desc_id = st.selectbox("Selecione a Descrição da Categoria", [desc[0] for desc in desccategorias])

        if desc_id:
            # Pegar os valores da descrição selecionada para exibir no formulário
            descricao_selecionada = next((desc for desc in desccategorias if desc[0] == desc_id), None)
            if descricao_selecionada:
                categoria_id = st.selectbox(
                    "Selecione a Categoria",
                    [cat[0] for cat in categorias],
                    index=[cat[0] for cat in categorias].index(descricao_selecionada[1]),
                    format_func=lambda x: dict(categorias)[x]
                )
                tipo_desc = st.text_input("Tipo de Descrição", value=descricao_selecionada[2])
                preco_diaria = st.number_input("Preço por Diária", min_value=0.0, value=float(descricao_selecionada[3] or 0.0))
                preco_total = st.number_input("Preço Total", min_value=0.0, value=float(descricao_selecionada[4] or 0.0))
                total_dias = st.number_input("Total de Dias", min_value=0, value=int(descricao_selecionada[5] or 0))
                img_cat = st.text_input("URL da Imagem da Categoria", value=descricao_selecionada[6])
                link_url = st.text_input("Link URL para mais informações", value=descricao_selecionada[7])

                if st.button("Atualizar Descrição da Categoria"):
                    atualizar_dados(
                        "UPDATE data_collect.db_datatv.desccategorias SET categoria_id=?, tipo=?, preco_diaria=?, preco_total=?, total_dias=?, img_cat=?, link_url=? WHERE desc_id=?",
                        (categoria_id, tipo_desc, preco_diaria, preco_total, total_dias, img_cat, link_url, desc_id)
                    )

    elif acao == "Deletar":
        # Selecionar descrição de categoria para deletar
        desccategorias = visualizar_dados("SELECT * FROM data_collect.db_datatv.desccategorias")
        desc_id = st.selectbox("Selecione a Descrição da Categoria para Deletar", [desc[0] for desc in desccategorias])

        if st.button("Deletar Descrição da Categoria"):
            deletar_dados("DELETE FROM data_collect.db_datatv.desccategorias WHERE desc_id=?", (desc_id,))
