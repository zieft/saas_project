from django.shortcuts import render, redirect
from django.urls import reverse

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
        form.instance.project = request.tracer.project  # 这一项不是用户填写的，因此需要手动地添加
        form.save()
        # return redirect('wiki') # 这里只写wiki不行，因为需要提供项目的id
        url = reverse('wiki', kwargs={'project_id': project_id})
        return redirect(url)

    return render(request, 'wiki_add.html', {'form': form})  # 验证不通过，显示错误信息
