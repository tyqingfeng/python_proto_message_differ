#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : liangychang
# @Time : 2021/05/04
import os
import os.path
from util import Util
from config import Config
import message_handler
from message_compare import MessageCompare


def process_file(path):
    if not Util.is_str_not_empty(path):
        print("input path empty")
    elif not os.path.isfile(path):
        print("input path is not file")
    elif not os.path.exists(path):
        print("input file not exist")
    else:
        handler = message_handler.MessageHandler()
        with open(path, 'r') as file:
            lines = file.readlines()
            if not lines:
                return
            for line in lines:
                handler.handle_message(line)
        return handler


def diff_handle(handler, cmp_handler, desc, file_name, brief_file_name):
    if handler and cmp_handler:
        compare = MessageCompare()
        compare.compare(handler.messages, cmp_handler.messages)
        compare.print_diff_message()
        compare.save_compare_result(desc, file_name)
        compare.save_brief_result(desc, brief_file_name)


if __name__ == "__main__":
    print("cur_path:", os.listdir())
    msg_handler = process_file(Config.MESSAGE_FILE_PATH)
    msg_handler.rename_messages(Config.ALIAS_DICT)
    msg_1_handler = process_file(Config.MESSAGE_FILE_1_PATH)
    cmp_message_handler = process_file(Config.CMP_MESSAGE_FILE_PATH)
    diff_handle(cmp_message_handler, msg_handler, "diff1", Config.OUTPUT_FILE_NAME, Config.OUTPUT_BRIEF_FILE_NAME)
    print("\n\n=========live compare==========")
    diff_handle(cmp_message_handler, msg_1_handler, "diff2", Config.OUTPUT_FILE_2_NAME, Config.OUTPUT_BRIEF_FILE_2_NAME)
