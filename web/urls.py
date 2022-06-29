# 路由划分
from django.conf.urls import url
from web.views import account

urlpatterns = [
    url(r'^register/$', account.register, name='register'),  # name可以方便反向解析
    url(r'^send/sms/$', account.send_sms, name='send_sms'),  # 反向解析：在前端url里：'{% url "send_sms" %}'

]
