import pandas as pd
from google.cloud import bigquery
import streamlit as st
import json

class BigQuery:
    def __init__(self) -> None:
        pass
    
    def create_credentials(self):
   

    # Carrega secrets do Streamlit
        project_id = st.secrets["project_id"]
        private_key = st.secrets["private_key"].replace("\\n", "\n") 
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

        client = bigquery.Client.from_service_account_info(credentials)

        return client

    def create_querys_and_load_df(self):

        client = self.create_credentials()  

        query_brent_oil = """
            SELECT * FROM `tc-fiap.fase_4.ipea_tratada_final` 
            WHERE Data > DATE_SUB(CURRENT_DATE(), INTERVAL 5 YEAR)
            """

        petroleum_consumption= pd.DataFrame({
            "year": [2024, 2023, 2022, 2021, 2020, 2019],
            "Consumo": [102.0, 100.0, 99.0, 96.0, 91.0, 100.5],
            "Fontes": [
                "EIA (Energy Information Administration)",
                "EIA (Energy Information Administration)",
                "IEA (International Energy Agency)",
                "IEA (International Energy Agency)",
                "OPEC (Organization of the Petroleum Exporting Countries)",
                "EIA (Energy Information Administration)"  # Example source for 2024
            ]
        })
                
        ipea_df = client.query(query_brent_oil).to_dataframe()
        
        return ipea_df, petroleum_consumption
    

    def prepare_data(self, df):

        df_0 = df.copy()

        df_0 = df_0.rename(columns={'Preco': 'preco_bpd_US', 'Data': 'data'})
        df_0['data'] = pd.to_datetime(df_0['data'])
        df_0 = df_0.set_index('data').asfreq('D')
        df_0 = df_0.fillna(method='bfill')
        df_0 = df_0[df_0.index <= pd.to_datetime('today')]

        df_0['year'] = df_0.index.year
        ipea_avg_per_year = df_0.groupby('year')['preco_bpd_US'].mean().reset_index()

        
        return df_0 , ipea_avg_per_year
    
    
    def create_dfs(self):
        ipea_df, petroleum_consumption = self.create_querys_and_load_df()

        ipea_df, ipea_avg_per_year = self.prepare_data(ipea_df)

        merged_df = pd.merge(ipea_avg_per_year, petroleum_consumption, on='year', how='left')
        

        return ipea_df, merged_df
    
