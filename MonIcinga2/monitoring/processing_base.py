#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from .base_request import BaseRequest


checkout = False

def processing_modal(data):
    """Modal request processing"""

    error_base = True
    if 'delete' in data.keys():
        error_base = BaseRequest.modal_delete(None, data.get('delete'))
    elif 'number' in data.keys():
        error_base, table_now = BaseRequest.value_table(None, data.get('number'))
        valid_2, now_trable = table_2(data.get('trable'))
        data['trable'] = now_trable
        # Move between tables
        if error_base == True:
            del data['csrfmiddlewaretoken']
            if 'table2' in data.keys():
                del data['table2']
                if 'table3' in data.keys():
                    del data['table3']
                    data['table'] = (3)
                else:
                    if valid_2 == True:
                        data['table'] = (2)
                    else:
                        data['table'] = (table_now)
            elif 'table3' in data.keys():
                del data['table3']
                data['table'] = (3)
            else:
                if valid_2 == True and table_now != 3:
                    data['table'] = (2)
                else:
                    data['table'] = (table_now)
            data = message_time(data)
            error_base = BaseRequest.modal_edit(None, data)
    return error_base

def table_2(data_t):
    """Valid for table 2"""

    valid_2 = True
    test = len(data_t)
    if test >= 4:
        try:
            test = int(data_t)
        except:
            data_t = 'Нет'
            valid_2 = False
    else:
        data_t = 'Нет'
        valid_2 = False
    return valid_2, data_t

def message_time(data):
    """Time in message"""

    ind_time = '%d.%m'  # '%Y,%m,%d,%H,%M'
    data['message'] = (data['message'] + ' ' + time.strftime(ind_time, time.localtime()))
    return data

