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

