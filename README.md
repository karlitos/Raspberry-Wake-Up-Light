Raspberry-Wake-Up-Light
========================

Raspberry Wake-Up (Light) is development of a small music alarm clock, based on Raspberry Pi with the possibility of steering the the Philips HUE lights. This project is strongly inspired by the Philips Wake-Up Light alarm clock just trying to improve the flaws of the original Philips design. 

## The LED clock display

For the clock display I used the wonderful LED 7-Segment, 4-Digit Display w/I2C Backpack made by Adafruit. For further details and specifications see the [product page](https://www.adafruit.com/products/881). I rely in this project on the provided Python library, you can download the latest code on the [Adafruit GitHub page](https://github.com/adafruit/Adafruit_Python_LED_Backpack). Follow the steps stated there for the installation of the necessary libraries.

If you choose to use another LED display, yo have to adapt the [clock.py](clock.py) file. But I will strongly recommend using the Adafruit parts, they very high quality and you get also a good support for them.
 
 ## Prerequisites
 sudo apt-get install python-gst0.10 
 