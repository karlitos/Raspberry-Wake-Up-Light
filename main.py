import gst_player
import time
import gobject
import glob
import os
import random

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

    #Specify your file bellow
    #It can be any video/audio supported by gstreamer
    music_files = generate_random_music_file_list(MUSIC_FOLDER)
    print music_files

    player = gst_player.Player(music_files)
    player.play()

    # for vol_lvl in range(1, 20):
    #     player.set_volume(vol_lvl*0.1)
    #     time.sleep(2)

    #player.set_volume(0.,1)
    loop = gobject.MainLoop()
    player.set_loop(loop)
    loop.run()

#Execution starts here
if __name__ == '__main__':
    main()