import streamlit as st
import pandas as pd
from google.cloud import bigquery
import altair as alt

st.set_page_config(layout="wide")

try:
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
    
    # Cria o BigQuery client utilizando as credenciais
    client = bigquery.Client.from_service_account_info(credentials)
    
    # Query the data
    query = """
    SELECT * FROM `tc-fiap.fase_4.ipea_tratada_final` 
    WHERE Data > DATE_SUB(CURRENT_DATE(), INTERVAL 5 YEAR)
    """

    query2 = """
    SELECT * FROM `tc-fiap.fase_4.consumo_mundial_petroleo`
    WHERE Data > DATE_SUB(CURRENT_DATE(), INTERVAL 5 YEAR)
    """   
except Exception as e:
    st.error(f"An error occurred: {e}")

ipea_df = client.query(query).to_dataframe()
ipea_df = ipea_df.rename(columns={'Preco': 'preco_bpd_US', 'Data': 'data'})
ipea_df['data'] = pd.to_datetime(ipea_df['data'])
ipea_df = ipea_df.set_index('data').asfreq('D')
ipea_df = ipea_df.fillna(method='bfill')
ipea_df = ipea_df[ipea_df.index <= pd.to_datetime('today')]
consumo_mundial_df = client.query(query2).to_dataframe()

# Create tabs
tabs = st.tabs(["Introdução", "Relatório", "Dashboard", "Modelo Machine Learning"])

# Tab: Introdução
with tabs[0]:
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.header("Introdução")
            st.write("""
            Bem-vindo(a) ao nosso projeto de análise e previsão de preços do petróleo Brent. 
            Este projeto foi desenvolvido para atender a uma demanda específica de um cliente, 
            que busca insights detalhados e previsões precisas para apoiar suas decisões estratégicas.
            """)

            st.write("""
            Nosso trabalho está dividido em três componentes principais:
            """)
            st.markdown("##### Análise de Dados Históricos")
            st.write("""Realizamos uma análise detalhada dos dados históricos de preços do petróleo Brent, 
            destacando as principais tendências e variações ao longo do tempo. Utilizamos gráficos para ilustrar essas informações 
            de forma clara e compreensível.""")

            st.markdown("##### Dashboard Interativo")
            st.write("""Desenvolvemos um dashboard dinâmico que oferece uma visualização interativa dos preços do petróleo. 
            Este dashboard considera fatores como eventos geopolíticos, crises econômicas e mudanças na demanda global por energia, 
            proporcionando uma compreensão aprofundada das flutuações do mercado.""")

            st.markdown("##### Modelo de Machine Learning")
            st.write("""Criamos um modelo de Machine Learning especializado em séries temporais para prever os preços do petróleo diariamente. 
            Incluímos uma análise de desempenho do modelo e as previsões geradas, demonstrando a eficácia e a aplicabilidade prática do nosso trabalho.""")

            st.write("""O resultado deste projeto é uma combinação de visualizações interativas e previsões precisas que oferecem uma visão 
            abrangente do mercado de petróleo com insights adicionados em um relatório. As informações detalhadas sobre a análise de dados, o dashboard interativo e o 
            modelo de Machine Learning estão disponíveis em suas respectivas abas: Relatório, Dashboard e Modelo Machine Learning.""")

# Tab: Relatório
with tabs[1]:
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.header("Base de Dados")
            st.write("""
            Para este projeto, utilizamos dados históricos de preços do petróleo, que são fornecidos pelo site do IPEA. 
            Esses dados incluem informações sobre as datas e os preços do petróleo ao longo do tempo. Para garantir que esses dados sejam bem organizados 
            e facilmente acessíveis, armazenamos tudo no BigQuery, uma plataforma de armazenamento de dados na nuvem. Isso não só facilita a 
            estruturação dos dados, mas também permite que eles sejam integrados automaticamente com o Streamlit, a ferramenta que usamos para 
            criar nosso dashboard interativo e o modelo de previsão. Dessa forma, conseguimos atualizar e visualizar os dados em tempo real, 
            proporcionando uma experiência mais eficiente e dinâmica para os usuários.
            """)

            st.header("Análise Exploratória de Dados")
            
            st.subheader("Variação do Preço do Petróleo ao Longo de 5 anos")
            line_chart = alt.Chart(ipea_df.reset_index()).mark_line().encode(
                x=alt.X('data:T', title='Data', axis=alt.Axis(format='%Y', tickCount='year')),
                y=alt.Y('preco_bpd_US', title='Preço (USD)')
            ).properties(
                width=700,
                height=400
            )
            st.altair_chart(line_chart, use_container_width=True)

            st.write("""**Análise de Tendência:** Ao examinar o gráfico de linha apresentado, podemos identificar a evolução dos preços do 
            petróleo entre 2020 e 2024. Notamos que, em 2020, houve uma forte queda nos preços devido à pandemia de COVID-19, que resultou 
            em uma drástica redução na demanda global por petróleo. Essa queda foi acentuada pelas medidas de lockdown e pela diminuição das 
            atividades econômicas.
            Após essa fase crítica, os preços começaram a se recuperar lentamente em 2021, à medida que a economia global foi se reabrindo. 
            Desde então, observamos uma tendência levemente ascendente, indicando um aumento gradual nos preços do petróleo. Essa trajetória 
            sugere que, apesar das flutuações ocasionais, o mercado está se ajustando às novas condições e à crescente demanda.
            """)
 
            st.subheader("Variação Anual dos Preços do Petróleo")
            
            current_year = pd.Timestamp.now().year
            start_year = current_year - 5

            filtered_data = ipea_df[(ipea_df.index.year > start_year) & (ipea_df.index.year <= current_year)]

            annual_prices = filtered_data.resample('Y').mean().reset_index()
            bar_chart = alt.Chart(annual_prices).mark_bar().encode(
                x=alt.X('year(data):T', title='Ano', axis=alt.Axis(labelAngle=0), bandPosition=0),
                y=alt.Y('preco_bpd_US', title='Preço Médio por Litro (USD)')
            ).properties(
                width=700,
                height=400
            )

            st.altair_chart(bar_chart, use_container_width=True)
            
            st.write("""**Análise do Preço Médio por Litro:** Ao analisar o gráfico de barras da variação anual dos preços do petróleo, 
            podemos identificar anos específicos em que houve aumentos ou quedas significativas nos preços médios. Esses picos ou quedas podem estar associados a eventos econômicos ou 
            geopolíticos importantes, como mudanças na produção de petróleo, conflitos internacionais ou flutuações na demanda global. 
            Monitorar esses eventos pode ajudar a prever futuras variações nos preços.
            Em 2020, os preços foram significativamente baixos, muito provavelmente devido ao surto da pandemia de COVID-19, 
            que impactou drasticamente a demanda global. Em 2021, observou-se um crescimento nos preços, culminando em um recorde histórico em 2022. 
            Nos anos subsequentes, 2023 e 2024, os preços recuaram ligeiramente, mas ainda permanecem em níveis elevados. Este comportamento pode ser 
            atribuído a uma recuperação gradual da economia global e ajustes na produção de petróleo.
            """)

            st.subheader("Volatilidade Mensal do Preço do Petróleo ao Longo de 5 anos")
            monthly_volatility = ipea_df['preco_bpd_US'].resample('M').std().reset_index()
            volatility_line_chart = alt.Chart(monthly_volatility).mark_line().encode(
                x=alt.X('data:T', title='Data', axis=alt.Axis(format='%Y-%m', tickCount='month')),
                y=alt.Y('preco_bpd_US', title='Desvio Padrão Mensal (USD)')
            ).properties(
                width=700,
                height=400
            )
            st.altair_chart(volatility_line_chart, use_container_width=True)

            st.write("""**Análise de Volatilidade:** O gráfico acima mostra a volatilidade mensal dos preços do petróleo ao longo dos últimos 5 anos. 
            Podemos observar períodos de alta volatilidade, indicando maior instabilidade nos preços, e períodos de baixa volatilidade, indicando maior estabilidade nos preços.
            A análise da volatilidade é importante para os investidores, pois permite avaliar o risco associado aos investimentos em petróleo. 
            Períodos de alta volatilidade podem indicar maiores oportunidades de lucro, mas também maiores riscos. 
            Por outro lado, períodos de baixa volatilidade podem ser mais atraentes para investidores que buscam estabilidade e menor risco em seus portfólios. 
            Compreender esses padrões ajuda os investidores a tomar decisões mais informadas sobre quando entrar ou sair do mercado.
            """)

            st.header("Conclusão")
            st.write("""Com base na exploração dos dados, podemos concluir o seguinte:
            - Insight 1
            - Insight 2
            - Insight 3
            - Insight 4
            """)

# Tab: Dashboard
with tabs[2]:
    with st.container():
        col_dash, col_filters = st.columns([5, 1])
        with col_filters:
            st.subheader("Filtros Interativos")
            min_date = ipea_df.index.min()
            max_date = ipea_df.index.max()
            start_date = st.date_input("Data de Início", value=min_date, min_value=min_date, max_value=max_date)
            end_date = st.date_input("Data de Fim", value=max_date, min_value=min_date, max_value=max_date)

            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

            filtered_data = ipea_df[(ipea_df.index >= start_date) & (ipea_df.index <= end_date)]

        with col_dash:
            st.header("Dashboard")
            col1, col2 = st.columns(2)

            with col1: 
                st.subheader("Variação Anual dos Preços do Petróleo")
                annual_prices = filtered_data.resample('Y').mean().reset_index()
                bar_chart = alt.Chart(annual_prices).mark_bar().encode(
                    x=alt.X('year(data):T', title='Ano', axis=alt.Axis(labelAngle=0), bandPosition=0),
                    y=alt.Y('preco_bpd_US', title='Preço Médio por Litro (USD)')
                ).properties(
                    width=400,
                    height=300
                )

                st.altair_chart(bar_chart, use_container_width=True)

            with col2:
                st.subheader("Volatilidade Mensal")
                monthly_volatility_data = filtered_data['preco_bpd_US'].resample('M').std().reset_index()
                monthly_volatility_chart = alt.Chart(monthly_volatility_data).mark_line().encode(
                    x=alt.X('data:T', title='Data', axis=alt.Axis(format='%Y-%m', tickCount='month')),
                    y=alt.Y('preco_bpd_US', title='Volatilidade Mensal (USD)')
                ).properties(
                    width=400,
                    height=300
                )
                st.altair_chart(monthly_volatility_chart, use_container_width=True)

            col3, col4 = st.columns(2)

            #with col3:
                #Adicione um grafico

            #with col4:
                #Adicione um grafico

# Tab: Modelo Machine Learning
with tabs[3]:
    st.header("Modelo Machine Learning")
    st.write("""Aqui será apresentado o modelo de Machine Learning.""")
