from django.urls import include,path, re_path
from posts import views, utils

subscribe_patterns = [
    path('send_confirm_mail/', views.send_confirmation_mail, name='send-confirm-mail'),
    path('confirm_subscriber/<str:user_mail_hash>', views.confirm_subscriber, name='confirm-subscriber'),
    path('modify_subscription/<str:user_mail_hash>', views.modify_subscription, name='modify-subscription'),
    path('unsubscribe/<str:user_mail_hash>', views.unsubscribe, name='unsubscribe')
]

user_patterns = [
    path('register/', views.register_user, name='register-user'),
    path('login/', views.login_user, name='login-user'),
]

urlpatterns = [
    path('', views.home, name='home'),
    path('subscribe/', include(subscribe_patterns)),
    path('user/', include(user_patterns)),
    re_path(r'^(?P<year>[0-9]{4})/$', views.year_archive, name='year-archive'),
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive, name='month-archive'),
    re_path(r'^tags/(?P<tag>[-\w]+)/$', views.tag_archive, name='tag-archive'),
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[-\w]+)/$', views.post_detail, name='post-detail'),
]
