spotify-ripper
==============

A fork of a fork of
`spotify-ripper <https://github.com/robbeofficial/spotifyripper>`__ that
uses `pyspotify <https://github.com/mopidy/pyspotify>`__ v2.x

Spotify-ripper is a small ripper script for Spotify that rips Spotify
URIs to MP3 files and includes ID3 tags and cover art.

**Note that stream ripping violates the libspotify's ToS**

**Hometaping kills music**

Features
--------

-  real-time VBR or CBR ripping from spotify PCM stream

-  writes id3 tags (including album covers)

-  creates files and directories based on the following structure
   artist/album/artist - song.mp3

-  optionally skip existing files

-  accepts tracks, playlists, albums, and artist URIs

-  search for tracks using Spotify queries

-  options for interactive login (no password in shell history) and
   relogin using previous credentials

-  option to remove tracks from playlist after successful ripping

-  globally installs ripper script using pip

-  Python 2.7.x and 3.4.x compatible.  Python 3 will occasionally throw a ``NameError: name '_lock' is not defined`` exception at the end of the script due to an `upstream bug <https://github.com/mopidy/pyspotify/issues/133>`__ in ``pyspotify``.

-  use a config file to specify common command-line options

Usage
-----

Command Line
~~~~~~~~~~~~

``spotify-ripper`` takes many command-line options

.. code::

    usage: spotify-ripper [-h] [-S SETTINGS] [-a] [-A] [-b {160,320,96}] [-c]
                          [-d DIRECTORY] [-f] [-F] [-g {artist,album}] [-k KEY]
                          [-u USER] [-p PASSWORD] [-l] [-L LOG] [-m] [-o]
                          [-P] [-s] [-v VBR] [-V] [-r]
                          uri

    Rips Spotify URIs to MP3s with ID3 tags and album covers

    positional arguments:
      uri                   Spotify URI (either URI, a file of URIs or a search query)

    optional arguments:
      -h, --help            show this help message and exit
      -S SETTINGS, --settings SETTINGS
                            Path to settings, config and temp files directory [Default=~/.spotify-ripper]
      -a, --ascii           Convert the file name and the ID3 tag to ASCII encoding [Default=utf-8]
      -A, --ascii-path-only
                            Convert the file name (but not the ID3 tag) to ASCII encoding [Default=utf-8]
      -b {160,320,96}, --bitrate {160,320,96}
                            Bitrate rip quality [Default=320]
      -c, --cbr             Lame CBR encoding [Default=VBR]
      -d DIRECTORY, --directory DIRECTORY
                            Base directory where ripped MP3s are saved [Default=cwd]
      -f, --flat            Save all songs to a single directory instead of organizing by album/artist/song
      -F, --Flat            Similar to --flat [-f] but includes the playlist index at the start of the song file
      -g {artist,album}, --genres {artist,album}
                            Attempt to retrieve genre information from Spotify's Web API [Default=skip]
      -k KEY, --key KEY     Path to Spotify application key file [Default=cwd]
      -u USER, --user USER  Spotify username
      -p PASSWORD, --password PASSWORD
                            Spotify password [Default=ask interactively]
      -l, --last            Use last login credentials
      -L LOG, --log LOG     Log in a log-friendly format to a file (use - to log to stdout)
      -m, --pcm             Saves a .pcm file with the raw PCM data
      -o, --overwrite       Overwrite existing MP3 files [Default=skip]
      -P, --playlist        Store playlist in separate directories and keep track of changes
      -s, --strip-colors    Strip coloring from output[Default=colors]
      -v VBR, --vbr VBR     Lame VBR encoding quality setting [Default=0]
      -V, --version         show program's version number and exit
      -r, --remove-from-playlist
                            Delete tracks from playlist after successful ripping [Default=no]

    Example usage:
        rip a single file: spotify-ripper -u user -p password spotify:track:52xaypL0Kjzk0ngwv3oBPR
        rip entire playlist: spotify-ripper -u user -p password spotify:user:username:playlist:4vkGNcsS8lRXj4q945NIA4
        rip a list of URIs: spotify-ripper -u user -p password list_of_uris.txt
        search for tracks to rip: spotify-ripper -l -b 160 -o "album:Rumours track:'the chain'"

Config File
~~~~~~~~~~~

For options that you want set on every run, you can use a config file named ``config.ini`` in the settings folder (defaults to ``~/.spotify-ripper``).  The options in the config file use the same name as the command line options with the exception that dashes are tranlated to ``snake_case``.  Any option specified in the command line will overwrite any setting in the config file.  Please put all options under a ``[main]`` section.

Here is an example config file

.. code:: ini

    [main]
    ascii = True
    bitrate = 160
    flat = True
    last = True
    remove_from_playlist = True

Installation
------------

Prerequisites
~~~~~~~~~~~~~

-  `libspotify <https://developer.spotify.com/technologies/libspotify>`__

-  `pyspotify <https://github.com/mopidy/pyspotify>`__

-  a Spotify binary `app
   key <https://devaccount.spotify.com/my-account/keys/>`__
   (spotify\_appkey.key)

-  `lame <http://lame.sourceforge.net>`__

-  `mutagen <https://mutagen.readthedocs.org/en/latest/>`__

-  `colorama <https://pypi.python.org/pypi/colorama>`__

- `requests`__

License
-------

`MIT License <http://en.wikipedia.org/wiki/MIT_License>`__

.. |Version| image:: http://img.shields.io/pypi/v/spotify-ripper.svg?style=flat-square
  :target: https://pypi.python.org/pypi/spotify-ripper
