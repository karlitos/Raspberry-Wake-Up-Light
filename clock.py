#!/usr/bin/python

import time
import datetime
import SDL_PCF8563

from Adafruit_LED_Backpack import SevenSegment
from Adafruit_LED_Backpack import HT16K33


class LedAlarmClock:

    # adapt to match yor setup
    _BUS_NUMBER = 0  # 0 on the very first Raspberry Pi revision, 1 on every later version
    _LED_DISPLAY_ADDRESS = 0x70

    def __init__(self, address=_LED_DISPLAY_ADDRESS, bus_number=_BUS_NUMBER):
        # Remember the I2C address and bus number
        self._address = address
        self._bus_number = bus_number
        # Create display instance on specified I2C address and bus number.
        self._display = SevenSegment.SevenSegment(address=self._address, busnum=self._bus_number)
        # Create display backpack instance
        self._backpack = HT16K33.HT16K33(address=self._address, busnum=self._bus_number)
        # Initialize the display. Must be called once before using the display.
        self._display.begin()
        # Clear the display buffer.
        self._display.clear()

        # store an instance of the real-time clock module providing the time information
        self._real_time_clock = SDL_PCF8563.SDL_PCF8563(0, 0x51)
        # update the time with the time from time server
        # only if timeserver reachable

        # the alarm part begins here

        # We start with predefined alarm at 8:00 which will not be active
        self._alarm_hour = 8
        self._alarm_minute = 0
        self.set_alarm_time(self._alarm_hour, self._alarm_minute)
        self.deactivate_alarm()
        # the alarm should be stopped after some time (1h 00min) so it won't play a whole day or so
        self._maximal_alarm_duration = datetime.timedelta(hours=1, minutes=0)

    def update_display(self):
        now = self._real_time_clock.read_datetime()
        #set the tens and ones of hours and minutes
        self._display.set_digit(0, int(now.hour / 10))     # Tens
        self._display.set_digit(1, now.hour % 10)          # Ones
        self._display.set_digit(2, int(now.minute / 10))   # Tens
        self._display.set_digit(3, now.minute % 10)        # Ones
        # Toggle colon at 1Hz
        self._display.set_colon(now.second % 2)
        self._display.write_display()

    def set_display_brightness(self, brightness_level):
        self._backpack.set_display_brightness(brightness_level)

    def get_wake_up_time_str(self):
        return {'hour': self._alarm_hour, 'minute': self._alarm_minute}

    def get_wake_up_time(self):
        return datetime.time(hour=self._alarm_hour, minute=self._alarm_minute)

    def set_alarm_time(self, hour, minute):
        self._alarm_hour = hour
        self._alarm_minute = minute
        self._real_time_clock.set_daily_alarm(self._alarm_hour, self._alarm_minute)

    def activate_alarm(self):
        # first stop alarm (could be triggered in the time of alarm interrupt inactivity)
        self.stop_alarm()
        self._real_time_clock.enable_alarm_interrupt()

    def deactivate_alarm(self):
        self._real_time_clock.disable_alarm_interrupt()

    def is_alarm_active(self):
        return self._real_time_clock.check_for_alarm_interrupt()

    def check_if_alarm_on(self):
        return self._real_time_clock.check_if_alarm_on()

    def stop_alarm(self):
        self._real_time_clock.turn_alarm_off()

    def on_alarm(self):
        # start the wake up procedure ;-)
        print 'Wake up!'