# -*- coding: utf-8 -*-
import re
import time
import json
import requests

class Train:

  def getCodes(self,f,t,stationlist):
    f_code = re.findall(self.getPattern(f),stationlist)[0]
    t_code = re.findall(self.getPattern(t),stationlist)[0]
    return [f_code,t_code]

  def getPattern(self,s):
    regtex = r'\|'+s+'\|(.*?)\|'
    return re.compile(regtex,re.S)

  def getDate(self,time_str):
    year = str(time.localtime()[0])
    month = time_str[:2]
    day = time_str[2:]
    return year+'-'+month+'-'+day

  def getTrains(self,from_station,to_station,monthDay,tra_type='gdkctz'):

    #获取站名和代码的对照表
    stationlist_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
    s_unicode = requests.get(stationlist_url, verify=False).text
    stationlist = s_unicode.encode('utf-8')

    #获取出发站和终点站的代码
    [f_code,t_code] = self.getCodes(from_station,to_station,stationlist)

    #初始化查询日期
    t_str = self.getDate(monthDay)

    #获取列车json数据
    query_url='https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate='+t_str+'&from_station='+f_code+'&to_station='+t_code
    resp = requests.get(query_url,verify=False).text
    trains_data = resp.encode('utf-8')
    tra_lists = json.loads(trains_data)['data']['datas']

    #对筛选参数进行处理
    sx = list(tra_type.upper())
    recontent = u'查询结果筛选后如下:\n'
    recontent += u'*******************\n'
    recontent += u'车次|发车|历时|余票\n'
    recontent += u'*******************'
    count = 0
    for tra_list in tra_lists:
      f_c = tra_list['from_station_telecode']
      t_c = tra_list['to_station_telecode']
      if f_c == f_code and t_c == t_code :
        t_type = tra_list['station_train_code'][0]
        if t_type in sx:
          if t_type in ['G','D','C']
            recontent += '\n'+tra_list['station_train_code']+'|'+tra_list['start_time']+'|'+tra_list['lishi']+'|'+tra_list['ze_num']
          else: 
            recontent += '\n'+tra_list['station_train_code']+'|'+tra_list['start_time']+'|'+tra_list['lishi']+'|'+tra_list['yz_num']
          count = count + 1
          if count % 5 == 0:
            recontent += u'\n-------------------'
    return recontent
