from django import setup
import os
import sys

# 将本文件所在的文件夹路径添加到path，即当前文件所在目录的上一级的上一级
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# manage.py中的一行，模拟运行一下manage.py，setup各种参数，链接数据库等
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saas_project.settings")
setup()
