# -*- coding: utf-8 -*-
import time
import requests
import json
from threading import Thread
from flask import request, Flask
import kabis, re
import logging


FLASK = Flask(__name__)
APP_ID = 'app_ID'
PASSWORD = 'secret' # секрет от бота
context =('fullchain.pem', 'privkey.pem') # относительные или абсолютные пути к файлам, которые сгенерировал cert_bot
TOKEN = {}


def get_token():
    global TOKEN
    payload = {'grant_type': 'client_credentials',
               'client_id': APP_ID,
               'client_secret': PASSWORD,
               'scope': 'https://api.botframework.com/.default',
              }
    token = requests.post('https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token', data=payload).content
    TOKEN = json.loads(str(token)[2:-1])
    return json.loads(str(token)[2:-1])


def send_token_to_connector(token):
    url = 'https://groupme.botframework.com/v3/conversations'
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.post(url, headers=headers)
    return r


def get_and_verify_token():
    global TOKEN
    while True:
        get_token()
        send_token_to_connector(TOKEN['access_token'])
        time.sleep(TOKEN['expires_in']*0.9)


def get_menu(mod, day=''):
    menu = kabis.get_kabis_menu(mod, day=day, fl=FLASK)
    attachments = [
        {
            "contentType": "application/vnd.microsoft.card.receipt",
            "content": {
                "title": menu['title'],
                "items": menu['menu'],
                "Total": "265"
            }
        }
    ]
    return {'title': menu['title'], 'attachments': attachments}


def select_menu(day, text):
    m = re.search('\w+\s\w+\s(-{0,1}\+{0,1}\d{1,})', text)
    if m:
        found = m.group(1)
        return get_menu(found, day)
    else:
        return get_menu(0, day)

@FLASK.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@FLASK.route('/', methods=['GET', 'POST'])
def handle():
    data = request.get_json()
    talk_id = data['conversation']['id']
    kab = re.search('кабис', data['text'])
    version = re.search('версия', data['text'])
    response = ''

    if(kab):
        if re.search('(понед|\sпн(\s|$))',data['text']):
            response = select_menu('понедельник', data['text'])
        if re.search('(втор|\sвт(\s|$))',data['text']):
            response = select_menu('вторник', data['text'])
        if re.search('(сред|\sср(\s|$))',data['text']):
            response = select_menu('среда', data['text'])
        if re.search('(четв|\sчт(\s|$))',data['text']):
            response = select_menu('четверг', data['text'])
        if re.search('(пятн|\sпт(\s|$))',data['text']):
            response = select_menu('пятница', data['text'])
        if re.search('(субб|\sсб(\s|$)|воск|\sвс(\s|$))',data['text']):
            response = {'title':'Обедаем дома','attachments':[]}
        if re.search('(^макса$)', data['text']):
            response = kabis.get_vegan_style()
        if (data['from']['name'] == "Maxim Timonin"):
            response = kabis.get_vegan_style()
        if not response:
            response = get_menu(0)
    else:
        if (version):

            response = {'title': kabis.get_version_of_deploy(),'attachments': []}
        else:
            response = {'title': 'Используй команду "кабис [ день недели [-2...+2] ]"','attachments': []}
    msg = {
        "type": "message",
        "from": {
                "id": APP_ID,
                "name": "YouLunch"
            },
        "conversation": {
            "id": talk_id,
        },
        "text": response['title'],
        "attachments": response['attachments']

    }
    url = data['serviceUrl'] + '/v3/conversations/{}/activities/'.format(data['conversation']['id'])
    headers = {'Authorization': 'Bearer ' + TOKEN['access_token'],
               'content-type': 'application/json; charset=utf8'}
    r = requests.post(url, headers=headers, data=json.dumps(msg))
    return 'success'


if __name__ == '__main__':
    thread = Thread(target=get_and_verify_token)
    thread.start()
    FLASK.logger.setLevel(logging.INFO)
    FLASK.run(host='0.0.0.0', port=8080)