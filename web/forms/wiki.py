from django import forms

from web import models
from web.forms.bootstrap import BootstrapForm


class WikiModelForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = models.Wiki
        exclude = ['project', 'depth']  # 不在前端显示的字段

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 找到想要显示的字段，把它绑定的显示数据给重写
        total_data_list = [("", '请选择'), ]  # 提供“未选择父类”时，应有的选项
        total_data_list.extend(models.Wiki.objects.filter(project=request.tracer.project).values_list('id', 'title'))
        self.fields['parent'].choices = total_data_list  # 格式是[(1, "xx"), (2, "xxx")]
