from django import forms
from django.forms import models

from bootstrap import BootstrapForm


class IssuesModelForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = models.Issues
        exclude = ['project', 'creator', 'create_datetime', 'latest_update_datetime']
        widgets = {
            "assign": forms.Select(attrs={'class': 'selectpicker', 'data-live-search'}),
            'attention': forms.SelectMultiple(

            )
        }
