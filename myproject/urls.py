"""cs_411 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup', 'cs411.views.signup'),
    url(r'^data', 'cs411.views.get_data'),
    url(r'^login','cs411.views.log'),
    url(r'^logout','cs411.views.logout'),
    url(r'^verify','cs411.views.login'),
    url(r'^index','cs411.views._ini_'),
    url(r'^test','cs411.views.searchresult_name'),
    url(r'^delete','cs411.views.deleteby_name'),
    url(r'^add','cs411.views.add_page'),
    url(r'^update','cs411.views.update_render'),
    url(r'^_update','cs411.views.update'),
    url(r'^pictureadd','cs411.views.picture_add'),
    url(r'^detail','cs411.views.detail'),
    url(r'^like','cs411.views.like'),
    url(r'^dislike','cs411.views.dislike'),
    url(r'^profile','cs411.views.profile'),
    url(r'^rank','cs411.views.ranking'),
    url(r'^contact','cs411.views.contact'),



] + staticfiles_urlpatterns()
