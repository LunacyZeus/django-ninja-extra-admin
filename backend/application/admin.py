# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.text import capfirst
from collections import OrderedDict
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin

#from djcelery.admin import IntervalSchedule,CrontabSchedule,PeriodicTask,PeriodicTaskAdmin
# Register your models here.

#admin.autodiscover()
#from django_q.admin import ScheduleAdmin, TaskAdmin, FailAdmin
#from django_q.models import Schedule, Success, Failure


class MyAdminSite(admin.AdminSite):
    site_header = '后台管理'

admin_site = MyAdminSite()
admin_site.enable_nav_sidebar = False#禁用nav_sidebar

def find_model_index(name):
    count = 0
    for model, model_admin in admin_site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        templateresponse = func(*args, **kwargs)
        for app in templateresponse.context_data['app_list']:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return templateresponse

    return inner

"""
这里使用一个函数修饰符来使django支持根据models register顺序来显示
"""
registry = OrderedDict()
registry.update(admin_site._registry)
admin_site._registry = registry
admin_site.index = index_decorator(admin_site.index)
admin_site.app_index = index_decorator(admin_site.app_index)

admin_site.register(User,UserAdmin)
admin_site.register(Group,GroupAdmin)


#admin_site.register(Schedule, ScheduleAdmin)
#admin_site.register(Success, TaskAdmin)
#admin_site.register(Failure, FailAdmin)