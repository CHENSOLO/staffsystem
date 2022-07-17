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


# 靓号列表
def pretty_num_list(request):

    # # 循环创建300个号码测试使用
    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile="13534013146", price="9999", level="1", status="0")

    # 拿到当前的页数
    pages = int(request.GET.get("page", 1))
    # 每页10条数据
    page_size = 10
    start_page = (pages - 1)*page_size
    end_page = (pages*page_size)

    # 存储搜索得到数据
    data_dict = {}
    # 获取前端q=?的值
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data
    # 1. 从数据库提取数据并渲染到前端模板,order_by顺序
    pretty_data = models.PrettyNum.objects.filter(
        **data_dict).order_by("-level")[start_page:end_page]

    # 计算数据库总共有多少条数据
    total_count = models.PrettyNum.objects.filter(
        **data_dict).order_by("-level").count()
    # 总数据除每页10条的数据，可以得到总共多少页
    total_page_count, div = divmod(total_count, page_size)
    # 数据除的余>0,进1
    if div:
        total_page_count + 1

    """       
    <li><a href="?page=2">2</a></li>
    <li><a href="?page=1">1</a></li>
    <li><a href="?page=3">3</a></li>
    <li><a href="?page=4">4</a></li>
    <li><a href="?page=5">5</a></li>"""
    # 页码值
    page_str_dict = []

    # 首页
    prev = '<li><a href="?page=1">首页</a></li>'.format(pages)
    page_str_dict.append(prev)

    # 上一页
    if pages > 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(pages-1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    page_str_dict.append(prev)

    # 计算出，显示当前页的前5页以及后5页
    plus = 5
    if total_page_count <= 2 * plus + 1:
        # 数据库中的数据比较少 没有达到11页
        star_pages = 1
        end_pages = total_page_count
    else:
        # 数据库中的数据<5页时
        if pages <= plus:
            star_pages = 1
            end_pages = 2 * plus + 1
        else:
            # 当前页>5的时
            if (pages + plus) > total_page_count:
                star_pages = total_page_count - 2 * plus
                end_pages = total_page_count
            else:
                star_pages = pages - plus
                end_pages = pages + plus

    # 因为range的值最后一个数是取不到的 所以+1
    for i in range(star_pages, end_pages):
        if i == pages:
            page_size = '<li class="active"><a href="?page={}">{}</a></li>'.format(
                i, i)
        else:
            page_size = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_dict.append(page_size)

    # 下一页
    if pages < total_page_count:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(pages+1)
    else:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(total_page_count)
    page_str_dict.append(prev)

    # 尾页
    prev = '<li><a href="?page={}">尾页</a></li>'.format(total_page_count)
    page_str_dict.append(prev)

    # 页码数量
    page_string = mark_safe("".join(page_str_dict))
    return render(request, "pretty_num_list.html", {"pretty_data": pretty_data, "search_data": search_data, "page_string": page_string})


# 新建手机号码
def pretty_num_add(request): 

    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, "pretty_num_add.html", {"form": form})

    else:
        # 1.获取用户提交的post数据
        form = PrettyModelForm(data=request.POST)
        # 2.数据验证
        if form.is_valid():
            # 3.保存到数据库
            form.save()
            # 4.重定向回到靓号列表页面
            return redirect("/pretty_num/list/")
        else:
            # 5.如果校验失败，在上面提示错误的信息
            return render(request, "pretty_num_add.html", {"form": form})

# 编辑靓号
def pretty_num_edit(request, nid):
    # 1.首先拿到ID
    row_obj = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = PrettyModelFormEdit(instance=row_obj)
        # 2.数据库数据渲染传到前端页面
        return render(request, 'pretty_num_edit.html', {"form": form})
    else:
        # 3.提交数据,前端页面通过post方法请求，需要拿到post请求的数据
        form = PrettyModelFormEdit(data=request.POST, instance=row_obj)
        # 4.校验数据
        if form.is_valid():
            form.save()
            return redirect("/pretty_num/list/")
        else:
            return render(request, 'pretty_num_edit.html', {"form": form})

# 删除靓号
def pretty_num_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty_num/list/")
