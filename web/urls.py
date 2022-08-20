# 路由划分
from django.conf.urls import url
from web.views import account

urlpatterns = [
    url(r'^register/$', account.register, name='register'),  # name可以方便反向解析
    url(r'^login/sms/$', account.login_sms, name='login_sms'),
    url(r'^send/sms/$', account.send_sms_fake, name='send_sms')

]
