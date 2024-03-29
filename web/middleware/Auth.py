import datetime

from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from web import models


class Tracer(object):
    def __init__(self):
        self.user = None
        self.price_policy = None
        self.project = None


class AuthMiddleware(MiddlewareMixin):
    # 下面定义的方法是按顺序执行，process_request执行完后，request.tracer就可以被后面的方法用到了
    def process_request(self, request):
        """
        如果用户已登录，则在request中赋值
        比如：
        request.tracer = 666
        则，当用户登录成功以后，在所有的视图中都可以通过request.tracer来获取666这个值
        """
        request.tracer = Tracer()

        user_id = request.session.get('user_id', 0)  # 从session中获取用户名，没有则定义为0

        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer.user = user_object
        # 去数据库中找这个user，如果存在这个user就给request.tracer赋值，不存在就赋None
        # 定义好的中间件，记得要去settings.py中去注册
        # 然后就可以在前端通过判断request.tracer是否有值，来判断用户的登录状态

        # 白名单：没有登录都可以访问的路由
        white_list = settings.WHITE_REGEX_URL_LIST
        # 获取当前用户请求的URL
        url = request.path_info
        # 检擦是否在白名单里，在则返回，不在则继续判断用户是否登录
        if url in white_list:
            return  # 中间件返回None时，说明什么都不做，继续往后走

        # 检查用户是否已登录，已登录则继续往后走，未登录则跳回登录界面
        if not request.tracer.user:
            return redirect('login')

        # 登录成功后，访问后台管理时：获取当前用户所拥有的额度
        # 方式1：免费额度在交易记录中存储
        # models.Transaction.objects.filter(user=user_object) # 查找当前用户所有交易记录
        # 获取当前用户id值最大（表示最新)的交易记录
        _object = models.Transaction.objects.filter(user=user_object,
                                                    status=2
                                                    ).order_by('-id').first()
        # 判断_object是否已过期

        current_datetime = datetime.datetime.now()
        if _object.end_datetime and \
                _object.end_datetime < \
                current_datetime:  # 只有非免费版才有end_datetime
            # 付费版 and 过期
            _object = models.Transaction.objects.filter(user=user_object,
                                                        status=2,
                                                        price_policy__category=1
                                                        ).first()
            # project.py中就可以通过request.transaction.user / price_policy 等等来获取可用额度
            request.tracer.price_policy = _object.price_policy
        request.tracer.price_policy = _object.price_policy

        # 方式2： 免费的额度存储配置文件
        # if not _object:
        #     # 没有购买
        #     request.price_policy = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()
        # else:
        #     # 付费版
        #     current_datetime = datetime.datetime.now()
        #     if _object.end_datetime < current_datetime:
        #         request.price_policy = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()
        #     else:
        #         request.tracer.price_policy = _object.price_policy

    def process_view(self, request, view, args, kwargs):
        """ 在进入本中间件之前，确保路由匹配先得通过，否则无法拿到project_id """

        # 1.判断URL是否已manage开头，如果是继续2.，否则重定向
        if not request.path_info.startswith('/manage/'):
            return  # return 表示验证通过，继续往下走第2步

        # 1.5 获取project_id和用户对象
        project_id = kwargs.get('project_id')
        user_object = request.tracer.user

        # 2. 判断是不是我创建的
        project_object = models.Project.objects.filter(
            creator=user_object,
            id=project_id
        ).first()

        if project_object:  # if是我创建的
            request.tracer.project = project_object
            return

        # 2.5 不是我创建的有可能是我参与的，先获取我参与的项目对象
        project_user_object = models.ProjectUser.objects.filter(
            user=request.tracer.user,
            project_id=project_id
        ).first()

        if project_user_object:  # if是我参与的
            request.tracer.project = project_user_object.project
            return

        # 以上判断都不满足的，重定向
        return redirect('project_list')
