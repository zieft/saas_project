from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from web.forms.project import ProjectModelForm
from web import models


def project_list(request):
    """ 项目列表 """
    if request.method == 'GET':  # 有网址直接访问，展示项目
        """
        1. 从数据库中获取两个部分数据
            我创建的所有项目：已星标、未星标
            我参与的所有项目：已星标、未星标
        2. 循环两个列表，提取所有已星标的项目
        
        得到三个列表：星标、创建、参与
        """
        project_dict = {'star': [], 'my': [], 'join': []}

        my_project_list = models.Project.objects.filter(  # 保存的是Project对象
            creator=request.tracer.user
        )
        for project in my_project_list:
            if project.star:
                project_dict['star'].append(project)
            else:
                project_dict['my'].append(project)

        join_project_list = models.ProjectUser.objects.filter(  # 保存的是ProjectUser对象
            user=request.tracer.user
        )
        for project_user in join_project_list:
            if project_user.star:
                project_dict['star'].append(project_user.project)
            else:
                project_dict['join'].append(project_user.project)

        form = ProjectModelForm(request)
        return render(request, 'project_list.html', {'form': form, 'project_dict': project_dict})

    # post请求由添加项目的表单通过ajax提交过来
    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        # 验证通过: 项目名、颜色、描述 + 创建者（当前登录的用户）
        form.instance.creator = request.tracer.user  # 直接在form实例里添加creator

        # 创建项目
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def project_star(request, project_type, project_id):
    """ 星标项目 """
    if project_type == 'my':
        models.Project.objects.filter(
            id=project_id,
            creator=request.tracer.user  # 确保是用户本人操作自己的项目
        ).update(star=True)
        return redirect('project_list')
    if project_type == 'join':
        models.ProjectUser.objects.filter(
            project_id=project_id,
            user=request.tracer.user,  # 确保是我参与的项目
        ).update(star=True)
        return redirect('project_list')

    return HttpResponse("请求错误")
