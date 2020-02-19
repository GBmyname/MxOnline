import xadmin

from apps.organizations.models import City, CourseOrg, Teacher


class CityAdmin(object):
    list_display = ['id', 'name', 'desc']
    list_editable = ['name', 'desc']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'tag', 'city']
    list_filter = ['name', 'desc', 'tag', 'city']
    list_editable = ['name', 'desc', 'tag', 'city']
    search_fields = ['name', 'desc', 'tag', 'city']


class TeacherAdmin(object):
    list_display = ['name','work_years','work_company','org']
    list_filter =['name','work_years','work_company','org']
    list_editable =['name','work_years','work_company','org']
    search_fields =['name','work_years','work_company','org']


xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(City, CityAdmin)
