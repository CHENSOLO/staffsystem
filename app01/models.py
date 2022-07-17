from urllib import request
from django.db import models

# Create your models here.

# 管理员
class Admin(models.Model):
    """管理员"""
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)
    confirm_password = models.CharField(verbose_name="确认密码",max_length=64,default="")


class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='标题',max_length=32)
    
    def __str__(self) -> str:
        return self.title

class UserInfo(models.Model):


    """员工表"""
    name = models.CharField(verbose_name='姓名',max_length=16)
    password = models.CharField(verbose_name='密码',max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额', max_digits=10,decimal_places=2,default=0)
#    create_time = models.DateTimeField(verbose_name='入职时间')
    create_time = models.DateField(verbose_name='入职时间')

    # 无约束
    #depart_id = models.BigIntegerField(verbose_name='部门id')

    # 1.有约束
    # - to，与那张表有关联
    # - to_field,表中的那一列关联
    # 2. django自动
    #   - 写的depart
    #   - 生成数据列 depart_id
    # 3.1 on_delete=models.CASCADE 属于级联删除,部门表被删除,员工表也会被删除掉。
    # depart = models.ForeignKey(to='Department',to_field='id',on_delete=models.CASCADE)
    # 3.2 置空 null=True,blank=True 相当于部门表被删除，员工表的员工都变成置空不会被删除
    depart = models.ForeignKey(verbose_name='部门',to='Department',null=True,blank=True,to_field='id',on_delete=models.CASCADE)

    # 4. 性别 在django中的约束
    gender_choices = (
        (1,'男'),
        (2,'女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别',choices=gender_choices)

class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号",max_length=11)
    # 想要允许为空 null=True，blank=True
    price = models.IntegerField(verbose_name="价格",default=0)

    level_choice = (
        (1,"1级"),
        (2,"2级"),
        (3,"3级"),
        (4,"4级"),
        (5,"5级"),
    )

    status_choice = (
        (0,"未启用"),
        (1,"已启用"),
    )

    level = models.SmallIntegerField(verbose_name="级别",choices=level_choice,default=0)
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choice,default=0)