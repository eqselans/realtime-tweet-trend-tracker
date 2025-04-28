from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, from_json, window, current_timestamp
from pyspark.sql.types import StructType, StringType, DoubleType,TimestampType, ArrayType

# Spark oturumu
spark = SparkSession.builder \
    .appName("TrendingWords") \
    .getOrCreate()

# Kafka JSON veri şeması
schema = StructType() \
    .add("user", StringType()) \
    .add("text", StringType()) \
    .add("timestamp", TimestampType()) \
    .add("hashtags", ArrayType(StringType())) \
    .add("likes", StringType()) \
    .add("retweets", StringType())

# Kafka'dan veriyi oku
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "tweets") \
    .option("startingOffsets", "earliest") \
    .option("kafka.group.id", "spark-streaming-consumer") \
    .load()

# Kafka verisini JSON'a parse et
# value
# value kafka'dan gelen veridir ve JSON formatında olduğu varsayılmaktadır.
# Bu nedenle, value'yu JSON formatına dönüştürmek için from_json fonksiyonunu kullanıyoruz.
# from_json fonksiyonundan çıktıyı "data" adında bir alias ile alıyoruz.
# Ardından, JSON'dan "text" ve "timestamp" alanlarını alıyoruz
# ve timestamp'ı güncel zamanla değiştiriyoruz.
df_json = df_raw.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.hashtags", current_timestamp().alias("timestamp"))


# split fonksiyonu, metni boşluk karakterine göre böler ve her kelimeyi ayrı bir satıra yerleştirir.
# explode fonksiyonu, bu kelimeleri ayrı satırlara dönüştürür.
# Kelimeleri ayırdıktan sonra, timestamp'ı da alıyoruz.
# Bu sayede, her kelimenin hangi zaman diliminde geçtiğini görebiliyoruz.

# words = df_json.select(
#     explode(split(col("text"), "\s+")).alias("word"),
#     col("timestamp")
# )

hashtags = df_json.select(
    explode(col("hashtags")).alias("hashtag"),
    col("timestamp")
)

# Watermark ve pencere ile grupla (10 saniyelik pencere örneği)
# word_counts = words \
#     .withWatermark("timestamp", "10 seconds") \
#     .groupBy(
#         window(col("timestamp"), "10 seconds"),
#         col("word")
#     ).count()
    
hashtag_counts = hashtags \
    .withWatermark("timestamp", "10 seconds") \
    .groupBy(
        window(col("timestamp"), "10 seconds"),
        col("hashtag")
    ).count()

# Sonucu console'a yaz
# query = word_counts.writeStream \
#     .outputMode("append") \
#     .format("parquet") \
#     .option("path", "/app/output") \
#     .option("checkpointLocation", "/app/checkpoint") \
#     .trigger(processingTime="10 seconds") \
#     .start()

query = hashtag_counts.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "/app/output") \
    .option("checkpointLocation", "/app/checkpoint") \
    .trigger(processingTime="10 seconds") \
    .start()



query.awaitTermination()
