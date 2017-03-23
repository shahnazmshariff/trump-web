from django.conf.urls import include, url
from trump_web import views

urlpatterns = [
    url(r'^news', views.web_contents_view, name='trump'),
]