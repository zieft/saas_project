# DAY3 用户认证

## 内容回顾

- 虚拟环境 venv（为每个项目创）

- requirements.txt (pip freeze > requirements.txt)

- Local_settings.py

- gitignore

- 腾讯短信

  - API，提供URL，根据提示传入参数去请求

    ```
    requests.get("https://www.xxx.com/adsf/adsfa", json={......})
    ```

  - SDK，模块，下载安装后，基于模块来完成功能

    ```python
    sms.py
    	def func():
        return requests.get("https://www.xxx.com/adsf/adsfa", json={......})
    ```

    ```python
    pip install sms
    sms.func()
    ```

- Redis

  - 第一步：在A主机安装配置redis

  - 第二部 连接redis

    - redis-cli 从机 看文档
    - python 模块直接连接  不推荐，因为连接需要时间
    - 使用python模块连接池 推荐

    ```python
    imort redis
    
    pool = redis.Redis(host, port, password, encoding, max_connections=1000)
    conn = redis.Redis(connection_pool=pool)
    conn.set(key, value)
    conn.get(key)
    ```

- Django-redis，在django中方便地使用redis

  - 安装django-redis: pip install django-redis

  - 使用：

    - 去local_settings.py中配置CACHE

      ```python
      CACHE= {
        'default': {
          'BACKEND': 'django_redis.cache.RedisCache',
          'LOCATION': 'redis://IP:Port',
          "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS":{
                    "max_connections": 1000,
            "encoding": 'utf-8'
            },
      			"PASSWORD": "foobared"
          }
        }
      }
      ```

    - view.py里写

      ```python
      from django_redis import get_redis_connection
      
      def index(request):
        conn = get_redis_connection('default')
        conn.set(key, value)
        value = conn.get(key)
        return HttpResponse("OK")
      ```

      

      

## 今日概要

- 注册
- 短信验证码登录
- 用户名密码登录


