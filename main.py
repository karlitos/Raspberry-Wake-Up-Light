#!/usr/bin/python

import gst_player
import clock
import time
import gobject
import glob
import os
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# some global variables, will be moved elsewhere in the future probably
SUPPORTED_AUDIO_FORMATS = ['.mp3', '.ogg', '.flac']
MUSIC_FOLDER = './music'


def generate_random_music_file_list(music_folder):
    try:
        music_file_list = []
        for filename in glob.glob(os.path.join(music_folder, '*.*')):
             if os.path.splitext(filename)[1] in SUPPORTED_AUDIO_FORMATS:
                #music_file_list.append(os.path.realpath(filename))
                # insert the files on random positions
                music_file_list.insert(random.randrange(len(music_file_list)+1), os.path.realpath(filename))
        return music_file_list
    except IOError as e:
        print 'Error when generating the music file list from the directory {0}, {[1]}'.format(MUSIC_FOLDER, e)
    except Exception, e:
        pass


def main():
    # the main part of the program

    # # Get audio files from the music folder in random order
    # music_files = generate_random_music_file_list(MUSIC_FOLDER)
    # print music_files

    #player = gst_player.Player(music_files)
    #player.play()

    # for vol_lvl in range(1, 20):
    #     player.set_volume(vol_lvl*0.1)
    #     time.sleep(2)

    # initialize the led clock
    alarm_clock = clock.LedAlarmClock()

    # set up some alarm
    print 'Alarm ringing:', alarm_clock.check_if_alarm_on()
    print 'Alarm enabled', alarm_clock.is_alarm_active()

    # define some callbacks
    # the callback which reacts on the clock pulse
    def clock_alarm_callback(channel):
        print 'Alarm ringing:', alarm_clock.check_if_alarm_on()
        print 'Alarm enabled', alarm_clock.is_alarm_active()
        alarm_clock.on_alarm()

    # the callback which reacts on the alarm
    def clock_pulse_callback(channel):
        #print "Clock tick"
        alarm_clock.update_display()

    # assign the callbacks to the GPIO events
    GPIO.add_event_detect(4, GPIO.FALLING, callback=clock_alarm_callback, bouncetime=100)
    GPIO.add_event_detect(17, GPIO.FALLING, callback=clock_pulse_callback, bouncetime=100)

    try:
        h, m = input('Enter the alarm hour and minute (with a comma in between hh,mm): ')
        alarm_clock.set_alarm_time(h, m)
        print 'Daily alarm set for {0}:{1}'.format(h, m)
        alarm_clock.activate_alarm()
        print 'Alarm enabled', alarm_clock.is_alarm_active()
        raw_input('Press Enter to exit\n>')
        #loop = gobject.MainLoop()
        #player.set_loop(loop)
        #loop.run()

    except KeyboardInterrupt:
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit

    #player.set_volume(0.,1)


#Execution starts here
if __name__ == '__main__':
    main()
    print 'END!'
    GPIO.cleanup()