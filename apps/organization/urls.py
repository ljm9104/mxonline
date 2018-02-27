from django.conf.urls import url, include

from organization.views import *
# from organization.views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView,
# OrgDescView, OrgTeacherView, AddFavView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="org_list"),                         # 课程机构列表url
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),                #
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),     #
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),  # 访问课程
    # 访问机构描述
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    # 访问机构讲师
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),
    # 机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),
    # 讲师列表
    url('teacher/list/', TeacherListView.as_view(), name="teacher_list"),
    # 讲师 详情页
    url('teacher/detail/(?P<teacher_id>\d+)/', TeacherDetailView.as_view(), name="teacher_detail"),

]
