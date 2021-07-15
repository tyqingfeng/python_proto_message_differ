#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : liangychang
# @Time : 2021/05/04
import os

from util import Util
from message import Message
from config import Config

"""[summary]
比较时，message只希望知道field中的增量？
"""


class MessageCompare(object):

    def __init__(self):
        self.diff_messages = {}

    """[summary]
    @param messages 如正式文档消息
    @param cmp_messages 本地文档消息
    """

    def compare(self, messages, cmp_messages):
        if not messages or not cmp_messages:
            Util.print_log("compare fail for None")
            return
        for message in messages:
            is_exist_match = False
            for cmp_message in cmp_messages:
                if message.name == cmp_message.name:
                    Util.print_log("MessageCompare#compare--> %s, cmp:%s" % (message.name, cmp_message.name))
                    self.diff_message(message, cmp_message)
                    is_exist_match = True
            if not is_exist_match:
                # 测试ignore
                # self.diff_messages[message.name] = message
                pass

    def diff_message(self, message, cmp_message):
        diff_message = Message()
        # for cmp_messages change and minus
        self.__compare_message(diff_message, message, cmp_message)
        # for cmp_messages inc fields
        self.__compare_message(diff_message, cmp_message, message, True, 1)
        if len(diff_message.field_map) > 0 or len(diff_message.cmp_inc_map) > 0:
            diff_message.name = message.name
            self.diff_messages[message.name] = diff_message
        else:
            Util.print_log("MessageCompare#diff_message--> %s no diff\n" % message.name)

    @staticmethod
    def __compare_message(diff_message, message, cmp_message, is_only_increment=False, store_type=0):
        for index in message.field_map.keys():
            cmp_field = cmp_message.get(index)
            if cmp_field:
                # 有对应的field
                if not is_only_increment:
                    field = message.get(index)
                    compare_result = field.compare_to(cmp_field, message.name)
                    if Config.MATCH_IS_CATCH_OTHER_DISMISS_TYPE:
                        if compare_result == 1:
                            diff_message.put(index, field, cmp_field, store_type)
                        pass
                    elif compare_result > 0:
                        diff_message.put(index, field, cmp_field, store_type)
            else:
                # 没有对应的field
                if Config.MATCH_IS_CATCH_LEAK_FIELD:
                    diff_message.put(index, message.get(index), cmp_field, store_type)
                pass

    def print_diff_message(self):
        Util.print_result_log("\n================print_diff_message===================")
        for _, message in self.diff_messages.items():
            if len(message.field_map) > 0:
                Util.print_result_log("\n---------field变化和缺少--------")
                Util.print_result_log(message.__str__())
            # print("message: "+ str(message))
            # Util.print_result_log("\n")
            if Config.IS_PRINT_INC_FIELD and len(message.cmp_inc_map) > 0:
                Util.print_result_log("---------field增加--------")
                Util.print_result_log(message.cmp_inc_str())

    def save_compare_result(self, desc, file_name):
        if os.path.exists(file_name):
            # os.path.isfile(file_name):
            os.remove(file_name)
        with open(file_name, 'w') as file:
            for _, message in self.diff_messages.items():
                if len(message.field_map) > 0:
                    file.write(message.__str__())
                if Config.IS_PRINT_INC_FIELD and len(message.cmp_inc_map) > 0:
                    file.write(message.cmp_inc_str())
                    file.write("\n")

    def save_brief_result(self, desc, file_name):
        if os.path.exists(file_name):
            # os.path.isfile(file_name):
            os.remove(file_name)
        with open(file_name, 'w+') as file:
            file.write(desc + "\n")
            for _, message in self.diff_messages.items():
                if len(message.field_map) > 0:
                    file.write(message.name)
                    file.write("\n")
                if Config.IS_PRINT_INC_FIELD and len(message.cmp_inc_map) > 0:
                    file.write(message.name)
                    file.write("\n")
