from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, monotonically_increasing_id
from pyspark.sql.types import IntegerType, StringType, StructType, StructField,FloatType


def create_spark_session():
    """
    Create a Spark session.
    """
    spark = SparkSession.builder \
        .appName("Movies") \
        .master("local[*]") \
        .config('spark.sql.shuffle.partitions', 2) \
        .config('spark.sql.warehouse.dir', 'hdfs://node1:8020/user/hive/warehouse') \
        .config('hive.metastore.uris', 'thrift://node1:9083') \
        .config("spark.jars", "/usr/share/java/mysql-connector-java.jar") \
        .enableHiveSupport() \
        .getOrCreate()
        
    return spark

spark = create_spark_session()

schema = StructType().add("movieId", IntegerType(), True)\
.add("movie_name", StringType(), True)\
.add("movie_tag", StringType(), True)\
.add("movie_country", StringType(), True)\
.add("movie_length", IntegerType(), True)\
.add("movie_release", StringType(), True)\
.add("movie_rate", IntegerType(), True)\
.add("movie_summary", StringType(), True)\
.add("movie_director", StringType(), True)\
.add("movie_actor", StringType(), True)\
.add("movie_rank", StringType(), True)\
.add("movie_firtweek_ticket", StringType(), True)\
.add("movie_all_ticket", StringType(), True)\


df = spark.read.format("csv")\
.option("header", "true")\
.option("sep", ",")\
.option("encoding", "UTF-8")\
.schema(schema=schema)\
.load("movieFeature.csv")

df = df.withColumn("movieId", monotonically_increasing_id())

df.write.mode("overwrite").\
format("jdbc").\
option("url", "jdbc:mysql://node1:3306/movies").\
option("dbtable", "movieData").\
option("user", "root").\
option("password", "sakura0113").\
option("driver", "com.mysql.cj.jdbc.Driver").\
option("encoding", "UTF-8").\
save()

df.write.mode("overwrite").saveAsTable("default.moviedata", format="parquet")
spark.sql("USE default")
spark.sql("SHOW TABLES").show()
spark.sql("select * from movieData").show()
