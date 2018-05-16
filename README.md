# spark_tutorial_materials

## Getting Spark

http://spark.apache.org/downloads.html

Install Java
```
> sudo apt install openjdk-8-jre-headless
```
*Requires Java 8, NOT Java 9*


Download: http://spark.apache.org/downloads.html
```
> curl -O http://apache.claz.org/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz
```

Run (python): 
```
> cd spark-2.3.0-bin-hadoop2.7
> ./bin/pyspark
```

## Getting around 

### Load a text file
```
> textFile = spark.read.text("README.md")
> textFile
```
-> DataFrame[value: string]  ## A data frame w/ a single field "value" of type "string"

### Show it
```
> textFile.show()
```

### Count the number of records in the data frame
```
> textFile.count()
-> 103
```

### The first record in the data frame
```
> textFile.first()
```
-> Row(value=u'# Apache Spark')

### The first 10 records in the data frame
```
> textFile.take(10)
```
-> [Row(value=u'# Apache Spark'), Row(value=u''), Row(value=u'Spark is a fast and general cluster computing system for Big Data. It provides'), Row(value=u'high-level APIs in Scala, Java, Python, and R, and an optimized engine that'), Row(value=u'supports general computation graphs for data analysis. It also supports a'), Row(value=u'rich set of higher-level tools including Spark SQL for SQL and DataFrames,'), Row(value=u'MLlib for machine learning, GraphX for graph processing,'), Row(value=u'and Spark Streaming for stream processing.'), Row(value=u''), Row(value=u'<http://spark.apache.org/>')]


## Transforming the data

```
> from pyspark.sql.functions import *
```
some utility functions

```
> lines = textFile.select( split(textFile["value"], "\s+") )
```
"select(cols)" works like "SELECT" in SQL.  Can put any expression?   Not quite...

Many expressions work.
Column references: 
* lines["foo"]   # General use case
* lines.foo      # Shorthand for friendly column names
* col("foo")     # Shorthand, with no compile-time type-checking
* "foo"          # Works sometimes... but can't be manipulated


```
> lines
```
-> DataFrame[split(value, \s+): array<string>]
Whoops... need to give the field a name

```
> lines = textFile.select( split(textFile["value"], "\s+").name("words") )
> lines
```
-> DataFrame[words: array<string>]
```
> lines.first()
```
-> Row(words=[u'#', u'Apache', u'Spark'])

Unnest: Explode 
```
> words = lines.select(explode(lines.words).name("word"))
> words = lines.select(explode(lines.words).name("word"), lines.words.name("sentence"))
```

Filter
```
> words.filter(words.word == "tests").show()
```

Aggregate
```
> lineSizes = lines.select(size(lines.words).name("len"))
> lineSizes.select( avg(lineSizes.len) ).show()
```

Group-By Aggregate
```
> wordCount = words.groupBy("word").count()
> wordCount.show()
> wordCount.select( avg(wordCount["count"]), max(wordCount["count"]), sum(wordCount["count"]) ).show()
```

SQL
```
> wordCount.createOrReplaceTempView("WORDCOUNT")
> spark.sql("SELECT MAX(`count`) FROM WORDCOUNT").show()
```



## Data Sources 

Postgres
```
> sudo apt install libpostgresql-jdbc-java
> apt content libpostgresql-jdbc-java
> ./bin/pyspark --driver-class-path /usr/share/java/postgresql.jar --jars /usr/share/java/postgresql.jar
```

Pyspark running
```
> sensors = spark.read.format("jdbc").option("url", "jdbc:postgresql:homebase").option("dbtable", "sensors").option('user', 'test_user').option('password', '12345').load()
> readings = spark.read.format("jdbc").option("url", "jdbc:postgresql:homebase").option("dbtable", "readings").option('user', 'test_user').option('password', '12345').load()
> sensors.show()
> readings.show()
> sensors.alias('s').join(readings.alias('r'), col('r.sensor') == col('s.id')).show()
```

```
> from datetime import datetime
> from datetime import timedelta
> four_days_ago = datetime.now() - timedelta(days = 4)
> readings.filter(readings.time > four_days_ago & readings.sensor == 4).count()
```
whoooops...
```
> readings.filter((readings.time > four_days_ago) & (readings.sensor == 4)).count()
> readings.filter((readings.time > four_days_ago) & (readings.sensor == 4)).show()
> snake_tank = readings.filter((readings.time > four_days_ago) & (readings.sensor == 4)).select(readings.time, readings.data)
> snake_tank.show()
```

```
> import json
> snake_temp = snake_tank.rdd.map( lambda x : { "time": x.time, "data": json.loads(x.data) }  ).toDF()
> snake_temp.select( snake_temp.time, snake_temp.data.temp.name("temp") ).show()
```

^Z
```
> sudo -H pip2 install pandas
> sudo -H pip2 install setuptools
> sudo -H pip2 install matplotlib
> fg
```

```
> import matplotlib.pyplot as plt
> raw_temp = snake_temp.select( snake_temp.time, snake_temp.data.temp.name("temp")).toPandas()
> plt.plot(raw_temp.temp)
> plt.show()
```

```
> import matplotlib.dates as mdates
> plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
> plt.gca().xaxis.set_major_locator(mdates.DayLocator())
> plt.gcf().autofmt_xdate()
> plt.plot(raw_temp.time, raw_temp.temp)
> plt.show()
```


## In the Cloud

https://cloud.google.com/dataproc/




