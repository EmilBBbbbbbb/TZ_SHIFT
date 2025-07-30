import pandas as pd

# Сохранение в csv
def save_to_csv(df: pd.DataFrame, filename: str):
    df.to_csv(filename, index=False)
