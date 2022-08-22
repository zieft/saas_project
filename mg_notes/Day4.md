# 今日详细

1. ### 点击注册

1.1 点击收集数据&ajax

```js
$.ajax({
    url:"{% url 'register' %}", // url可以随便写，这里用register是为了省urL
    type:"POST", // 要去urls.py中判断收到的是get还是post请求
    data:$('#regForm').serialize(),
    dataType:"JSON",
    success:function (res) {
        console.log(res);
    }
                })
```



1.2 数据校验(每一个字段都需要校验)

1.3 写入数据库

1.4 一个bug

​	如果开启了验证码验证的功能（由于不能发短信，现在默认是关闭的），那么两次注册使用完全相同的信息时，页面会卡住。

原因是，第二次表单在进行用户名校验的时候，因为用户名已存在，校验用户名的钩子函数直接抛出异常，而剩下字段的校验就不再进行，后面再校验验证码的时候需要从cleaned_data里找"mobile_phone"，因为校验在username的时候就停止了，显然cleaned_data里还没有"mobile_phone"，所以网页卡住了。

confirmpassword里也有相同的问题。

两种解决思路

一，在clean钩子函数中，把抛出异常改成添加异常，这样，函数还会继续返回，将即使没有验证通过的字段添加到cleaned_data里面

二，由于前端报错是KeyError，那么可以通过不用key去取值即可

```python
mobile_phone = self.cleaned_data['mobile_phone'] # 如果没有直接报错
改成
mobile_phone = self.cleaned_data.get('mobile_phone') # 如果没有，则是None
if not mobile_phone:
    return code
```

2. ### 短信登陆

   2.1 展示页面

   2.2 点击发送短信

   2.3 点击登录

3. ### 用户名、密码登陆

   3.1 生成图片验证码

   `pip install pillow`

   ```python
   from PIL import Image
   
   img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
   ```

   3.2 session & Cookie

   ```
   Cookie存在于用户浏览器中，用于存储服务端返回的key (sessionid)
   Session存储于服务端，用于存储key and Value
   Cookie可以用key取Session里取Value
   ```
   
   django中的session
   
   ![image-20220822101027545](C:\Users\zieft\AppData\Roaming\Typora\typora-user-images\image-20220822101027545.png)
   
   redis和session功能上相似，session可以自动生成用户识别标识(sessionid)，redis不能生成，需要用户自己指定（手机号）。
   
   3.3 页面显示
   
    	1. 用户访问注册页面
    	2. 页面给用户返回一个带有img标签的响应，其中包含src指向图片验证码的路由
    	3. 后端生成图片验证码，并发给前端
    	4. 同时code保存到session中
   
   3.4 登录
   
   ​	3.4.1 中间件
   
   ​	用户登录成功后，想要在header中显示已登录的用户名，并且去除登录、注册按钮，需要用到中间件。中间件初始化方法：
   
   ```python
   from django.utils.deprecation import MiddlewareMixin
   
   class AuthMiddleware(MiddlewareMixin):
   ```
   
   ```python
       def process_request(self, request):
           """
           如果用户已登录，则在request中赋值
           比如：
           request.tracer = 666
           则，当用户登录成功以后，在所有的视图中都可以通过request.tracer来获取666这个值
           """
           user_id = request.session.get('user_id', 0) # 从session中获取用户名，没有则定义为0
   
           user_object = models.UserInfo.objects.filter(id=user_id).first() # 去数据库中找这个user
           request.tracer = user_object
   ```
   
   定义好的中间件，要在settings.py里注册。

​		用的时候在前端中可以判断，request.tracer中有没有值，有则表示用户已经登陆，header显示用户名，去掉登录注册按钮。没有，则显示登录注册按钮。
