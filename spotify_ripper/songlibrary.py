# -*- coding: utf8 -*-

import os
import sys
import collections
import fnmatch
import logging
from spotify_ripper.utils import empty_tree
from spotify_ripper.id3 import get_id3_metadata


class SongLibrary():
    logger = logging.getLogger('spotify.songlibrary')

    library_dir = None
    musiclibrary = None

    def __init__(self, library_dir):
        self.library_dir = library_dir

        self.musiclibrary = empty_tree()
        self.__readlibrary()

    def __readlibrary(self):
        for root, dirnames, filenames in os.walk(self.library_dir):
            for filename in fnmatch.filter(filenames, '*.mp3'):
                mp3_file = os.path.join(root, filename)
                artist, album, title = get_id3_metadata(mp3_file)

                print(mp3_file)
                self.musiclibrary[artist][album][title] = mp3_file

    def contains_track(self, artist, album, title):
        return self.musiclibrary is not None and self.musiclibrary[artist][album][title]

if __name__ == '__main__':
    folder = "/home/keibak/Musik/Curriculum Vitae --- Jamendo - MP3 VBR 192k"
    song_lib = SongLibrary(folder)
    print(song_lib.musiclibrary)

