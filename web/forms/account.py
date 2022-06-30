# views中所用到的所有ModelForm，都放在forms文件夹中，方便管理

import random
from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings

from utils.tencent.sms import send_sms_single
from django_redis import get_redis_connection

class RegisterModelForm(forms.ModelForm):
    # model里的verbose_name可以被覆写

    # 密码输入框
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput
                                   (attrs={
                                   # 'class': 'form-control',
                                   'placeholder': '提示文字'
                               }
                               )
                               )

    # 下面的字段没有定义在model.py里，因此不会被迁移到数据库中
    confirm_password = forms.CharField(label="重复密码", widget=forms.PasswordInput())

    phone = forms.CharField(label="手机号",
                            validators=[RegexValidator(r'^(1|3|4|5|6|7|8|9)d{9}$',
                                                       "手机号格式错误")]
                            )

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


class SendSmsForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request  # 这样一来，我们就可以在钩子函数中使用self.request.GET.get()方法了

    # 为什么不用ModelForm? 因为sendsms里面处理的数据 mobilePhone 和 tpl 跟数据库没有关系
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1|3|4|5|6|7|8|9)d{9}$',
                                                                           "手机号格式错误")])

    def clean_mobile_phone(self):
        """
        钩子方法，手机号进行校验的钩子
        :return:
        """
        mobile_phone = self.cleaned_data['mobile_phone']

        # 判断模板是否有问题
        tpl = self.request.GET.get("tpl")
        template_id = settings.TENCENT_SMS_TEMPLATE.get('tpl')
        if not template_id:
            raise ValidationError("模板不存在")

        # 校验数据库中是否已有手机号
        # mobile_phone=mobile_phone 第一个是model.py里的，第二个就是上面刚定义的
        exist = models.UserInfo.objects.filter(phone=mobile_phone).exist()
        if exist:
            raise ValueError("手机号已存在")

        #
        code = random.randrange(1000, 9999)
        # 发短信
        sms = send_sms_single(mobile_phone, template_id, [code, ])
        if sms['result'] != 0: # 0代表发送成功
            raise ValidationError('短信发送失败，{}'.format(sms['errmsg']))

        # 写入redis（django-redis）
        conn = get_redis_connection()
        conn.set(mobile_phone, code, ex=300)

        return mobile_phone
