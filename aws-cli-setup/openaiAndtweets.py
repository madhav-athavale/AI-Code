

#The code uses tweets from a flat file and openai chatGPT to determine stock sentiment to TSLA. It can be used for any stock ticker
# Please note that my Twitter API - using tweepy - has stopped working for some reason. Waiting for an answer from Twitter support.
# Periodically Open AI becomes vey slow. That is why I am processing only 5 tweets. This number can be changed.
#I have attempted to use muli threading to improve performance.


import openai
import pandas as pd
import numpy as np
import concurrent.futures
import threading

sentiment = {'Positive': 0, "Negative": 0, "Neutral": 0}
sem_object = threading.Semaphore(2)


def setup():
    df = pd.read_csv('data/tweets-labeled.csv', sep=';', usecols=[0, 2])
    openai.api_key = 'XXXXXXXXX'  #open AI key
    model_engine = "text-davinci-003"
    df = df.drop('id', axis=1)
    df = df[df['text'].str.contains("TSLA")]
    return df


def getResponse(resp):
    global sentiment
    print(resp)
    if resp.strip() == "Positive":
        sentiment["Positive"] = sentiment["Positive"] + 1
    if resp.strip() == "Negative":
        sentiment["Negative"] = sentiment["Negative"] + 1


def getSentimentForATweet(tweet):
    model_engine = "text-davinci-003"
    global sem_object

    sem_object.acquire()
    prompt = "Positive or Negative? "
    prompt = prompt + tweet
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=10,
        n=1,
        stop=None,
        temperature=0.5, )
    getResponse(completion.choices[0].text)
    sem_object.release()

def submitWorker(row, pool):
    pool.submit(getSentimentForATweet(row.text));


def getSentiments(df):
    i = 0
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)

    for index, row in df.iterrows():
        submitWorker(row, pool)
        if i > 5:
            break
        i += 1

    pool.shutdown(wait=True)
    pool.join()



if __name__ == "__main__":

    df = setup()
   # global sentiment
    try:
        getSentiments(df)
        print(" Positive : " + str(sentiment["Positive"]))
        print(" Negative : " + str(sentiment["Negative"]))
    except Exception as e:
        print("Error : ", e)
