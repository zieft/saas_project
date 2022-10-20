from django.shortcuts import render


def setting(request, project_id):
    return render(request, 'setting.html')


def setting_delete(request, project_id):
    if request.method == 'GET':
        return render(request, 'setting_delete.html')

    project_name = request.POST.get('project_name')
    if not project_name or project_name != request.tracer.project.name:
        return render(request, 'setting_delete.html', {'error': '项目名称错误'})

    # 项目名称正确，删除项目
    if request.tracer.user != request.tracer.project.creator:
        # 确保只有项目的创建者才可删除项目
        return render(request, 'setting_delete.html', {'error': '只有项目创建者可删除项目'})

    # 1. 删除桶
    # 1.1 删除桶中的文件： 找到并删除
    # 1.2 删除桶中的所有碎片
    # 1.3 删除桶
    # 2. 删除项目
