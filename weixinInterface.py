# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree
import talk_api
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
          if content[0:1] == 'm':
            str_for_md5 = content[1:]
            md5 = hashlib.md5()
            md5.update(str_for_md5)
            recontent = md5.hexdigest()
            #str_for_resp = hashlib.md5().update(str_for_md5).hexdigest()
            #recontent = str_for_resp
          elif(content == u"你好"):
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
          picUrl = xml.find('PicUrl').text #picUrl 暂未使用
          # print 'picurl'+picUrl
          mediaId = xml.find('MediaId').text
          return self.render.reply_image(fromUser,toUser,int(time.time()),mediaId)
        elif msgType == 'event':
          exact_event = xml.find('Event').text
          if exact_event == 'subscribe':
            recontent = u'你好，欢迎关注我的微信公众号，目前暂提供一下功能:\n1.机器人聊天\n2.md5加密m****\n3.更多请回复“功能”'
            
            #recontent = u'你好，欢迎关注我的微信公众号，目前暂提供一下功能: 1.机器人聊天 2.md5加密m**** 3.更多请回复“功能”'
          if exact_event == 'unsubscribe':
            recontent = u'拜拜'
        else:
          pass
        return self.render.reply_text(fromUser,toUser,int(time.time()),recontent)
