import pandas as pd
from sqlalchemy import create_engine
import loguru

# Сохранение в csv
def save_to_csv(df: pd.DataFrame, filename: str):
    df.to_csv(filename, index=False)

def save_to_db(df: pd.DataFrame):
    # Создаём движок подключения
    try:
        engine = create_engine('postgresql+psycopg2://user:pass@localhost:5432/weather_db')
        df.to_sql('weather_data', con=engine, if_exists='append', index=False)
    except Exception as error:
        loguru.logger.error(error)