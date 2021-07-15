#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : liangychang
# @Time : 2021/05/04
import re
from util import Util
from message import MessageField
from config import Config


class Matcher(object):

    def __init__(self):
        # for start search
        self.start_reg = r'(?P<type>message) +(?P<name>\w+) *(?P<end_tag>{?)'
        self.start_end_reg = r'(?P<end_tag>{)'
        self.start_end_reg_cp = r'(?P<end_tag>{?)'
        self.key_message_name = "name"
        self.key_message_start_end_tag = "end_tag"
        # enum define， 策略可以进行更新
        self.start_enum__reg = r'(?P<type>enum) +(?P<name>\w+) *(?P<end_tag>{?)'
        self.start_regs = [self.start_reg, self.start_enum__reg]
        # for middle search
        self.syntax_words = Config.SYNTAX_WORDS
        self.key_message_type = "type"
        self.key_message_syntax = "syntax"
        self.key_message_index = "index"
        reg_str = r"(?P<syntax>("
        for syntax_word in self.syntax_words:
            reg_str = reg_str + syntax_word + "|"
        self.middle_reg = reg_str[:-1] + r")) +(?P<type>[\w.?]+)\s*(?P<name>\w+)\s*= *(?P<index>\d+)"
        self.middle_value_start_reg = r'\[\('
        self.middle_value_end_reg = r'\}\]'

        # for end search
        self.end_reg = r'(?P<end_tag>})'
        self.end_and_middle_reg = r'(?P<end_exist_field>=).*(?P<end_tag>})'
        self.key_end_exist_field = "end_exist_field"
        self.key_end_end_tag = "end_tag"

    def is_exist_end_tag(self, match_dict):
        if match_dict:
            Util.print_log("is_exist_end_tag %s" % str(type(match_dict)))
            if isinstance(match_dict, dict) and match_dict.__contains__(self.key_message_start_end_tag) and len(
                    match_dict[self.key_message_start_end_tag]) > 0:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def print_match_dict(match_dict, log_tag):
        if match_dict:
            for key, value in match_dict.items():
                Util.print_log("log_tag:%s key:%s value:%s" % (log_tag, key, value))

    """ 匹配消息类型或者enum类型
    @:returns message_name 消息名称， is_exist_end_tag 是否存在结束标记, message_type 类型如：message enum
    """

    def match_start(self, content):
        for start_reg in self.start_regs:
            message_name, is_exist_end_tag, message_type = self._match_start_inner(start_reg, content)
            if Util.is_str_not_empty(message_name):
                return message_name, is_exist_end_tag, message_type
        return "", False, ""

    def _match_start_inner(self, reg, content):
        result = re.search(
            reg, content)
        message_name = ""
        message_type = ""
        is_exist_end_tag = False
        if result and result.groupdict:
            key_dict = result.groupdict()
            for key in key_dict.keys():
                Util.print_log("match_start key:%s value:%s" %
                               (key, key_dict[key]))
            if key_dict.__contains__(self.key_message_name):
                message_name = key_dict[self.key_message_name]
            if self.is_exist_end_tag(key_dict):
                is_exist_end_tag = True
            if key_dict.__contains__(self.key_message_type):
                message_type = key_dict[self.key_message_type]
        Util.print_log("match_start--->%s is_exist_end_tag:%s message_type:%s" % (message_name, str(is_exist_end_tag), message_type))
        return message_name, is_exist_end_tag, message_type

    def match_start_end(self, content):
        result = re.search(
            self.start_end_reg, content)
        if result and self.is_exist_end_tag(result.groupdict()):
            _, end_index = result.span(1)
            return True, end_index
        return False, -1

    def match_middle(self, content):
        result = re.search(self.middle_reg, content)

        if result and result.groupdict:
            field = MessageField()
            key_dict = result.groupdict()
            self.print_match_dict(key_dict, "match_middle:")
            field.syntax = Util.dict_get(
                key_dict, self.key_message_syntax, "")
            field.field_type = Util.dict_get(key_dict, self.key_message_type, "")
            field.name = Util.dict_get(key_dict, self.key_message_name, "")
            field.index = int(Util.dict_get(key_dict, self.key_message_index, -1))
            field.content = content
            return field
            # 不存在语法关键词，匹配是否定义了message类型
        return None

    def match_middle_value(self, content):
        result = re.search(self.middle_value_start_reg, content)
        if result:
            result = re.search(self.middle_value_end_reg, content)
            if result:
                return True
        return False

    @staticmethod
    def remove_annotation(content):
        if Util.is_str_not_empty(content):
            result = content.split("//")
            return result[0]
        return ""

    def match_stop_middle(self, content):
        Util.print_log("match_stop_middle--->" + content)
        result = re.search(self.end_and_middle_reg, content)
        if result and result.groupdict:
            return True
        else:
            return False

    def match_stop(self, content):
        result = re.search(self.end_reg, content)
        if result and result.groupdict:
            Util.print_log("match_stop true--->" + content)
            return True
        Util.print_log("match_stop False--->" + content)
        return False
