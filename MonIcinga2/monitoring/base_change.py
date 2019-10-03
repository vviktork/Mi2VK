#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base_request import BaseRequest


def base_filling():
    """Database update"""

    rezult = True
    bd_error = []

    remember_base, old_base = BaseRequest.remember_db(None)
    bd_error += [remember_base]
    print('Cоздание шаблона базы -', remember_base)

    error_del = base_del()
    bd_error += [error_del]
    print('Удаление таблиц -', error_del)

    group_api, group_base = BaseRequest.group_base(None)
    bd_error += [group_api, group_base]
    print('Заполнение таблицы Регионов -', group_api, group_base)

    host_api, host_base = BaseRequest.host_base(None)
    bd_error += [host_api, host_base]
    print('Заполнение таблицы Объектов -', host_api, host_base)

    service_api, service_base = BaseRequest.service_base(None)
    bd_error += [service_api, service_base]
    print('Заполнение таблицы Сервисов -', service_api, service_base)

    common_api, common_base = BaseRequest.common_api(None)
    bd_error += [common_api, common_base]
    print('Заполнение таблицы Каналов связи -', common_api, common_base)

    author_base = BaseRequest.author_base(None)
    bd_error += [author_base]
    print('Общее заполнение -', author_base)

    timing_base = BaseRequest.timing_db(None, old_base)
    bd_error += [timing_base]
    print('Синхронизация баз -', timing_base)

    if False in bd_error:
        rezult = False
        print('Ошибка выполнения')
    else:
        print('Выполнено')
    return rezult


def base_del():
    """Delete tables from the database"""

    rezult = True
    error_del = []
    tabl_all = ['group', 'service', 'author']
    for i in tabl_all:
        del_base = BaseRequest.del_data(None, i)
        error_del += [del_base]
    if False in error_del:
        rezult = False
    return rezult



