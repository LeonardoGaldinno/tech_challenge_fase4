# Brent Oil Price Forecasting

This project focuses on analyzing and forecasting Brent oil prices using historical data and machine learning models. We built an interactive application using Streamlit to provide valuable insights into oil price trends, volatility, and predictive analysis to guide decision-making for stakeholders.

## Table of Contents

- Project Overview
- Project Phases
- Features
- Technologies Used
- Data Sources
- Machine Learning Model
- Results
- Collaborators
- Access the Application

## Project Overview

Our team developed an interactive **Streamlit** application to analyze and forecast Brent oil prices. The primary goal of this project was to provide actionable insights into oil price trends and help stakeholders make data-driven decisions based on historical data and predictive models.

## Project Phases

1. **Project Planning**: Defined objectives, selected data sources, and established clear milestones.
2. **Data Setup**: Stored historical data from sources like **IPEA**, **EIA**, **IEA**, **OPEC**, and **YFinance** in **BigQuery** to ensure seamless integration with Streamlit.
3. **Data Analysis**: Conducted trend, volatility, and seasonality analysis to identify key factors affecting oil prices, including economic indicators and geopolitical events.
4. **Machine Learning Model**: Developed a **Prophet-based forecasting model** to predict oil prices. The model achieved strong performance with:
    - MAE (Mean Absolute Error): 7.68
    - RMSE (Root Mean Squared Error): 8.52
    - WMAPE (Weighted Mean Absolute Percentage Error): 9.91%
5. **Results**: The model provided daily price forecasts and actionable insights into price trends and volatility.

## Features

- Interactive **Streamlit** dashboard for visualizing historical data and predictions.
- **Prophet-based machine learning model** for accurate daily forecasting.
- **Trend**, **volatility**, and **seasonality** analysis of Brent oil prices.
- Integration with **BigQuery** to retrieve data from multiple sources.
- Ability to analyze key factors influencing oil prices, such as geopolitical events and economic indicators.

## Technologies Used

- **Python**: For data analysis and machine learning model development.
- **Streamlit**: For the interactive dashboard and data visualization.
- **Prophet**: For time series forecasting.
- **BigQuery**: For storing and querying large datasets.
- **Pandas, NumPy**: For data manipulation and analysis.
- **Matplotlib, Plotly**: For data visualization.

## Data Sources

- **IPEA (Institute for Applied Economic Research)**
- **EIA (U.S. Energy Information Administration)**
- **IEA (International Energy Agency)**
- **OPEC (Organization of the Petroleum Exporting Countries)**
- **Yahoo Finance (YFinance)**

## Machine Learning Model

We used **Prophet**, a forecasting tool by Facebook, to predict the price of Brent oil based on historical data. This model handles missing data well and is particularly suited for time series data that exhibit daily, weekly, or yearly seasonal trends.

The model achieved the following performance metrics:
- **MAE**: 7.68
- **RMSE**: 8.52
- **WMAPE**: 9.91%

## Results

Our model was able to provide daily price predictions with reasonable accuracy. Additionally, the analysis of oil price volatility, trends, and seasonality allowed us to identify key external factors such as economic indicators and geopolitical events that impact oil prices.

## Collaborators

This project was a collaborative effort from the following team members:

- **Alice Falconi**
- **João Pereira**
- **Iago Coelho**
- **Rafaella Cardoso**
- **Leonardo Galdino**

## Access the Application

You can access the interactive **Brent Oil Price Forecasting** application by following this link:

[**Brent Oil Price Forecasting App**](https://tcfiap4.streamlit.app/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
