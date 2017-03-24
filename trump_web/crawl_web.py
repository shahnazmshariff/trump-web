# -*- coding: utf-8 -*-

# import mechanize
from bs4 import BeautifulSoup
import requests
import re
import json
import logging
djangologger = logging.getLogger('django')

def get_desc_of_article(contents):
    soup = BeautifulSoup(contents,'html')
    for tag in soup.find_all("meta"):
        attributes_meta_tag = tag.attrs
        for key,val in attributes_meta_tag.items():
            if attributes_meta_tag[key] == "description":
                desc = attributes_meta_tag["content"]
                return desc

def crawl_cnn(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.content, 'xml')

    all_articles = []
    # new_article = {}
    for url in soup.find_all("url"):
        if len(all_articles)<25:
            try:
                if "Trump" in url.title.string and url.loc.string is not None:
                    get_article = requests.get(url.loc.string)
                    contents = get_article.content
                    desc = get_desc_of_article(contents)
                    # if(len(desc)>150):
                    #     desc = desc[0:150]
                    new_article = {"title": url.title.string,"link":url.loc.string,"img_url":url.image.string,"desc":desc}
                    all_articles.append(new_article)
            except Exception as e:
                djangologger.error(str(e) + "Error in parsing cnn content")
        else:
            break
    return(all_articles)

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



