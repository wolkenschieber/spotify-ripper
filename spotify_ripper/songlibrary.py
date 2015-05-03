# -*- coding: utf8 -*-
from logging import info

import os
import re
import sys
import collections
import fnmatch
import logging
from spotify_ripper.utils import empty_tree
from spotify_ripper.id3 import get_id3_metadata
from spotify_ripper.targetprovider import *


class SongLibrary():
    logger = logging.getLogger('spotify.songlibrary')

    attic = 'attic'
    target_provider = None
    musiclibrary = None

    def __init__(self, target_provider):
        self.target_provider = target_provider

        self.musiclibrary = empty_tree()
        self.__readlibrary()

    def __readlibrary(self):
        includes = ['*.mp3']
        excludes = ["*"+self.attic+"*"]

        # transform glob patterns to regular expressions
        includes = r'|'.join([fnmatch.translate(x) for x in includes])
        excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

        print("includes: " + includes)
        print("excludes: " + excludes)

        for root, dirs, files in os.walk(self.target_provider.get_base_dir()):

            dirs[:] = [os.path.join(root, d) for d in dirs]
            dirs[:] = [d for d in dirs if not re.match(excludes, d)]

            files = [os.path.join(root, f) for f in files]
            files = [f for f in files if not re.match(excludes, f)]
            files = [f for f in files if re.match(includes, f)]

            for fname in files:
                mp3_file = os.path.join(root, fname)
                artist, album, title = get_id3_metadata(mp3_file)

                print(mp3_file)
                self.musiclibrary[artist][album][title] = mp3_file

    def contains_track(self, artist, album, title):
        return self.musiclibrary is not None and self.musiclibrary[artist][album][title]


class FolderTargetProvider(TargetProvider):

    folder = None

    def __init__(self, folder):
        self.folder = folder

    def get_base_dir(self):
        return self.folder

if __name__ == '__main__':
    folder_target_provider = FolderTargetProvider("/home/keibak/Musik/Curriculum Vitae --- Jamendo - MP3 VBR 192k")
    song_lib = SongLibrary(folder_target_provider)
    print(song_lib.musiclibrary)



