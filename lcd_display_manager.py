# -*- coding: utf-8 -*-
import threading

import time
from queue import Queue

from utils import lcddriver


class LCDDisplayManager:
    def __init__(self):
        self.lcd = lcddriver.lcd()
        self.framebuffer = ["", ""]  # 2 lines LCD
        self.scroll_index = [0, 0]
        self.row_size = 16  # number of letters in a row of the LCD display
        self.writing_thread = threading.Thread(target=self.show, args=(), kwargs={})
        self.queue = Queue()
        self.writing_thread.start()

    def display_message(self, data):
        self.queue.put(data)

    def show(self):
        data = self.queue.get()
        self.set_framebuffer(data)
        while True:
            for line_index, line in enumerate(self.framebuffer):
                i = self.scroll_index[line_index]
                to_display_str = line[i : (i + self.row_size)]
                self.lcd.lcd_display_string(to_display_str, line_index + 1)
                self.scroll_index[line_index] += 1
                if self.scroll_index[line_index] > len(line):
                    self.scroll_index[line_index] = 0
            time.sleep(0.3)

    def set_framebuffer(self, data):
        self.framebuffer[0] = "Temperature: " + str(data['temperature']) + "°C" + " " * self.row_size
        self.framebuffer[1] = "Humidity: " + str(data['humidity']) + "%" + " " * self.row_size
        self.scroll_index = [0, 0]

    def loop_string(self, string):
        pass
        # for i in range(0, len(full_temp_str)):
        #     text = full_temp_str[i:(i + 20)]
        #     time.sleep(0.2)

    def center_string(self, string):
        str_len = len(string)
        if str_len > self.row_size:
            return string[:self.row_size-1]
        spaces_needed = self.row_size - str_len
        mod = 0
        if spaces_needed % 2 != 0:
            mod = 1
        return " " * (spaces_needed // 2) + string + " " * (spaces_needed // 2 + mod)
