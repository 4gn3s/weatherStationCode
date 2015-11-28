# Building a simple weather station with Raspberry Pi and Python (in the future: Haskell)
###############################################################

1. The setup
    * A headless Raspberry Pi 2 connected to the wifi network
    * A AM2303 temperature and humidity sensor
    * Jumper cables

2. Installing software
I have OSMC installed on my memory card, so first I needed to install some
software:
    
```sh
    sudo apt-get update
    sudo apt-get install -y gcc make build-essentials python3 screen
```

Installing pigpio:

```sh
    wget abyz.co.uk/rpi/pigpio/pigpio.zip
    unzip pigpio.zip
    make
    sudo make install
```

Running pigpio (in a new screen window):

```sh
    sudo pigpiod
```

Gathering the DHT22 module for pigpio:
```sh
    wget http://abyz.co.uk/rpi/pigpio/code/DHT22_py.zip
    unzip DHT22_py.zip
```

3. Wiring
The weather and humidity sensor AM2302 (DHT22) has 3 pins:
    * VCC (+) - input (3V to 5.5V)
    * GND (-) - ground
    * OUT     - data output

![Raspberry Pi 2 GPIO
pins](http://www.megaleecher.net/sites/default/files/images/raspberry-pi-rev2-gpio-pinout.jpg)

4. Testing the configuration
To perform a simple test if everything works as expected, let's open up
python3 console and run:
   
```python
    import pigpio
    import DHT22
    pi = pigpio.pi()
    probe = DHT22.sensor(pi, 4)
    probe.trigger()
    temp = probe.temperature()
    humid = probe.humidity
    print("Current temperature is {}C, while current humidity is
    {}%".format(temp, humid))
```

5. Gathering data
New data from the sensor can be obtained every 2 seconds.

6. Visualizing data
The data is visualized using the D3 library.

7. Final thoughts
