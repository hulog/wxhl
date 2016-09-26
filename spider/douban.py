import requests
import json
import time
import re

class Douban:
  def getItems(self):
    douban_url = 'https://movie.douban.com/'
    douban_html = requests.get(douban_url).text
    c = re.compile(r' <a onclick="moreurl.*?href="(.*?)"[\s\S]*?src="(.*?)" alt="(.*?)" [\s\S]*?class="subject-rate">(.*?)</span>', re.S)
    DOUBAN = re.findall(c, douban_html)
    piaofang_url = 'http://www.cbooo.cn/boxOffice/GetHourBoxOffice?d=%s'%str(time.time()).split('.')[0]
    piaofang_json = requests.get(piaofang_url).text
    PIAOFANG = json.loads(piaofang_json)['data2']

    PIAOFANGS = []
    for piaofang in PIAOFANG:
      PIAOFANGS.append((piaofang['MovieName'], float(piaofang['sumBoxOffice'])))
    PIAOFANGS = sorted(PIAOFANGS, key=lambda x: x[1], reverse=True)
    INFOS = []
    for piao in PIAOFANGS:
      piaofang_name = piao[0]
      for douban in DOUBAN:
        douban = list(douban)
        douban_name = douban[2]
        if piaofang_name == douban_name:
           douban.append(str("%.3f"%(piao[1]/10000.0)))
           INFOS.append(douban)
           break
    total_num = len(INFOS)
    if total_num>10:
      num = 10
    else:
      num = total_num
    return INFOS,num
