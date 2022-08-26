from django.shortcuts import render
from web.forms.project import ProjectModelForm


def project_list(request):
    """ 项目列表 """
    form = ProjectModelForm()
    return render(request, 'project_list.html', {'form': form})

