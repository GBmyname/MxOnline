from django.views import View
from django.http import JsonResponse

from apps.operations.models import UserFavorite, CourseComments
from apps.operations.forms import AddFavForm, AddCommentForm
from apps.courses.models import Course
from apps.organizations.models import CourseOrg, Teacher


class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'fail',
                'msg': '用户未登陆'
            })

        user_comment_form = AddCommentForm(request.POST)
        if user_comment_form.is_valid():
            course = user_comment_form.cleaned_data['course']
            comments = user_comment_form.cleaned_data['comments']

            existed_records = CourseComments.objects.filter(user=request.user,
                                                            course=course, comments=comments)
            if not existed_records:
                user_comment_form.save()

                return JsonResponse({
                    'status': 'success',
                })
            else:
                return JsonResponse({
                    'status': 'fail',
                    'msg': 'Duplicate input'
                })


        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '参数错误'
            })


class AddFavView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'fail',
                'msg': '用户未登陆'
            })

        user_fav_form = AddFavForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data['fav_id']
            fav_type = user_fav_form.cleaned_data['fav_type']

            existed_records = UserFavorite.objects.filter(user=request.user,
                                                          fav_id=fav_id, fav_type=fav_type)
            if existed_records:
                existed_records.delete()

                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 2:
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_nums -= 1
                    org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()

                return JsonResponse({
                    'status': 'success',
                    'msg': '收藏'
                })
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()
                return JsonResponse({
                    'status': 'success',
                    'msg': '已收藏'
                })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '参数错误'
            })
