from django import forms
from django.core.exceptions import ValidationError

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
