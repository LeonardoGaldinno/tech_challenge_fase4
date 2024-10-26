# Importação de bibliotecas
import streamlit as st
import pandas as pd
from google.cloud import bigquery
import os


st.set_page_config(
    page_title="Tech Challenge Phase 4",
    layout = "centered"
)

# Introdução
st.title("Tech Challenge Phase 4")
st.header("Introdução")
st.write("""
Bem-vindo a este projeto. Neste projeto, exploraremos os dados, descobriremos insights e tiraremos conclusões.
""")

# Organização dos dados
st.header("Organização do Banco de Dados")
st.write("""
Estrutura dos dados no Big Query
""")

# Verificar se a variável de ambiente está definida
#if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
#    st.error("A variável de ambiente GOOGLE_APPLICATION_CREDENTIALS não está definida.")
#else:

# Importação dos dados

#project_id = 'tc-fiap'
#client = bigquery.Client(project=project_id)

#query = """
#SELECT * FROM your_dataset.your_table LIMIT 10
#"""
#ipea_df = client.query(query).to_dataframe()

# Dados de Exemplo
st.header("Demonstração dos Dados (tabelas)")
#st.write(ipea_df.head())

# Exploração de Dados
st.header("Análise Exploratória de Dados")
st.write("Aqui exploraremos os dados para encontrar padrões e insights interessantes.")

# Exibir estatísticas básicas
st.subheader("Estatísticas + Insights")
st.write("""
Com base na exploração dos dados, podemos concluir o seguinte:
- Insights relevantes sobre a variação do preço do petróleo
- Situações geopolíticas
- Crises econômicas
- Demanda global por energia e Outros fatores relevantes.
- É obrigatório trazer pelo menos 4 insights neste desafio.
""")
#st.write(ipea_df.describe())

# Exibir um gráfico
st.subheader("Visualização de Dados + insights")
#st.line_chart(ipea_df)

# Modelo Machine Learning
st.header("Modelo Machine Learning")
st.write("""
Com base na exploração dos dados, podemos concluir o seguinte:
- Modelo de Machine Learning que faça a previsão do preço do petróleo diariamente
- O modelo deve estar contemplado no storytelling.
- Incluir o código utilizado e análise das performances do modelo.
- Criar um plano para deploy em produção do modelo, com as ferramentas necessárias.
- Fazer um MVP do modelo em produção utilizando o Streamlit.
""")

# Conclusões
st.header("Conclusão")
st.write("""
Com base na exploração dos dados, podemos concluir o seguinte:
- Insight 1
- Insight 2
- Insight 3
""")