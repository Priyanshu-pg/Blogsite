from django.urls import path, re_path
from posts import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^(?P<year>[0-9]{4})/$', views.year_archive, name='year-archive'),
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive, name='month-archive'),
    re_path(r'^tags/(?P<tag>[-\w]+)/$', views.tag_archive, name='tag-archive'),
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[-\w]+)/$', views.post_detail, name='post-detail'),
]
