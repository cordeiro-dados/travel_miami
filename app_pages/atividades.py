import streamlit as st
import uuid
from db_functions import inserir_dados, visualizar_dados, atualizar_dados, deletar_dados

def app():
    st.title("Gerenciamento de Atividades")

    # Escolher a ação desejada
    acao = st.selectbox("Escolha a ação", ["Inserir", "Alterar", "Deletar"])

    if acao == "Inserir":
        locais = visualizar_dados("SELECT local_id, nome FROM data_collect.db_datatv.locais")
        local_id = st.selectbox("Selecione o Local", [local[0] for local in locais], format_func=lambda x: dict(locais)[x])
        nome_atividade = st.text_input("Nome da Atividade")
        descricao = st.text_area("Descrição")
        preco_total = st.number_input("Preço Total", min_value=0.0)
        if st.button("Salvar Atividade"):
            atividade_id = str(uuid.uuid4())  # Gerar UUID para atividade_id
            inserir_dados(
                "INSERT INTO data_collect.db_datatv.atividades (atividade_id, local_id, nome, descricao, preco_total) VALUES (?, ?, ?, ?, ?)",
                (atividade_id, local_id, nome_atividade, descricao, preco_total)
            )

    elif acao == "Alterar":
        atividades = visualizar_dados("SELECT * FROM data_collect.db_datatv.atividades")
        atividade_id = st.selectbox("Selecione a Atividade", [atividade[0] for atividade in atividades])

        if atividade_id:
            locais = visualizar_dados("SELECT local_id, nome FROM data_collect.db_datatv.locais")
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
                        "UPDATE data_collect.db_datatv.atividades SET local_id=?, nome=?, descricao=?, preco_total=? WHERE atividade_id=?",
                        (local_id, nome_atividade, descricao, preco_total, atividade_id)
                    )

    elif acao == "Deletar":
        # Selecionar atividade para deletar
        atividades = visualizar_dados("SELECT * FROM data_collect.db_datatv.atividades")
        atividade_id = st.selectbox("Selecione a Atividade para Deletar", [atividade[0] for atividade in atividades])

        if st.button("Deletar Atividade"):
            deletar_dados("DELETE FROM data_collect.db_datatv.atividades WHERE atividade_id=?", (atividade_id,))