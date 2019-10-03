#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
from .icinga_api import request_api
from .base_request import BaseRequest


checkout = False

def processing_r():
    """Basis function"""

    proc_error = True
    # Create title template
    title_1, title_2 = title_templates()

    try:
        # Request Icinga
        data_api, error_api = request_api('request')
        table_2 = [i['attrs'] for i in data_api]
        # Request DB
        host, error_base1 = BaseRequest.all_value(None, 'host')
        common, error_base2 = BaseRequest.all_value(None, 'common')
        service, error_base4 = BaseRequest.all_value(None, 'service')
        a_host = BaseRequest.a_host(None)
        # Fusion dict
        table_0, error_1 = combine_dict(host, 'id', common, 'host_id')
        table_1, error_2 = combine_dict(service, 'id', table_0, 'service_id')
        # Primary bringing data to the lists
        object_all = []
        critical = 0
        for val1 in table_1:
            for val2 in table_2:
                if val1['h_id'] == val2['host_name'] and val1['s_name'] == val2['display_name']:
                    # Save to DB
                    error_base6 = BaseRequest.common_change(None, val1, val2)
                    if val1['c_online'] == True and val2['active'] == True:
                        # Create time and status
                        val1_1, time_check, status = time_exit(val1, val2)
                        critical += status
                        # Create trable
                        val1_1['trable_name'] = (val1_1['c_trable'])
                        # Create project
                        m2m_val, error_base7 = BaseRequest.m2m_val(None, 'host', val1['host_id'])

                        project_n = ''
                        for i in m2m_val: project_n += i['p_name'] + ' '
                        val1_1['p_name'] = (project_n)
                        # Create list
                        values_tabl = ['h_name', 'p_name', 's_name', 'state_check', 'c_ip',
                                       'last_now', 'time_check', 'trable_name', 'c_comment', 'id', 'c_table']
                        # Sort list val1_1
                        object_now = []
                        for i in values_tabl:
                            object_now += [val1_1[i]]
                        object_all += [object_now]
        # Secondary bringing data to the lists
        rezult_1, rezult_2, rezult_3, error_10 = rezult_list(object_all, a_host)
        # Data conversion for template
        if error_10 == False:
            rezult_1 = rezult_template(rezult_dict(rezult_1))
            rezult_2 = rezult_template(rezult_dict(rezult_2))
            rezult_3 = rezult_template(rezult_dict(rezult_3))
        else:
            rezult_1 = rezult_2 = rezult_3 = []

        error_all = [error_api, error_base1, error_base2, error_base4, error_1, error_2]
        if [i for i in error_all if i == False] != []: proc_error = False

    except Exception as e:
        if checkout == True:
            print(e, '\nData_api -', error_api, '\nHost -', error_base1, '\nCommon', error_base2,
                '\nService -', error_base4, '\nTable_0 -', error_1, '\nTable_1 -', error_2,
                '\nSave_DB -', error_base6
                  )
        proc_error = False

    return rezult_1, rezult_2, rezult_3, proc_error, title_1, title_2, error_10, a_host, critical

def title_templates():
    """Create titles"""

    text = ['Объект', 'Проект', 'Сервис', 'Статус',
            'Адрес IP', 'Обновлено', 'Время статуса',
            'Заявка', 'Сообщение', '№', ''
            ]
    title_1 = text
    title_2 = []
    title_2 += title_1
    del title_1[7]
    del title_2[5]
    return title_1, title_2

def combine_dict(dict1, val1, dict2, val2): #host, 'id', common, 'host_id'
    """Merger dict"""

    pro_base = True
    dict1_dict2 = []
    try:
        for i in dict1:
            for o in dict2:
                if i[val1] == o[val2]:
                        z = i.copy()
                        z.update(o)
                        dict1_dict2 += [z]
    except Exception as e:
        if checkout == True: print('combine_dict -', e)
        pro_base = False
    return dict1_dict2, pro_base

def time_t(data_t):
    """Sort by the time"""

    ind_time = '%Y,%m,%d,%H,%M'
    data_t = time.strftime(ind_time, time.localtime(data_t)).split(',')
    data_t = [int(i) for i in data_t]
    data_t = datetime.datetime(data_t[0], data_t[1], data_t[2], data_t[3], data_t[4])
    return data_t

def time_delta(t1, t2):
    """The differense time"""

    try:
        t1 = time_t(t1)
        t2 = time_t(t2)
        if t1 >= t2:
            d_t = str(t1 - t2).split(' ')
            d = d_t[0]
        try:
            time_e = d + ' д., ' + d_t[2]
            if int(d) > 100:
                time_e = '> 100 дней'
        except:
            time_e = d_t[0]
    except Exception as e:
        if checkout == True: print('time_delta - Error ', e)
        time_e = 'Error'
    return time_e

def time_exit(val1, val2):
    """Formatting time and status to template"""

    status = 0
    try:
        h_state = int(val2['last_hard_state'])
        time_test = time_delta(val2['last_check'], val2['last_state_change'])
        if h_state == 0:
            time_check = time_delta(val2['last_state_ok'], val2['last_state_change'])
            state_check = 'OK'
        elif h_state == 2:
            time_check = time_delta(val2['last_state_critical'], val2['last_state_change'])
            state_check = 'CRITICAL'
            status = 1
        elif h_state > 2 or h_state == 1:
            time_check = time_test  # 'Нет'
            state_check = 'НЕИЗВЕСТНО'
        # Last update time in title (0:00:00)
        last_check = str(time_t(val2['last_check'])).split(' ')[1]

    except Exception as e:
        if checkout == True: print('time_exit - Error ', e)
        time_check = 'Error'
        state_check = 'Error'
        last_check = 'Error'

    val1['last_now'] = (last_check)
    val1['time_check'] = (time_check)
    val1['state_check'] = (state_check)
    return val1, time_check, status

def rezult_template(data_all):
    """Conversion for template"""

    tabl_data = []
    for key, values in data_all.items():
        for idx, val in enumerate(values):
            if idx == 0:
                k = key.split(',')
                tabl_data += [k + val]
            else:
                tabl_data += [['', ''] + val]
    return tabl_data

def rezult_list(data_r, data):
    """Conversion to the list with"""

    error_data = False
    rezult_1 = []
    rezult_2 = []
    rezult_3 = []
    if len(data['name'].split(' В')) != 3:
        error_data = True
    for i in data_r:
        # Limit 1h
        ind_time = i[6].split(' д., ')
        try:
            ind_time = int(ind_time[0])
        except:
            try:
                ind_time = int(ind_time[0].split(':')[0])
            except:
                ind_time = 1
        # Table 1
        if i[-1] <= 1 and i[3] == 'CRITICAL' and ind_time >= 1:
            del i[-1]
            del i[7]
            rezult_1 += [i]
        # Table 2
        elif i[-1] == 2:
            del i[-1]
            del i[5]
            rezult_2 += [i]
        # Table 3
        elif i[-1] == 3:
            del i[-1]
            del i[5]
            rezult_3 += [i]
    return rezult_1, rezult_2, rezult_3, error_data

def rezult_dict(data_r):
    """Conversion list to dict"""

    dict_r = {}.fromkeys([(i[0] + ',' + i[1]) for i in data_r])
    for k, v in dict_r.items():
        values = []
        for i in data_r:
            if (i[0] + ',' + i[1]) == k:
                i[0:2] = []
                values += [i]
            dict_r[k] = (values)
    return dict_r