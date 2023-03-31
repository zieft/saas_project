from django.shortcuts import render


def dashboard(request, project_id):
    return render(request, 'dashboard.html')




def statistics(request, project_id):
    return render(request, 'statistics.html')


def file(request, project_id):
    return render(request, 'file.html')


""" wiki将会有很多子功能，所以单独定义在wiki.py中
def wiki(request, project_id):
    return render(request, 'wiki.html')
"""
