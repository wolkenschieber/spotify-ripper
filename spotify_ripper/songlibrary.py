# -*- coding: utf8 -*-
import os
import re
import sys
import collections
import shutil
import fnmatch
from colorama import Fore, Style
from spotify_ripper.utils import empty_tree
from spotify_ripper.id3 import get_id3_metadata
from spotify_ripper.targetprovider import *


class SongLibrary():
    attic = 'attic'
    target_provider = None
    musiclibrary = None

    def __init__(self, target_provider):
        self.target_provider = target_provider

        self.musiclibrary = empty_tree()
        self.__readlibrary()

    def __readlibrary(self):
        includes = ['*.mp3']
        excludes = ["*" + self.attic + "*"]

        # transform glob patterns to regular expressions
        includes = r'|'.join([fnmatch.translate(x) for x in includes])
        excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

        print("Scanning library")

        for root, dirs, files in os.walk(self.target_provider.get_base_dir()):

            dirs[:] = [os.path.join(root, d) for d in dirs]
            dirs[:] = [d for d in dirs if not re.match(excludes, d)]

            files = [os.path.join(root, f) for f in files]
            files = [f for f in files if not re.match(excludes, f)]
            files = [f for f in files if re.match(includes, f)]

            for fname in files:
                mp3_file = os.path.join(root, fname)
                artist, album, title = get_id3_metadata(mp3_file)
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
        print("Updating library")
        print(Fore.GREEN + "Moving existing files" + Fore.RESET)
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

                    if source_file != target_file:
                        print(Fore.CYAN + "Moving " + source_file + " to " + target_file + Fore.RESET)
                        shutil.move(source_file, target_file)
                    del self.musiclibrary[artist][album][title]

        print(Fore.GREEN + "Moving unmatched files to attic" + Fore.RESET)
        attic_dir = os.path.join(self.target_provider.get_base_dir(), self.attic)
        if not os.path.exists(attic_dir):
            os.makedirs(attic_dir)
        for artist, atf in self.musiclibrary.items():
            for ablum, tf in atf.items():
                for title, filename in tf.items():
                    attic_file = os.path.join(attic_dir, os.path.basename(filename))
                    print(Fore.MAGENTA + "Archiving " + filename + " to " + attic_file + Fore.RESET)
                    shutil.move(filename, attic_file)
