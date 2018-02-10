from datetime import datetime

from django.db import models
from organization.models import CourseOrg, Teacher

# Create your models here.
'''
course中需要那些表:
    1.课程本身需要一张表
    2.课程基本信息需要一张表, 章节表与课程表存在(一个课程对应多个章节)
    3.章节表中：章节的名称。 
    4.章节与视频(一个章节对应多个视频)
结构: 
    课程本身–(一对多)>章节-(一对多)->视频信息 
    资源下载放在课程里面的。一个课程对应多个资源
    
共四张表：课程本身–(一对多)>章节-(一对多)->视频信息 & 资源表

一对多, 多对一都可以使用django的外键来完成。
'''


# 课程信息表
class Course(models.Model):
    DEGREE_CHOICES = (
        ("cj", u"初级"),
        ("zj", u"中级"),
        ("gj", u"高级")
    )
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    category = models.CharField(default=u'后端开发', max_length=20, verbose_name=u"课程类别")
    # TextField允许我们不输入长度。可以输入到无限大。暂时定义为TextFiled，之后更新为富文本
    detail = models.TextField(verbose_name=u"课程详情")
    teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", null=True, blank=True)
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=2, verbose_name=u"难度")
    # 使用分钟做后台记录(存储最小单位)前台转换
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    # 保存学习人数:点击开始学习才算
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    you_need_know = models.CharField(max_length=300, default=u"一颗勤学的心是本课程必要前提", verbose_name=u"课程须知")
    teacher_tell = models.CharField(max_length=300, default=u"按时交作业,不然叫家长", verbose_name=u"老师告诉你")

    image = models.ImageField(
        upload_to="courses/%Y/%m",
        verbose_name=u"封面图",
        max_length=100)
    # 保存点击量，点进页面就算
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    tag = models.CharField(default='', max_length=20, verbose_name=u'课程标签')

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程章节数
        all_lessons = self.lesson_set.all().count()
        return all_lessons

    def get_learn_users(self):
        # 获取学习用户
        all_lessons = self.usercourse_set.all()[:5]
        return all_lessons

    def get_teacher_nums(self):
        # 获取课程机构教师
        return self.teacher_set.all().count()

    def get_course_lesson(self):
        # 获取课程章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name


# 章节
class Lesson(models.Model):
    # 因为一个课程对应很多章节。所以在章节表中将课程设置为外键。
    # 作为一个字段来让我们可以知道这个章节对应那个课程
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        # 获取章节视频
        return self.video_set.all()


# 每章视频
class Video(models.Model):
    # 因为一个章节对应很多视频。所以在视频表中将章节设置为外键。
    # 作为一个字段来存储让我们可以知道这个视频对应哪个章节.
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    url = models.CharField(max_length=200, default='', verbose_name=u"访问地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}章节的视频 >> {1}'.format(self.lesson, self.name)


# 课程资源
class CourseResource(models.Model):
    # 因为一个课程对应很多资源。所以在课程资源表中将课程设置为外键。
    # 作为一个字段来让我们可以知道这个资源对应那个课程
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    # 这里定义成文件类型的field，后台管理系统中会直接有上传的按钮。
    # FileField也是一个字符串类型，要指定最大长度。
    download = models.FileField(
        upload_to="course/resource/%Y/%m",
        verbose_name=u"资源文件",
        max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程的资源: {1}'.format(self.course, self.name)