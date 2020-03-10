from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')  # 不要直接调用now（），否则会在编译时候直接赋值

    class Meta:
        abstract = True  # 抽象类不生成表,仅用于继承


GENDER_CHOICES = (
    ('male', '男'),
    ('female', '女')
)


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(verbose_name='性别', choices=GENDER_CHOICES, max_length=6)
    address = models.CharField(max_length=500, verbose_name='地址', default='')
    mobile = models.CharField(max_length=11, verbose_name='手机号码')
    image = models.ImageField(upload_to='head_image/%Y/%m', default='default.jpg', verbose_name='用户头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username

    def has_not_read_message(self):
        user_message=self.usermessage_set.filter(has_read=False)
        return user_message
