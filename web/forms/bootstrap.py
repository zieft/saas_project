# 这里专门存放经常被复用的bootstrap样式Form

class BootstrapForm(object):
    bootstrap_class_exclude = []  # 类变量，可以被子类覆写。在这个列表里的字段不应用bootstrap样式

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.bootstrap_class_exclude:
                continue  # 跳过当前循环，也就是不运行下面两行直接进入下一个循环
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入{}'.format(field.label)
