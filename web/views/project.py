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
        pass

    return JsonResponse({'status': False, 'error': form.errors})
