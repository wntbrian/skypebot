# -*- coding: utf-8 -*-
import datetime, json, os, gimage


NUMBER_OF_WEEKS = 4

weeks = ['понедельник',
         'вторник',
         'среда',
         'четверг',
         'пятница',
         'суббота',
         'воскресенье',
         ]

week_number = [
    'first.json',
    'second.json',
    'third.json',
    'fourth.json',
]

week_number_print = [
    '1-ая',
    '2-ая',
    '3-ья',
    '4-ая',

]


def day_of_week(num):
    global weeks
    return weeks[num]


def get_number_of_week(mod, day = datetime.datetime.today()):
    return (datetime.date(day.year, day.month, day.day).isocalendar()[1] + int(mod)) % NUMBER_OF_WEEKS


def get_number_of_day(day=''):
    global weeks
    if day:
        return weeks.index(day)

    return datetime.datetime.today().weekday()


def get_kabis_menu(mod, day='', fl=''):
    result = ''
    number_of_day = 0
    number_of_week = 0
    number_of_day = get_number_of_day(day)
    number_of_week = get_number_of_week(mod)
    data = None
    fl.logger.info(f"number_of_day: {number_of_day}")
    fl.logger.info(f"number_of_week: {number_of_week}")
    fl.logger.info(f"mod: {mod}")
    with open(os.path.join('ironkabis_menu',week_number[number_of_week]), encoding='utf-8') as f:
        data = json.load(f)
    menu = []
    for m in data[number_of_day]:
        menu.append({'title':m['title'], 'subtitle':m['subtitle'], 'image':{'url':gimage.get_image_link(m['title'])}})
    result = f'{result}Меню в <b>Ирон Кабисе</b> на : {day_of_week(number_of_day)}({week_number_print[number_of_week]})'
    return {'title': result,'menu':menu}


def get_vegan_style():
    result = ''
    number_of_day = get_number_of_day()
    with open(os.path.join('ironkabis_menu','vegan_style.json'), encoding='utf-8') as f:
        data = json.load(f)
    menu = data[0]
    result = f'{result}Меню в <b>Ирон Кабисе</b> на : {day_of_week(number_of_day)}'
    attachments = [
        {
            "contentType": "application/vnd.microsoft.card.receipt",
            "content": {
                "title": result,
                "items": menu,
                "Total": "280"
            }
        }
    ]
    return {'title': result, 'attachments': attachments}


def get_version_of_deploy():
    try:
        with open(os.path.join("version.info"), encoding='utf-8') as ver_file:
            data = ver_file.readlines()
    except:
        data = ["Unknown"]
    return data[0]