from django.conf.urls import url, include

from organization.views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView


urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="org_list"),                         # 课程机构列表url
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),                #
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),     #
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),      # 访问课程
]
