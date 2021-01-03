#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Simply plug your PS4 controller into your computer using USB and run this
# script!
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
#
# Distributed under terms of the MIT license.

import pygame

JOY_LEFT_Y = 1
JOY_LEFT_X = 0
JOY_RIGHT_X = 2
JOY_RIGHT_Y = 3
TRIGGER_RIGHT = 4
TRIGGER_LEFT = 5


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    def __init__(self, joy_id):
        """
        :type joy_id: int
        """
        self.controller = pygame.joystick.Joystick(joy_id)
        self.controller.init()

        self.axis_data = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: -1,
            5: -1,
        }
        self.button_data = {}
        self.hat_data = {}
        self.listeners = []

        for i in range(self.controller.get_numbuttons()):
            self.button_data[i] = False

        for i in range(self.controller.get_numhats()):
            self.hat_data[i] = (0, 0)

    def add_listener(self, func):
        self.listeners.append(func)

    def remove_listener(self, func):
        self.listeners.remove(func)

    def listen(self):
        while True:
            had_event = False
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    new_movement = round(event.value, 2)
                    if new_movement != self.axis_data[event.axis]:
                        had_event = True
                        self.axis_data[event.axis] = new_movement
                elif event.type == pygame.JOYBUTTONDOWN:
                    if not self.button_data[event.button]:
                        had_event = True
                        self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    if self.button_data[event.button]:
                        had_event = True
                        self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    if self.hat_data[event.hat] != event.value:
                        had_event = True
                        self.hat_data[event.hat] = event.value

            if had_event:
                for listener in self.listeners:
                    listener({
                        "axis_data": self.axis_data,
                        "button_data": self.button_data,
                        "hat_data": self.hat_data
                    })
