import time

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from utils.tencent.cos import create_bucket
from web import models
from web.forms.project import ProjectModelForm


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
                project_dict['star'].append({'value': project, 'type': 'my'})
            else:
                project_dict['my'].append(project)

        join_project_list = models.ProjectUser.objects.filter(  # 保存的是ProjectUser对象
            user=request.tracer.user
        )
        for project_user in join_project_list:
            if project_user.star:
                project_dict['star'].append({'value': project_user.project, 'type': 'my'})
            else:
                project_dict['join'].append(project_user.project)

        form = ProjectModelForm(request)
        return render(request, 'project_list.html', {'form': form, 'project_dict': project_dict})

    # post请求由添加项目的表单通过ajax提交过来
    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        porject_name = form.cleaned_data.get('name')
        # 验证通过: 项目名、颜色、描述 + 创建者（当前登录的用户）
        # 1.为项目创建一个桶
        # 桶名里不能有中文，所以加入项目名称不是好主意
        bucket = '{}-{}-{}'.format(request.tracer.user.mobile_phone,
                                   str(int(time.time())),
                                   settings.COS_BUCKET_NAME_NR
                                   )
        region = settings.COS_REGION
        create_bucket(bucket)

        # 2.创建项目
        form.instance.region = region
        form.instance.bucket = bucket

        # 直接在form实例里添加creator
        form.instance.creator = request.tracer.user

        # 创建项目
        instance = form.save()

        # 3.项目初始化问题类型
        issues_type_object_list = []
        for item in models.IssuesType.PROJECT_INIT_LIST:  # ['任务', '功能', 'Bug']
            issues_type_object_list.append(models.IssuesType(project=instance, title=item))
        models.IssuesType.objects.bulk_create(issues_type_object_list)

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


def project_unstar(request, project_type, project_id):
    """ 取消星标项目 """
    if project_type == 'my':
        models.Project.objects.filter(
            id=project_id,
            creator=request.tracer.user  # 确保是用户本人操作自己的项目
        ).update(star=False)
        return redirect('project_list')
    if project_type == 'join':
        models.ProjectUser.objects.filter(
            project_id=project_id,
            user=request.tracer.user,  # 确保是我参与的项目
        ).update(star=False)
        return redirect('project_list')

    return HttpResponse("请求错误")
