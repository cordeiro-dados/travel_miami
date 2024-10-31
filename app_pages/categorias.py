import streamlit as st
from db_functions import inserir_dados, visualizar_dados, atualizar_dados, deletar_dados

def app():
    st.title("Gerenciamento de Categorias")

    # Escolher a ação desejada
    acao = st.selectbox("Escolha a ação", ["Inserir", "Alterar", "Deletar"])

    if acao == "Inserir":
        # Formulário para inserir uma nova categoria
        locais = visualizar_dados("SELECT local_id, nome FROM Locais")
        local_id = st.selectbox("Selecione o Local", [local[0] for local in locais], format_func=lambda x: dict(locais)[x])
        tipo_categoria = st.text_input("Tipo da Categoria (ex: Aéreo, Carro, Hotel)")
        
        if st.button("Salvar Categoria"):
            inserir_dados(
                "INSERT INTO Categorias (local_id, tipo) VALUES (%s, %s)",
                (local_id, tipo_categoria)
            )

    elif acao == "Alterar":
        # Selecionar categoria para editar
        categorias = visualizar_dados("SELECT * FROM Categorias")
        categoria_id = st.selectbox("Selecione a Categoria", [cat[0] for cat in categorias])

        if categoria_id:
            # Carregar locais para o campo de seleção
            locais = visualizar_dados("SELECT local_id, nome FROM Locais")
            
            # Pegar os valores da categoria selecionada para exibir no formulário
            categoria_selecionada = next((cat for cat in categorias if cat[0] == categoria_id), None)
            if categoria_selecionada:
                local_id = st.selectbox(
                    "Selecione o Local",
                    [local[0] for local in locais],
                    index=[local[0] for local in locais].index(categoria_selecionada[1]),
                    format_func=lambda x: dict(locais)[x]
                )
                tipo_categoria = st.text_input("Tipo da Categoria", value=categoria_selecionada[2])

                if st.button("Atualizar Categoria"):
                    atualizar_dados(
                        "UPDATE Categorias SET local_id=%s, tipo=%s WHERE categoria_id=%s",
                        (local_id, tipo_categoria, categoria_id)
                    )

    elif acao == "Deletar":
        # Selecionar categoria para deletar
        categorias = visualizar_dados("SELECT * FROM Categorias")
        categoria_id = st.selectbox("Selecione a Categoria para Deletar", [cat[0] for cat in categorias])

        if st.button("Deletar Categoria"):
            deletar_dados("DELETE FROM Categorias WHERE categoria_id=%s", (categoria_id,))
