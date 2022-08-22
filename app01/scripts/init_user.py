from django import setup
import os
import sys

# 将本文件所在的文件夹路径添加到path，即当前文件所在目录的上一级的上一级
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# manage.py中的一行，模拟运行一下manage.py，setup各种参数，链接数据库等
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saas_project.settings")
setup()

# 下面就可以导入django运行时才能调用的函数跟方法了，例如
# 像用户表里添加一行新用户数据
from web import models

models.UserInfo.objects.create(username='django离线脚本', email='example@example.com', mobile_phone='8888888888',
                               password='87654321') # 注意：这时候表单没有验证功能，且密码不会被md5加密
