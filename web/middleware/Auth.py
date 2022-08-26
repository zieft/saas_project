from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings
from web import models


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        如果用户已登录，则在request中赋值
        比如：
        request.tracer = 666
        则，当用户登录成功以后，在所有的视图中都可以通过request.tracer来获取666这个值
        """
        user_id = request.session.get('user_id', 0)  # 从session中获取用户名，没有则定义为0

        user_object = models.UserInfo.objects.filter(id=user_id).first()
        # 去数据库中找这个user，如果存在这个user就给request.tracer赋值，不存在就赋None
        request.tracer = user_object
        # 定义好的中间件，记得要去settings.py中去注册
        # 然后就可以在前端通过判断request.tracer是否有值，来判断用户的登录状态

        # 白名单：没有登录都可以访问的路由
        white_list = settings.WHITE_REGEX_URL_LIST
        # 获取当前用户请求的URL
        url = request.path_info
        # 检擦是否在白名单里，在则返回，不在则继续判断用户是否登录
        if url in white_list:
            return # 中间件返回None时，说明什么都不做，继续往后走

        # 检查用户是否已登录，已登录则继续往后走，未登录则跳回登录界面
        if not request.tracer:
            return redirect('login')
