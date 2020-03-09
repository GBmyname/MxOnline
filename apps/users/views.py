from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.users.forms import LoginForm, UploadImageForm, UserInfoForm,UpdatePwdForm

class UpdatePwdView(View):
    def post(self,request,*args,**kwargs):
        update_pwd_form=UpdatePwdForm(request.POST)
        if update_pwd_form.is_valid():
            new_pwd=update_pwd_form.cleaned_data['password1']
            user=request.user
            user.set_password(new_pwd)
            user.save()
            login(request,user)
            return JsonResponse({
                'status':'success'
            })
        return JsonResponse({
            'status':'fail',
            'msg':update_pwd_form.errors
        })




class UploadImageView(View):
    def post(self, request, *args, **kwargs):
        upload_image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if upload_image_form.is_valid():
            upload_image_form.save()
            return JsonResponse({
                'status': 'success',
            })
        return JsonResponse({
            'status': 'fail',
        })


class InfoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, 'usercenter-info.html', {
            'user': user,

        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                'status': 'success'
            })
        return JsonResponse(user_info_form.errors)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        next = request.GET.get('next', '')
        return render(request, 'login.html', {
            'next': next
        })

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

                next = request.GET.get('next', '')
                if next:
                    return HttpResponseRedirect(next)

                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})
