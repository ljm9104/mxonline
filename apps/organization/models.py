from datetime import datetime

from django.db import models

# Create your models here.
'''
课程是属于机构的, 机构有机构类别，城市等字段。讲师实体。
我要学习的提交表单会与用户关联，存放在机构。
其中课程数，学习人数可以动态统计。机构地址，机构经典课程。

机构讲师，机构课程可以通过外键获取到, 不保存到机构中。

创建了三张表：分别是城市，课程机构，讲师。
'''


# 城市字典
class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"城市")
    # 城市描述：备用不一定展示出来
    desc = models.CharField(max_length=200, verbose_name=u"描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 课程机构
class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"机构名称")
    # 机构描述，后面会替换为富文本展示
    desc = models.TextField(verbose_name=u"机构描述")
    ORG_CHOICES = (("pxjg", u"培训机构"), ("gx", u"高校"), ("gr", u"个人"),)
    # 机构类别:
    category = models.CharField(max_length=20, choices=ORG_CHOICES, verbose_name=u"机构类别", default="pxjg")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(
        upload_to="org/%Y/%m",
        verbose_name=u"logo",
        max_length=100)
    address = models.CharField(max_length=150, verbose_name=u"机构地址")
    # 一个城市可以有很多课程机构，通过将city设置外键，变成课程机构的一个字段
    # 可以让我们通过机构找到城市
    city = models.ForeignKey(CityDict, verbose_name=u"所在城市")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    # 当学生点击学习课程，找到所属机构，学习人数加1
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    # 当发布课程就加1
    course_nums = models.IntegerField(default=0, verbose_name=u"课程数")

    class Meta:
        verbose_name = u"课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 讲师
class Teacher(models.Model):
    # 一个机构会有很多老师，所以我们在讲师表添加外键并把课程机构名称保存下来
    # 可以使我们通过讲师找到对应的机构
    org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构")
    name = models.CharField(max_length=50, verbose_name=u"教师名称")
    work_years = models.IntegerField(default=0, verbose_name=u"工作年限")
    work_company = models.CharField(max_length=50, verbose_name=u"就职公司")
    work_position = models.CharField(max_length=50, verbose_name=u"公司职位")
    points = models.CharField(max_length=50, verbose_name=u"教学特点")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    image = models.ImageField(
        default='',
        upload_to="teacher/%Y/%m",
        verbose_name=u"头像",
        max_length=100)

    class Meta:
        verbose_name = u"教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



