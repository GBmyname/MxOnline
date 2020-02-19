import xadmin

from apps.courses.models import Course,Video,Lesson,CourseResource

class CourseAdmin(object):
    list_display=['name','desc','detail','degree','learn_time','students']
    search_fields=['name','desc','detail','degree','students']
    list_filter=['name','desc','detail','degree','learn_time','students']
    lister_editable=['desc','degree']

class LessonAdmin(object):
    list_display = ['name',  'learn_time', 'course']
    search_fields = ['name',  'learn_time', 'course']
    list_filter = ['name',  'learn_time', 'course']
    lister_editable = ['name',  'learn_time', 'course']

class VideoAdmin(object):
    list_display = ['name', 'learn_time', 'url','lesson']
    search_fields = ['name', 'learn_time', 'url','lesson']
    list_filter = ['name', 'learn_time', 'url','lesson']
    lister_editable = ['name', 'learn_time', 'url','lesson']

class CourseResourceAdmin(object):
    list_display = ['name',  'file', 'course']
    search_fields = ['name',  'file', 'course']
    list_filter = ['name',  'file', 'course']
    lister_editable = ['name',  'file', 'course']

xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)