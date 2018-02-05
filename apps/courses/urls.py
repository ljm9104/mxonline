from courses.views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView, VideoPlayView
from django.conf.urls import url, include
app_name = "courses"

urlpatterns = [
    # 课程列表url
    url('list/', CourseListView.as_view(), name="list"),
    # 课程详情页
    url('detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),
    # 课程章节信息页
    url('info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name="course_info"),

    # 课程章节信息页
    url('comments/(?P<course_id>\d+)/', CommentsView.as_view(), name="course_comments"),

    # 添加课程评论,已经把参数放到post当中了
    url('add_comment/', AddCommentsView.as_view(), name="add_comment"),

    # 课程视频播放页
    url('video/(?P<video_id>\d+)/', VideoPlayView.as_view(), name="video_play"),
]
