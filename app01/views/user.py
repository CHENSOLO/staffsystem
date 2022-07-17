from dataclasses import dataclass, fields
from ntpath import join
from pyexpat import model
from re import L
from statistics import mode
from charset_normalizer import utils
from django.shortcuts import render, redirect
from app01 import models
from django import forms
from django.utils.safestring import mark_safe
from app01.utils.Pagination import Pagination
from app01.utils.form import UserModelForm, PrettyModelForm, PrettyModelFormEdit
# Create your views here.



def user_list(request):

    # 获取数据库的数据
    query_set = models.UserInfo.objects.all()
    # 调用工具类
    page_object = Pagination(request, query_set, page_size=1)
    context = {
        "query_set": page_object.page_queryset,
        "page_string": page_object.html(),
    }


    return render(request, 'user_list.html',context)


def user_add(request):
    # 从数据库取出数据渲染到前端页面
    if request.method == 'GET':
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }

        return render(request, 'user_add.html', context)

    # 获取前端输入的数据
    user = request.POST.get("user")
    passwd = request.POST.get("passwd")
    age = request.POST.get("age")
    money = request.POST.get("money")
    time = request.POST.get("time")
    sex = request.POST.get("sex")
    dp = request.POST.get("dp")

    # 将前端输入的数据存储到数据库
    models.UserInfo.objects.create(
        name=user, password=passwd, age=age, account=money, create_time=time, gender=sex, depart_id=dp)
    return redirect('/user/list')


# ModelForm 示例 ####################################################3



def user_model_form_add(request):
    # 添加用户(ModelForm版本):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})

    # 用户POST提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    else:
        # 校验失败了(在页面上显示错误的信息)
        return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    row_obj = models.UserInfo.objects.filter(id=nid).first()
    # 编辑用户
    # 根据ID提取数据
    if request.method == 'GET':
        form = UserModelForm(instance=row_obj)
    else:
        # 数据校验
        # 1.用户用POST提交数据
        form = UserModelForm(data=request.POST, instance=row_obj)
        # 2.数据校验
        if form.is_valid():
            # 3.更新到数据库
            form.save()
        # 4.返回到用户列表
            return redirect('/user/list')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    # 删除数据
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')

