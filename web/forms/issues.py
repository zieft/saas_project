from django import forms

from web import models
from web.forms.bootstrap import BootstrapForm


class IssuesModelForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = models.Issues
        exclude = ['project', 'creator', 'create_datetime', 'latest_update_datetime']
