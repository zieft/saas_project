# 路由划分
from django.conf.urls import url
from web.views import account, home, project

urlpatterns = [
    url(r'^register/$', account.register, name='register'),  # name可以方便反向解析
    url(r'^login/sms/$', account.login_sms, name='login_sms'),
    url(r'^login/$', account.login, name='login'),
    url(r'^logout/$', account.logout, name='logout'),
    url(r'^image/code/$', account.image_code, name='image_code'),
    url(r'^send/sms/$', account.send_sms_fake, name='send_sms'),
    url(r'^index/$', home.index, name='index'),

    url(r'^project/list/$', project.project_list, name='project_list'),
    # project_type: {'my', 'join'}
    # eg.: /project/start/join/12/
    url(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_star, name='project_star'),

]
