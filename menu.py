# -*- coding:utf-8 -*-
#filename:menu.py

import urllib

class Menu(object):
  def __init__(self):
    pass
  def create(self,postData,accessToken):
    postUrl = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' %accessToken
    if isinstance(postData,unicode):
      postData = postData.encode('utf-8')
    urlResp = urllib.urlopen(url = postUrl,data = postData)

  def query(self,accessToken):
    postUrl = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s' % accessToken
    urlResp = urllib.urlopen(url = postUrl)

  def delete(self,accessToken):
    postUrl = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s' % accessToken
    urlResp = urllib.urlopen(url = postUrl)

  def get_current_selfmenu_info(self,accessToken):
    postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
    urlResp = urllib.urlopen(url=postUrl)
