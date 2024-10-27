import os
from google.cloud import bigquery
import streamlit as st

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

# Debug statement to check if the code reaches this point
st.write("Initializing BigQuery client...")

try:
    # Load secrets from Streamlit
    project_id = st.secrets["project_id"]
    private_key = st.secrets["private_key"].replace("\\n", "\n")  # Handle newline characters correctly
    client_email = st.secrets["client_email"]

    # Set up the credentials using the private key
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

    # Set the environment variable for Google credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials

    # Importação dos dados
    client = bigquery.Client.from_service_account_info(credentials)

    query = """
    SELECT * FROM `neural-journey-377617.cars.cars_table` LIMIT 1000
    """
    ipea_df = client.query(query).to_dataframe()

    # Debug statement to check if the query was successful
    st.write("Query executed successfully. Displaying data...")

    # Dados de Exemplo
    st.header("Demonstração dos Dados (tabelas)")
    st.write(ipea_df.head())

    # Exploração de Dados
    st.header("Análise Exploratória de Dados")
except Exception as e:
    st.error(f"An error occurred: {e}")
