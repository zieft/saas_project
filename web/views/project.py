from django.shortcuts import render
from web.forms.project import ProjectModelForm
from django.http import JsonResponse


def project_list(request):
    """ 项目列表 """
    if request.method == 'GET':  # 有网址直接访问，展示项目
        form = ProjectModelForm()
        return render(request, 'project_list.html', {'form': form})

    # post请求由添加项目的表单通过ajax提交过来
    form = ProjectModelForm(data=request.POST)
    if form.is_valid():
        # 验证通过: 项目名、颜色、描述 + 创建者（当前登录的用户）
        form.instance.creator = request.tracer.user  # 直接在form实例里添加creator

        # 创建项目
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})
