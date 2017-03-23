# -*- coding: utf-8 -*-

# import mechanize
# import cookielib
from bs4 import BeautifulSoup
import requests
import re
import json

def crawl_cnn(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.content, 'xml')

    all_articles = []
    for url in soup.find_all("url"):
            if "Trump" in url.title.string:
                new_article = {"title": url.title.string,"link":url.loc.string,"img_url":url.image.string}
                all_articles.append(new_article)
    return all_articles[0:25]

def crawl_twitter(url):
    access_token = "AAAAAAAAAAAAAAAAAAAAAJsVzwAAAAAAxBRtCkAUnQPWnjXqhSwDtxDH5I8%3DXIqX8EZwvJoLO5sbjwsecrLeblk65NNGrG9H3WAMReF5WyXk4f"
    get_headers = {"Authorization": 'Bearer '+access_token}
    result = requests.get(url,headers=get_headers)
    json_result = result.json()
    all_tweets = []
    for i in range(len(json_result["statuses"])):
        # check if tweet was by Donald Trump
        if len(json_result["statuses"][i]["entities"]["user_mentions"]) is 0:
            try:
                #Extract link within tweet
                link = re.search("(?P<url>https?://[^\s]+)", json_result["statuses"][i]["text"]).group("url")
            except:
                link = None
            new_tweet = {"text": json_result["statuses"][i]["text"],"link":link}
            all_tweets.append(new_tweet)
    if len(all_tweets) > 25:
        return(all_tweets[0:25])
    else:
        return(all_tweets)
