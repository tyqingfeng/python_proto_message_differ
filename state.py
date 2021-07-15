#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : liangychang
# @Time : 2021/05/03


class State(object):

    STATE_INIT = 0
    STATE_START_BEGIN = 10
    STATE_START_INTER = 11
    STATE_START_END = 12
    STATE_MIDDLE_BEGIN = 20
    STATE_MIDDLE_INTER = 21
    STATE_MIDDLE_START_CHECK = 22
    STATE_MIDDLE_END = 23
    STATE_STOP_BEGIN = 30
    STATE_STOP_INTER = 31
    STATE_STOP_END = 32
    STATE_ERROR = 100

    INIT_STAGE = 0
    START_STAGE = 1
    MIDDLE_STAGE = 2
    STOP_STAGE = 3
    ERROR_STAGE = 10

    @staticmethod
    def get_state_stage(state):
        if state == State.STATE_INIT:
            return State.INIT_STAGE
        elif State.STATE_START_BEGIN <= state <= State.STATE_START_END:
            return State.START_STAGE
        elif State.STATE_MIDDLE_BEGIN <= state <= State.STATE_MIDDLE_END:
            return State.MIDDLE_STAGE
        elif State.STATE_STOP_BEGIN <= state <= State.STATE_STOP_END:
            return State.STOP_STAGE
        else:
            return State.ERROR_STAGE
