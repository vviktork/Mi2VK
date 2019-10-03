#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from .processing_icinga import *


class TestRegvestIcinga (unittest.TestCase):

    def setUp(self):
        """Creating values for all methods"""
        self.time1 = 1562672912
        self.time2 = 1562672512

    def test_title_templates(self):
        """Table title test"""
        text_1 = ['Объект', 'Проект', 'Сервис', 'Статус', 'Адрес IP',
                  'Обновлено', 'Время статуса', 'Сообщение', '№', ''
                  ]
        text_2 = ['Объект', 'Проект', 'Сервис', 'Статус', 'Адрес IP',
                  'Время статуса','Заявка', 'Сообщение', '№', ''
                  ]
        title_1, title_2 = title_templates()
        self.assertListEqual(title_1, text_1)
        self.assertListEqual(title_2, text_2)

    def test_combine_dict(self):
        """Merger dict test"""
        dict1 = [{'name_1': 'Test_1', 'id': 1}]
        dict2 = [{'name_2': 'Test_2', 'host_id': 1}]
        dict_1_2 = [{'name_1': 'Test_1', 'id': 1, 'name_2': 'Test_2', 'host_id': 1}]
        dict1_dict2, _ = combine_dict(dict1, 'id', dict2, 'host_id')
        self.assertListEqual(dict1_dict2, dict_1_2)

    def test_time_t(self):
        """Test sort by the time in datetime"""
        time_return = time_t(self.time1)
        self.assertEqual(time_return, datetime.datetime(2019, 7, 9, 14, 48))

    def test_time_delta(self):
        """Test differense time"""
        delta = time_delta(self.time1, self.time2)
        self.assertEqual(delta, '0:07:00')

    def test_time_exit(self):
        """Test formatting time and status to template"""
        val_test1 = {'last_now': 1, 'time_check': 1, 'state_check': 1}
        val_test2 = dict.fromkeys(['last_check', 'last_state_ok', 'last_state_critical'], self.time1)
        val_test2.update({'last_hard_state': None, 'last_state_change': self.time2})
        v_test = {'OK': 0, 'НЕИЗВЕСТНО': 1, 'CRITICAL': 2}
        for k,v in v_test.items():
            val_test2['last_hard_state'] = v
            time_test, _, _ = time_exit(val_test1, val_test2)
            self.assertEqual(time_test['state_check'], k)

    def test_rezult_template(self):
        """Test conversion for template"""
        data_1 = {'Test_title,project': [['Test_1'], ['Test_2']]}
        data_test = rezult_template(data_1)
        data_1 = [['Test_title', 'project', 'Test_1'], ['', '', 'Test_2']]
        self.assertListEqual(data_test, data_1)

    def test_rezult_dict(self):
        """Conversion list to dict"""
        data_1 = [['Test', 'Project', '1', '2'],
                  ['Test', 'Project', '2', '3'],
                  ['Test_1', 'Project_1', '3', '4']
                  ]
        data_test = rezult_dict(data_1)
        data_1 = {'Test,Project': [['1', '2'], ['2', '3']], 'Test_1,Project_1': [['3', '4']]}
        self.assertEqual(data_test, data_1)


if __name__ == '__main__':
    unittest.main()
