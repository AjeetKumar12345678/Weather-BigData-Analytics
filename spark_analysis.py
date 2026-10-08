from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max, min


def analyze_weather(weather_data):

    spark = (
        SparkSession.builder
        .appName("WeatherBigDataAnalytics")
        .master("local[*]")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .getOrCreate()
    )

    hourly = weather_data["hourly"]

    rows = []

    for i in range(len(hourly["time"])):
        rows.append((
            hourly["time"][i],
            hourly["temperature_2m"][i],
            hourly["relative_humidity_2m"][i],
            hourly["precipitation"][i],
            hourly["wind_speed_10m"][i]
        ))

    columns = [
        "time",
        "temperature",
        "humidity",
        "rainfall",
        "wind_speed"
    ]

    df = spark.createDataFrame(rows, columns)

    result = df.select(
        avg("temperature").alias("avg_temperature"),
        max("temperature").alias("max_temperature"),
        min("temperature").alias("min_temperature"),
        avg("humidity").alias("avg_humidity"),
        avg("wind_speed").alias("avg_wind_speed"),
        avg("rainfall").alias("avg_rainfall")
    ).collect()[0]

    analysis = {
        "avg_temperature": round(result["avg_temperature"], 2),
        "max_temperature": round(result["max_temperature"], 2),
        "min_temperature": round(result["min_temperature"], 2),
        "avg_humidity": round(result["avg_humidity"], 2),
        "avg_wind_speed": round(result["avg_wind_speed"], 2),
        "avg_rainfall": round(result["avg_rainfall"], 2)
    }

    spark.stop()

    return analysis