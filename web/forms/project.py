from django import forms
from django.core.exceptions import ValidationError
from web.forms.bootstrap import BootstrapForm
from web.forms.widgets import ColorRadioSelect
from web import models


class ProjectModelForm(BootstrapForm, forms.ModelForm):
    # desc = forms.CharField(widget=forms.Textarea(attrs={'xx': 123})) # 让CharField用上Textarea的样式（大输入框）
    bootstrap_class_exclude = ['color']  # 覆写父类的空列表，在这个列表里的字段不应用bootstrap样式

    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']
        # 批量重写字段的插件
        widgets = {
            'desc': forms.Textarea(attrs={'xx': 123}),  # attrs按需添加
            'color': ColorRadioSelect(attrs={'class': 'color-radio'}),  # 把下拉框变成Radio选择框，并加入css样式color-radio
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_name(self):
        """ 项目校验 """
        # 1. 当前用户是否已经创建过此项目
        name = self.cleaned_data['name']
        exists = models.Project.objects.filter(name=name, creator=self.request.tracer.user).exists()

        if exists:
            raise ValidationError("您已经创建过该项目")

        # 2. 当前用户是否还有额度创建此项目
        max_count = self.request.tracer.price_policy.project_num

        # 当前用户已经创建过count个项目
        count = models.Project.objects.filter(creator=self.request.tracer.user).count()

        if count >= max_count:
            raise ValidationError("项目数量超过限制，请购买vip获得更多项目额度")

        return name
