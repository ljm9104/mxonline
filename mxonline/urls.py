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
# from users.views import LoginUnsafeView  #
from users.views import LogoutView       # 基于类登陆的
from users.views import RegisterView    # 注册
from users.views import ActiveUserView  # 激活
from users.views import ForgetPwdView   # 忘记密码
from users.views import ResetView       # 重置密码
from users.views import ModifyPwdView   #
from users.views import IndexView

from organization.views import OrgView
from .settings import MEDIA_ROOT
from .settings import STATIC_ROOT
from django.views.static import serve
from django.views.generic.base import RedirectView

urlpatterns = [

    url(r'^xadmin/', xadmin.site.urls),
    # Python3 Django2.0.1 的url的配置中          ???
    # url('xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name='index'),
    # url('^login/$', TemplateView.as_view(template_name='login.html'), name='login'),
    # 登录页面跳转url，login不直接调用，而是指向这个函数对象
    # url('^login/$', user_login, name='login'),
    # 基于类登陆,注意此时应该调用类的方法as_view（）
    url('^login/$', LoginView.as_view(), name='login'),             # 登陆
    # url('^login/', LoginUnsafeView.as_view(), name='login'),
    url('^logout/$', LogoutView.as_view(), name='logout'),          # 登出
    url("^register/$", RegisterView.as_view(), name="register"),    # 注册
    url(r'^captcha/', include('captcha.urls')),                     # 验证码
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),        # 激活
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),  # 忘记密码
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),                # 重置密码
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构
    # url(r'^org_list/$', OrgView.as_view(), name="org_list"),
    url(r'^org/', include('organization.urls', namespace='org')),

    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    # 公开课
    url(r'^course/', include('courses.urls', namespace='course')),

    # user app的url配置
    url(r'^users/', include('users.urls', namespace="users")),

]

# 全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
