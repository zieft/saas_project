from django.template import Library

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
