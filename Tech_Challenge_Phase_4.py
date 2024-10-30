import json
from google.cloud import bigquery
import streamlit as st

try:
    # Carrega secrets do Streamlit
    project_id = st.secrets["project_id"]
    private_key = st.secrets["private_key"].replace("\\n", "\n")  # Handle newline characters correctly
    client_email = st.secrets["client_email"]
    
    # Prepara o Credentials Dictionary
    credentials = {
        "type": "service_account",
        "project_id": project_id,
        "private_key_id": st.secrets["private_key_id"],
        "private_key": private_key,
        "client_email": client_email,
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"],
    }
    
    # Cria o BigQuery client utilizando as credenciais
    client = bigquery.Client.from_service_account_info(credentials)
    
    # Query dos dados
    query = """
    SELECT * FROM `neural-journey-377617.cars.cars_table` LIMIT 1000
    """
    ipea_df = client.query(query).to_dataframe()
    
except Exception as e:
    st.error(f"An error occurred: {e}")

# Create tabs
tabs = st.tabs(["Introdução", "Relatório", "Dashboard", "Modelo Machine Learning"])

# Tab: Introdução
with tabs[0]:
    st.header("Introdução")
    st.write("""
    Bem-vindo a este projeto. Neste projeto, exploraremos os dados, descobriremos insights e tiraremos conclusões.
    """)


with tabs[1]:
    # Organização dos dados
    st.header("Organização do Banco de Dados")
    st.write("""
    Estrutura dos dados no Big Query
    """)
  
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

    # Exibir um gráfico
    st.subheader("Visualização de Dados + insights")

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
    - Insight 4
    """)

with tabs[2]:
    st.header("Dashboard")
    st.write("""
    Aqui será apresentado o dashboard com os dados e insights encontrados.
    """)

with tabs[3]:
    st.header("Modelo Machine Learning")
    st.write("""
    Aqui será apresentado o modelo de Machine Learning.
    """)
