#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class MonFinForm(forms.Form):

    trable = forms.CharField(label='Заявка:', max_length=5)
    comment = forms.CharField(label='Сообщение:', max_length=99)
