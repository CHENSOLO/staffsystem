from django.urls import path
from app01.views import depart,user,pretty,admin,account
urlpatterns = [
    #部门管理
    path('depart/list/',depart.depart_list),
    path('depart/add/',depart.depart_add),
    path('depart/delete/',depart.depart_delete),
    #http://127.0.0.1:8000/depart/3/edit/
    path('depart/<int:nid>/edit/',depart.depart_edit),

    #用户管理
    path('user/list/',user.user_list),
    path('user/add/',user.user_add),


    #ModelForm
    path('user/model/form/add',user.user_model_form_add),
    path('user/<int:nid>/edit/',user.user_edit),
    path('user/<int:nid>/delete/',user.user_delete),


    # 靓号管理
    path('pretty_num/list/',pretty.pretty_num_list),
    path('pretty_num/add/',pretty.pretty_num_add),
    path('pretty/<int:nid>/edit/',pretty.pretty_num_edit),
    path('pretty/<int:nid>/delete/',pretty.pretty_num_delete),

    # 管理员管理
    path('admin/list/',admin.admin_list),
    path('admin/add/',admin.admin_add),
    path('admin/<int:nid>/edit/',admin.admin_edit),
    path('admin/<int:nid>/delete/',admin.admin_delete),
    path('admin/<int:nid>/reset/',admin.admin_reset),

    # 登录界面
    path('login/',account.login),
    path('logout/',account.logout),


]
