from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from web import models
from web.forms.file import FolderModelForm


def file(request, project_id):
    """ 文件列表 & 添加文件夹"""

    # http://localhost:8000/manage/1/file/?folder=2 表示进入了id为9的文件夹内部
    # 判断文件夹是否有父级
    parent_object = None
    folder_id = request.GET.get('folder', '')  # 第二个参数为空字符串，表示如果用户没有传参数进来，folder_id便为空
    if folder_id.isdecimal():  # 判断用户穿的folder参数是十进制的数而非其他非法字符
        parent_object = models.FileRepository.objects.filter(file_type=2,
                                                             project=request.tracer.project,
                                                             id=int(folder_id)).first()  # int确保用户传的参数是整数
    if request.method == 'GET':

        # 导航条
        breadcrumb_list = []
        parent = parent_object
        while parent:
            # breadcrumb_list.insert(0, {'id': parent.id, 'name': parent.name})  # insert(0, ..)在列表开头插入
            breadcrumb_list.insert(0, model_to_dict(parent, ['id', 'name']))  # 与上一行等价
            parent = parent.parent

        # 当前目录下所有的文件 & 文件夹获取到即可
        queryset = models.FileRepository.objects.filter(project=request.tracer.project)

        if parent_object:
            # 进入了某个目录
            file_object_list = queryset.filter(parent=parent_object).order_by('-file_type')  # -表示倒序排序
        else:
            # 处于根目录
            file_object_list = queryset.filter(parent__isnull=True)

        form = FolderModelForm(request, parent_object)
        context = {
            'form': form,
            'file_object_list': file_object_list,
            'breadcrmb_list': breadcrumb_list,
        }
        return render(request, 'file.html', context)

    form = FolderModelForm(request, parent_object, data=request.POST)
    if form.is_valid():
        form.instance.project = request.tracer.project
        form.instance.update_user = request.tracer.user
        form.instance.file_type = 2
        form.instance.parent = parent_object
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({"status": False, 'error': form.errors})
