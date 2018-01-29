from django import forms                    # 引入Django表单
from captcha.fields import CaptchaField


# 登陆表单验证
class LoginForm(forms.Form):
    # 用户名和密码不能为空
    # 登陆的时候很少验证长度的，在此将max_length，min_length去掉
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


# 验证码form & 注册表单form
class RegisterForm(forms.Form):
    # 此处email与前端name需保持一致。                                 # email格式验证如何完善
    email = forms.EmailField(required=True)
    # 密码不能小于5位
    password = forms.CharField(required=True, min_length=5)
    # 应用验证码
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


# 注册验证码实现
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


#
class ModifyForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)
    # 应用验证码
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误'})







