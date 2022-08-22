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
   Cookie存在于用户浏览器中，用于存储服务端返回的key
   Session存储于服务端，用于存储key and Value
   Cookie可以用key取Session里取Value
   ```
   
   django中的session
   
   ![image-20220822101027545](C:\Users\zieft\AppData\Roaming\Typora\typora-user-images\image-20220822101027545.png)
   
   3.3 页面显示
   
    	1. 用户访问注册页面
    	2. 页面给用户返回一个带有img标签的响应，其中包含src指向图片验证码的路由
    	3. 后端生成图片验证码，并发给前端
    	4. 同时code保存到session中
   
   3.4 登陆