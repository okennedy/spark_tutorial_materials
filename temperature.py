from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import requests
import json

data = requests.get("https://home.xthemage.net/graphs/temperature")
data = data.json()[5]["values"]

sc = SparkContext()
spark = SparkSession(sc)

df = spark.createDataFrame(data)
df.select(
    avg(col("y")).name("Avg Temperature"),
    count("y").name("Count")
).show()
