from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Criar sessão Spark
spark = SparkSession.builder.appName("ExtratoFinanceiro").getOrCreate()

# 2. Carregar o Excel (via pandas e converter para Spark)
caminho_excel = "/home/coyas/Documents/softwares/python/DataScience/archives/coyasCaixacv_transactions-20250616.xls"
df_excel = pd.read_excel(caminho_excel) 
df_spark = spark.createDataFrame(df_excel)

# 3. Corrigir datas
df_spark = df_spark.withColumn("Data Efetiva", to_date(col("Data Efetiva"), "dd-MM-yyyy"))

# 4. Converter valores para float (caso necessário)
df_spark = df_spark.withColumn("Valor", col("Valor").cast("float"))
df_spark = df_spark.withColumn("Saldo Após", col("Saldo Após").cast("float"))

# 5. Agrupar por descrição
df_agrupado = df_spark.groupBy("Descrição").sum("Valor")

# 6. Converter para Pandas para visualização
df_pandas = df_spark.toPandas()
df_agrupado_pandas = df_agrupado.toPandas()

# 7. Gráfico de saldo ao longo do tempo
plt.figure(figsize=(10,5))
sns.lineplot(data=df_pandas.sort_values("Data Efetiva"), x="Data Efetiva", y="Saldo Após", marker="o")
plt.title("Evolução do Saldo ao Longo do Tempo")
plt.xlabel("Data")
plt.ylabel("Saldo Após (CVE)")
plt.grid(True)
plt.tight_layout()
plt.show()

# 8. Gráfico de barras por descrição
plt.figure(figsize=(10,5))
sns.barplot(data=df_agrupado_pandas.sort_values("sum(Valor)", ascending=False), x="Descrição", y="sum(Valor)")
plt.title("Total por Descrição")
plt.xlabel("Descrição")
plt.ylabel("Valor Total (CVE)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# 9. Encerrar sessão Spark
# spark.stop()