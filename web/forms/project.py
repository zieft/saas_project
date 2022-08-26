from django import forms
from web.forms.bootstrap import BootstrapForm
from web import models


class ProjectModelForm(BootstrapForm, forms.ModelForm):
    # desc = forms.CharField(widget=forms.Textarea(attrs={'xx': 123})) # 让CharField用上Textarea的样式（大输入框）

    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']
        # 批量重写字段的插件
        widgets = {
            'desc': forms.Textarea(attrs={'xx': 123}),  # attrs按需添加
        }
