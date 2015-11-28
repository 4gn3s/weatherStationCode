#!/usr/bin/python
import pigpio
import DHT22
import json
import csv
import time
import urllib.request
import urllib.parse
import urllib.error

GPIO_PIN = 4
INTERVAL = 60  # seconds
JSON_CONFIG = "sparkfun.json"
BACKUP_FILE = "backup_sensor.csv"

class DataStreamer():
	def __init__(self, public_key, private_key):
		self.pi = pigpio.pi()
		self.sensor = DHT22.sensor(self.pi, GPIO_PIN)
		self.last_temperature = 0
		self.last_humidity = 0
		self.base_url = 'https://data.sparkfun.com/input/'
		self.url = self.base_url + public_key + "?private_key=" + private_key
	
	def run(self):
		while True:
			data = self.get_data()
			if data['temperature'] != self.last_temperature or data['humidity'] != self.last_humidity:
				self.stream_data(data)
				self.backup_data(data)
				self.last_temperature = data['temperature']
				self.last_humidity = data['humidity']
				print("Current temperature {}C, humidity {}%".format(data['temperature'], data['humidity']))
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

	def stream_data(self, data):
		data = urllib.parse.urlencode(data).encode('utf-8')
		request = urllib.request.Request(self.url)
		request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
		try:
			with urllib.request.urlopen(request, data) as response:
				print(response.read().decode('utf-8'))
		except urllib.error.URLError as e:
			print("Error", e.reason)
	
	def backup_data(self, data):
		with open(BACKUP_FILE, 'a') as csvfile:
			writer = csv.writer(csvfile, delimiter=";")
			writer.writerow([data[x] for x in data.keys()])

			

if __name__ == '__main__':
	with open(JSON_CONFIG) as config:
		sparkfun_keys = json.load(config)
		ds = DataStreamer(sparkfun_keys['publicKey'], sparkfun_keys['privateKey'])
		ds.run()
