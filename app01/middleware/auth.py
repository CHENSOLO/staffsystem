from django.shortcuts import HttpResponse,redirect
from django.utils.deprecation import MiddlewareMixin



class AuthMiddleware(MiddlewareMixin):
    """中间件 1"""
    def process_request(self, request):

        # 0.排除那些不需要登录就能访问的页面
        #request.path_info # 获取当前用户请求的url /login/
        if request.path_info == "/login/":
            return
        # 1.读取当前访问的用户的session信息，如果能读到，说明已经登陆过
        info_dict = request.session.get("info")
        if info_dict:
            return
        else:
        # 2.没有登陆过,重新回到登陆页面
            # return HttpResponse("请登录")
            return redirect('/login/')
        # 如果方法中没有返回值（返回none），继续向后走
        # 如果有返回值HttpResponse render redirect
    #     print("M1.process_request")
    #     return HttpResponse("无权访问")

    # def process_response(self,request,response):
    #     print("M1.process_response")
    #     return response

# class M2(MiddlewareMixin):
#     """中间件 1"""
#     def process_request(self, request):
#         print("M2.process_request")

#     def process_response(self,request, response):
#         print("M2.process_response")
#         return response
