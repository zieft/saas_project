from django.shortcuts import render


def wiki(request, project_id):
    """ wiki 首页的展示"""
    return render(request, 'wiki.html')
