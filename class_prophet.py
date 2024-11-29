import prophet
import joblib
import pandas as pd

class Prophet_model:
    def __init__(self, model_path='modelo_prophet.pkl'):
        # Carrega o modelo salvo
        self.model = joblib.load(model_path)

    def make_df_and_predict(self, max_date):

        start_date = "2024-07-24"
        end_date = max_date

        data_range = pd.date_range(start=start_date, end=end_date).size

        df_future = self.model.make_future_dataframe(periods=data_range, freq='D')
        
        df_forecast = self.model.predict(df_future)


        return df_forecast, data_range


