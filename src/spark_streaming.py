from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType

# Spark session başlatma
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .master("local[*]") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/spark-checkpoint") \
    .getOrCreate()

# Kafka'dan veri okuma
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "172.18.0.3:9092") \
    .option("subscribe", "normal-data,anomalies") \
    .load()

# Veri şeması
schema = StructType([
    StructField("id", IntegerType()),
    StructField("value", IntegerType()),
    StructField("anomaly", BooleanType())
])

# Kafka verilerini ayrıştırma
parsed_stream = kafka_stream.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

# Anomali tespiti ve konsola yazdırma
parsed_stream.writeStream \
    .format("console") \
    .outputMode("append") \
    .start() \
    .awaitTermination()
