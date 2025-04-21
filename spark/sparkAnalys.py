from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, monotonically_increasing_id
from pyspark.sql.types import IntegerType, StringType, StructType, StructField, FloatType
from pyspark.sql.functions import count,min,mean,col,sum,when,max,min,avg,explode,split,row_number,year,month
from pyspark.sql.window import Window

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

#创建session
spark = create_spark_session()

#读取电影文件
catMovieData = spark.read.table('movieData')


# """
# 标签统计
# """
explode_df = catMovieData.withColumn('movie_tag',explode(split(col('movie_tag'),'-')))
result1 = explode_df.groupby('movie_tag').agg(count('movie_tag').alias('tag_count'))

result1.write.mode("overwrite").\
format("jdbc").\
option("url", "jdbc:mysql://node1:3306/movies").\
option("dbtable", "movieTagCount").\
option("user", "root").\
option("password", "sakura0113").\
option("driver", "com.mysql.cj.jdbc.Driver").\
option("encoding", "UTF-8").\
save()

result1.write.mode("overwrite").\
saveAsTable("movieTagCount",format="parquet",)
spark.sql("select * from movieTagCount").show()

def saveTable(result,tableName):
    print(f'Saving {tableName}')
    result.write.mode("overwrite"). \
        format("jdbc"). \
        option("url", "jdbc:mysql://node1:3306/movies"). \
        option("dbtable", f"{tableName}"). \
        option("user", "root"). \
        option("password", "sakura0113"). \
        option("driver", "com.mysql.cj.jdbc.Driver"). \
        option("encoding", "UTF-8"). \
        save()

    result.write.mode("overwrite"). \
        saveAsTable(f"{tableName}", format="parquet", )
    spark.sql(f"select * from {tableName}").show()



"""
票房统计
"""
# 如果列中有非数字（如 "Unknown" 或空值），可以先过滤：
df_clean = catMovieData.filter(
    col("movie_all_ticket").rlike("^\\d+$"),
)
df_numeric = df_clean.withColumn(
    "movie_all_ticket_num",
    col("movie_all_ticket").cast("integer")
)

sort_df = df_numeric.orderBy(col("movie_all_ticket_num").desc())
sort_df.show()
result2 = sort_df.limit(10)
saveTable(result2,"ticketTopMovie")


# """
# 种类票房统计
# """
df_clean = catMovieData.filter(
    col("movie_all_ticket").rlike("^\\d+$"),
).filter(
    col("movie_firtweek_ticket").rlike("^\\d+$"),
)

df_numeric = df_clean.withColumn(
    "movie_all_ticket_num",
    col("movie_all_ticket").cast("integer")
).withColumn(
    "movie_firtweek_ticket_num",
    col("movie_firtweek_ticket").cast("integer")
)

explode_df = df_numeric.withColumn('movie_tag',explode(split(col('movie_tag'),'-')))
result3 = explode_df.groupby(col('movie_tag')).agg(
    max('movie_firtweek_ticket_num').alias('max_movie_firtweek_ticket'),
    max('movie_all_ticket_num').alias('max_movie_all_ticket'),)
saveTable(result3,"typeTopMovie")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""
国家统计
"""
explode_df = catMovieData.withColumn('country', explode(split(col('movie_country'), ',')))
result4 = explode_df.groupby('country').agg(
    count('country').alias('country_count'),
)
saveTable(result4,"countryCount")


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
评分分布
"""
cat_rate_df = catMovieData.withColumn(
    'rateCategory',
    when((col('movie_rate') >= 10) & (col('movie_rate') < 20), '0.5星')
    .when((col('movie_rate') >= 20) & (col('movie_rate') < 30), '1星')
    .when((col('movie_rate') >= 30) & (col('movie_rate') < 40), '1.5星')
    .when((col('movie_rate') >= 40) & (col('movie_rate') < 50), '2星')
    .when((col('movie_rate') >= 50) & (col('movie_rate') < 60), '2.5星')
    .when((col('movie_rate') >= 60) & (col('movie_rate') < 70), '3星')
    .when((col('movie_rate') >= 70) & (col('movie_rate') < 80), '3.5星')
    .when((col('movie_rate') >= 80) & (col('movie_rate') < 90), '4星')
    .when((col('movie_rate') >= 90) & (col('movie_rate') <= 100), '4.5星')
    .otherwise('未知')  # 处理不在上述范围的情况
)
cat_rate_df = cat_rate_df.filter(col('movie_rate') != 0)
result5 = cat_rate_df.groupby(col('rateCategory')).count()

saveTable(result5,"rateCount")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
种类票房Top10
"""
# 如果列中有非数字（如 "Unknown" 或空值），可以先过滤：
df_clean = catMovieData.filter(
    col("movie_all_ticket").rlike("^\\d+$"),
)
df_numeric = df_clean.withColumn(
    "movie_all_ticket_num",
    col("movie_all_ticket").cast("integer")
)
explode_df = df_numeric.withColumn('type',explode(split(col('movie_tag'),'-')))
group_df = explode_df.groupby('type','movie_name').agg({'movie_all_ticket':'sum'}).withColumnRenamed('sum(movie_all_ticket)','movie_all_ticket')

window = Window.partitionBy('type').orderBy(col('movie_all_ticket').desc())
rank = group_df.withColumn('rank',row_number().over(window))
result6 = rank.filter(col('rank') <= 10).drop(col('rank'))
saveTable(result6,"perTypeTickets")




""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
种类评分
"""
filter_df = explode_df.filter(col('movie_rate') != 0)
filter_df.groupby('type').agg(mean('movie_rate').alias('mean_typeRate'))
result7 = filter_df.groupby('type').agg(mean('movie_rate').alias('mean_typeRate'))
saveTable(result7,"meanTypeRate")


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
种类时长
"""
result8 = explode_df.groupby('type').agg(mean('movie_length').alias('typeAvgLen'))
saveTable(result8,"avgTypeLen")
