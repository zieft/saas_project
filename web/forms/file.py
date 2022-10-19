from django import forms
from django.core.exceptions import ValidationError

from utils.tencent.cos import check_file
from web import models
from web.forms.bootstrap import BootstrapForm


class FolderModelForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = models.FileRepository
        fields = ['name']

    def __init__(self, request, parent_object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.parent_object = parent_object

    def clean_name(self):
        name = self.cleaned_data.get('name')

        # 判断数据库里，当前目录下，此文件夹是否已经存在
        queryset = models.FileRepository.objects.filter(file_type=2, name=name, project=self.request.tracer.project)
        if self.parent_object:
            exists = queryset.filter(parent=self.parent_object).exists()
        else:
            exists = queryset.filter(parent__isnull=True)

        if exists:
            raise ValidationError('文件夹已存在')

        return name


class FileModelForm(forms.ModelForm):
    etag = forms.CharField(label='ETag')

    class Meta:
        model = models.FileRepository
        exclude = ['project', 'file_type', 'update_user', 'update_datetime']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_file_path(self):
        return 'https://{}'.format(self.cleaned_data['file_path'])

    def clean(self):
        """
        这个校验主要是防止恶意用户利用post请求不上传文件就往数据库里写东西
        思路就是对比前端发来的写入数据库请求的内容，跟cos里该内容的etag、大小进行比对，结果一致说明用户确实在上传文件，比对不一致，
        则说明要么上传过程中出现了问题，要么该用户就在搞事情。
        """
        key = self.cleaned_data['key']
        etag = self.cleaned_data['etag']
        size = self.cleaned_data['file_size']
        # 向COS校验文件是否合法

        if not key or not etag:
            # 为空表示校验没通过
            return self.cleaned_data

        from qcloud_cos.cos_exception import CosServiceError
        try:
            response = check_file(
                bucket=self.request.tracer.project.bucket,
                region=self.request.tracer.project.region,
                key=key
            )
        except CosServiceError as e:
            self.add_error(key, '文件不存在')
            return self.cleaned_data

        cos_etag = response.get('etag')
        if etag != cos_etag:
            self.add_error('etag', 'ETag异常')
        cos_length = response.get('Content-Length')
        if int(cos_length) != size:
            self.add_error('size', '文件大小错误')

        return self.cleaned_data
