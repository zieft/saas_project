from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名",
                                max_length=32)

    email = models.CharField(verbose_name="邮箱",
                             max_length=32)


    # verbosename可以在ModelForm里被覆写
    password = models.CharField(verbose_name="密码",
                                max_length=32)

    phone = models.CharField(verbose_name='电话',
                             max_length=12)

    # ModelForm里也可以定义这里没有的字段，这种字段将不会被迁移到数据库中
