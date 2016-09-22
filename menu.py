# -*- coding:utf-8 -*-
#filename:menu.py

import urllib
import urllib2
import json

class Menu(object):
    appId = wx78c9a94295d1c4dd
    appSecret = 7d3c02a2e4395ef8a2000187b5f277af

  def __init__(self):
    pass
    
  def getAccessToken(self):
    access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appId + '&secret=' + secret
    f = urllib2.urlopen(access_token_url)
    jsonString = f.read()
    access_token = json.loads(jsonString)['access_token']
    return access_token

  def create(self,postData,accessToken):
    postUrl = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % accessToken
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
