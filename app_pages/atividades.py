import streamlit as st
from db_functions import inserir_dados, visualizar_dados, atualizar_dados, deletar_dados

def app():
    st.title("Gerenciamento de Atividades")

    # Escolher a ação desejada
    acao = st.selectbox("Escolha a ação", ["Inserir", "Alterar", "Deletar"])

    if acao == "Inserir":
        # Formulário para inserir uma nova atividade
        locais = visualizar_dados("SELECT local_id, nome FROM Locais")
        local_id = st.selectbox("Selecione o Local", [local[0] for local in locais], format_func=lambda x: dict(locais)[x])
        nome_atividade = st.text_input("Nome da Atividade")
        descricao = st.text_area("Descrição")
        preco_total = st.number_input("Preço Total", min_value=0.0)
        if st.button("Salvar Atividade"):
            inserir_dados(
                "INSERT INTO Atividades (local_id, nome, descricao, preco_total) VALUES (%s, %s, %s, %s)",
                (local_id, nome_atividade, descricao, preco_total)
            )

    elif acao == "Alterar":
        # Selecionar atividade para editar
        atividades = visualizar_dados("SELECT * FROM Atividades")
        atividade_id = st.selectbox("Selecione a Atividade", [atividade[0] for atividade in atividades])

        if atividade_id:
            # Pegar os valores da atividade selecionada para exibir no formulário
            atividade_selecionada = next((atividade for atividade in atividades if atividade[0] == atividade_id), None)
            if atividade_selecionada:
                local_id = st.selectbox(
                    "Selecione o Local",
                    [local[0] for local in locais],
                    index=[local[0] for local in locais].index(atividade_selecionada[1]),
                    format_func=lambda x: dict(locais)[x]
                )
                nome_atividade = st.text_input("Nome da Atividade", value=atividade_selecionada[2])
                descricao = st.text_area("Descrição", value=atividade_selecionada[3])
                preco_total = st.number_input("Preço Total", min_value=0.0, value=float(atividade_selecionada[4] or 0.0))

                if st.button("Atualizar Atividade"):
                    atualizar_dados(
                        "UPDATE Atividades SET local_id=%s, nome=%s, descricao=%s, preco_total=%s WHERE atividade_id=%s",
                        (local_id, nome_atividade, descricao, preco_total, atividade_id)
                    )

    elif acao == "Deletar":
        # Selecionar atividade para deletar
        atividades = visualizar_dados("SELECT * FROM Atividades")
        atividade_id = st.selectbox("Selecione a Atividade para Deletar", [atividade[0] for atividade in atividades])

        if st.button("Deletar Atividade"):
            deletar_dados("DELETE FROM Atividades WHERE atividade_id=%s", (atividade_id,))
