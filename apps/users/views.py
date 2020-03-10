from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination import Paginator, PageNotAnInteger

from apps.users.forms import LoginForm, UploadImageForm, UserInfoForm, UpdatePwdForm, DeletUserFavForm
from apps.operations.models import UserCourse, UserFavorite, UserMessage
from apps.organizations.models import Teacher, CourseOrg
from apps.courses.models import Course


class MessageView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        user_message = UserMessage.objects.filter(user=request.user).order_by('-add_time')
        for message in user_message:
            message.has_read = True
            message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(user_message, request=request, per_page=5)

        # 需要特别注意，此时org_list已经不再是QuerySet,将数据库信息封装进了xx.object_list，所以在前端需要修改命名格式
        user_message = p.page(page)

        return render(request, 'usercenter-message.html', {
            "user_message": user_message,
        })


class FavOrgView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        user_fav_set = UserFavorite.objects.filter(user=request.user, fav_type=2)
        fav_course_id = [user_fav.fav_id for user_fav in user_fav_set]
        fav_orgs = CourseOrg.objects.filter(id__in=fav_course_id)
        return render(request, 'usercenter-fav-org.html', {
            'fav_orgs': fav_orgs,
            'active': 'orgs'
        })


class FavCoursesView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        user_fav_set = UserFavorite.objects.filter(user=request.user, fav_type=1)
        fav_course_id = [user_fav.fav_id for user_fav in user_fav_set]
        fav_courses = Course.objects.filter(id__in=fav_course_id)
        return render(request, 'usercenter-fav-course.html', {
            'fav_courses': fav_courses,
            'active': 'courses'
        })


class FavTeacherView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        user_fav_set = UserFavorite.objects.filter(user=request.user, fav_type=3)
        fav_teacher_id = [user_fav.fav_id for user_fav in user_fav_set]
        fav_teacher = Teacher.objects.filter(id__in=fav_teacher_id)
        return render(request, 'usercenter-fav-teacher.html', {
            'fav_teacher': fav_teacher,
            'active': 'teachers'
        })


class CoursesView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        user_courses = UserCourse.objects.filter(user_id=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
        })


class UpdatePwdView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        update_pwd_form = UpdatePwdForm(request.POST)
        if update_pwd_form.is_valid():
            new_pwd = update_pwd_form.cleaned_data['password1']
            user = request.user
            user.set_password(new_pwd)
            user.save()
            login(request, user)
            return JsonResponse({
                'status': 'success'
            })
        return JsonResponse(update_pwd_form.errors)


class UploadImageView(LoginRequiredMixin, View):
    login_url = '/login/'

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
