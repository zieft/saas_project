from django.template import Library
from django.urls import reverse

from web import models

register = Library()

"""
inclusion_tag可以封装经常使用到的前端和后端代码块，
前端负责样式和显示的内容，后端负责和数据库进行交流获取需要的数据
"""


@register.inclusion_tag('inclusion/all_project_list.html')
def all_project_list(request):  # 这不是视图函数，所以request参数需要在调用的时候手动传入
    # 1. 获取我创建的所有项目
    my_project_list = models.Project.objects.filter(creator=request.tracer.user)

    # 2. 获取我参与的所有项目
    join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)

    return {'my': my_project_list, 'join': join_project_list}
    # 这里返回的内容可以直接传到上面的html页面


@register.inclusion_tag('inclusion/manage_menu_tag.html')
def manage_menu_list(request):
    data_list = [
        # 下面每一个字典，对应着要在前端<li>标签里使用的内容
        # reverse可以根据url别名，反向解析出url字符串并返回该字符串
        {'title': '概览', 'url': reverse('dashboard', kwargs={'project_id': request.tracer.project.id})},
        {'title': '问题', 'url': reverse('issues', kwargs={'project_id': request.tracer.project.id})},
        {'title': '统计', 'url': reverse('statistics', kwargs={'project_id': request.tracer.project.id})},
        {'title': '文档', 'url': reverse('wiki', kwargs={'project_id': request.tracer.project.id})},
        {'title': '文件', 'url': reverse('file', kwargs={'project_id': request.tracer.project.id})},
        {'title': '设置', 'url': reverse('setting', kwargs={'project_id': request.tracer.project.id})},
    ]

    for item in data_list:
        # 比较item['url']和用户请求的url：request.path_info
        # 如果用户请求url跟当前item的开头相同，比如都是dashboard
        # 则给当前item添加一个class=active的属性
        if request.path_info.startswith(item['url']):
            item['class'] = 'active'  # 给item字典添加一个键值对

    return {'data_list': data_list}
