#!/usr/bin/python

import time
import datetime

from Adafruit_LED_Backpack import SevenSegment


class LedClock:

    def __init__(self, address=0x70, bus_number=0):
        # Remember the I2C address and bus number
        self.address = address
        self.bus_number = bus_number
        # Create display instance on specified I2C address and bus number.
        self.display = SevenSegment.SevenSegment(address=self.address, busnum=self.bus_number)
        # Initialize the display. Must be called once before using the display.
        self.display.begin()
        # Keep track of the colon being turned on or off.
        # Clear the display buffer.
        self.display.clear()
        # set the initial time
        self.hour = 0
        self.minute = 0
        self.second = 0
        # the update interval in seconds
        self.update_interval = 1
        self.keep_running = True
        # the instance of the alarm
        self.alarm = AlarmClock()

    def run(self):
        while self.keep_running:
            # update the clock time
            now = datetime.datetime.now()
            self.hour = now.hour
            self.minute = now.minute
            self.second = now.second
            # set the tens and ones of hours and minutes
            self.display.set_digit(0, int(self.hour / 10))     # Tens
            self.display.set_digit(1, self.hour % 10)          # Ones
            self.display.set_digit(2, int(self.minute / 10))   # Tens
            self.display.set_digit(3, self.minute % 10)        # Ones
            # Toggle colon at 1Hz
            self.display.set_colon(self.second % 2)
            self.display.write_display()
            # now check if the alarm should not be started
            if self.alarm.is_active():
                print self.alarm.time_till_next_alarm()
            time.sleep(self.update_interval)

    def get_alarm(self):
        return self.alarm


class AlarmClock:
    def __init__(self, hour=8, minute=0):
        # We start with predefined alarm at 8:00 which is not active
        self.hour = hour
        self.minute = minute
        self.active = False
        # the alarm should be stopped after some time (1h 00min)
        self.duration = datetime.timedelta(hours=1, minutes=0)

    def time_till_next_alarm(self):
        now = datetime.datetime.now()  # get current date & time

        # separate date and time from each other:
        currdate = datetime.date(now.year, now.month, now.day)
        currtime = datetime.time(now.hour, now.minute)
        alarmtime = self.get_wake_up_time()
        # add today's date onto the alarm time entered
        alarmdatetime = datetime.datetime.combine(currdate, alarmtime)
        if alarmtime <= currtime:  # if the alarm time is less than the current time set clock for tomorrow
            alarmdatetime += datetime.timedelta(hours=24)

        return (alarmdatetime - now).total_seconds()


    def get_wake_up_time_str(self):
        return {'hour': self.hour, 'minute': self.minute}

    def get_wake_up_time(self):
        return datetime.time(hour=self.hour, minute=self.minute)

    def set_time(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def is_active(self):
        return self.active

    def on_wake_up(self):
        # start the wake up
        print 'Wake up!'





#Execution starts here
if __name__ == '__main__':

    clock = LedClock(0x70, 0)
    clock.get_alarm().activate()
    clock.get_alarm().set_time(1,26)
    clock.run()

