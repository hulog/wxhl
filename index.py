import re
import time
import json
import requests
from spider.douban import Douban

class Index:
  def get(self):
    douban = Douban()
    return douban.getItems()
if __name__ =='__main__':
  i = Index()
  print 'time-->%s'% int(time.time())
  print i.get()[0][0]
