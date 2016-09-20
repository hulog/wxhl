# -*- coding: utf-8 -*-
import requests
import json
global s
s = requests.session()


def talk(content):
    url = 'http://www.tuling123.com/openapi/api'
    da = {"key": "9a978db57a904c5a9c3f0b52fcfe040b", "info": content}
    data = json.dumps(da)
    r = s.post(url, data=data)
    j = eval(r.text)
    code = j['code']
    if code == 100000:
        recontent = j['text']
    elif code == 200000:
        recontent = j['text']+j['url']
    elif code == 302000:
        recontent = j['text']+j['list'][0]['info']+j['list'][0]['detailurl']
    elif code == 308000:
        recontent = j['text']+j['list'][0]['info']+j['list'][0]['detailurl']
    else:
        recontent = '这货还没学会怎么回复这句话'
    return recontent
