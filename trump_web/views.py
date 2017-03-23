from django.shortcuts import render
from django.http import HttpResponse
from trump_web.crawl_web import crawl_cnn,crawl_twitter
# Create your views here.


def web_contents_view(request):
    cnn_contents = crawl_cnn('http://edition.cnn.com/sitemaps/sitemap-news.xml')
    twitter_contents = crawl_twitter('https://api.twitter.com/1.1/search/tweets.json?q=from%3ArealDonaldTrump&count=75')
    return render(request,'index.html',{'news':cnn_contents,'tweets':twitter_contents})
    # return HttpResponse(cnn_contents,content_type = "application/json")