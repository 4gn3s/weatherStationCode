# Building a simple weather station with Raspberry Pi and Python
###############################################################

## The setup
* A headless Raspberry Pi 2 connected to the wifi network
* A AM2303 temperature and humidity sensor
* Jumper cables

## Installing software
I have OSMC installed on my memory card, so first I needed to install some
software:
    
```sh
    sudo apt-get update
    sudo apt-get install -y gcc make build-essentials python3 screen
```

Install raspi-config as defined [here](https://github.com/snubbegbg/install_raspi-config).

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

Installing smbus:
```sh
sudo -i
apt-get install python3-dev
apt-get install libi2c-dev
cd /tmp
wget http://ftp.de.debian.org/debian/pool/main/i/i2c-tools/i2c-tools_3.1.0.orig.tar.bz2 # download Python 2 source
tar xavf i2c-tools_3.1.0.orig.tar.bz2
cd i2c-tools-3.1.0/py-smbus
mv smbusmodule.c smbusmodule.c.orig # backup
wget https://gist.githubusercontent.com/sebastianludwig/c648a9e06c0dc2264fbd/raw/2b74f9e72bbdffe298ce02214be8ea1c20aa290f/smbusmodule.c # download patched (Python 3) source
python3 setup.py build
python3 setup.py install
exit
```

The next step is to enable i2c via raspi-config: sudo raspi-config , select advance menu, select i2c, then enable it.

Use:
```sh
sudo i2cdetect -y 1
```
to check if the i2c device is found. If not, follow the advice [here](https://raspberrypi.stackexchange.com/questions/14153/adafruit-i2c-library-problem).

## Wiring
The weather and humidity sensor AM2302 (DHT22) has 3 pins:
 * VCC (+) - input (3V to 5.5V)
 * GND (-) - ground
 * OUT     - data output

![Raspberry Pi 2 GPIO
pins](http://www.megaleecher.net/sites/default/files/images/raspberry-pi-rev2-gpio-pinout.jpg)

## Testing the configuration
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

## Gathering data
New data from the sensor can be obtained every 2 seconds. It is streamed to my sparkfun API account.

## Visualizing data
The data is visualized using the D3 library. The results can be viewed here: [https://4gn3s.github.io/weatherStation/](https://4gn3s.github.io/weatherStation/)
There are separate graphs for temperature and humidity.

## Ideas for the future

### More sensors to measure:
* wind & speed direction
* light cycles
* air quality
* barometric pressure

### Data gathering
How does the temperature in my room vary between day and night, weekdays and weekend?

### Full webapp
* get a touch display
* view radar images from the internet (served as gifs)
* show alerts (from wunderground)

