# -*- coding:utf-8 -*-
#filename:menu.py

import urllib
import urllib2
import json

class Menu:
  appId = 'wx78c9a94295d1c4dd'
  appSecret = '7d3c02a2e4395ef8a2000187b5f277af'

  def __init__(self):
    pass

  def getAccessToken(self):
    access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + self.appId + '&secret=' + self.appSecret
    f = urllib2.urlopen(access_token_url)
    jsonString = f.read()
    access_token = json.loads(jsonString)['access_token']
    return access_token

  def create(self,postData,accessToken):
    postUrl = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % accessToken
    if isinstance(postData,unicode):
      postData = postData.encode('utf-8')
    urlResp = urllib.urlopen(url = postUrl,data = postData).readline()
    print json.loads(urlResp)['errcode']
    #print 'urlResp====>'+urlResp

  def query(self,accessToken):
    postUrl = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s' % accessToken
    urlResp = urllib.urlopen(url = postUrl)

  def delete(self,accessToken):
    postUrl = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s' % accessToken
    urlResp = urllib.urlopen(url = postUrl)

  def get_current_selfmenu_info(self,accessToken):
    postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
    urlResp = urllib.urlopen(url=postUrl)

if __name__ =='__main__':
    menu = Menu()
    accessToken = menu.getAccessToken()
    print ' accessToken===>'+accessToken
    postData = '''{
                "button":[
                     {    
          "type":"click",
          "name":"今日歌曲",
          "key":"V1001_TODAY_MUSIC"
      },
      {
           "type":"view",
           "name":"歌手简介",
           "url":"http://www.qq.com/"
      },
      {
           "name":"菜单",
           "sub_button":[
            {"type":"click","name":"hello word","key":"V1001_HELLO_WORLD"},{"type":"click","name":"赞一下我们","key":"V1001_GOOD"}]}]}'''

    resp = menu.create(postData,accessToken)
    print resp
