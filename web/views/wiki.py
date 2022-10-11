from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from utils.encrypt import uid
from utils.tencent.cos import upload_file
from web import models
from web.forms.wiki import WikiModelForm


def wiki(request, project_id):
    """ wiki 首页的展示"""
    wiki_id = request.GET.get('wiki_id')  # wiki_id有值，表示用户请求查看文章详细内容
    # 用户可能在url给wiki_id传入非数字的字符，导致后端无法查询，所以要判断wiki_id是不是数

    if not wiki_id or not wiki_id.isdecimal():
        return render(request, 'wiki.html')

    wiki_object = models.Wiki.objects.filter(id=wiki_id, project_id=project_id).first()

    return render(request, 'wiki.html', {'wiki_object': wiki_object})


def wiki_add(request, project_id):
    """ 添加文章 """
    if request.method == 'GET':  # 用户访问页面
        form = WikiModelForm(request)
        return render(request, 'wiki_form.html', {'form': form})

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

    return render(request, 'wiki_form.html', {'form': form})  # 验证不通过，显示错误信息


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


# def wiki_detail(request, project_id):
#     """ 查看文章详情 /detail?wiki_id=1, 2, 3..."""
#     return HttpResponse('查看文章详细')

def wiki_delete(request, project_id, wiki_id):
    """ 删除当前文章 """
    # 一定也要按文章id查询，这样就不会通过url删除别人的文章
    models.Wiki.objects.filter(project_id=project_id, id=wiki_id).delete()
    url = reverse('wiki', kwargs={'project_id': project_id})
    return redirect(url)


def wiki_edit(request, project_id, wiki_id):
    """ 编辑文章 """

    wiki_object = models.Wiki.objects.filter(project_id=project_id, id=wiki_id).first()
    if not wiki_object:
        url = reverse('wiki', kwargs={'project_id': project_id})
        return redirect(url)
    if request.method == 'GET':
        form = WikiModelForm(request, instance=wiki_object)
        return render(request, 'wiki_form.html', {'form': form})

    form = WikiModelForm(request, data=request.POST, instance=wiki_object)
    if form.is_valid():
        if form.instance.parent:  # 如果存在父文章
            form.instance.depth = form.instance.parent.depth + 1
        else:  # 不存在父文章
            form.instance.depth = 1
        form.instance.project = request.tracer.project  # 这一项不是用户填写的，因此需要手动地添加
        form.save()
        # return redirect('wiki') # 这里只写wiki不行，因为需要提供项目的id
        url = reverse('wiki', kwargs={'project_id': project_id})
        preview_url = "{0}?wiki_id={1}".format(url, wiki_id)  # 跳转到当前文章

        return redirect(preview_url)
    return render(request, 'wiki_form.html', {'form': form})


@csrf_exempt  # 此装饰器将免除本视图函数的csrf认证
def wiki_upload(request, project_id):
    """ Markdown插件上传图片 """

    image_object = request.FILES.get('editormd-image-file')

    # 为了防止桶内文件名重复，先给文件改个名
    ext = image_object.name.rsplit('.')[-1]  # 获取上传文件的后缀名
    key = "{}.{}".format(uid(request.tracer.user.mobile_phone), ext)  # 上传到bucket里的名称

    image_url = upload_file(
        request.tracer.project.bucket,
        request.tracer.project.region,
        image_object,
        key
    )

    # 上传结果通知给markdown组件的固定格式
    result = {
        'success': 1,
        'message': None,
        'url': image_url
    }

    return JsonResponse(result)
