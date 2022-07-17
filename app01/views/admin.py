from urllib import request
from charset_normalizer import models
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.Pagination import Pagination
from app01.utils.form import AdminModelForm, AdminModelFormEdit, AdminModelFormReset
from django.core.exceptions import ValidationError

# 管理员列表
def admin_list(request):

    # # 检查用户是否已登录，已登录正常使用，未登录，跳转回到登陆页面
    # # 用户发来请求,获取cookie随机字符串，拿着随机字符串看看session中有没有该值
    info = request.session["info"]
    print(info)
    # if not info:
    #     return redirect('/login/')


    # 搜索
    # 存储搜索得到数据
    data_dict = {}
    # 获取前端q=?的值
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data

    # 分页
    queryset = models.Admin.objects.filter(**data_dict)   # 根据搜索条件去搜索
    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
        "search_data": search_data
    }

    return render(request, 'admin_list.html', context)


# 添加管理员
def admin_add(request):
    form = AdminModelForm()
    title = "新建管理员"
    if request.method == 'GET':
        return render(request, 'change.html', {"form": form, "title": title})
    else:
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/list')
    return render(request, 'change.html', {"form": form, "title": title})


# 修改管理员
def admin_edit(request, nid):

    title = '修改管理员'
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {"msg": "数据不存在！ "})
    if request.method == 'GET':
        form = AdminModelFormEdit(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})
    else:
        # instance=row_object就是默认传递过来的数据
        form = AdminModelFormEdit(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect("/admin/list")
        else:
            return render(request, 'cha nge.html', {"form": form, "title": title})


# 删除管理员
def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


# 重置管理员的密码
def admin_reset(request, nid):
    title = "重置密码"
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {"msg": "数据不存在！ "})
    if request.method == 'GET':
        form = AdminModelFormReset( instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})
    else:
        form = AdminModelFormReset(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect("/admin/list")
    return render(request, 'change.html', {"form":form ,"title": title})
