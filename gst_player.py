#!/usr/bin/python

import pygst
pygst.require('0.10')
import gst

# Define the player class wrapping the g-streamer playing capability


class Player:
    def __init__(self, audio_files):
        # raise an exception if audio_files is empty or not a list
        if not isinstance(audio_files, list) or not audio_files:
            raise TypeError
        # create playlist
        self.playlist = audio_files
        # Element playbin automatic plays any file
        self.player = gst.element_factory_make('playbin2', 'player')
        #Set the uri to the file
        self.current_song_nr = 1
        self.player.set_property('uri', 'file://' + self.playlist[self.current_song_nr - 1])
        # the variable storing the reference to the loop serving the player - empty on the beginning
        self.loop = None
        #Enable message bus to check for errors in the pipeline
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)
        # take care about a continuous playback
        self.player.connect("about-to-finish", self.on_about_to_finish)

    def play(self):
        self.player.set_state(gst.STATE_PLAYING)

    def pause(self):
        self.player.set_state(gst.STATE_PAUSED)

    def stop(self):
        self.player.set_state(gst.STATE_NULL)

    def set_volume(self, volume_level):
        print 'Original volume: {0}'.format(self.player.get_property('volume'))
        self.player.set_property('volume', volume_level)
        print 'Volume se to: {0}'.format(self.player.get_property('volume'))

    def set_loop(self, loop):
        self.loop = loop

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            # # file ended, play next if there is any or stop
            # if self.current_song_nr < len(self.playlist):
            #     print 'Playing next song'
            #     self.current_song_nr += 1
            #     self.player.set_state(gst.STATE_NULL)
            #     self.player.set_property('uri', 'file://' + self.playlist[self.current_song_nr - 1])
            #     self.player.set_state(gst.STATE_PLAYING)
            # else:
            # we played all the songs - exit
            self.player.set_state(gst.STATE_NULL)
            self.loop.quit()
        elif t == gst.MESSAGE_ERROR:
            # Error occurred, print and stop
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print 'Error: %s' % err, debug
            self.loop.quit()

    def on_about_to_finish(self, player):
        # The current song is about to finish, if we want to play another song after this, we have to do that now
        # play next if there is any or stop
        if self.current_song_nr < len(self.playlist):
            print 'Playing next song'
            self.current_song_nr += 1
            self.player.set_property('uri', 'file://' + self.playlist[self.current_song_nr - 1])