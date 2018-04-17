# coding=utf-8

'''
Задача:
Есть список из наименования судов и их идентификаторов.
Необходимо перевести их во все падежные формы, кроме множественных
'''

import sys
import requests
import codecs
from xml.etree import ElementTree

#Постоянная часть адреса
cons_adr = 'https://ws3.morpher.ru/russian/declension?s='

'''
Переменную часть достаем из файла.
Строки в файле представляют собой ИД записи в файле с наименованием суда,
сепарируются посредством знака '|'
Открываем файл с исходными данными
'''
file_open = codecs.open('courts.txt','r', 'utf_8_sig')
#file_open = open('courts.txt','r')

#Открываем файл для записи результатов
res_file = open('result_file.txt', 'w')
for line in file_open:
    #Сепарируем по |
    spl_line = line.split('|')
    id_court = spl_line[0]
    name_court = spl_line[1]
    name_court = name_court.rstrip()
    #name_court = name_court.replace('\n', '')

    #Небольшой костыль для вывода именительного падежа
    total_string = '1|'+name_court+'|'+id_court+'\n'
    res_file.write(total_string)

    # Пример вызова сервиса = 'https://ws3.morpher.ru/russian/declension?s=Соединенное%20королевство'
    # Перед вызовом строки заменим пробелы на разделитель, с которым работает сервис = '%20'

    url_str = cons_adr + name_court.replace(' ', '%20')

    # Вызываем сервис, парсим и декодируем

    response = requests.get(url_str)
    str_code = response.content
    prs = str_code.decode('utf8')
    xml = ElementTree.fromstring(prs)

    # Спровчник кодов платежей

    '''
    1	Именительный (Кто? Что?)
    2	Родительный (Кого? Чего?)
    3	Дательный (Кому? Чему?)
    4	Винительный (Кого? Что?)
    5	Творительный (Кем? Чем?)
    6	Предложный (О ком? О чем?)
    '''
    '''
    Заменяем имена тегов на коды из справочника, чтобы получить вид:
    Код справочника, пробел, падежная форма
    '''

    for table in xml.getiterator('xml'):
        for child in table:
            grm_type = str(child.tag)
            if grm_type == 'Р':
                grm_type = '2'
            elif grm_type == 'Д':
                grm_type = '3'
            elif grm_type == 'В':
                grm_type = '4'
            elif grm_type == 'Т':
                grm_type = '5'
            elif grm_type == 'П':
                grm_type = '6'
            else:
                grm_type = ''
                child.text = ''

        # Собираем строку
            court = str(child.text)
            court = court.rstrip()
            total_string = grm_type + '|' + court+'|'+id_court+'\n'
            #Еще один костыль, дабы не выводить неинформативные строки
            if total_string == '||'+id_court+'\n':
                total_string=''
            print(total_string)
            res_file.write(total_string)
file_open.close()
res_file.close()