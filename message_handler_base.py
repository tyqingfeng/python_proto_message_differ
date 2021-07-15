#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : liangychang
# @Time : 2021/05/04
from abc import ABCMeta, abstractmethod


class MessageHandlerBase(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def handle_message(self, input_line):
        pass
