import argparse
from etl.extract import get_weather_data
from etl.transform import transform
from etl.load import save_to_csv, save_to_db

def main(start_date, end_date):
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude=55.0344&longitude=82.9434&"
        "daily=sunrise,sunset,daylight_duration&"
        "hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,"
        "temperature_80m,temperature_120m,wind_speed_10m,wind_speed_80m,wind_direction_10m,"
        "wind_direction_80m,visibility,evapotranspiration,weather_code,soil_temperature_0cm,"
        "soil_temperature_6cm,rain,showers,snowfall&"
        "timezone=auto&timeformat=unixtime&wind_speed_unit=kn&temperature_unit=fahrenheit&"
        "precipitation_unit=inch&"
        f"start_date={start_date}&end_date={end_date}"
    )

    data = get_weather_data(url)
    df = transform(data)
    save_to_csv(df, f"output_{start_date}_to_{end_date}.csv")
    save_to_db(df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weather ETL pipeline")
    parser.add_argument('--start_date', default='2025-05-16', help="Start date in YYYY-MM-DD format")
    parser.add_argument('--end_date', default='2025-05-30', help="End date in YYYY-MM-DD format")
    args = parser.parse_args()
    main(args.start_date, args.end_date)
