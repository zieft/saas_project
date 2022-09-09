from django import forms

from web import models
from web.forms.bootstrap import BootstrapForm


class WikiModelForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = models.Wiki
        exclude = ['project', ]
