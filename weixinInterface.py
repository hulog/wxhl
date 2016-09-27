# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree
import talk_api
import requests
import re
from spider.douban import Douban
from spider.train import Train
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
        #sha1加密算法        
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()

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
        # 请求内容为文本
        if msgType == 'text':
          functions = {'1':'将需要加密的字符串前加m，例如对"sae3"加密，请输入msae3'}
          content = xml.find("Content").text#获得用户所输入的内容

          # md5
          if content[0:1] == 'm':
            str_for_md5 = content[1:]
            md5 = hashlib.md5()
            md5.update(str_for_md5)
            recontent = md5.hexdigest()[11:19].upper()

          # openid
          elif(content == 'o'):
            recontent = '您的OpenId为:\n'+fromUser

          # 查询热评电影
          elif content == u'电影':
            douban = Douban()
            (INFOS,num) = douban.getItems()
            return self.render.reply_morepic(fromUser,toUser,INFOS,num)

          elif content[:3] == 'hcp':
            train = Train()
            detail = content.split(' ')
              err_reply = u'你输入的格式有误，请按照格式输入:\nhcp 出发站 终点站 时间 车型\n如：hcp 上海 无锡 1001 gkd'
            if(len(detail) != 5):
              recontent = err_reply
            else:
              try:
                [f,t,d,l] = detail[1:5]
                recontent = train.getTrains(f,t,d,l)
              except:
                recontent = err_reply
          # 调用机器人
          else:
            try:
              msg = talk_api.talk(content,userid)
              recontent = msg
            except:
              recontent = u'我有点懵逼，你说人话好不咯'
        # 请求内容为语音
        elif msgType == 'voice':
            content = xml.find('Recognition').text
            try:
                msg = talk_api.talk(content,userid)
                recontent = msg
            except:
                recontent = u'买个iphone吧，你发的语音我听不清楚啦～'
        # 请求内容为图片
        elif msgType == 'image':
          picUrl = xml.find('PicUrl').text #picUrl 暂未使用
          # print 'picurl'+picUrl
          mediaId = xml.find('MediaId').text
          return self.render.reply_image(fromUser,toUser,int(time.time()),mediaId)
        # 请求内容为事件
        elif msgType == 'event':
          exact_event = xml.find('Event').text

          if exact_event == 'subscribe':
            recontent = u'你好，欢迎关注我的微信公众号，目前暂提供一下功能:\n1.机器人聊天\n2.md5加密:m****\n3.查看openId:o\n4.查看热评电影:电影\n5.更多请回复“功能”'
            
          if exact_event == 'unsubscribe':
            recontent = u'拜拜'
        else:
          pass

        return self.render.reply_text(fromUser,toUser,int(time.time()),recontent)
