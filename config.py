#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : liangychang
# @Time : 2021/05/04


class Config(object):
    # 日志
    IS_PRINT_LOG = True
    IS_PRINT_RESULT_LOG = True
    IS_PRINT_INC_FIELD = False
    IS_PRINT_FIELD_DETAIL_INFO = False
    IS_PRINT_FIELD_TYPE_DIS_MATCH = True

    # 测试配置
    IS_PRINT_LOG = False
    MESSAGE_FILE_PATH = "msg.txt"
    MESSAGE_FILE_1_PATH = "msg1.txt"
    CMP_MESSAGE_FILE_PATH = "msg_compare.txt"

    # 是否匹配字段的缺失
    MATCH_IS_CATCH_LEAK_FIELD = False
    # 是否只匹配由于类型不一致引起的diff；忽略其他原因
    MATCH_IS_CATCH_OTHER_DISMISS_TYPE = False
    # 不匹配类型， 如int32 和 string； 如协议中定义的枚举，在其他协议中为int类型
    MATCH_IS_IGNORE_TYPE = False
    MATCH_IS_IGNORE_PACKAGE_NAME = True  # 忽略包名
    # 强制匹配部分类型
    MATCH_IS_MAKE_BYTES_STRING_EQUAL = False

    # 输出结构
    OUTPUT_FILE_NAME = "result_1.txt"
    OUTPUT_BRIEF_FILE_NAME = "brief_result_1.txt"
    OUTPUT_FILE_2_NAME = "result_2.txt"
    OUTPUT_BRIEF_FILE_2_NAME = "brief_result_2.txt"

    # 语法词
    SYNTAX_WORDS = ["optional", "repeated", "required"]
    # 定义message 名称不同，实际为一个协议时，使用匿名方式比较
    ALIAS_DICT = {
        "AddressBookAlias": "AddressBook"
    }

