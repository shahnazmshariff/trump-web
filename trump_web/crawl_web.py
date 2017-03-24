# -*- coding: utf-8 -*-

# import mechanize
from bs4 import BeautifulSoup
import requests
import re
import json
import logging
import datetime
from datetime import datetime,timezone
import dateparser
djangologger = logging.getLogger('django')

def unescape(s):
   s = s.replace("&lt;", "<")
   s = s.replace("&gt;", ">")
   s = s.replace("&amp;", "&")
   return s

def get_desc_of_article(contents):
    soup = BeautifulSoup(contents,'html')
    for tag in soup.find_all("meta"):
        attributes_meta_tag = tag.attrs
        for key,val in attributes_meta_tag.items():
            if attributes_meta_tag[key] == "description":
                desc = attributes_meta_tag["content"]
                desc = unescape(desc)
                return desc

def get_time_since_tweet(total_sec):
    if total_sec>60:
        total_min = int(total_sec/60)
        if total_min>60:
            total_hr = int(total_min/60)
            if total_hr>24:
                total_days = int(total_hr/24)
                if total_days == 1:
                     sincewhen = str(total_days) + " day ago"
                else:
                    sincewhen = str(total_days) + " days ago"
            else:
                sincewhen = str(total_hr) + " hours ago"
        else:
            sincewhen = str(total_min) + " mins ago"
    else:
        sincewhen = str(total_sec) + " secs ago"
    if total_min == 1:
        sincewhen = str(total_min) + " min ago"
    if total_hr == 1:
        sincewhen = str(total_hr) + " hour ago"
    return sincewhen

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
                    parsed_date = dateparser.parse(url.publication_date.string)
                    final_date = parsed_date.strftime('%b %d %Y %I:%M %p')
                    new_article = {"title": url.title.string,"link":url.loc.string,"img_url":url.image.string,"desc":desc,"date":final_date}
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
        try:
            link = re.search("(?P<url>https?://[^\s]+)", json_result["statuses"][i]["text"]).group("url")
        except:
            link = None
        if "retweeted_status" not in json_result["statuses"][i]:
            retweeted_status = False
        else:
            retweeted_status = True
        created_at = json_result["statuses"][i]["created_at"]
        tweet_date = dateparser.parse(created_at[:-5])
        date_now = datetime.now(timezone.utc)
        time_delta = date_now - tweet_date
        total_sec = time_delta.total_seconds()
        sincewhen = get_time_since_tweet(total_sec)
        fav_count = json_result["statuses"][i]["favorite_count"]
        retweet_count = json_result["statuses"][i]["retweet_count"]
        tweet = unescape(json_result["statuses"][i]["text"])
        new_tweet = {"text": tweet ,"link":link,"time":sincewhen,"fav":fav_count,
        "retweet":retweet_count,"retweeted_status":retweeted_status}
        all_tweets.append(new_tweet)
    if len(all_tweets) > 25:
        return(all_tweets[0:25])
    else:
        return(all_tweets)


