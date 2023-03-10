# -*- coding: utf-8 -*-
"""count_words.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NwJj18AVExlutgas6jAsKjq4ZL3SD7y8

# Prepared By: Taghreed Alghamdi 
Big Data Technologies
 Twitter Sentiment Analysis
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install pyspark

from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import Tokenizer,StopWordsRemover,CountVectorizer,IDF,StringIndexer
from pyspark.ml import Pipeline 
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
import pyspark.sql.functions as f

spark = SparkSession.builder.getOrCreate()

import pyspark.sql.functions as f
df = spark.read.csv('/content/drive/MyDrive/train_arabic_tweets.tsv', sep='\t', encoding='utf-8', header=False).toDF('sentiment', 'tweet' )
df.head()

ar_stop_list = open("/content/drive/MyDrive/arabic_stopwords.txt", encoding="utf-8")
stop_words = ar_stop_list.read().split('\n')
print(stop_words)

tokenizer = Tokenizer(inputCol='tweet',outputCol='words_token')
tokenized = tokenizer.transform(df).select('sentiment','words_token')

stopwords_remover = StopWordsRemover(inputCol='words_token',outputCol='words_clean').setStopWords(stop_words)

data_clean = stopwords_remover.transform(tokenized).select('sentiment', 'words_clean')
data_clean.show()

pos_tweets = data_clean[df["sentiment"] == 'pos']
pos_tweets.show()

print('Top 50 Frequent of Positive')
pos_tweets = pos_tweets.withColumn('word', f.explode(f.col('words_clean'))) \
  .groupBy('word') \
  .count()\
  .sort('count', ascending=False) \

pos_tweets.show(50)

neg_tweets = data_clean[df["sentiment"] == 'neg']
neg_tweets.show()

print('Top 50 Frequent of Negative')
neg_tweets = neg_tweets.withColumn('word', f.explode(f.col('words_clean'))) \
  .groupBy('word') \
  .count()\
  .sort('count', ascending=False) \

neg_tweets.show(50)
