from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from utils.tencent.cos import delete_file, delete_file_list
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

    fid = request.POST.get('fid', '')  # 修改文件夹名称时，要带着文件夹id，以便知道修改的是数据库中的哪一条
    # edit_object = None
    if fid.isdecimal():  # fid存在，表明用户想要修改文件夹名
        edit_object = models.FileRepository.objects.filter(file_type=2,
                                                           project=request.tracer.project,
                                                           id=int(fid)).first()
        # if edit_object:
        form = FolderModelForm(request, parent_object, data=request.POST, instance=edit_object)
    else:  # fid不存在时，说明用户在新建文件夹
        form = FolderModelForm(request, parent_object, data=request.POST)

    if form.is_valid():
        form.instance.project = request.tracer.project
        form.instance.update_user = request.tracer.user
        form.instance.file_type = 2
        form.instance.parent = parent_object
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({"status": False, 'error': form.errors})


# http://localhost:8000/manage/1/file/delete/?fid=1
def file_delete(request, project_id):
    """ 删除文件 """
    fid = request.GET.get('fid')
    # 两个步骤
    # 删除 数据库中 文件 & 文件夹下面的子文件（夹）。 级联删除
    # 删除cos中对应的文件

    # 去除待删除的对象
    delete_object = models.FileRepository.objects.filter(id=fid, project=request.tracer.project).first()
    # 判断对象是个文件，还是个文件夹
    if delete_object.file_type == 1:  # 要删除的是个文件
        # 删除数据库中的文件记录，cos中的具体文件，项目已使用的空间容量，
        # delete_object.file_size  # 单位：字节

        # 释放当前项目已使用的空间
        request.tracer.project.use_space -= delete_object.file_size
        request.tracer.project.save()

        # cos中删除文件
        delete_file(request.tracer.project.bucket, request.tracer.project.region, delete_object.key)

        # db中删除文件记录
        delete_object.delete()
        return JsonResponse({'status': True})

    else:  # 要删除的是个文件夹
        # 找到文件夹下所有的文件，遍历上边删除文件的过程
        # models.FileRepository.objects.filter(parent=delete_object)
        total_size = 0
        folder_list = [delete_object, ]
        key_list = []  # 用于cos批量删除
        """
        在循环一个列表的过程中，向列表中append新元素，新元素也会被循环到！
        list = [1, ]
        for i in list:
            list.append(i+1)
            print(i)
        上面这个循环是死循环，打印自然数列。
        """
        for folder in folder_list:
            # 拿到当前文件夹下的所有文件及文件夹，并按文件夹在上的顺序排序
            child_list = models.FileRepository.objects.filter(project=request.tracer.project, parent=folder).order_by(
                '-file_type')
            for child in child_list:
                if child.file_type == 2:  # 是文件夹
                    folder_list.append(child)
                else:  # 是文件
                    #  文件大小汇总
                    total_size += child.file_size
                    # 加入到cos待删除文件列表
                    key_list.append({'Key': child.key})  # cos批量删除要求构建成这样

        # cos批量删除
        if key_list:
            delete_file_list(request.tracer.project.bucket, request.tracer.project.region, key_list)

        # 释放容量
        if total_size:
            request.tracer.project.use_space -= total_size
            request.tracer.project.save()

        # 级联删除数据库中的文件记录
        delete_object.delete()
