import json
import requests
import time
piaofang_url = 'http://www.cbooo.cn/boxOffice/GetHourBoxOffice?d=%s'%str(time.time()).split('.')[0]
piaofang_json = requests.get(piaofang_url).text
PIAOFANG = json.loads(piaofang_json)['data2']
PIAOFANGS = []
for piaofang in PIAOFANG:
    PIAOFANGS.append((piaofang['MovieName'], float(piaofang['sumBoxOffice'])))
PIAOFANGS = sorted(PIAOFANGS, key=lambda x: x[1], reverse=True)
print PIAOFANGS[:5]
