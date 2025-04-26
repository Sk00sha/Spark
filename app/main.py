from pyspark.sql import SparkSession
from pyspark.sql.functions import desc, asc
import datetime
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


# Timestamp to create unique output folder
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Start Spark
spark = SparkSession.builder.appName("SimpleSparkJob").getOrCreate()

schema = StructType([
    StructField("seller_id", StringType(), True),
    StructField("seller_zip_code_prefix", IntegerType(), True),
    StructField("seller_city", StringType(), True),
    StructField("seller_state", StringType(), True)
])
# Dummy data
df = spark.read.csv("/app/Dataset/sellers_dataset.csv",header=True,schema=schema)
df_group_by = df.groupBy("seller_city").count().orderBy(desc("count"))

# Output path
out=f"s3a://match-result-test-bucket/run_{timestamp}"

print(f"Writing to: {out}")
df_group_by.write.csv(out, header=True)

spark.stop()
