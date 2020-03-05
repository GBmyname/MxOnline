import xadmin

from apps.courses.models import Course,Video,Lesson,CourseResource,CourseTag

class CourseTagAdmin(object):
    list_display=['course','tag']
    search_fields=['course','tag']
    list_filter=['course','tag']
    lister_editable=['course','tag']

class CourseAdmin(object):
    list_display=['name','desc','detail','degree','students']
    search_fields=['name','desc','detail','degree','students']
    list_filter=['name','desc','detail','degree','students']
    lister_editable=['desc','degree']

class LessonAdmin(object):
    list_display = ['name',  'course']
    search_fields = ['name', 'course']
    list_filter = ['name', 'course']
    lister_editable = ['name',  'course']

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
xadmin.site.register(CourseTag,CourseTagAdmin)