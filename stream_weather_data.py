#!/usr/bin/python
import csv
import json
import time
import pigpio

import urllib.error
import urllib.parse
import urllib.request

from utils import DHT22
from lcd_display_manager import LCDDisplayManager

GPIO_PIN = 4
INTERVAL = 5  # seconds
SPARKFUN_REQUEST_INTERVAL = 2
JSON_CONFIG = "sparkfun.json"
BACKUP_FILE = "backup_sensor.csv"

class DataStreamer():
    def __init__(self, public_key, private_key, stream_data=True, show_on_lcd=True):
        self.pi = pigpio.pi()
        self.sensor = DHT22.sensor(self.pi, GPIO_PIN)
        self.last_temperature = 0
        self.last_humidity = 0
        self.base_url = 'https://data.sparkfun.com/input/'
        self.url = self.base_url + public_key + "?private_key=" + private_key
        self.stream_data = stream_data
        self.show_on_lcd = show_on_lcd
        self.lcd_display_manager = LCDDisplayManager()

    def run(self):
        queued_data = []
        while True:
            if len(queued_data) > 0:
                print("Has to resend %s packages" % len(queued_data))
                temp_queued_data = []
                while len(queued_data) > 0:
                    data = queued_data.pop()  # the ones the longest in the list are the oldest ones
                    if not self.do_stream_data(data):  # if not successful, queue it again
                        temp_queued_data.append(data)
                    time.sleep(SPARKFUN_REQUEST_INTERVAL)
                queued_data = temp_queued_data
                print("Managed to reduce the queue size to %s" % len(queued_data))
            data = self.get_data()
            if data['temperature'] != self.last_temperature or data['humidity'] != self.last_humidity:
                if not self.do_stream_data(data):
                    print("Error sending %s, queueing" % data)
                    queued_data.append(data)
                self.backup_data(data)
                self.last_temperature = data['temperature']
                self.last_humidity = data['humidity']
                print("Current temperature {}C, humidity {}%".format(data['temperature'], data['humidity']))
                if self.show_on_lcd:
                    self.lcd_display_manager.display_message(data)
            time.sleep(INTERVAL)

    def get_data(self):
        self.sensor.trigger()
        data = {}
        temperature = round(self.sensor.temperature(), 2)
        if temperature == (-999):
            temperature = self.last_temperature
        data['temperature'] = temperature
        humidity = round(self.sensor.humidity(), 2)
        if humidity == (-999):
            humidity = self.last_humidity
        data['humidity'] = humidity
        return data

    def do_stream_data(self, data):
        if self.stream_data:
            data = urllib.parse.urlencode(data).encode('utf-8')
            request = urllib.request.Request(self.url)
            request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
            try:
                with urllib.request.urlopen(request, data) as response:
                    print(response.read().decode('utf-8'))
            except urllib.error.URLError as e:
                print("URL Error ", e.reason)
                return False
            except http.client.BadStatusLine as e:
                print("BadStatusLine Error ", e.reason)
                return False
            return True
        return True

    def backup_data(self, data):
        with open(BACKUP_FILE, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow([data[x] for x in data.keys()])


if __name__ == '__main__':
    with open(JSON_CONFIG) as config:
        sparkfun_keys = json.load(config)
        ds = DataStreamer(sparkfun_keys['publicKey'], sparkfun_keys['privateKey'], False, True)
        ds.run()
