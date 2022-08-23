import django.contrib.auth.models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名",
                                max_length=32,
                                db_index=True,  # db_index=True, 意为给此字段创建索引，这样查询更快
                                )

    email = models.CharField(verbose_name="邮箱",
                             max_length=32)

    # verbosename可以在ModelForm里被覆写
    password = models.CharField(verbose_name="密码",
                                max_length=32)

    mobile_phone = models.CharField(verbose_name='电话',
                                    max_length=12)

    # ModelForm里也可以定义这里没有的字段，这种字段将不会被迁移到数据库中


class PricePolicy(models.Model):
    """ 价格策略 """
    category_choices = (
        (1, '免费版'),
        (2, '收费版'),
        (3, '其他'),
    )

    category = models.SmallIntegerField(verbose_name='收费类型', default=2, choices=category_choices)
    title = models.CharField(verbose_name='标题', max_length=32)
    price = models.PositiveIntegerField(verbose_name='价格')

    project_num = models.PositiveIntegerField(verbose_name='项目数量')
    project_member = models.PositiveIntegerField(verbose_name='项目成员数量')
    project_space = models.PositiveIntegerField(verbose_name='单项目空间')
    per_file_size = models.PositiveIntegerField(verbose_name='单文件大小/Mb')

    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


class Transaction(models.Model):
    """ 交易记录 """
    status_choice = (
        (1, '未支付'),
        (2, '已支付'),
    )

    status = models.SmallIntegerField(verbose_name='交易状态', choices=status_choice)

    order = models.CharField(verbose_name='订单号', max_length=64, unique=True)
    user = models.ForeignKey(verbose_name='用户', to='UserInfo')
    price_policy = models.ForeignKey(verbose_name='价格策略', to='PricePolicy')

    count = models.IntegerField(verbose_name='数量/年', help_text='0表示无限期')

    price = models.IntegerField(verbose_name='实际支付价格')

    start_datetime = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    end_datetime = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)

    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Project(models.Model):
    """ 项目表 """
    COLOR_CHOICES = (
        (1, '#56b8eb'),
        (2, '#f28033'),
        (3, '#ebc656'),
        (4, '#a2d148'),
        (5, '#20BFA4'),
        (6, '#7461c2'),
        (7, '#20bfa3'),
    )

    name = models.CharField(verbose_name='项目名称', max_length=32)
    color = models.SmallIntegerField(verbose_name='颜色', choices=COLOR_CHOICES, default=1)
    desc = models.CharField(verbose_name='项目描述', max_length=255, null=True, blank=True)
    use_space = models.IntegerField(verbose_name='已使用空间', default=0)
    star = models.BooleanField(verbose_name='星标', default=False)

    join_count = models.SmallIntegerField(verbose_name='参与人数', default=1)
    creator = models.ForeignKey(verbose_name='创建者', to='UserInfo')
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class ProjectUser(models.Model):
    """ 项目参与者 """
    # user 和 invitee 都关联了 UserInfo 表
    # 当从 UserInfo 反向关联 ProjectUser的时候，django 将不知道用户的意图是找user 还是 invitee，
    # 反向关联语法：
    # obj = UserInfo.objects.filter(id=1)
    # obj.projectuser_set.all() # 这就是反向关联的默认写法

    # related_name 参数就是为了让django在反向关联的时候，知道要找具体哪个字段
    # 这样就可以把projectuser_set 替换为 related_name 来指定找哪个字段
    # obj.invites.all()
    # obj.projects.all()
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', related_name='projects')
    invitee = models.ForeignKey(verbose_name='邀请人', to='UserInfo', related_name='invites', null=True, blank=True)

    project = models.ForeignKey(verbose_name='项目', to='Project')


    star = models.BooleanField(verbose_name='星标', default=False)

    create_datetime = models.DateTimeField(verbose_name='加入时间', auto_now_add=True)
