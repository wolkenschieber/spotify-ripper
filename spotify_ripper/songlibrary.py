# -*- coding: utf8 -*-
from logging import info

import os
import re
import sys
import collections
import shutil
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

    def update_existing(self, artist, album, title, index):
        pass

    def store_new_track(self, artist, album, track_name, idx, filename):
        pass

    def update_library(self):
        pass


class PlaylistLibrary(SongLibrary):

    playlist = None
    new_tracks = None

    def __init__(self, target_provider):
        super().__init__(target_provider)
        self.playlist = empty_tree()
        self.new_tracks = empty_tree()

    def update_existing(self, artist, album, title, index):
        self.__store_playlist_entry(artist, album, title, index)

    def store_new_track(self, artist, album, title, index, filename):
        self.__store_playlist_entry(artist, album, title, index)
        self.new_tracks[artist][album][title] = filename

    def __store_playlist_entry(self, artist, album, title, index):
        self.playlist[artist][album][title] = index

    def update_library(self):
        for artist, ati in self.playlist.items():
            for album, ti in ati.items():
                for title, index in ti.items():

                    source_file = None
                    if self.new_tracks[artist][album][title]:
                        source_file = self.new_tracks[artist][album][title]
                    elif self.musiclibrary[artist][album][title]:
                        source_file = self.musiclibrary[artist][album][title]
                    else:
                        continue

                    target_file = self.target_provider.get_mp3_file(index, artist, album, title)
                    shutil.move(source_file, target_file)

        # TODO move unmatched library entries into the attic

# for testing
class FolderTargetProvider(TargetProvider):

    folder = None

    def __init__(self, folder):
        self.folder = folder

    def get_base_dir(self):
        return self.folder

if __name__ == '__main__':
    #folder_target_provider = FolderTargetProvider("/home/keibak/Musik/Curriculum Vitae --- Jamendo - MP3 VBR 192k")
    folder_target_provider = FolderTargetProvider("/home/keibak/Musik/Martin_Tungevaag_-_Wicked_Wonderland-(8056450046671)-WEB-2014-ZzZz")
    song_lib = PlaylistLibrary(folder_target_provider)
    song_lib.update_existing("foo", "bar", "baz", 3)
    print(song_lib.musiclibrary)
    print(song_lib.playlist)
    song_lib.update_library()



