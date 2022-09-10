from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from web import models
from web.forms.wiki import WikiModelForm


def wiki(request, project_id):
    """ wiki 首页的展示"""
    return render(request, 'wiki.html')


def wiki_add(request, project_id):
    """ 添加文章 """
    if request.method == 'GET':  # 用户访问页面
        form = WikiModelForm(request)
        return render(request, 'wiki_add.html', {'form': form})

    # post，用户提交表单
    form = WikiModelForm(request, data=request.POST)
    if form.is_valid():
        # 为新添加的文章设置深度
        # 判断用户是否已经选择父文章，如果有，则本深度在父文章深度的基础上+1，否则本深度为1
        if form.instance.parent:  # 如果存在父文章
            form.instance.depth = form.instance.parent.depth + 1
        else:  # 不存在父文章
            form.instance.depth = 1
        form.instance.project = request.tracer.project  # 这一项不是用户填写的，因此需要手动地添加
        form.save()
        # return redirect('wiki') # 这里只写wiki不行，因为需要提供项目的id
        url = reverse('wiki', kwargs={'project_id': project_id})
        return redirect(url)

    return render(request, 'wiki_add.html', {'form': form})  # 验证不通过，显示错误信息


def wiki_catalog(request, project_id):
    """ 获取wiki的目录 """
    # 获取当前项目的所有目录: data = QuerySet类型
    # data = models.Wiki.objects.filter(project=request.tracer.project).values_list(
    # 'id', 'title', 'parent_id') # 前端获取id要用item[0]
    # data = models.Wiki.objects.filter(project=request.tracer.project).values('id', 'title',
    #                                                                          'parent_id')  # 前端获取id可以直接item.id
    data = models.Wiki.objects.filter(project=request.tracer.project).values(
        'id', 'title', 'parent_id').order_by('depth', 'id')
    # JsonResponse会调用json.dumps()不能直接处理QuerySet类型，所以要先转换成列表
    return JsonResponse({'status': True, 'data': list(data)})
