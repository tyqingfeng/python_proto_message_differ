#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import Config


class Util(object):

    @staticmethod
    def is_str_not_empty(content):
        if isinstance(content, str) and len(content.strip()) != 0:
            return True
        else:
            return False

    @staticmethod
    def print_log(content, tag=""):
        if Config.IS_PRINT_LOG:
            print(tag, content)

    @staticmethod
    def print_result_log(content, tag=""):
        if Config.IS_PRINT_RESULT_LOG:
            print(tag, content)

    @staticmethod
    def dict_get(dict_ins, key, default_value=None):
        if dict_ins:
            if dict_ins.__contains__(key):
                return dict_ins[key]
        return default_value

    @staticmethod
    def sub_str(content, start_index, end_index=-1):
        Util.print_log("Util#sub_str---> %s start_index:%d end_index:%d" % (content, start_index, end_index))
        if Util.is_str_not_empty(content):
            length = len(content)
            if length > start_index:
                if end_index == -1:
                    end_index = length
                elif end_index > length:
                    end_index = length
                return content[start_index:end_index]
            else:
                print("Util--> start_index out of len")
        return ""
