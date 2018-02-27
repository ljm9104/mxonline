from django.conf.urls import url, include

from users.views import UserinfoView, UploadImageView, UpdatePwdView
# from organization.views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView,
# OrgDescView, OrgTeacherView, AddFavView

urlpatterns = [
    # 用户信息
    url(r'^info/$', UserinfoView.as_view(), name="user_info"),

    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),

    # # 个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),


]
