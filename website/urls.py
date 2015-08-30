from django.conf.urls import patterns, url, include
import website.views

urlpatterns = patterns('website.views',
                       url(r'^$', 'index', name='website_index'),
                       url(r'^project/(?P<project_name>[\w.]+)/$', 'project_page', name='project_page'),
                       url(r'^project/(?P<project_name>[\w.]+)/(?P<file_name>[\w.]+)$', 'file_page', name='file_page'),
                       url(r'^message/(?P<id>.+)$', 'message', name='message_detail'),
)
