from django.urls import include,path, re_path
from posts import views, utils

subscribe_patterns = [
    path('resend_confirm_mail/', views.resend_confirmation_mail, name='resend-confirm-mail'),
    path('confirm_subscriber/<str:usermail>', views.confirm_subscriber, name='confirm-subscriber')
]

urlpatterns = [
    path('', views.home, name='home'),
    path('subscribe/', include(subscribe_patterns)),
    re_path(r'^(?P<year>[0-9]{4})/$', views.year_archive, name='year-archive'),
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive, name='month-archive'),
    re_path(r'^tags/(?P<tag>[-\w]+)/$', views.tag_archive, name='tag-archive'),
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[-\w]+)/$', views.post_detail, name='post-detail'),
]
