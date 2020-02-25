from django.db import models

from apps.users.models import BaseModel
from apps.organizations.models import Teacher,CourseOrg

# 设计表结构重点
'''
实体1 <关系> 实体2
课程 <> 章节 
章节 <> 视频 
课程 <> 课程资料

'''


class Course(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='任课教师')
    course_org=models.ForeignKey(CourseOrg,on_delete=models.CASCADE,verbose_name='课程所属机构',blank=True,null=True)
    name = models.CharField(verbose_name='课程名', max_length=50)
    desc = models.CharField(verbose_name='课程描述', max_length=300)
    learn_time = models.IntegerField(default=0, verbose_name='学习时长（分钟）')
    degree = models.CharField(verbose_name='难度', choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2)
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.CharField(default=u'后端开发', max_length=20, verbose_name='课程类别')
    tag = models.CharField(default='', verbose_name='课程标签', max_length=10)
    youneed_know = models.CharField(default='', max_length=300, verbose_name='课程须知')
    teacher_tell = models.CharField(default='', max_length=300, verbose_name='老师告诉你')
    is_classic=models.BooleanField(default=False,verbose_name='是否是经典课程')

    detail = models.TextField(verbose_name='课程详情')  # TextField不限制长度
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name='封面图', max_length=100)

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # on_delet(必填)表示外建被删除后，当前数据如何处理
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    learn_time = models.IntegerField(default=0, verbose_name='学习时长（分钟）')

    class Meta:
        verbose_name = '课程章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名称')
    learn_time = models.IntegerField(default=0, verbose_name='学习时长（分钟）')
    url = models.CharField(max_length=200, verbose_name=u'访问地址')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    file = models.FileField(upload_to='courses/resourse/%Y/%m', verbose_name='下载地址', max_length=200)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
