#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf.urls import url
from monitoring.views import MonFinView, AjaxMon


urlpatterns = [
    url('admin/', admin.site.urls),
    url('login/', auth_views.LoginView.as_view()),
    url(r'^monitoring/$', MonFinView.as_view(), name='form'),
    url(r'^monitoring/ajax/$', AjaxMon.as_view(), name='ajax'),

]
