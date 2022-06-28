# Day 2

## 今日概要

- 腾讯发送短信
- django的ModelForm组件
- redis
- 注册逻辑设计
- 开发
- 讲解

## 今日详细

### 1 腾讯云发短信                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

``` 
pythonav.com/wiki/10/81
```

### 2 ModelForm

app01/views.py:

##### ModelForm 里改写 models 定义的verbose_name

```python
    # verbosename可以在ModelForm里被覆写
    password = models.CharField(verbose_name="密码", max_length=32)
```

##### 手机号格式验证 正则表达式

```python
    phone = forms.CharField(label="手机号（被覆写）",
            validators=[RegexValidator(r'^(1|3|4|5|6|7|8|9)d{9}$',
                                       "手机号格式错误")]
                            )
```

##### 后端向前端传form

```python
return render(request, 'app01/templates/app01/register.html', {'form': form})
```

app01/templates/register.html

##### 前端渲染form

```html
    {% for field in form %}
        <p> {{ field.label }} : {{ field }}</p> <!-- .label 获取的就是verbose_name -->
    {% endfor %}
```

##### 通过css样式，更改form的位置

```html
<!--这里时从doc里直接考下来的源码，在用的时候需要稍加改造-->
<head>
    <style>
        .account{
            width: 600px;
            margin: 0 auto;
        }
    </style>
</head>

<body>
<div class="account">
    <h1>注册</h1>
    {% for field in form %}
        <p> {{ field.label }} : {{ field }}</p> <!-- .label 获取的就是verbose_name -->
    {% endfor %}
</div>
```



##### 使用bootstrap表单模板

```css
<form>
  <div class="form-group">
    <label for="exampleInputEmail1">Email address</label>
    <input type="email" class="form-control" id="exampleInputEmail1" placeholder="Email">
  </div>
  <div class="form-group">
    <label for="exampleInputPassword1">Password</label>
    <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password">
  </div>
  <div class="form-group">
    <label for="exampleInputFile">File input</label>
    <input type="file" id="exampleInputFile">
    <p class="help-block">Example block-level help text here.</p>
  </div>
  <div class="checkbox">
    <label>
      <input type="checkbox"> Check me out
    </label>
  </div>
  <button type="submit" class="btn btn-default">Submit</button>
</form>
```

```html
<!--这里是改造后的代码，form-control样式在前端中定义-->
<body>
<div class="account">
    <h1>注册</h1>
    <form>
        {% for field in form %}
        <div class="form-group">
            <!--label for规定了label与哪个表单元素绑定-->
            <label for={{ field.id_for_label }}>{{ field.label }}</label>
            <!--form-control样式就是美化输入框的关键元素，同样可以在ModelForm中定义-->
            <input type="email" class="form-control" id="exampleInputEmail1" placeholder="Email">
            <!--{{ field }}-->
        </div>
        {% endfor %}
        <button type="submit" class="btn btn-default">注 册</button>
    </form>
</div>
</body>
```

##### Form-control样式也可以在ModelForm中定义，比如：

```python
class RegisterModelForm(forms.ModelForm):
  	password = forms.CharField(label="密码", 
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': '提示文字'}))

```

##### 如果每一个字段都要加入Form-control， 则可以重新定义init方法，批量化传入

```python
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # 对model和ModelForm定义的所有字段进行遍历
            # name是变量名，field就是name变量里保存的对象，比如CharField对象
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs["placeholder"] = '请输入%s' % (field.label)
```

##### 给输入验证码的文本框加一个”发送短信“的按钮，本质上就是用if判断当前标签是不是code，如果是，就在文本框后加一个按钮

```html
        {% for field in form %}
            {% if field.name == 'code' %}
                <div class="form-group">
                    <!--label for规定了label与哪个表单元素绑定-->
                    <label for={{ field.id_for_label }}>{{ field.label }}</label>
                    <!--form-control样式就是美化输入框的关键元素，同样可以在ModelForm中定义-->
                    <!--input type="email" class="form-control" id="exampleInputEmail1" placeholder="Email"-->
                    <div class="clearfix">
                        <div class="col-md-6" style="padding-left: 0;">{{ field }}</div>
                        <div class="col-md-6">
                            <button type="submit" class="btn btn-default">点击获取短信</button>
                        </div>
                    </div>

                </div>
            {% else %}
                <div class="form-group">
                    <!--label for规定了label与哪个表单元素绑定-->
                    <label for={{ field.id_for_label }}>{{ field.label }}</label>
                    <!--form-control样式就是美化输入框的关键元素，同样可以在ModelForm中定义-->
                    <!--input type="email" class="form-control" id="exampleInputEmail1" placeholder="Email"-->
                    {{ field }}
                </div>
            {% endif %}
        {% endfor %}
        <button type="submit" class="btn btn-primary">注 册</button>
```

### 3 ajax请求 获取验证码思路

- ##### 思路：

  - 点击获取手机号

  - 向后台发起ajax请求

    - 手机号

    - tpl=register

  - 向手机发送短信

  - 验证码有效时间设定

    - 点击发送验证码时：把手机号和时间戳 保存在reddis中，设置多长时间失效 
    - 点击注册按钮时：失效时间内，通过手机号来取对应的值是可以取到对应的码，超时以后就不行

### 4. redis基本操作

##### 4.1 安装redis

文档：pythonav.com/wiki/detail/10/82

mac上直接 brew install redis

然后 redis-server启动

配置文件在/usr/local/etc/redis.conf里

可以bind 0.0.0.0 使得局域网中其他计算机可以访问到

requirepass foobared 可以将密码设定为foobared

##### 4.2 python操作redis p25

文档：pythonav.com/wiki/detail/10/82/

pip3 install redis

```pyhton
import redis

conn = redis.Redis(
		host='本机ip',
		port=6379,
		password='foobared',
		encoding='utf-8'
)

# 设置键值，传入的值默认会转成utf-8的字节，再保存
conn.set('15131255089', 999, ex=10)

# 根据键获取值，不存在则返回None，存在则获取到的值为字节类型
value = conn.get('15131255089')
print(value)

# 字节转成字符串
decode(value)
```

