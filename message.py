#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : liangychang
# @Time : 2021/05/04
from util import Util
from config import Config


class MessageField(object):

    def __init__(self):
        self.set("", "", -1, "")

    def set(self, syntax, name, index, field_type, content=""):
        self.syntax = syntax
        self.name = name
        self.index = index
        self.field_type = field_type
        self.content = content

    """
    @:return 0匹配; 1 type不匹配，造成的不匹配; 2 其他原因造成的不匹配
    """

    def compare_to(self, cmp_field, message_name):
        if not cmp_field:
            return False
        is_type_equal = self.__compare_type(cmp_field.field_type, message_name)
        is_other_equal = self.syntax == cmp_field.syntax and self.index == cmp_field.index
        if is_other_equal and is_type_equal:
            return 0
        elif is_other_equal and not is_type_equal:
            return 1
        else:
            return 2

    def __compare_type(self, field_type, message_name):
        if Config.MATCH_IS_IGNORE_TYPE or not Util.is_str_not_empty(field_type):
            return True
        type_result = False
        if Config.MATCH_IS_IGNORE_PACKAGE_NAME:
            field_type = self.__remove_package(field_type)
            self.field_type = self.__remove_package(self.field_type)
        if self.field_type == field_type:
            type_result = True
        elif Config.MATCH_IS_MAKE_BYTES_STRING_EQUAL and (self.field_type == "bytes" or self.field_type == "string"):
            type_result = field_type == "bytes" or field_type == "string"
        else:
            type_result = self.__alias_compare_type(field_type)
        if Config.IS_PRINT_FIELD_TYPE_DIS_MATCH and not type_result:
            Util.print_result_log("__compare_type dis match: message_name: %s, index: %d, cmp_type: %s, self_type: %s"
                                  % (message_name, self.index, field_type, self.field_type))
        return type_result

    def __alias_compare_type(self, field_type):
        if field_type and Config.ALIAS_DICT.__contains__(field_type):
            alias_type = Config.ALIAS_DICT[field_type]
            if self.field_type == alias_type:
                return True
            else:
                return False
        else:
            return False

    def __remove_package(self, field_type):
        if Util.is_str_not_empty(field_type):
            result = field_type.split(".")
            if result and len(result) > 0:
                return result[-1]
            else:
                return ""
        return ""

    def __str__(self):
        if Config.IS_PRINT_FIELD_DETAIL_INFO:
            return "\nMessageField content: %s ----- index: %d name: %s syntax: %s type:%s" % \
                   (self.content, self.index, self.name, self.syntax, self.field_type)
        else:
            return "%s" % self.content


class Message(object):

    def __init__(self):
        self.field_map = {}
        self.cmp_field_map = {}
        # only for compare
        self.cmp_inc_map = {}
        self.name = ""
        self.type = "\nmessage"

    def put(self, field_index, field, cmp_field=None, type=0):
        if not isinstance(field, MessageField):
            Util.print_log("failed type error")
            return
        if field_index < 0:
            Util.print_log("index invalid: %d, field: %s" %
                           (field_index, field))
            return
        # elif not Util.is_str_not_empty(field_name):
        #     Util.print_log("name invalid: %s, field: %s" %
        #               (field_name, field))
        #     return
        if type == 0:
            self.field_map[field_index] = field
            if cmp_field is not None:
                self.cmp_field_map[field_index] = cmp_field
        elif type == 1:
            self.cmp_inc_map[field_index] = field
        Util.print_log("field_index valid: %d, field: %s" %
                       (field_index, field))

    def get(self, field_index, type=0):
        tmp_map = self.field_map
        if type == 1:
            tmp_map = self.cmp_inc_map
        if field_index in tmp_map:
            return tmp_map[field_index]
        else:
            return None

    def field_count(self):
        return len(self.field_map.keys())

    def __str__(self):
        content = "  " + self.type + " " + self.name + "\n"
        for index, field in self.field_map.items():
            field_str = field.__str__().strip().strip("\n")
            content = content + field_str
            if self.cmp_field_map.__contains__(index):
                content = content + "        被比较字段:" + self.cmp_field_map[index].__str__()
        return content

    def cmp_inc_str(self):
        content = "  " + self.type + " " + self.name + "\n"
        if len(self.cmp_inc_map) == 0:
            return ""
        for _, field in self.cmp_inc_map.items():
            content = content + field.__str__()
        return content
