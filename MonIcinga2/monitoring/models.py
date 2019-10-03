#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


class Groups(models.Model):
    g_name = models.CharField(max_length=70)

    def __str__(self):
        return self.g_name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
        ordering = ['g_name']


class Project(models.Model):
    p_name = models.CharField(max_length=20)

    def __str__(self):
        return self.p_name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['p_name']


class Service(models.Model):
    s_name = models.CharField(max_length=30)

    def __str__(self):
        return self.s_name

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'
        ordering = ['s_name']


class Host(models.Model):
    h_id = models.CharField(max_length=10)
    h_name = models.CharField(max_length=70)
    h_online = models.BooleanField()
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    project = models.ManyToManyField(Project, related_name='project')

    def get_project(self):
        return ",  ".join([str(p) for p in self.project.all()])

    def __str__(self):
        return self.h_name

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
        ordering = ['h_name']


class Common(models.Model):
    """General table for work"""

    host = models.ForeignKey(Host, on_delete=models.CASCADE)  # Host
    service = models.ForeignKey(Service, default=None, on_delete=models.SET_DEFAULT)  # Service
    c_ip = models.CharField(max_length=15)  # IP address
    c_status = models.IntegerField()  # API Status 0-4
    c_table = models.IntegerField()  # Table number in template
    c_time = models.FloatField()  # Table filling time
    c_comment = models.CharField(max_length=100, default='Нет')  # Comments to the service
    c_online = models.BooleanField()  # On/Off service
    c_trable = models.CharField(max_length=20, default='Нет')  # Trouble number

    def __str__(self):
        return '{}: {}'.format(self.host, self.service)

    class Meta:
        verbose_name = 'Канал связи'
        verbose_name_plural = 'Каналы связи'
        ordering = ['host']


class Icinga(models.Model):
    """Icinga Access Settings"""

    username = models.CharField(max_length=15, default='root')
    password = models.CharField(max_length=15, default='root')
    protocol = models.CharField(max_length=10, default='https')
    ip = models.CharField(max_length=15, default='192.168.0.1')
    port = models.CharField(max_length=6, default='5665')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Настройки доступа к Icinga'
        verbose_name_plural = 'Настройки доступа к Icinga'


class Author(models.Model):
    """Authorship"""

    company = models.CharField(max_length=15, default='Нет')
    position = models.CharField(max_length=35, default='Нет')
    name = models.CharField(max_length=30, default='Нет')
    phone = models.CharField(max_length=20, default='Нет')
    email = models.CharField(max_length=20, default='Нет')







