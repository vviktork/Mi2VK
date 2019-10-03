#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import MonFinForm

from .processing_icinga import processing_r
from .processing_base import processing_modal
from .data_test import templates_test


test_on = True  # For template test
VERSION = '1.00'


class MonFinView(LoginRequiredMixin, FormView):
    """View for the main service"""

    form_class = MonFinForm
    template_name = 'monitor/Mon.html'
    success_url = reverse_lazy('form')

    def __init__(self):
        self.html = '/monitoring/'

    def get(self, request, *args, **kwargs):
        context = super(MonFinView, self).get(self, request, *args, **kwargs)
        values_get ={}
        values_get.update(request.GET.items())
        if values_get != {}:
            return HttpResponseRedirect(self.html)
        return context

    def post(self, request, *args, **kwargs):
        context = super(MonFinView, self).post(self, request, *args, **kwargs)
        values_post ={}
        values_post.update(request.POST.items())
        error_base = processing_modal(values_post)
        if error_base == True:
            return HttpResponseRedirect(self.html)
        elif error_base == False:
            return HttpResponse(status=502)
        return context

    def get_context_data(self, **kwargs):
        """We pass data to the project"""

        context = super(MonFinView, self).get_context_data()
        if test_on == False:
            rezult_1, rezult_2, rezult_3, proc_error, title_1, title_2, titles_10, data_p, critical = processing_r()
            context['table_1'] = rezult_1
            context['table_2'] = rezult_2
            context['table_3'] = rezult_3
            context['titles_10'] = titles_10
            context['data_p'] = data_p
            context['critical'] = critical
        else:  # Test data for the template
            table_1, table_23, proc_error, title_1, title_2, critical = templates_test()
            context['table_1'] = table_1
            context['table_2'] = table_23
            context['table_3'] = table_23
            context['critical'] = critical
            context['data_p'] = {'company': '',
                                 'position': '',
                                 'name': 'Копенок Виктор',
                                 'phone': '',
                                 'email': 'vkopenok@mail.ru'
                                 }
        context['titles_1'] = title_1
        context['titles'] = title_2
        context['connect'] = proc_error
        context['version'] = VERSION
        return context

    def get_initial(self):
        return None

    def form_valid(self, form):
        context = super(MonFinView, self).form_valid(form)
        return context


class AjaxMon(LoginRequiredMixin, View):
    """View for the modal"""

    def post(self, request):
        return JsonResponse({})

    def get(self, request):
        return JsonResponse({})

