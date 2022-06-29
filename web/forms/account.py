# views中所用到的所有ModelForm，都放在forms文件夹中，方便管理

from django import forms
from web import models
from django.core.validators import RegexValidator


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
                  'phone', 'code']  # 自定义显示字段的顺序

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # 对model和ModelForm定义的所有字段进行遍历
            # name是变量名，field就是name变量里保存的对象，比如CharField对象
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs["placeholder"] = '请输入%s' % (field.label)
