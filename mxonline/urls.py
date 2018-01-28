"""mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import xadmin
from django.views.generic import TemplateView
from users.views import user_login      # 基于函数登陆的
from users.views import LoginView       # 基于类登陆的
from users.views import RegisterView    # 注册
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # Python3 Django2.0.1 的url的配置中          ???
    # url('xadmin/', xadmin.site.urls),
    url('^$', TemplateView.as_view(template_name='index.html'), name='index'),
    # url('^login/$', TemplateView.as_view(template_name='login.html'), name='login'),
    # 登录页面跳转url，login不直接调用，而是指向这个函数对象
    # url('^login/$', user_login, name='login'),
    # 基于类登陆
    # 注意此时应该调用类的方法as_view（）
    url('^login/$', LoginView.as_view(), name='login'),             # 登陆
    url("^register/$", RegisterView.as_view(), name="register"),    # 注册
    url(r'^captcha/', include('captcha.urls')),                     #

]
