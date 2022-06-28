# 从主路由分发而来，方便以后删除

from django.conf.urls import url
from app01 import views

urlpatterns = [
    # url(r'^send/sms/', views.send_sms),
    url(r'^register/', views.register, name='register'), # 这里的name与web里的register重名了，
    # 但因为我们在主路由中定义了namespace='app01'，所以，想要反向解析这里的register，需要使用'app01:register'

]
