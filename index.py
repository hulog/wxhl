import re
import time
import json
import requests
from spider.douban import Douban

class :
  def get(self):
    url='https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date=2016-09-27&leftTicketDTO.from_station=WXH&leftTicketDTO.to_station=SHH&purpose_codes=ADULT'
    s=requests.get(url)
    return s.text
if __name__ =='__main__':
  i = Index()
  print i.get()
