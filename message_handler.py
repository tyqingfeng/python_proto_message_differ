#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : liangychang
# @Time : 2021/05/04
from message_handler_base import MessageHandlerBase
from state import *
from util import Util
import re
from matcher import Matcher
from message import Message


class MessageHandler(MessageHandlerBase):

    def __init__(self):
        # super.__init__(self)
        self.reset()
        
    def reset(self):
        self.state = State.STATE_INIT
        self.last_state = State.STATE_INIT
        self.stage = State.INIT_STAGE
        self.stack = []
        self.matcher = Matcher()
        self.messages = []

    def peek(self):
        if len(self.stack) > 0:
            top_message = self.stack.pop()
            self.stack.append(top_message)
            return top_message
        return None
        
    def __match_start(self, input_line):
        Util.print_log("match_start input_line：\n" + input_line + " state:" + str(self.state) + "\n")
        if self.state == State.STATE_INIT or self.state == State.STATE_START_BEGIN:
            name, end_flag, message_type = self.matcher.match_start(input_line)
            Util.print_log("name:" + name + " end_flag:" + str(end_flag))
            if end_flag or Util.is_str_not_empty(name):
                message = Message()
                message.name = name
                message.type = message_type
                self.messages.append(message)
                self.stack.append(message)
                if end_flag:
                    self.state = State.STATE_MIDDLE_BEGIN
                else:
                    self.state = State.STATE_START_INTER
                Util.print_log("stack input message: " + message.__str__())
            else: 
                Util.print_log("__match_start init not match")
        elif self.state == State.STATE_START_INTER:
            Util.print_log("STATE_START_INTER")
            is_exist, end_index = self.matcher.match_start_end(input_line)
            if is_exist:
                message = self.peek()
                if not message:
                    self.state = State.STATE_ERROR
                else:
                    self.state = State.STATE_START_END
                return end_index
            else:
                Util.print_log("__match_start STATE_START_INTER not match")
        else:
            Util.print_log("__match_start not match")
        
    def __match_middle(self, input_line):
        """
        1. 匹配message field
        2. 检查是否包含结尾符
        3. 检查是否有新的message， 并处理
        """
        Util.print_log("match_middle input_line====\n" + input_line)
        
        if self.state == State.STATE_MIDDLE_BEGIN or self.state == State.STATE_MIDDLE_START_CHECK:
            message_field = self.matcher.match_middle(input_line)
            Util.print_log("message_field " + message_field.__str__())
            if message_field:
                message = self.peek()
                Util.print_log(message_field)
                if message:
                    message.put(message_field.index, message_field)
                    if self.matcher.match_stop_middle(input_line):
                        Util.print_log("__match_middle match middle end")
                        self.state = State.STATE_STOP_END
                    Util.print_log("__match_middle input field:%s, %s state:%d" % (message, message_field, self.state))
            elif self.matcher.match_middle_value(input_line):
                Util.print_log("__match_middle#match_middle_value True")
                pass
            elif self.matcher.match_stop(input_line):
                Util.print_log("__match_middle match end")
                self.state = State.STATE_STOP_END
            # elif self.state != State.STATE_MIDDLE_START_CHECK:
            else:
                Util.print_log("__match_middle STATE_MIDDLE_START_CHECK")
                name, _, _ = self.matcher.match_start(input_line)
                if Util.is_str_not_empty(name):
                    # 有新的message, 改变状态，并通过handle_message处理
                    self.state = State.STATE_START_BEGIN
                    Util.print_log("__match_middle match message start")
                Util.print_log("__match_middle STATE_MIDDLE_BEGIN not match")

    def handle_message(self, input_line):
        Util.print_log("handle_message==========\n" + input_line)
        line = self.matcher.remove_annotation(input_line)
        if not Util.is_str_not_empty(line):
            Util.print_log("line empty")
            return
        self.stage = State.get_state_stage(self.state)
        Util.print_log("stage:%d" % self.stage)
        if self.stage == State.INIT_STAGE or self.stage == State.START_STAGE:
            match_end_index = self.__match_start(line)
            if self.state == State.STATE_START_END:
                # 匹配message body
                self.state = State.STATE_MIDDLE_START_CHECK
                if match_end_index:
                    sub_input_line = Util.sub_str(input_line, match_end_index)
                    Util.print_log(sub_input_line, "MessageHandler#handleMessage#STATE_MIDDLE_START_CHECK")
                    self.handle_message(sub_input_line)
                else:
                    self.handle_message(input_line)
            pass
        elif self.stage == State.MIDDLE_STAGE:
            self.__match_middle(input_line)
            if self.state == State.STATE_START_BEGIN:
                self.handle_message(input_line) 
        elif self.stage == State.STOP_STAGE:
            self.stack.pop()
            if len(self.stack) == 0:
                self.state = State.STATE_START_BEGIN
            else:
                self.state = State.STATE_MIDDLE_BEGIN
            self.handle_message(input_line)
            pass
        Util.print_log("handle_message end:" + str(self.state))

    def match_test(self, input_line):
        reg = r"message +(?P<name>\w+) *(?P<end_tag>{?)"
        result = re.search(reg, input_line)

        if result and result.groupdict():
            key_dict = result.groupdict()
            for key in key_dict.keys():
                Util.print_log("key:%s value:%s" % (key, key_dict[key]))
            if key_dict and key_dict.__contains__("end_tag"):
                self.state = State.STATE_START_END
            Util.print_log("state:%d" % (self.state))

    def print_message(self):
        Util.print_log("================print_message===================")
        for message in self.messages:
            Util.print_log("message:" + message.__str__())
            Util.print_log("\n")
            
    def rename_messages(self, name_dict):
        if name_dict and isinstance(name_dict, dict):
            for message in self.messages:
                if message.name:
                    alias_name = Util.dict_get(name_dict, message.name)
                    if Util.is_str_not_empty(alias_name):
                        message.name = alias_name
