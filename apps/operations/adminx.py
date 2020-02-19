import xadmin

from apps.operations.models import UserAsk, UserCourse, UserFavorite, UserMessage, CourseComments


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name']
    list_editable = ['name', 'mobile', 'course_name']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name']


class UserCourseAdmin(object):
    list_display = ['user', 'course']
    list_editable = ['user', 'course']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course']


class UserFavoriteAdmin(object):
    list_display = ['user.name', 'fav_id', 'fav_type']
    list_editable = ['user.name', 'fav_id', 'fav_type']
    search_fields = ['user.name', 'fav_id', 'fav_type']
    list_filter = ['user.name', 'fav_id', 'fav_type']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read']
    list_editable = ['user', 'message', 'has_read']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments']
    list_editable = ['user', 'course', 'comments']
    search_fields = ['user', 'course', 'comments']
    list_filter = [ 'course__name', 'comments']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
