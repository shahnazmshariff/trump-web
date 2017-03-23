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
    new_article = {}
    for url in soup.find_all("url"):
            if "Trump" in url.title.string:
                new_article = {"title": url.title.string,"link":url.loc.string,"img_url":url.image.string}
                # new_article["title"] = url.title.string
                # new_article["link"] = url.loc.string
                # new_article["img_url"] = url.image.string
                # all_articles.append(new_article)
    return all_articles[0:25]

# def crawl_twitter(url):

    # link_list = []
    # result = requests.get(url)
    # soup = BeautifulSoup(result.content,"html.parser")
    # for h3tag in soup.find_all("h3",re.compile("cd__headline")):
    #     for atag in h3tag.find_all(re.compile("^a")):
    #         link_list.append(atag)
    # return link_list

# for tag in soup.find_all("div", re.compile("ksoContent")):
#     for tag1 in tag.find_all(re.compile("^p")):

        # # print tag1.text
        # tag1 = tag1.text.decode('unicode-escape');
        # # print tag1.string
        # print
        # tag1
        # lang = guess_language.guessLanguageName(tag1)
        # print
        # lang
        # if lang == 'English' or lang == 'Hindi' or lang == 'Nepali' or lang == 'Tamil' or lang == 'Telugu' or lang == 'Punjabi' or lang == 'Malayalam' or lang == 'Marathi' or lang == 'Gujarati' or lang == 'Bengali':
        #     ans = "known"
        # else:
        #     ans = "unknown"
        # with open("post_shahnaz.json", "a") as outfile:
        #     json.dump({'post': tag1, 'language': lang, 'type': ans}, outfile, sort_keys=False)
        #     outfile.write('\n')