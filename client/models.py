from django.db import models

# Create your models here.
class Client(models.Model):
    ip = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    online_time = models.DateTimeField()
    username = models.CharField(max_length=255)

    class Meta:
        db_table = 'client'


class client_setting(models.Model):
    ip = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    class Meta:
        db_table = 'set'


class user(models.Model):
    username = models.CharField(max_length=255, verbose_name="账号")
    password = models.CharField(max_length=255, verbose_name="密码")


class picture(models.Model):
    path = models.CharField(max_length=255, verbose_name="图片名称")
