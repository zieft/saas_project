# views中所用到的所有ModelForm，都放在forms文件夹中，方便管理

import random
from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings

# from utils.tencent.sms import send_sms_single
from utils.AWS.sms import send_sms_single
from django_redis import get_redis_connection
from utils import encrypt

class RegisterModelForm(forms.ModelForm):
    # model里的verbose_name可以被覆写

    # 下面定义的字段，谁定义在前，谁优先被校验
    # 密码输入框
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput
                                   (attrs={
                                   # 'class': 'form-control',
                                   'placeholder': '提示文字'
                                            }
                                    ),
                               min_length=8,
                               max_length=64,
                               error_messages={
                                   'min_length': '密码长度不能少于8个字符',
                                   'max_length': '密码长度不能大于64个字符',
                               },

                               )

    # 下面的字段没有定义在model.py里，因此不会被迁移到数据库中
    confirm_password = forms.CharField(label="重复密码",
                                       widget=forms.PasswordInput(),
                                       min_length=8,
                                       max_length=64,
                                       error_messages={
                                           'min_length': '重复密码长度不能少于8个字符',
                                           'max_length': '重复密码长度不能大于64个字符',
                                                        },
                                       )

    mobile_phone = forms.CharField(label="手机号",
                                   validators=[RegexValidator(settings.MOBILE_PHONE_VALIDATOR, "手机号格式错误"), ])

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput()
    )

    class Meta:
        model = models.UserInfo
        # fields = "__all__" # 用默认顺序展示所有字段
        fields = ['username', 'email', 'password', 'confirm_password',
                  'mobile_phone', 'code']  # 自定义显示字段的顺序

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # 对model和ModelForm定义的所有字段进行遍历
            # name是变量名，field就是name变量里保存的对象，比如CharField对象
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs["placeholder"] = '请输入%s' % (field.label)

    # 为“用户名不得重复”而定义的钩子方法
    def clean_username(self):
        username = self.cleaned_data['username']

        # 优化查询方法：我们给models.UserInfo.username添加一个db_index=True的参数
        exists = models.UserInfo.objects.filter(username=username).exists()

        if exists:
            # raise ValidationError('用户名已存在')
            self.add_error('username', '用户名已存在') # 用这种方法，即使校验失败，也继续运行下面的return
            # 这样cleaned_data里依然可以取到这个值
        return username # 这里的return， 就是把username添加到cleaned_data里面去

    def clean_password(self):
        pwd = self.cleaned_data['password']

        return encrypt.md5(pwd)

    # 判断两次输入的密码是否相同
    def clean_confirm_password(self):
        # 注意！！！！！！
        # self.cleaned_data里储存的是已经校验了的数据
        # 因此这里只能从cleaned_data里取到'username', 'email', 'password', 'confirm_password'
        pwd = self.cleaned_data.get('password')
        # pwd在前面已经加密过了
        # 因为使用的是encrypt.md5使用的是同一个盐，因此返回的值跟password里的密文是一样的
        cfm_pwd = encrypt.md5(self.cleaned_data['confirm_password'])
        if pwd != cfm_pwd:
            raise ValidationError('两次密码不一致')
        return cfm_pwd

    # 校验手机号，按注册和按获取验证码按钮时都需要校验
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已注册')
        return mobile_phone

    # def clean_code(self):
    #     code = self.cleaned_data['code']
    #     # mobile_phone = self.cleaned_data['mobile_phone']
    #     # 上面一行的写法会造成一个bug，详见Day4 1.4节
    #     mobile_phone = self.cleaned_data.get('mobile_phone')
    #     if not mobile_phone:
    #         return code
    #     conn = get_redis_connection()
    #     redis_code = conn.get(mobile_phone)
    #     if not redis_code:
    #         raise ValidationError('验证码失效或未发送，请重新发送')
    #
    #     redis_str_code = redis_code.decode('utf-8')
    #
    #     if redis_code.strip() != redis_str_code: # .strip()用于将用户误输入的空格去掉
    #        raise ValidationError('验证码错误，请重新输入')
    #
    #     return code

class SendSmsForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request  # 这样一来，我们就可以在钩子函数中使用self.request.GET.get()方法了

    # 为什么不用ModelForm? 因为sendsms里面处理的数据 mobilePhone 和 tpl 跟数据库没有关系
    mobile_phone = forms.CharField(label='手机号',
                                   validators=[RegexValidator(settings.MOBILE_PHONE_VALIDATOR, "手机号格式错误"), ])

    def clean_mobile_phone(self):
        """
        钩子方法，手机号进行校验的钩子
        :return:
        """
        mobile_phone = self.cleaned_data['mobile_phone']

        # 判断模板是否有问题
        tpl = self.request.GET.get("tpl")
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        # template_id = 548760
        if not template_id:
            raise ValidationError("模板不存在")

        # 校验数据库中是否已有手机号
        # mobile_phone=mobile_phone 第一个是model.py里的，第二个就是上面刚定义的
        # exist = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exist()
        # if exist:
        #     raise ValueError("手机号已存在")

        #
        code = random.randrange(1000, 9999)
        # 发短信
        # sms = send_sms_single(mobile_phone, template_id, [code, ])
        sms = send_sms_single(mobile_phone, tpl, [code, ])  # 从AWS发短信

        if sms['result'] != 0:  # 0代表发送成功
            raise ValidationError('短信发送失败，{}'.format(sms['errmsg']))

        # 写入redis（django-redis）
        conn = get_redis_connection()
        conn.set(mobile_phone, code, ex=300)

        return mobile_phone
