import streamlit as st
from db_functions import inserir_dados, visualizar_dados, atualizar_dados, deletar_dados

def app():
    st.title("Gerenciamento de Descrições de Categorias")

    # Escolher a ação desejada
    acao = st.selectbox("Escolha a ação", ["Inserir", "Alterar", "Deletar"])

    if acao == "Inserir":
        # Formulário para inserir uma nova descrição de categoria
        categorias = visualizar_dados("SELECT categoria_id, tipo FROM Categorias")
        categoria_id = st.selectbox("Selecione a Categoria", [cat[0] for cat in categorias], format_func=lambda x: dict(categorias)[x])
        tipo_desc = st.text_input("Tipo de Descrição")
        preco_diaria = st.number_input("Preço por Diária", min_value=0.0)
        preco_total = st.number_input("Preço Total", min_value=0.0)
        total_dias = st.number_input("Total de Dias", min_value=0)
        img_cat = st.text_input("URL da Imagem da Categoria")
        link_url = st.text_input("Link URL para mais informações")

        if st.button("Salvar Descrição da Categoria"):
            inserir_dados(
                "INSERT INTO DescCategorias (categoria_id, tipo, preco_diaria, preco_total, total_dias, img_cat, link_url) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (categoria_id, tipo_desc, preco_diaria, preco_total, total_dias, img_cat, link_url)
            )

    elif acao == "Alterar":
        # Selecionar descrição de categoria para editar
        desccategorias = visualizar_dados("SELECT * FROM DescCategorias")
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
                        "UPDATE DescCategorias SET categoria_id=%s, tipo=%s, preco_diaria=%s, preco_total=%s, total_dias=%s, img_cat=%s, link_url=%s WHERE desc_id=%s",
                        (categoria_id, tipo_desc, preco_diaria, preco_total, total_dias, img_cat, link_url, desc_id)
                    )

    elif acao == "Deletar":
        # Selecionar descrição de categoria para deletar
        desccategorias = visualizar_dados("SELECT * FROM DescCategorias")
        desc_id = st.selectbox("Selecione a Descrição da Categoria para Deletar", [desc[0] for desc in desccategorias])

        if st.button("Deletar Descrição da Categoria"):
            deletar_dados("DELETE FROM DescCategorias WHERE desc_id=%s", (desc_id,))
