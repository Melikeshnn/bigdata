from pyspark.sql import SparkSession
import time
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config("spark.master", "local[*]") \
    .config("spark.hadoop.fs.defaultFS", "file:///") \
    .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") \
    .getOrCreate()
# SparkSession başlat
spark = SparkSession.builder.appName("DemoApp").getOrCreate()

print("Spark Application is running...")
time.sleep(600)  # 10 dakika bekle
