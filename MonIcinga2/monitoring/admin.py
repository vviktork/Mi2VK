#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sessions.models import Session
from django.contrib import messages

from .models import Groups, Project, Host, Service, Common, Icinga
from .base_change import base_filling


admin.site.site_url = 'http://127.0.0.1:8000/monitoring/'
admin.site.site_header = 'Панель Администратора'
admin.site.disable_action('delete_selected')
admin.site.unregister(Group)

def check_active(self, request, queryset):
    """Database update"""

    _ok = 'Выполнено обновление Базы Данных'
    _err = 'Ошибка обновления Базы Данных'
    try:
        _update = base_filling()
        if _update == True:
            messages.info(request, _ok)
        else:
            messages.error(request, _err)

    except Exception as e:
        print(_err + ' -', e)
        messages.error(request, _err)

admin.site.add_action(check_active, 'Обновление Базы Данных (выбрать все)')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'expire_date')
    list_filter = ('session_data',)
    fields = ('expire_date',)
    actions = None


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('g_name',)
    list_filter = ('g_name',)
    search_fields = ('g_name',)
    actions = None


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ('h_name', 'get_project', 'h_id', 'h_online')
    list_filter = ('h_name',)
    fields = ('project',)
    search_fields = ('h_name',)
    actions = None


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('p_name',)
    actions = None


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('s_name',)
    actions = None


@admin.register(Common)
class CommonAdmin(admin.ModelAdmin):
    list_display = ('host', 'service', 'c_ip', 'c_trable', 'c_comment', 'c_table')
    fields = ('c_comment', 'c_trable')
    actions = None


@admin.register(Icinga)
class IcingaAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'protocol', 'ip', 'port')
    actions = None
