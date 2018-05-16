from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

sc = SparkContext()
spark = SparkSession(sc)
df = sc.parallelize( ( ("A", 1), ("B", 2) ) ).toDF()
print("The number of lines is {}".format(df.count()))
