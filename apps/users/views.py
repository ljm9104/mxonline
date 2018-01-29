from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.http.response import HttpResponse

# 并集运算
from django.db.models import Q

# 导入View，基于类实现需要继承的view
from django.views.generic.base import View
from operation.models import UserCourse, UserFavorite, UserMessage
from .models import UserProfile, EmailVerifyRecord
# form表单验证 & 验证码
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyForm
from django.contrib.auth.hashers import make_password       # 密码加密
from utils.email_send import send_register_eamil            # 发送邮件


# 实现用户名和邮箱都可以登陆
# 继承ModelBackend类，他有方法authenticate，可以重载他实现自己业务逻辑
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 注：get只能获取具有唯一的，两个一样的将报错，Q并集查找
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # django的后台中有自己的密码加密，所以不用password=password
            # UserProfile继承的AbstractUser有def check_password(self，raw_input)方法
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# Create your views here.


# 基于类实现登陆功能，自定义类需要继承django模块中View
# 代码含义基本同基于函数的，在此不再写
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        # 类实例需要一个字典参数dict：request.POST就是一个QueryDict所以直接传入
        # POST中的username，password，对应到form中
        login_form = LoginForm(request.POST)
        # is_valid判断我们字段是否有错执行我们原有逻辑，验证失败跳回login页面
        if login_form.is_valid():
            # 取不到时为空，username，password为前端页面name值
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            # 成功返回user对象,失败返回null
            user = authenticate(username=user_name, password=pass_word)
            # 如果不是null说明验证成功
            if user is not None:
                # login_in 两参数：request, user
                # 实际是对request写了一部分东西进去，然后在render的时候：
                # request是要render回去的。这些信息也就随着返回浏览器。完成登录

                if user.is_active:
                    login(request, user)
                    # 跳转到首页 user request会被带回到首页
                    return render(request, "index.html")
                else:
                    return render(request, 'login.html', {"msg": "用户名尚未激活!"})
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误!"})
        # 验证不成功跳回登录页面
        # 没有成功说明里面的值是None，并再次跳转回主页面
        else:
            return render(request, "login.html", {'login_form': login_form})


# 当我们配置url被这个view处理时，自动传入request对象
def user_login(request):
    # 前端向后端发送的请求方式：get/post
    # 登陆提交表单为post
    if request.method == 'POST':
        # 当取不到是为空，username，password为前台页面name值
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')
        # 成功返回user对象，就是登陆成功
        user = authenticate(username=user_name, password=pass_word)
        # 如果不是null就是说明验证成功
        if user is not None:
            # login_in 两个参数：request，user
            # 实际上对request谢了一部分东西进去，然后在render回去，返回浏览器，完成登陆
            login(request, user)
            return render(request, 'index.html')
        # 没有成功说明值是none，并继续跳转到登陆界面
        else:
            return render(request, 'login.html', {'msg':'用户名或密码错误！'})
    elif request.method == 'GET':
        # render渲染html返回用户三个参数：request，模板，字典（给前台传值）
        return render(request, 'login.html', {})


# 注册功能的view类
class RegisterView(View):
    # get方法直接返回页面
    def get(self, request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        # 实例化form
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 这里注册时前端的name为email
            user_name = request.POST.get("email", "")
            # 用户查重
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已存在"})

            pass_word = request.POST.get("password", "")

            # 实例化一个user_profile对象，将前台值存入
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name

            # 默认激活状态为false
            user_profile.is_active = False

            # 加密password进行保存
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册雪竺轩的慕课小站!! --来自系统自动消息"
            user_message.save()

            # 发送注册激活邮件
            send_register_eamil(user_name, "register")

            # 跳转到登录页面
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


# 激活
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return HttpResponse("验证码已经失效")
        return render(request, "login.html")


# 忘记密码，找回密码
class ForgetPwdView(View):
    # get方法
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    # post方法
    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_eamil(email, 'forget')
            return render(request, 'send_success.html', {'msg': '重置密码链接已发送，请登录邮箱查看'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


# 重置密码
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {'email': email})

        else:
            # user = UserProfile.objects.get(email=email)
            # user.is_active = True
            # user.save()
            return HttpResponse("验证码已经失效")
        return render(request, "login.html")


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {'email': email, 'msg': '两次密码输入不一致'})
            user = UserProfile.objects.get(email=email)
            user.password1 = make_password(pwd1)
            user.password2 = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get('email', '')
            return render(request, "password_reset.html", {'email': email, 'modify_form': modify_form})