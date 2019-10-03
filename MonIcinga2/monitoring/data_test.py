#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .processing_icinga import title_templates
import random


def templates_test():
    """Test data for template validation"""

    title_1, title_2 = title_templates()
    user_1 = ['', '', 'Канал 1', 'CRITICAL', '168.39.101.19', '25/07/2019 9:25',
              '1ч. 20м.', '!!!! ТЕСТ !!!!', '2116']
    user_2 = ['Берн', 'РРР', 'Основной канал', 'CRITICAL', '192.19.19.25', '25/07/2019 9:25',
              '1ч. 20м.', '!!!! ТЕСТ !!!!', '2116']
    user_3 = ['Сан-Франциско', 'РРР, ЗЗЗ, ХХ', 'Основной канал', 'CRITICAL', '100.10.99.25',
              '1ч. 20м.', str(random.randint(1000, 10000)), '!!!! ТЕСТ !!!!', '2116']
    user_4 = ['', '', 'Резервный канал', 'CRITICAL','172.56.112.34',
              '1ч. 20м.', 'QWER', '!!!! ТЕСТ !!!!', '2116']
    table_1 = [user_1, user_2, user_1, user_2]
    table_23 = [user_3, user_4, user_3, user_4]
    critical = 40
    connect = False
    return table_1, table_23, connect, title_1, title_2, critical