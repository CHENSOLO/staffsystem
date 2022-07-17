from dataclasses import dataclass, fields
from ntpath import join
from pyexpat import model
from statistics import mode
from charset_normalizer import utils
from django.shortcuts import render, redirect
from app01 import models
from django import forms
from django.utils.safestring import mark_safe
from app01.utils.Pagination import Pagination
from app01.utils.form import UserModelForm, PrettyModelForm, PrettyModelFormEdit
# Create your views here


def depart_list(request):
    """部门列表"""

    # 将数据库的数据取出来并展示
    data_list = models.Department.objects.all()
    page_obj = Pagination(request,data_list,page_size=1)
    context = {
        "data_list": page_obj.page_queryset,
        "page_string": page_obj.html()
    }
    # print(data_list)
    return render(request, 'depart_list.html', context)
    

def depart_add(request):
    # 添加部门
    if request.method == 'GET':
        return render(request, 'depart_add.html')
    else:
        title = request.POST.get("title")
        models.Department.objects.create(title=title)
        # 重定向回到部门列表
        return redirect('/depart/list')


def depart_delete(request):
    # 获取数据
    nid = request.GET.get("nid")
    # print(nid)
    # 删除数据
    models.Department.objects.filter(id=nid).delete()
    # 重定向回到部门列表
    return redirect('/depart/list')


def depart_edit(request, nid):
    # 编辑部门
    if request.method == 'GET':
        # 根据nid获取他的数据[obj,]
        row_object = models.Department.objects.filter(id=nid).first()
        # print(row_object.id,row_object.title)
        return render(request, 'depart_edit.html', {"row_object": row_object})

    # 获取用户提交的标题
    title = request.POST.get("title")

    # 根据id找到数据库中的数据更新到数据库
    models.Department.objects.filter(id=nid).update(title=title)

    # 重定向回到list页面
    return redirect('/depart/list')

