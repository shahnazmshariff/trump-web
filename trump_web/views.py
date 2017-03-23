from django.shortcuts import render
from django.http import HttpResponse
from trump_web.crawl_web import crawl_cnn
# Create your views here.


def web_contents_view(request):
    cnn_contents = crawl_cnn('http://edition.cnn.com/sitemaps/sitemap-news.xml')
    # return render(request,'index.html',{'news':cnn_contents})
    return HttpResponse(cnn_contents,content_type = "application/json")