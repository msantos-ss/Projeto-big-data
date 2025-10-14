from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("AnaliseRestaurante")
    .master("local[*]")
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.RawLocalFileSystem")
    .getOrCreate()
)


df_spark = spark.read.option("header", True).option("inferSchema", True).csv("dados/vendas/*/*/*.csv")


df_spark.printSchema()
df_spark.show(5)

