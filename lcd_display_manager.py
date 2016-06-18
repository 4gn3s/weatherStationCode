from utils import lcddriver


class LCDDisplayManager:
    def __init__(self):
        self.lcd = lcddriver.lcd()
        self.framebuffer = ["", ""] # 2 lines LCD
        self.row_size = 16 # number of letters in a row of the LCD display

    def show(self, data):
        self.set_framebuffer(data)
        index = 1
        for line in self.framebuffer:
            to_display_str = self.center_string(line)
            print(len(to_display_str))
            print(to_display_str)
            self.lcd.lcd_display_string(to_display_str, index)
            index += 1

    def set_framebuffer(self, data):
        self.framebuffer[0] = "Temperature: " + str(data['temperature']) + u"\u00b0" + "C"
        self.framebuffer[1] = "Humidity: " + str(data['humidity']) + "%"

    def loop_string(self, string):
        pass
        #
        # self.lcd.lcd_display_string(full_temp_str[:19], 1)
        # self.lcd.lcd_display_string(, 2)
        # for i in range(0, len(full_temp_str)):
        #     text = full_temp_str[i:(i + 20)]
        #     self.lcd.lcd_display_string(self.center_string(text), 1)
        #     self.lcd.lcd_display_string(self.center_string("Humidity: " + str(data['humidity']) + "%"), 2)
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
