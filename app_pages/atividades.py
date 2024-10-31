import streamlit as st
import uuid
from db_functions import inserir_dados, visualizar_dados, atualizar_dados, deletar_dados

def app():
    st.title("Gerenciamento de Atividades")

    # Escolher a ação desejada
    acao = st.selectbox("Escolha a ação", ["Inserir", "Alterar", "Deletar"])

    if acao == "Inserir":
        # Carregar cidades e locais
        cidades = visualizar_dados("SELECT DISTINCT cidade FROM data_collect.db_datatv.locais")
        cidade_selecionada = st.selectbox("Selecione a Cidade", [cidade[0] for cidade in cidades])

        if cidade_selecionada:
            # Filtrar locais pela cidade selecionada
            locais = visualizar_dados("SELECT local_id, nome FROM data_collect.db_datatv.locais WHERE cidade = ?", (cidade_selecionada,))
            locais_dict = {local[0]: local[1] for local in locais}  # Mapeia 'local_id' para 'nome'

            # Selecionar local a partir dos locais filtrados
            local_id = st.selectbox("Selecione o Local", [local[0] for local in locais], format_func=lambda x: locais_dict.get(x, ""))

            # Inserir detalhes da atividade
            nome_atividade = st.text_input("Nome da Atividade")
            descricao = st.text_area("Descrição")
            preco_total = st.number_input("Preço Total", min_value=0.0)

            if st.button("Salvar Atividade"):
                atividade_id = str(uuid.uuid4())  # Gerar UUID para atividade_id
                inserir_dados(
                    "INSERT INTO data_collect.db_datatv.atividades (atividade_id, local_id, cidade, nome, descricao, preco_total) VALUES (?, ?, ?, ?, ?, ?)",
                    (atividade_id, local_id, cidade_selecionada, nome_atividade, descricao, preco_total)
                )

    elif acao == "Alterar":
        # Carregar atividades e criar um dicionário para mapear id e nome
        atividades = visualizar_dados("SELECT atividade_id, nome FROM data_collect.db_datatv.atividades")
        atividades_dict = {atividade[0]: atividade[1] for atividade in atividades}

        # Selecionar a atividade com o nome exibido, mas o ID como valor de referência
        atividade_id = st.selectbox("Selecione a Atividade", list(atividades_dict.keys()), format_func=lambda x: atividades_dict.get(x, ""))

        if atividade_id:
            # Carregar dados da atividade selecionada
            atividades_full = visualizar_dados("SELECT * FROM data_collect.db_datatv.atividades")
            atividade_selecionada = next((atividade for atividade in atividades_full if atividade[0] == atividade_id), None)
            if atividade_selecionada:
                # Selecionar a cidade e carregar locais com base na cidade selecionada
                cidade_selecionada = atividade_selecionada[2]
                st.write(f"Cidade Selecionada: {cidade_selecionada}")
                locais = visualizar_dados("SELECT local_id, nome FROM data_collect.db_datatv.locais WHERE cidade = ?", (cidade_selecionada,))
                locais_dict = {local[0]: local[1] for local in locais}

                # Garantir que local_id selecionado esteja na lista, caso contrário usar o primeiro item como padrão
                local_ids = [local[0] for local in locais]
                local_index = local_ids.index(atividade_selecionada[1]) if atividade_selecionada[1] in local_ids else 0

                local_id = st.selectbox(
                    "Selecione o Local",
                    local_ids,
                    index=local_index,
                    format_func=lambda x: locais_dict.get(x, "")
                )

                # Preencher detalhes da atividade
                nome_atividade = st.text_input("Nome da Atividade", value=atividade_selecionada[3])
                descricao = st.text_area("Descrição", value=atividade_selecionada[4])
                preco_total = st.number_input("Preço Total", min_value=0.0, value=float(atividade_selecionada[5] or 0.0))

                if st.button("Atualizar Atividade"):
                    atualizar_dados(
                        "UPDATE data_collect.db_datatv.atividades SET local_id=?, cidade=?, nome=?, descricao=?, preco_total=? WHERE atividade_id=?",
                        (local_id, cidade_selecionada, nome_atividade, descricao, preco_total, atividade_id)
                    )

    elif acao == "Deletar":
        # Selecionar atividade para deletar, mostrando o nome da atividade
        atividades = visualizar_dados("SELECT atividade_id, nome FROM data_collect.db_datatv.atividades")
        atividades_dict = {atividade[0]: atividade[1] for atividade in atividades}
        atividade_id = st.selectbox("Selecione a Atividade para Deletar", list(atividades_dict.keys()), format_func=lambda x: atividades_dict.get(x, ""))

        if st.button("Deletar Atividade"):
            deletar_dados("DELETE FROM data_collect.db_datatv.atividades WHERE atividade_id=?", (atividade_id,))
