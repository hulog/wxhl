# -*- coding: utf-8 -*-
import re
import time
import json
import requests

class Ticket:
  def init(self):
    pass
  def getTicket(self,from_station,to_station,md,sx):
    stationlist_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
    s_unicode = requests.get(stationlist_url, verify=False).text
    stationlist = s_unicode.encode('utf-8')
    re1 = r'\|'+from_station+'\|(.*?)\|'
    re2 = r'\|'+to_station+'\|(.*?)\|'
    p1 = re.compile(re1,re.S)
    p2 = re.compile(re2,re.S)
    from_code = re.findall(p1,stationlist)[0]
    to_code = re.findall(p2,stationlist)[0]

    #初始化查询日期
    year = time.localtime()[0]
    month = md[:2]
    day = md[2:]
    t_str = str(year)+'-'+month+'-'+day

    #获取列车json数据
    query_url='https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate='+t_str+'&from_station='+from_code+'&to_station='+to_code
    resp = requests.get(query_url,verify=False).text
    trains_data = resp.encode('utf-8')
    tra_lists = json.loads(trains_data)['data']['datas']
    print len(tra_lists)

    #对筛选参数进行处理
    sx = list(sx.upper())
    recontent = u'*******************\n'
    recontent += u'车次|发车|历时|余票\n'
    recontent += u'*******************'
    for tra_list in tra_lists:
      if tra_list['station_train_code'][0] in sx:
        recontent += '\n'+tra_list['station_train_code']+'|'+tra_list['start_time']+'|'+tra_list['lishi']+'|'+tra_list['ze_num']
    print recontent
    return stationlist
if __name__ =='__main__':
  print '程序运行中……'
  t1 = time.time()
  i = Ticket()
  print len(i.getTicket('南京南','无锡','0929','kd'))
  time_long = time.time()-t1
  print '耗时====> %.3f 秒' %time_long
