import os
import spotify
from spotify_ripper.utils import norm_path, to_ascii, escape_filename_part


class TargetProvider():
    args = None

    def __init__(self, args):
        self.args = args

    def get_mp3_file_from_track(self, idx, track):
        # args = self.args
        # artist = to_ascii(args, escape_filename_part(track.artists[0].name))
        # album = to_ascii(args, escape_filename_part(track.album.name))
        # track_name = to_ascii(args, escape_filename_part(track.name))

        artist, album, track_name = self.get_track_metadata(track)

        mp3_file = self.get_mp3_file(idx, artist, album, track_name)
        return mp3_file

    def get_track_metadata(self, track):
        args = self.args

        artist = to_ascii(args, escape_filename_part(', '.join(tas.name for tas in track.artists)))
        album = to_ascii(args, escape_filename_part(track.album.name))
        track_name = to_ascii(args, escape_filename_part(track.name))

        return artist, album, track_name

    def get_mp3_file(self, idx, artist, album, track_name):
        args = self.args
        base_dir = self.get_base_dir()

        if args.flat:
            mp3_file = to_ascii(args, os.path.join(base_dir, artist + " - " + track_name + ".mp3"))
        elif args.Flat:
            filled_idx = str(idx).zfill(self.get_idx_digits())
            mp3_file = to_ascii(args, os.path.join(base_dir, filled_idx + " - " + artist + " - " + track_name + ".mp3"))
        else:
            mp3_file = to_ascii(args, os.path.join(base_dir, artist, album, artist + " - " + track_name + ".mp3"))

        # create directory if it doesn't exist
        mp3_path = os.path.dirname(mp3_file)
        if not os.path.exists(mp3_path):
            os.makedirs(mp3_path)

        return mp3_file

    def get_base_dir(self):
        base_dir = norm_path(self.args.directory[0]) if self.args.directory is not None else os.getcwd()
        return base_dir

    def get_idx_digits(self):
        return 3


class PlaylistTargetProvider(TargetProvider):
    args = None
    playlist = None

    def __init__(self, args, playlist):
        self.args = args
        self.playlist = playlist

    def get_base_dir(self):
        base_dir = super(PlaylistTargetProvider, self).get_base_dir()

        if self.playlist and self.playlist.name != "":
            playlist_name = to_ascii(self.args, escape_filename_part(self.playlist.name))
            base_dir = os.path.join(base_dir, playlist_name)

        return base_dir

    def get_idx_digits(self):
        if self.args.Flat and self.playlist:
            idx_digits = len(str(len(self.playlist.tracks)))
            return idx_digits
