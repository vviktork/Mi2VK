#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .icinga_api import request_api
from .models import Groups, Project, Host, Service, Common, Author


checkout = False
MAKER = 'Копенок Виктор Викентьевич'


class BaseRequest(object):

    def group_base(self):
        """Filling in GROUPS tables"""

        error_base = True
        g_api, error_api = request_api('group')  # Request icinga
        if error_api == True:
            group_all = [i['name'] for i in g_api]
            group_all = test_none(group_all, 1)
            try:
                for i in group_all:
                    group_i = Groups(g_name=i)
                    group_i.save()
            except Exception as e:
                if checkout == True: print('group_base -', False, e)
                error_base = False
        return error_api, error_base

    def host_base(self):
        """Filling in HOST tables"""

        error_base = True
        h_api, error_api = request_api('host')  # Request icinga
        if error_api == True:
            host_all = [[i['name'], i['attrs']['display_name'], i['attrs']['groups']] for i in h_api]
            host_all = test_none(host_all, 3)
            try:
                for i in host_all:
                    f = i
                    group = Groups.objects.get(g_name=i[2])
                    host_i = Host(h_id=i[0], h_name=i[1], h_online=True, group=group)
                    host_i.save()
            except Exception as e:
                if checkout == True: print('host_base -', False, f, e)
                error_base = False
        return error_api, error_base

    def service_base(self):
        """Filling in SERVICE tables"""

        error_base = True
        service_name, error_api = request_api('service')  # Request icinga
        if checkout == True: print('Заполнение таблицы СЕРВИСОВ -', error_api)
        if error_api == True:
            service_all = list(set([i['attrs']['display_name'] for i in service_name]))
            service_all = test_none(service_all, 1)
            try:
                for i in service_all:
                    service_i = Service(s_name=i)
                    service_i.save()
            except Exception as e:
                if checkout == True: print('service_base -', False, e)
                error_base = False
        return error_api, error_base

    def common_api(self):
        """Filling in COMMON tables"""

        error_base = True
        common_name, error_api = request_api('common')  # Request icinga
        if checkout == True: print('Заполнение таблицы COMMON -', error_api)
        if error_api == True:
            common_all = [[i['attrs']['host_name'],
                           i['attrs']['display_name'],
                           i['attrs']['last_check_result']['command'][2],
                           i['attrs']['active'],
                           'Нет',
                           int(i['attrs']['last_hard_state']),
                           str(i['attrs']['last_check']),
                           0
                           ] for i in common_name]
            try:
                for i in common_all:
                    host = Host.objects.get(h_id=i[0])
                    service = Service.objects.get(s_name=i[1])
                    #s_trable =Trable.objects.get(sys_trable=i[6])

                    host_i = Common(host=host, service=service, c_trable=i[4],
                                  c_ip=i[2], c_online=i[3], c_comment=i[4],
                                  c_status=i[5], c_time=i[6], c_table=i[7]
                                  )
                    host_i.save()
            except Exception as e:
                if checkout == False: print('common_api -', False, e)
                error_base = False
        return error_api, error_base

    def author_base(self):
        """Filling in the given author"""

        error_base = True

        name = ['',
                '',
                '',
                'vkopenok@mail.ru'
                ]
        try:
            _author = Author(company=name[0], position=name[1],  name=MAKER, phone=name[2], email=name[3])
            _author.save()
        except Exception as e:
            if checkout == True:print('author_base -', False, e)
            error_base = False
        return error_base

    def del_data(self, tabl):
        """Deleting values from the db"""

        error_base = True
        table = name_table(tabl)
        try:
            table.objects.all().delete()

        except Exception as e:
            if checkout == True: print('del_data -', False, e)
            error_base = False
        return error_base

    def all_value (self, tabl):
        """Getting values of the whole table from the db"""

        error_base = True
        table = name_table(tabl)
        try:
            val = list(table.objects.all().values())
        except Exception as e:
            if checkout == True: print('all_value -', False, e)
            error_base = False
        return val, error_base

    def common_change(sale, val1, val2):
        """Save values to db"""

        error_base = True
        try:
            h_state = int(val2['last_hard_state'])
            if val1['c_status'] != h_state:
                id_v = Common.objects.get(id=val1['id'])
                id_v.c_status = h_state
                id_v.save()
                if checkout == True:print('c_status - save')
        except Exception as e:
            if checkout == True: print('common_change -', False, e)
            error_base = False
        return error_base

    def m2m_val(self, tabl, id):
        """Getting values of the m2m table"""

        error_base = True
        table = name_table(tabl)
        try:
            a1 = table.objects.get(id=id)
            val = list(a1.project.all().values())
        except Exception as e:
            if checkout == True: print('m2m_val -', False, e)
            error_base = False
        return val, error_base

    def modal_delete(self, id):
        """Data from modal window - delete"""

        error_base = True
        try:
            now_object = Common.objects.get(id=id)
            now_object.c_comment = 'Нет'
            now_object.c_trable = 'Нет'
            now_object.c_table = 0
            now_object.save()
        except Exception as e:
            if checkout == True: print('madal_delete -', False, e)
            error_base = False
        return error_base

    def modal_edit(self, data):
        """Data from modal window - edit"""

        error_base = True
        try:
            now_object = Common.objects.get(id=data.get('number'))
            now_object.c_trable = data.get('trable')
            now_object.c_comment = data.get('message')
            now_object.c_table = data.get('table')
            now_object.save()
        except Exception as e:
            if checkout == True: print('modal_exit -', False, e)
            error_base = False
        return error_base

    def value_table(self, id):
        """Getting values from the COMMON table"""

        now_table = None
        error_base = True
        try:
            now_table = list(Common.objects.filter(id=id).values('c_table'))[0].get('c_table')
        except Exception as e:
            if checkout == True: print('value_table -', False, e)
            error_base = False
        return error_base, now_table

    def a_host(self):
        a_data = list(Author.objects.filter(name=MAKER).values())[0]
        return a_data

    def remember_db(self):
        """Creating a db template"""

        error_base = True
        rezult = []
        host_del = ['h_id', 'group_id', 'h_online', 'id']  # Exclude from table
        common_del = ['service_id', 'id', 'c_status', 'c_online', 'c_time', 'host_id']  # Exclude from table
        try:
            host = list(Host.objects.all().values())
            common = list(Common.objects.all().values())
            # Table processing Host
            for i in host:
                host_copy = i.copy()
                for key in host_del: del host_copy[key]
                for k,v in i.items():
                    if k == 'id':
                        host_data = Host.objects.get(id=v)
                        proj_numer = host_data.project.count()
                        proj_data = list(host_data.project.all().values('id'))
                        if proj_numer >= 1:
                            proj = [i.get('id') for i in proj_data]
                        else:
                            proj = []
                        host_copy['project'] = proj
            # Table processing Common
                        comm_temp =[]
                        for c in common:
                            for k2, v2 in c.items():
                                if k2 == 'host_id':
                                    if v == v2:
                                        common_copy = c.copy()
                                        for key in common_del: del common_copy[key]
                                        comm_temp += [common_copy]

                        host_copy['common'] = comm_temp
                        rezult += [host_copy]
        except Exception as e:
            if checkout == True: print('recovery_database -', False, e)
            error_base = False
        return error_base, rezult

    def timing_db(self, old_base):
        """Database synchronization"""

        error_base = True
        try:
            host = list(Host.objects.all().values())
            common = list(Common.objects.all().values())
            for i in old_base:
                common_data = i['common']
                for h in host:
                    if i['h_name'] == h['h_name'] and i['project'] != []:

                        host_data = Host.objects.get(id=h['id'])
                        host_data.project.set(i['project'])
                        host_data.save()
                for com in common_data:
                    for c in common:
                        if c['c_ip'] == com['c_ip']:
                            common_data = Common.objects.get(id=c['id'])

                            if com['c_comment'] != 'Нет':
                                common_data.c_comment = com['c_comment']
                            if com['c_trable'] != 'Нет':
                                common_data.c_trable = com['c_trable']
                            if com['c_table'] != 0:
                                common_data.c_table = com['c_table']
                            common_data.save()
        except Exception as e:
            if checkout == True: print('timing_db -', False, e)
            error_base = False
        return error_base


def test_none(data_t, index):
    """Filling tables with value - 'Нет'"""

    data_1 = []
    data_2 = []
    if index == 3:
        c_none = [i[0] for i in data_t if i[2] == []]
        for i in data_t:
            if i[0] is not c_none and len(i[2]) == 1:
                data_1 += [[i[0], i[1], i[2][0]]]
            else:
                data_2 += [[i[0], i[1], 'Нет']]
        data_all = data_1 + data_2
    elif index == 1:
        for i in data_t:
            if i == '':
                data_1 += ['Нет']
            else:
                data_2 += [i]
        data_all = list(set(['Нет'] + data_1 + data_2))
    return data_all

def name_table(tabl):
    """Name of db tables"""

    if tabl == 'group':
        table = Groups
    elif tabl == 'host':
        table = Host
    elif tabl == 'service':
        table = Service
    elif tabl == 'common':
        table = Common
    elif tabl == 'project':
        table = Project
    elif tabl == 'author':
        table = Author
    return table