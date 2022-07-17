from django.core.exceptions import ValidationError
from app01 import models
from django import forms
from django.utils.safestring import mark_safe
from app01.utils.bootstrap import BootStrapModelForm,BootStrapForm
from app01.utils.encrypt import md5
class UserModelForm(BootStrapModelForm):
    
    # 单独对每一个字段做校验(例如)
    name = forms.CharField(min_length=5, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account',
                  'create_time', 'gender', 'depart']


# 靓号管理的ModelForm
class PrettyModelForm(BootStrapModelForm):

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile','price','level','status']
        fields = "__all__"

    # 对mobile做验证 方式1：
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误'),],
    # )

    # 对mobile做验证 方式2：
    def clean_mobile(self):
        # 当前编辑的哪一行的ID
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        else:
            return txt_mobile


# 编辑靓号的ModelForm
class PrettyModelFormEdit(BootStrapModelForm):
    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']
    # 对字段做设置
    mobile = forms.CharField(disabled=True, label="手机号码")


# 管理员的ModelForm
class AdminModelForm(BootStrapModelForm):
    # 添加一个字段
    class Meta:
        model = models.Admin
        fields = ['username','password','confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True),
            "confirm_password": forms.PasswordInput(render_value=True),
        } 
        # 确认密码匹配
    def clean_confirm_password(self):
        pwd = md5(self.cleaned_data.get("password"))
        confirm_pwd = md5(self.cleaned_data.get("confirm_password"))
        if confirm_pwd != pwd: 
            raise ValidationError("密码不一致")
        # 此字段，返回什么数据库就是什么
        return confirm_pwd

# 管理员的编辑
class AdminModelFormEdit(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']
    # 对字段做设置
    # mobile = forms.CharField(disabled=True, label="姓名")


# 管理员密码的重置功能
class AdminModelFormReset(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username','password','confirm_password']
        widgets = {
        "password": forms.PasswordInput(render_value=True),
        "confirm_password": forms.PasswordInput(render_value=True),   #render_value=true是隐藏密码
}
    username = forms.CharField(disabled=True, label="用户名称")

    # 确认密码匹配
    def clean_confirm_password(self):
        pwd = md5(self.cleaned_data.get("password"))
        confirm_pwd = md5(self.cleaned_data.get("confirm_password"))

        # 去数据库校验当前密码和新输入的密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, confirm_password=confirm_pwd).exists()
        if exists:
            raise ValidationError("密码不能与之前的一致")
        if confirm_pwd != pwd:
            raise ValidationError("密码不一致")
        # 此字段，返回什么数据库就是什么
        return confirm_pwd


# 登录管理
class LoginForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username','password']
        widgets = {
        "username": forms.TextInput(),
        "password": forms.PasswordInput(render_value=True),
}
    username = forms.CharField(label="用户名称")
    password = forms.CharField(label="密码")


# class LoginForm(BootStrapForm):
#     class Meta:
#         model = models.Admin
#         fields = ['username','password']
#         widgets = {
#         "password": forms.PasswordInput(render_value=True),
#         "confirm_password": forms.PasswordInput(render_value=True),   #render_value=true是隐藏密码
# }

#     username = forms.CharField(label="用户名",required=True) # required=True必填不能为空
#     password = forms.CharField(label="密码",required=True)