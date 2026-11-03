
# The code uses tweets from a flat file and openai chatGPT to determine stock sentiment to TSLA. It can be used for any stock ticker
# Please note that my Twitter API - using tweepy - has stopped working for some reason. Waiting for an answer from Twitter support.
# Periodically Open AI becomes vey slow. That is why I am processing only 5 tweets. This number can be changed.
# I have attempted to use muli threading to improve performance.


import bard
import pandas as pd
import numpy as np

bard = bard.Bard()

df = pd.read_csv('data/tweets-labeled.csv', sep=';', usecols=[0, 2])

df = df.drop('id', axis=1)
df = df[df['text'].str.contains("TSLA")]
prompt = "Positive or Negative? "
prompt = prompt + df[0]
resp = bard.generate(prompt)
print(resp)

