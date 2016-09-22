# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree
import talk_api
import md5
class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="norman454325" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法        

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        userid = fromUser[0:15]
        if msgType == 'text':
          content = xml.find("Content").text#获得用户所输入的内容
          if content[0:1] == u'm':
            recontent = u"md5正在开发中……"
          if(content == u"你好"):
            recontent = u"你要的情感助手正在开发中，请耐心等待"
          else:
            try:
              msg = talk_api.talk(content,userid)
              return self.render.reply_text(fromUser,toUser,int(time.time()), msg)
            except:
              return self.render.reply_text(fromUser,toUser,int(time.time()), u'这货还不够聪明，换句话聊天吧')
        elif msgType == 'voice':
            content = xml.find('Recognition').text
            try:
                msg = talk_api.talk(content,userid)
                return self.render.reply_text(fromUser,toUser,int(time.time()), msg)
            except:
                return self.render.reply_text(fromUser,toUser,int(time.time()),u'你刚刚说的啥么也？我咋没听懂尼')
        elif msgType == 'image':
          recontent = u"你发的什么东东，我咋看不懂啊"
        else:
          pass
        return self.render.reply_text(fromUser,toUser,int(time.time()),recontent)
