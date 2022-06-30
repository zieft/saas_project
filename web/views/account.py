from django.shortcuts import render, HttpResponse
from web.forms.account import RegisterModelForm, SendSmsForm
from django.http import JsonResponse


def register(request):
    form = RegisterModelForm()
    return render(request, 'web/templates/register.html', {'form': form})


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
