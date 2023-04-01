from django import forms

from web import models
from web.forms.bootstrap import BootstrapForm


class IssuesModelForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = models.Issues
        exclude = ['project', 'creator', 'create_datetime', 'latest_update_datetime']
        widgets = {
            # doc: https://www.bootstrapselect.cn/examples.html
            'assign': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'attention': forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
        }
