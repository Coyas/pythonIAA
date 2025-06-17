# pip install pyspark openpyxl pandas

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, to_date, sum as spark_sum
import pandas as pd

# === 1. Criar sessão Spark ===
spark = SparkSession.builder \
    .appName("Extrato Financeiro Excel") \
    .config("spark.executor.memory", "2g") \
    .getOrCreate()

# === 2. Carregar Excel com pandas (requer openpyxl) ===
caminho_excel = "/home/coyas/Documents/softwares/python/DataScience/archives/coyasCaixacv_transactions-20250616.xls"
df_excel = pd.read_excel(caminho_excel)

# === 3. Criar DataFrame Spark ===
df_spark = spark.createDataFrame(df_excel)

# === 4. Verificar colunas disponíveis ===
print("Colunas detectadas:")
print(df_spark.columns)

# === 5. Padronizar datas (ajuste os nomes exatos se necessário) ===
df_spark = df_spark.withColumn("Data do Movimento", to_date(col("Data do Movimento"), "dd-MM-yyyy")) \
                   .withColumn("Data Efetiva", to_date(col("Data Efetiva"), "dd-MM-yyyy"))

# === 6. Mostrar primeiros dados ===
df_spark.show(10, truncate=False)

# === 7. Análise de valores ===
df_spark.select(
    spark_sum(when(col("Valor") > 0, col("Valor"))).alias("Total Entradas"),
    spark_sum(when(col("Valor") < 0, col("Valor"))).alias("Total Saídas"),
    spark_sum("Valor").alias("Saldo Final")
).show()

# === 8. Inconsistências: saldo negativo ===
print("⚠️ Dias com saldo negativo:")
df_spark.filter(col("Saldo Após") < 0).show()

# === 9. Exportar resultado em CSV ===
df_spark.write.csv("extrato_processado.csv", header=True, mode="overwrite")

# === 10. Encerrar sessão Spark ===
spark.stop()
