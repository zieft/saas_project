# 路由划分
from django.conf.urls import url, include

from web.views import account, home, project, manage, wiki

urlpatterns = [
    url(r'^register/$', account.register, name='register'),  # name可以方便反向解析
    url(r'^login/sms/$', account.login_sms, name='login_sms'),
    url(r'^login/$', account.login, name='login'),
    url(r'^logout/$', account.logout, name='logout'),
    url(r'^image/code/$', account.image_code, name='image_code'),
    url(r'^send/sms/$', account.send_sms_fake, name='send_sms'),
    url(r'^index/$', home.index, name='index'),

    # 项目列表
    url(r'^project/list/$', project.project_list, name='project_list'),
    # project_type: {'my', 'join'}
    # eg.: /project/start/join/12/
    url(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_star, name='project_star'),
    url(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_unstar, name='project_unstar'),

    # 项目管理，涉及非常多的路由，因此再做一次路由分发
    # 阅读include()源码，内部参数可以是str（路径），也可以是列表中套这url，跟前面的url做拼接

    url(r'^manage/(?P<project_id>\d+)/', include([
        url(r'^dashboard/$', manage.dashboard, name='dashboard'),
        url(r'^issues/$', manage.issues, name='issues'),
        url(r'^statistics/$', manage.statistics, name='statistics'),
        url(r'^file/$', manage.file, name='file'),
        url(r'^wiki/$', wiki.wiki, name='wiki'),  # 不能在manage.py中导入wiki，要直接从url.py中导入
        url(r'^wiki/add/$', wiki.wiki_add, name='wiki_add'),  # 不能在manage.py中导入wiki，要直接从url.py中导入
        url(r'^wiki/catalog/$', wiki.wiki_catalog, name='wiki_catalog'),  # 不能在manage.py中导入wiki，要直接从url.py中导入
        url(r'^setting/$', manage.setting, name='setting'),
    ])),

]
