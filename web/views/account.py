import django_redis
from django.shortcuts import render, HttpResponse
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm, SendSmsFormFake
from django.http import JsonResponse
from web import models


def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'web/templates/register.html', {'form': form})

    # 对表单进行校验
    # 验证的规则定义在class RegisterModelForm()里
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # 验证通过，写入数据库
        form.save()  # 因为我们使用的时ModelForm，所以可以直接使用.save()方法。
        # 事实上.save()方法等价于下面这几行，且可以自动pop掉数据表中没有的字段
        # data = form.cleaned_data
        # data.pop('code')
        # data.pop('confirm_password')
        # instance = models.UserInfo.objects.create(**data)
        # 用这种方式保存的密码在数据库中是明文的，所以还要对密码再进行一次加密
        # 这个可以写在视图函数的钩子方法里，因为密码经过校验以后，会再返回一个校验后的密码，我们可以在返回的时候加密
        # 返回给前端：'status': True表示验证成功，然后让前端判断如果验证成功，则跳转到/login/页面
        return JsonResponse({'status': True, 'data': '/login/'})
    # 如果没有通过验证，则返回验证没通过的错误信息
    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    """  短信登陆  """
    if request.method == "GET":
        form = LoginSMSForm()
        return render(request, 'login_sms.html', {"form": form})

    # 接收到登陆POST请求，对请求内容进行校验
    form = LoginSMSForm(request.POST)
    if form.is_valid():
        # 用户输入信息正确，登陆成功
        user_object = form.cleaned_data['mobile_phone']
        # 用户信息放入session
        request.session['user_id'] = user_object.id
        request.session['user_name'] = user_object.username

        return JsonResponse({'status': True, 'data': '/index/'})

    return JsonResponse({"status": False, 'error': form.errors})

def send_sms(request):
    # mobile_phone = request.Get.get('mobile_phone')
    # tpl = request.GET.get('tpl')
    # 以上代码我希望放到form里面去处理，因此，在实例化SendSmsForm的时候要把request作为参数也传过去
    # 以便我们可以在SendSmsForm中调用request.GET.get()方法
    # 因此，我们需要重构一下SendSmsForm的__init__方法，使其接收request参数
    # form = SendSmsForm(data=request.GET)

    form = SendSmsForm(request, data=request.GET)

    # 只校验手机号：不能为空，格式是否正确。
    # 不会校验手机号是否已被注册，相关校验在SendSmsForm里的钩子函数里进行
    if form.is_valid():
        # 可以在这里发短信，但是
        # 为了校验、获取和在前端展示错误信息比较方便，
        # 发短信的功能也应该写在forms里的钩子函数里
        # 如果校验通过，说明forms里面定义的所有步骤都完成了，包括发短息、写入redis
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def send_sms_fake(request):
    form = SendSmsFormFake(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})
