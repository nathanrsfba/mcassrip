#!/usr/bin/python3

import csv
from argparse import ArgumentParser
from collections import namedtuple
from pathlib import Path
from sys import stderr
from mutagen.oggvorbis import OggVorbis

FileInfo = namedtuple( 'FileInfo', ('filename', 'title', 'artist') )

def main():
    parser=ArgumentParser(
            prog='metaunite', 
            description='Reunite .ogg files with their metadata',
            )

    parser.add_argument( 'index', help='Path to index .csv file' )
    parser.add_argument( 'files', nargs='+', help='Files to tag' )

    parser.add_argument( '-v', '--verbose', action='store_true',
                        help="Show files as they're tagged" )
    opts = parser.parse_args()

    filemap = {}

    with open( opts.index ) as f:
        reader = csv.reader( f, delimiter=',', quotechar='"' )
        heading = next( reader )
        for row in reader:
            info = FileInfo( *row )
            filemap[info.filename] = info

    for f in opts.files:
        path = Path( f )
        if path.name in filemap:
            info = filemap[path.name]
            if opts.verbose:
                print( f"{info.filename}: {info.title}, {info.artist}" )
            tag = OggVorbis( path )
            tag['artist'] = info.artist
            tag['title'] = info.title
            tag.save()
        else:
            perror( f"File not recognized: {path.name}" )

def perror( *args ):
    """Print a message to stderr"""

    print( *args, file=stderr )

def die( *args, status=1 ):
    """Print an error end exit"""

    perror( *args )
    exit( status )

if __name__ == "__main__":
    main()




