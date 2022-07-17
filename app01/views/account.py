from http.client import HTTPResponse
import pstats
from app01 import models
from django.shortcuts import render, redirect
from app01.utils.form import LoginForm,AdminModelFormReset

# 登录功能
def login(request):
    """登录"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'login.html',{"form": form})
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
            if not admin_object:
                form.add_error("password","用户名或密码错误")
                return render(request,'login.html',{"form": form})
            else:
            #用户名和密码正确
            # 网站生成随机字符串: 写到用户浏览器随机的cookie中,在写入到sesion中:           
                request.session['info'] = {'id': admin_object.id,'name': admin_object.username}
                return redirect("/admin/list/")
    return render(request,'login.html',{"form": form})


# 注销功能
def logout(request):
    request.session.clear() # 删除的是数据库保存的seesion的信息
    return redirect('/login/')