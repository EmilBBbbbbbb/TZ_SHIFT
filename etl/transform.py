import pandas as pd

# Функция перевода Фаренгейт в Цельсии
def fahrenheit_to_celsius(fahrenheit: pd.Series) -> pd.Series:
    return (fahrenheit - 32) * 5 / 9

# Функция перевода инч в миллиметры
def inch_to_mm(inch: pd.Series) -> pd.Series:
    return inch * 25.4

# Функция перевода футов в метры
def fut_to_m(fut: pd.Series) -> pd.Series:
    return fut / 3.281

# Функция для перевода узлов в м/с
def knots_to_ms(knots: pd.Series) -> pd.Series:
    return knots * 0.514444

def transform(data: dict) -> pd.DataFrame:
    df_hourly = pd.DataFrame(data['hourly'])
    df_daily = pd.DataFrame(data['daily'])

    df_hourly['time'] = pd.to_datetime(df_hourly['time'], unit='s')
    df_daily['time'] = pd.to_datetime(df_daily['time'], unit='s')
    df_daily['sunrise'] = pd.to_datetime(df_daily['sunrise'], unit='s')
    df_daily['sunset'] = pd.to_datetime(df_daily['sunset'], unit='s')

    df_hourly['date'] = df_hourly['time'].dt.date
    df_daily['date'] = df_daily['time'].dt.date

    merged = pd.merge(df_hourly, df_daily, on='date', suffixes=('_hourly', '_daily'))

    # Подсчет средних значений
    simple_daily_avg: pd.DataFrame = merged.groupby('date').agg({
    'temperature_2m': 'mean',
    'relative_humidity_2m': 'mean',
    'dew_point_2m': 'mean',
    'apparent_temperature': 'mean',
    'temperature_80m': 'mean',
    'temperature_120m': 'mean',
    'wind_speed_10m': 'mean',
    'wind_speed_80m': 'mean',
    'visibility': 'mean',
    'rain': 'sum',
    'showers':'sum',
    'snowfall': 'sum'
    }).reset_index()

    # Переименование столбцов
    simple_daily_avg = simple_daily_avg.rename(columns={
        'temperature_2m': 'avg_temperature_2m_24h',
        'relative_humidity_2m': 'avg_relative_humidity_2m_24h',
        'dew_point_2m': 'avg_dew_point_2m_24h',
        'apparent_temperature': 'avg_apparent_temperature_24h',
        'temperature_80m': 'avg_temperature_80m_24h',
        'temperature_120m': 'avg_temperature_120m_24h',
        'wind_speed_10m': 'avg_wind_speed_10m_24h',
        'wind_speed_80m': 'avg_wind_speed_80m_24h',
        'visibility': 'avg_visibility_24h',
        'rain': 'total_rain_24h',
        'showers':'total_showers_24h',
        'snowfall': 'total_snowfall_24h'})

    # Преобразование в метрическую систему
    simple_daily_avg['avg_temperature_2m_24h'] = fahrenheit_to_celsius(simple_daily_avg['avg_temperature_2m_24h'])
    simple_daily_avg['avg_dew_point_2m_24h'] = fahrenheit_to_celsius(simple_daily_avg['avg_dew_point_2m_24h'])
    simple_daily_avg['avg_apparent_temperature_24h'] = fahrenheit_to_celsius(simple_daily_avg['avg_apparent_temperature_24h'])
    simple_daily_avg['avg_temperature_80m_24h'] = fahrenheit_to_celsius(simple_daily_avg['avg_temperature_80m_24h'])
    simple_daily_avg['avg_temperature_120m_24h'] = fahrenheit_to_celsius(simple_daily_avg['avg_temperature_120m_24h'])
    simple_daily_avg['avg_wind_speed_10m_24h'] = knots_to_ms(simple_daily_avg['avg_wind_speed_10m_24h'])
    simple_daily_avg['avg_wind_speed_80m_24h'] = knots_to_ms(simple_daily_avg['avg_wind_speed_80m_24h'])
    simple_daily_avg['avg_visibility_24h'] = fut_to_m(simple_daily_avg['avg_visibility_24h'])
    simple_daily_avg['total_rain_24h'] = inch_to_mm(simple_daily_avg['total_rain_24h'])
    simple_daily_avg['total_showers_24h'] = inch_to_mm(simple_daily_avg['total_showers_24h'])
    simple_daily_avg['total_snowfall_24h'] = inch_to_mm(simple_daily_avg['total_snowfall_24h'])


    mask = (merged['time_hourly'] >= merged['sunrise']) & (merged['time_hourly'] <= merged['sunset'])

    # Подсчет средних значений для светового дня
    daylight_daily_avg: pd.DataFrame = merged[mask].groupby('date').agg({
        'temperature_2m': 'mean',
        'relative_humidity_2m': 'mean',
        'dew_point_2m': 'mean',
        'apparent_temperature': 'mean',
        'temperature_80m': 'mean',
        'temperature_120m': 'mean',
        'wind_speed_10m': 'mean',
        'wind_speed_80m': 'mean',
        'visibility': 'mean',
        'rain': 'sum',
        'showers':'sum',
        'snowfall': 'sum'
    })

    # Переименование столбцов

    daylight_daily_avg = daylight_daily_avg.rename(columns={
        'temperature_2m': 'avg_temperature_2m_daylight',
        'relative_humidity_2m': 'avg_relative_humidity_2m_daylight',
        'dew_point_2m': 'avg_dew_point_2m_daylight',
        'apparent_temperature': 'avg_apparent_temperature_daylight',
        'temperature_80m': 'avg_temperature_80m_daylight',
        'temperature_120m': 'avg_temperature_120m_daylight',
        'wind_speed_10m': 'avg_wind_speed_10m_daylight',
        'wind_speed_80m': 'avg_wind_speed_80m_daylight',
        'visibility': 'avg_visibility_daylight',
        'rain': 'total_rain_daylight',
        'showers':'total_showers_daylight',
        'snowfall': 'total_snowfall_daylight'
    })

    # Преобразование в метрическую систему
    daylight_daily_avg['avg_temperature_2m_daylight'] = fahrenheit_to_celsius(daylight_daily_avg['avg_temperature_2m_daylight'])
    daylight_daily_avg['avg_dew_point_2m_daylight'] = fahrenheit_to_celsius(daylight_daily_avg['avg_dew_point_2m_daylight'])
    daylight_daily_avg['avg_apparent_temperature_daylight'] = fahrenheit_to_celsius(daylight_daily_avg['avg_apparent_temperature_daylight'])
    daylight_daily_avg['avg_temperature_80m_daylight'] = fahrenheit_to_celsius(daylight_daily_avg['avg_temperature_80m_daylight'])
    daylight_daily_avg['avg_temperature_120m_daylight'] = fahrenheit_to_celsius(daylight_daily_avg['avg_temperature_120m_daylight'])
    daylight_daily_avg['avg_wind_speed_10m_daylight'] = knots_to_ms(daylight_daily_avg['avg_wind_speed_10m_daylight'])
    daylight_daily_avg['avg_wind_speed_80m_daylight'] = knots_to_ms(daylight_daily_avg['avg_wind_speed_80m_daylight'])
    daylight_daily_avg['avg_visibility_daylight'] = fut_to_m(daylight_daily_avg['avg_visibility_daylight'])
    daylight_daily_avg['total_rain_daylight'] = inch_to_mm(daylight_daily_avg['total_rain_daylight'])
    daylight_daily_avg['total_showers_daylight'] = inch_to_mm(daylight_daily_avg['total_showers_daylight'])
    daylight_daily_avg['total_snowfall_daylight'] = inch_to_mm(daylight_daily_avg['total_snowfall_daylight'])

    simple_daily_avg.reset_index()
    merged_all = pd.merge(merged, simple_daily_avg, on='date', how='left')
    merged_all = pd.merge(merged_all, daylight_daily_avg, on='date', how='left')

    merged_all['wind_speed_10m_m_per_s'] = knots_to_ms(merged_all['wind_speed_10m'])
    merged_all['wind_speed_80m_m_per_s'] = knots_to_ms(merged_all['wind_speed_80m'])
    merged_all['temperature_2m_celsius'] = fahrenheit_to_celsius(merged_all['temperature_2m'])
    merged_all['apparent_temperature_celsius'] = fahrenheit_to_celsius(merged_all['apparent_temperature'])
    merged_all['temperature_80m_celsius'] = fahrenheit_to_celsius(merged_all['temperature_80m'])
    merged_all['temperature_120m_celsius'] = fahrenheit_to_celsius(merged_all['temperature_120m'])
    merged_all['soil_temperature_0cm_celsius'] = fahrenheit_to_celsius(merged_all['soil_temperature_0cm'])
    merged_all['soil_temperature_6cm_celsius'] = fahrenheit_to_celsius(merged_all['soil_temperature_6cm'])
    merged_all['rain_mm'] = inch_to_mm(merged_all['rain'])
    merged_all['showers_mm'] = inch_to_mm(merged_all['showers'])
    merged_all['snowfall_mm'] = inch_to_mm(merged_all['snowfall'])
    merged_all['daylight_hours'] = (merged_all['sunset'] - merged_all['sunrise']).dt.total_seconds() / 3600
    merged_all['sunrise_iso'] = merged_all['sunrise'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    merged_all['sunset_iso'] = merged_all['sunset'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Удаление лишних столбцов
    merged_all = merged_all.drop(columns=['time_hourly',
                                          'temperature_2m',
                                          'relative_humidity_2m',
                                          'dew_point_2m',
                                          'apparent_temperature',
                                          'temperature_80m',
                                          'temperature_120m',
                                          'wind_speed_10m',
                                          'wind_speed_80m',
                                          'wind_direction_10m',
                                          'visibility',
                                          'evapotranspiration',
                                          'weather_code',
                                          'soil_temperature_0cm',
                                          'soil_temperature_6cm',
                                          'rain',
                                          'showers',
                                          'snowfall',
                                          'date',
                                          'time_daily',
                                          'wind_direction_80m',
                                          'sunrise',
                                          'sunset',
                                          'daylight_duration',
                                          ], axis=1)


    return merged_all