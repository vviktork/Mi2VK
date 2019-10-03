#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import MonFinView, AjaxMon


urlpatterns = [
    url(r'^$', MonFinView.as_view()),
    url(r'^$', AjaxMon.as_view()),
]