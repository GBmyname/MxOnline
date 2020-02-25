from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse

from apps.users.forms import LoginForm

class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        # 表单验证
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # 验证用户是否存在
            user = authenticate(username=user_name, password=password)
            if user is not None:
                login(request, user)  # 配置登陆，session/cookie
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request,'login.html',{'msg':'用户名或密码错误','login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})
