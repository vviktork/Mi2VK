#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from .models import Icinga
from icinga2api.client import Client

from requests.packages.urllib3.exceptions import InsecureRequestWarning  # Certificate Record Suppression
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)       #


"""When creating a database, override variables and create access settings Icinga"""
#URL=NAME=PASSWORD='root'
icinga_data = list(Icinga.objects.filter(username='root').values())[0]
URL = icinga_data['protocol'] + '://' + icinga_data['ip'] + ':' + icinga_data['port']
NAME = icinga_data['username']
PASSWORD = icinga_data['password']

client = Client(URL, username=NAME, password=PASSWORD)

def request_api(index):
    """API request Icinga"""

    data_api = None
    error_api = True
    try:
        if index == 'group':
            data_api = client.objects.list('HostGroup', attrs=['name'])
        elif index == 'host':
            data_api = client.objects.list('Host', attrs=['name', 'display_name', 'groups'])
        elif index == 'service':
            data_api = client.objects.list('Service', attrs=['display_name'])
        elif index == 'common':
            data_api = client.objects.list('Service', attrs=['host_name',
                                                             'display_name',
                                                             'last_hard_state',
                                                             'last_check',
                                                             'active',
                                                             'last_check_result'
                                                             ]
                                           )
        elif index == 'request':
            data_api = client.objects.list('Service',
                                           attrs=['host_name',  # Unique number host (int)
                                                  'display_name',  # Service name (str)
                                                  'last_hard_state',  # Last check (0-4, 0-OK, 2-Critical, int)
                                                  'last_check',  # Last Check Time (float)
                                                  'last_state_change',  # Last state change
                                                  'last_state_ok',  # Last time ok (float)
                                                  'last_state_critical',  # Last time critical (float)
                                                  'active'  # Service included (True/False)
                                                  ]
                                           )
    except:
        error_api = False
    return data_api, error_api
