# -*- coding: utf-8-*-
from robot.sdk import unit
from robot.sdk.AbstractPlugin import AbstractPlugin

# 调试用，发布时删除
SERVICE_ID='S19817'
API_KEY='8QLw6XtQBPKYXFh7GEmXu7CT'
SECRET_KEY='wG1iAfKtUpGEfN896GZdRmhaIdqAziOY'

class Plugin(AbstractPlugin):

    def handle(self, text, parsed):
        parsed = unit.getUnit(text, SERVICE_ID, API_KEY, SECRET_KEY) # 调试用，发布时删除
        slots = unit.getSlots(parsed, 'HELLO_WORLD')  # 取出所有词槽
        # 遍历词槽，找出 user_person 对应的值
        for slot in slots:
            if slot['name'] == 'user_person':
                self.say('您好，{}！'.format(slot['normalized_word']))
                return
        # 如果没命中词槽，说 hello world
        self.say('大家们好呀，我是小明同学，今天和柳同学一同前来答辩，还望大家多多关照呀！', cache=True)

    def isValid(self, text, parsed):
        parsed = unit.getUnit(text, SERVICE_ID, API_KEY, SECRET_KEY) # 调试用，发布时删除
        # 判断是否包含 HELLO_WORLD 意图
        return unit.hasIntent(parsed, 'HELLO_WORLD')