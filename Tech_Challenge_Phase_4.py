import streamlit as st
import pandas as pd
from google.cloud import bigquery
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from database import BigQuery
from class_prophet import Prophet_model


model_code = """# Base de treino e validação (Série Não Estacionária)
treino = df_base[df_base['ds'] < '2024-07-24']
valid_e = df_base.loc[(df_base['ds'] >= '2024-07-24') & (df_base['ds'] <= '2024-10-21')]
h = valid_e['ds'].nunique()

# Prophet
prophet_object = Prophet(interval_width=0.9)
prophet_object.fit(treino)
df_future = prophet_object.make_future_dataframe(periods=(pd.to_datetime('2030-06-30') - df_base['ds'].max()).days, freq='D')
df_forecast = prophet_object.predict(df_future)
forecast_prophet = df_forecast.merge(df_base, on=['ds'], how='left')

# Calcular métricas
y_test = valid_e['y'].values
y_pred = forecast_prophet[forecast_prophet['ds'].isin(valid_e['ds'])]['yhat'].values

wmape = np.sum(np.abs(y_test - y_pred)) / np.sum(y_test) * 100
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"WMAPE: {wmape:.2f}%")
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")


# Plotar previsões futuras
    plt.figure(figsize=(14, 5))
    plt.plot(df_base['ds'], df_base['y'], color='blue', label='Dados Históricos')
    plt.plot(forecast_prophet['ds'], forecast_prophet['yhat'], color='red', label='Previsões Prophet')
    plt.title('Previsões de Preços até 2024 usando Prophet')
    plt.xlabel('Data')
    plt.ylabel('Preço')
    plt.legend()
    plt.show()"""

st.set_page_config(layout="wide")

client = BigQuery()
ipea_df, merged_df = client.create_dfs()

model = Prophet_model()

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
            Para este projeto, utilizamos dados históricos de preços do petróleo brent, que são fornecidos pelo site do Instituto de Pesquisa 
            Econômica Aplicada (IPEA), como também dados de consumo mundial de petróleo de fontes como: Energy Information Administration (EIA), 
            International Energy Agency (IEA) e Organization of the Petroleum Exporting Countries (OPEC).
     
            Esses dados incluem informações sobre as datas, os preços e a média diária do consumo de petróleo ao longo do tempo. 
            Para garantir que os dados estejam bem organizados e facilmente acessíveis, armazenamos tudo no BigQuery, uma plataforma de 
            armazenamento de dados na nuvem. Isso não só facilita a estruturação dos dados, mas também permite que eles sejam integrados 
            automaticamente com o Streamlit, a ferramenta que usamos para criar nosso dashboard interativo e o modelo de previsão. 
            Dessa forma, conseguimos atualizar e visualizar os dados em tempo real, proporcionando uma experiência mais eficiente e dinâmica 
            para os usuários.
            """)
            
            st.header("Análise Exploratória de Dados")
            ipea_df = ipea_df.dropna(subset=['preco_bpd_US'])
            decomposition = seasonal_decompose(ipea_df['preco_bpd_US'], model='additive', period=12)
            decomposition_data = pd.DataFrame({
                'data': ipea_df.index,
                'trend': decomposition.trend,
                'seasonal': decomposition.seasonal,
                'residual': decomposition.resid
            }).dropna()

            trend_chart = alt.Chart(decomposition_data).mark_line(color='blue').encode(
                x=alt.X('data:T', title='Data', axis=alt.Axis(format='%Y-%m', tickCount='month')),
                y=alt.Y('trend', title='Preço do Petróleo (USD)')
            ).properties(width=500, height=300)

            seasonal_chart = alt.Chart(decomposition_data).mark_line(color='blue').encode(
                x=alt.X('data:T', title='Data', axis=alt.Axis(format='%Y-%m', tickCount='month')),
                y=alt.Y('seasonal', title='')
            ).properties(width=500, height=300)

            residual_chart = alt.Chart(decomposition_data).mark_line(color='blue').encode(
                x=alt.X('data:T', title='Data', axis=alt.Axis(format='%Y-%m', tickCount='month')),
                y=alt.Y('residual', title='')
            ).properties(width=500, height=300)

                
            st.subheader("Tendência")
            st.altair_chart(trend_chart, use_container_width=True)

            st.write("""**Análise de Tendência:** Ao examinar o gráfico de linha apresentado, podemos identificar a evolução dos preços do 
            petróleo entre 2020 e 2024. Notamos que, em 2020, houve uma forte queda nos preços devido à pandemia de COVID-19, que resultou 
            em uma drástica redução na demanda global por petróleo. Essa queda foi acentuada pelas medidas de lockdown e pela diminuição das 
            atividades econômicas.
            Após essa fase crítica, os preços começaram a se recuperar lentamente em 2021, à medida que a economia global foi se reabrindo. 
            Desde então, observamos uma tendência levemente ascendente, indicando um aumento gradual nos preços do petróleo. Essa trajetória 
            sugere que, apesar das flutuações ocasionais, o mercado está se ajustando às novas condições e à crescente demanda.
            """)

            st.subheader("Sazonalidade")
            st.altair_chart(seasonal_chart, use_container_width=True)

            st.write("""**Análise de Sazonalidade:** No gráfico acima podemos observar variações sazonais que podem estar associadas a eventos econômicos recorrentes. 
            É importante entender as flutuações periódicas nos preços e para fazer previsões mais precisas. 
            A sazonalidade pode ser causada por fatores como mudanças climáticas, feriados, eventos sazonais ou flutuações na demanda.
            """)

            st.subheader("Ruído")
            st.altair_chart(residual_chart, use_container_width=True)

            st.write("""**Análise de Ruído:** O ruído representa as flutuações aleatórias e imprevisíveis nos dados dos preços do petróleo. 
            Essas variações podem ser causadas por eventos inesperados, como desastres naturais, crises políticas, ou outras perturbações 
            que não seguem um padrão específico. No gráfico acima, podemos observar uma maior taxa de ruído em Abril de 2022, indicando uma maior volatilidade nos preços do petróleo nesse período.
            """)
 
            st.subheader("Variação Anual dos Preços do Petróleo")
            
            current_year = pd.Timestamp.now().year
            start_year = current_year - 5

            filtered_data = ipea_df[(ipea_df.index.year > start_year) & (ipea_df.index.year <= current_year)]

            annual_prices = filtered_data.resample('YE').mean().reset_index()
            bar_chart = alt.Chart(annual_prices).mark_bar().encode(
                x=alt.X('year(data):T', title='Ano', axis=alt.Axis(labelAngle=0), bandPosition=0),
                y=alt.Y('preco_bpd_US', title='Preço Médio por Barril (USD)')
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
            monthly_volatility = ipea_df['preco_bpd_US'].resample('ME').std().reset_index()
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

            st.subheader("Análise de Key Performance Indicators (KPIs)")

            st.write("""A taxa de juros dos Estados Unidos da América (EUA) e o preço do dólar são dois fatores importantes que influenciam os preços do petróleo.
            Os gráficos abaixo mostram a cotização do dólar e a taxa de juros dos EUA. 
            """)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(label="Preço Médio do Petróleo", value="R$ 105,90", delta="10%")
                
            with col2:
                st.metric(label="Tx Juros Americano", value="5,2%", delta="+25%")
                
            with col3:
                st.metric(label="Indice Dólar Americano", value="101.789", delta="15%")


            st.write("""- **Taxa de Juros dos EUA:** A taxa de juros afeta o consumo, pois custos de empréstimos mais altos tornam o crédito mais caro. 
            Isso reduz os fundos disponíveis para impulsionar o crescimento econômico e a demanda por petróleo, resultando na diminuição dos preços do petróleo.""")

            st.write("""- **Preço do Dólar:** O preço do dólar influencia diretamente o preço do petróleo, pois o barril de petróleo é cotado em dólar. 
            Flutuações no valor do dólar podem impactar significativamente os preços do petróleo.""")

            st.subheader("Análise da média diaria de consumo de petróleo por ano vs preço médio") 

            consumption_chart = alt.Chart(merged_df).mark_area(opacity=0.4, color='blue').encode(
                x=alt.X('year:O', title='Ano', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('Consumo', title='Consumo (média Mi. barris p/ dia)', axis=alt.Axis(titleColor='blue'),
                    scale=alt.Scale(domain=[0, merged_df['Consumo'].max()])),
                    ).properties(width=500, height=302)

            price_chart = alt.Chart(merged_df).mark_area(opacity=0.4, color='darkred').encode(
                x=alt.X('year:O', title='Ano', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('preco_bpd_US', title='Preço Médio por Barril (USD)', axis=alt.Axis(titleColor='darkred'),
                    scale=alt.Scale(domain=[0, merged_df['preco_bpd_US'].max()])),
                    ).properties(width=500, height=302)

            combined_chart = alt.layer(consumption_chart, price_chart).resolve_scale(
                y='independent')

            st.markdown("<h4 style='font-size: 22px;'>Consumo Mundial de Petróleo vs. Preço Médio</h4>", unsafe_allow_html=True)
            st.altair_chart(combined_chart, use_container_width=True)

            st.write("""**Análise de Consumo Mundial vs. Preço Médio:** 
            O gráfico acima compara a média diária por ano de consumo de petróleo com o preço médio do petróleo ao longo dos anos.
            Podemos observar que apesar das variações no preço do petróleo, o consumo mundial tem se mantido relativamente estável.
            Isso sugere que o consumo de petróleo é influenciado por fatores diferentes dos preços, como a demanda global por energia e a produção de petróleo.""")

            st.write("""Todos os gráficos apresentados acima permitem uma análise detalhada dos dados, incluindo componentes de tendência, sazonalidade e ruído, entre outros.
            Essa análise é fundamental para entender os padrões subjacentes e identificar possíveis tendências e anomalias que podem afetar os resultados no futuro.
            Para uma visualização mais interativa e dinâmica, todos os gráficos estão disponíveis na aba dashboard.
            """)

            st.header("Modelo Machine Learning")
            st.write("""Criamos um modelo de Machine Learning para séries temporais visando prever os preços do petróleo Brent diariamente. 
            Incluímos uma análise de desempenho do modelo e as previsões geradas, demonstrando a eficácia e a aplicabilidade prática do nosso trabalho. O modelo que trouxe uma melhor previsão foi o prophet.
            """)
            st.write("O modelo foi treinado a partir de uma base de 5 anos, e avaliado com as métricas:")
            st.write("MAE: 7.68")
            st.write("RMSE:8.52")
            st.write("WMAPE: 9.91%")
                
            st.write("As métricas indicam um bom desempenho, com erros médios inferiores a 10 unidades (na mesma escala dos dados), controle sobre os erros maiores e uma precisão elevada, já que o erro médio corresponde a menos de 10% dos valores reais.")

            st.write("O código de treino, teste e avaliação está disponível abaixo:")
            
            st.code(model_code, language="python")

            #st.write


            st.write("""O resultado deste projeto é uma combinação de visualizações interativas e previsões precisas que oferecem uma visão 
            abrangente do mercado de petróleo com insights adicionados em um relatório. As informações detalhadas sobre a análise de dados, o dashboard interativo e o 
            modelo de Machine Learning estão disponíveis em suas respectivas abas: Relatório, Dashboard e Modelo Machine Learning.""")

            st.header("Conclusão")
            
            st.write("""
            A evolução dos preços do petróleo entre 2019 e 2024 reflete o impacto de fatores econômicos e sociais significativos, como a pandemia da COVID-19 e a recuperação econômica.
            A queda em 2020 destaca a vulnerabilidade do mercado de petróleo a impactos externos, enquanto a recuperação gradual a partir de 2021 ilustra a resiliência e a capacidade de ajuste do mercado às mudanças na demanda global.
            O impacto da pandemia da COVID-19 em 2020 resultou em uma queda acentuada nos preços, seguida por uma alta significativa em 2021, atingindo um recorde em 2022. Nos anos seguintes, observa-se um leve recuo nos preços, ainda refletindo a recuperação econômica global e ajustes na produção. 
            Esse padrão destaca a importância de monitorar eventos externos e suas influências para antecipar tendências e planejar estratégias no setor de petróleo.
            """)

            st.write("""
            A variação sazonal nos preços é essencial para compreender os padrões recorrentes do mercado e melhorar a precisão das previsões econômicas. 
            Fatores como mudanças climáticas, feriados e eventos específicos têm um impacto nas flutuações sazonais, influenciando a demanda e os preços de forma previsível.
            """)
            
            st.write("""
            O ruído nos dados, representado por flutuações imprevisíveis, reflete a influência de eventos inesperados que impactam o mercado de petróleo de forma aleatória.
            A identificação de períodos com maior volatilidade, como observado em abril de 2022, é importante para entender as dinâmicas do mercado e gerenciar os riscos associados 
            a essas variações.
            O maior índice de ruído no primeiro trimestre de 2022 ocorre devido ao início da guerra entre Russia e Ucrânia. A pressão em cima dos preços do petróleo e do gás 
            natural vem como consequência do conflito, da limitação da oferta dessas commodities, os baixos níveis de armazenamento de gás na Europa e a dificuldade prática que 
            o continente tem de substituir o gás russo no curto prazo. De acordo com os dados da UOL, depois de duas semanas do início do conflito, o preço do petróleo subiu 20%.
            """)
            
            st.write("""
            Na análise de volatilidade dos preços do petróleo ao longo dos últimos cinco anos é uma ferramenta essencial para entender os níveis de risco e estabilidade no mercado.
            Períodos de alta volatilidade oferecem potencial para maiores retornos, mas também apresentam riscos elevados, enquanto períodos de baixa volatilidade são mais indicados para investidores que priorizam segurança e estabilidade.
            Ao identificar esses padrões, os investidores podem alinhar suas estratégias de acordo com seu perfil de risco, maximizando oportunidades e minimizando perdas em um mercado dinâmico como o de petróleo.
            """)
            
            st.write("""
            Contudo, concluímos que o consumo mundial de petróleo apresenta estabilidade ao longo dos anos, independentemente das variações nos preços. 
            O modelo e os gráficos no dashboard apresentam insights importantes que podem auxiliar nas previsões dos preços nos próximos anos, porém, conforme citado anteriormente,
            fatores externos que não podem ser previstos geram uma grande variação no preço do petróleo.
            """)
                    
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
            filtered_merged_df = merged_df[(merged_df['year'] >= start_date.year) & (merged_df['year'] <= end_date.year)]

            
            min_price = float(filtered_data['preco_bpd_US'].min())
            max_price = float(filtered_data['preco_bpd_US'].max())
            price_range = st.slider(
                "Preço do Petróleo (USD)",
                min_value=min_price,
                max_value=max_price,
                value=(min_price, max_price),
                step=0.1
            )

            
            filtered_data = filtered_data[(filtered_data['preco_bpd_US'] >= price_range[0]) & (filtered_data['preco_bpd_US'] <= price_range[1])]
            #filtered_merged_df = filtered_merged_df[(filtered_merged_df['preco_bpd_US'] >= price_range[0]) & (filtered_merged_df['preco_bpd_US'] <= price_range[1])]
            
            years = filtered_data.index.year.unique()
            selected_years = st.multiselect("Selecione o Ano", options=years, default=years.tolist())
            if not selected_years:
                st.warning("Selecione pelo menos um ano.")
                selected_years = years.tolist()
            filtered_data = filtered_data[filtered_data.index.year.isin(selected_years)]
            filtered_merged_df = filtered_merged_df[filtered_merged_df['year'].isin(selected_years)]
            
            months = filtered_data.index.month.unique()
            selected_months = st.multiselect("Selecione o Mês", options=months, default=months.tolist())
            filtered_data = filtered_data[filtered_data.index.month.isin(selected_months)]
            #filtered_merged_df = filtered_merged_df[filtered_merged_df['data'].dt.month.isin(selected_months)]

            volatility_window = st.slider("Janela para Média Móvel de Volatilidade (em meses)", min_value=1, max_value=12, value=1)
            monthly_volatility_data = filtered_data['preco_bpd_US'].resample('ME').std().reset_index()
            monthly_volatility_data['volatility_moving_avg'] = monthly_volatility_data['preco_bpd_US'].rolling(window=volatility_window).mean()

            seasonality_options = ["Anual", "Mensal"]
            seasonality_choice = st.selectbox(
                "Período da Decomposição Sazonal (Aplicável para Gráficos de Tendência, Sazonalidade e Ruído)",
                seasonality_options,
                index=1
            )

            if seasonality_choice == "Anual":
                period = 365 
            else:
                period = 12

            st.write(f"Janela para Média Móvel de Volatilidade: {volatility_window} meses")

            st.subheader("Filtros Aplicados:")
            st.markdown(f"**Data de Início:** {start_date.strftime('%d/%m/%Y')}")
            st.markdown(f"**Data de Fim:** {end_date.strftime('%d/%m/%Y')}")
            st.markdown(f"**Preço do Petróleo (USD):** {price_range[0]} - {price_range[1]}")
            st.markdown(f"**Anos Selecionados:** {', '.join(map(str, selected_years))}")
            st.markdown(f"**Meses Selecionados:** {', '.join(map(str, selected_months))}")
            st.markdown(f"**Janela para Média Móvel de Volatilidade:** {volatility_window} meses")
            st.markdown(f"**Período para a Decomposição Sazonal:** {(map(str, seasonality_choice))}")

        with col_dash:
            st.header("Dashboard")
            
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(label="Preço Médio do Petróleo", value="R$ 105,90", delta="10%")
                
            with col2:
                st.metric(label="Tx Juros Americano", value="5,2%", delta="+25%")
                
            with col3:
                st.metric(label="Indice Dólar Americano", value="101.789", delta="15%")
            

            col4, col5 = st.columns(2)

            with col4:
                st.subheader("Variação Anual da Media dos Preços do Petróleo")
                try:
                    annual_prices = filtered_data.resample('YE').mean().reset_index()
                    years_in_data = annual_prices['data'].dt.year.unique()

                    bar_chart = alt.Chart(annual_prices).mark_bar(color='steelblue').encode(
                        x=alt.X('year(data):O',  # Change to 'O' for ordinal (categorical) encoding
                                title='Ano',
                                axis=alt.Axis(
                                    labelAngle=0, 
                                    labelAlign='center',  # Center the labels horizontally
                                    labelOffset=10  # Optional: Adjust if labels are too close/far from bars
                                ),
                                scale=alt.Scale(domain=list(years_in_data))),  # Use the exact years
                        y=alt.Y('preco_bpd_US', title='Preço Médio por Barril (USD)'),
                    ).properties(width=500, height=303)

                    st.altair_chart(bar_chart, use_container_width=True)
                except Exception as e:
                    st.error(f"Erro ao gerar o gráfico de Variação Anual dos Preços do Petróleo: {e}")

            with col4:
                st.subheader("Volatilidade Mensal (com Média Móvel)")
                try:
                    volatility_chart = alt.Chart(monthly_volatility_data).mark_line(color='cornflowerblue').encode(
                        x=alt.X('data:T', title='Data', axis=alt.Axis(format='%Y-%m', tickCount='month')),
                        y=alt.Y('volatility_moving_avg', title='Volatilidade Mensal com Média Móvel (USD)')
                    ).properties(width=500, height=302)
                    st.altair_chart(volatility_chart, use_container_width=True)
                except Exception as e:
                    st.error(f"Erro ao gerar o gráfico de Volatilidade Mensal: {e}")
            
            with col4:
                try:
                    consumption_chart = alt.Chart(filtered_merged_df).mark_area(opacity=0.4, color='blue').encode(
                        x=alt.X('year:O', title='Ano', axis=alt.Axis(labelAngle=0)),
                        y=alt.Y('Consumo', title='Consumo (média Mi. barris p/ dia)', axis=alt.Axis(titleColor='blue'),
                                scale=alt.Scale(domain=[0, filtered_merged_df['Consumo'].max()])),
                    ).properties(width=500, height=302)

                    price_chart = alt.Chart(filtered_merged_df).mark_area(opacity=0.4, color='darkred').encode(
                        x=alt.X('year:O', title='Ano', axis=alt.Axis(labelAngle=0)),
                        y=alt.Y('preco_bpd_US', title='Preço Médio do Petróleo (USD)', axis=alt.Axis(titleColor='darkred'),
                                scale=alt.Scale(domain=[0, filtered_merged_df['preco_bpd_US'].max()])),
                    ).properties(width=500, height=302)

                    combined_chart = alt.layer(consumption_chart, price_chart).resolve_scale(
                        y='independent'
                    )

                    st.markdown("<h4 style='font-size: 22px;'>Consumo Mundial de Petróleo vs. Preço Médio</h4>", unsafe_allow_html=True)
                    st.altair_chart(combined_chart, use_container_width=True)
                except Exception as e:
                    st.error(f"Erro ao gerar o gráfico de Consumo Mundial e Preço Médio: {e}")

            with col5:
                try:
                    filtered_data = filtered_data.dropna(subset=['preco_bpd_US'])
                    decomposition = seasonal_decompose(filtered_data['preco_bpd_US'], model='additive', period=period)
                    decomposition_data = pd.DataFrame({
                        'data': filtered_data.index,
                        'trend': decomposition.trend,
                        'seasonal': decomposition.seasonal,
                        'residual': decomposition.resid
                    }).dropna()

                    trend_chart = alt.Chart(decomposition_data).mark_line(color='darkgreen').encode(
                        x=alt.X('data:T', title='Data', axis=alt.Axis(format='%Y-%m', tickCount='month')),
                        y=alt.Y('trend', title='Tendência')
                    ).properties(width=500, height=300)

                    seasonal_chart = alt.Chart(decomposition_data).mark_line(color='seagreen').encode(
                        x=alt.X('data:T', title='Data', axis=alt.Axis(format='%Y-%m', tickCount='month')),
                        y=alt.Y('seasonal', title='Sazonalidade')
                    ).properties(width=500, height=300)

                    residual_chart = alt.Chart(decomposition_data).mark_line(color='firebrick').encode(
                        x=alt.X('data:T', title='Data', axis=alt.Axis(format='%Y-%m', tickCount='month')),
                        y=alt.Y('residual', title='Ruído')
                    ).properties(width=500, height=300)

                    st.subheader("Tendência")
                    st.altair_chart(trend_chart, use_container_width=True)
                    st.subheader("Sazonalidade")
                    st.altair_chart(seasonal_chart, use_container_width=True)
                    st.subheader("Ruído")
                    st.altair_chart(residual_chart, use_container_width=True)
                except Exception as e:
                    print("")

# Tab: Modelo Machine Learning
with tabs[3]:
    st.header("""Modelo Machine Learning""")
    st.write("""Demonstração prática do modelo Prophet, treinado com dados históricos até 24/07/2024.""")

    max_date = st.date_input('Selecione a data limite para as previsões', min_value=pd.to_datetime('2024-07-25'))
    
    if end_date:
        if st.button(label='Fazer previsão'):

            prediction_df, data_range = model.make_df_and_predict(max_date=max_date)

            st.write("Previsão do preço em US$ para os próximos {} dias:".format(data_range))

            col1, col2 = st.columns([1,3])
            with col1:
                
                st.subheader("Previsões Geradas")
                st.write(prediction_df[['ds', 'yhat']])

            with col2:


                marker_date = '2024-07-24'

                line_chart = alt.Chart(prediction_df.reset_index()).mark_line().encode(
                    x=alt.X('ds:T', title='yhat', axis=alt.Axis(format='%d/%m/%Y', tickCount='day')),
                    y=alt.Y('yhat:Q', title='Preço Previsto (USD)') 
                ).properties(
                    width=700,
                    height=400
                )

                marker = alt.Chart(pd.DataFrame({'ds': [marker_date]})).mark_rule(color='red').encode(
                    x='ds:T'
                )

                marker_text = alt.Chart(pd.DataFrame({'ds': [marker_date], 'yhat': [prediction_df.loc[prediction_df['ds'] == marker_date, 'yhat'].values[0]]})).mark_text(
                    align='right',
                    baseline='bottom',
                    color='white',
                    fontSize=12
                ).encode(
                    x='ds:T',
                    y=alt.Y('yhat:Q'),
                    text=alt.value('Limite dos Dados de Treino')
                )

                final_chart = line_chart + marker + marker_text

                st.subheader("Visualização gráfica das previsões geradas.")
                st.altair_chart(final_chart, use_container_width=True)


