#!/usr/bin/python3

import json
from sys import argv, stderr
from pathlib import Path
from argparse import ArgumentParser
from shutil import copy

def main():
    parser=ArgumentParser(
            prog='mcassrip', 
            description='Rip Minecraft assets to their original paths',
            )

    parser.add_argument( 'index', help='Path to index .json file' )
    parser.add_argument( 'target', nargs='?', help='Path to save files to' )
    parser.add_argument( 'filter', nargs='*', help='Path or glob of file(s) to extract' )

    parser.add_argument( '-f', '--force', action='store_true',
                        help='Overwrite existing files' )
    parser.add_argument( '-s', '--no-subdirs', action='store_true',
                        help="Don't create subdirectories" )
    parser.add_argument( '-t', '--test', action='store_true',
                        help="Test: Show what would be copied but don't do it" )

    opts = parser.parse_args()
    #die( opts )


    # Path to index file
    indexpath = Path( opts.index )
    # Path to target directory
    targetpath = Path( opts.target ) if opts.target else None

    if not indexpath.exists():
        die( "File does not exist:", indexpath )

    with open( indexpath ) as f:
        # Decoded JSON index
        index = json.load( f )

    for name, data in index['objects'].items():
        # Name of hash file
        hash = data['hash']
        # Path to hash file
        hashpath = indexpath.parent.parent / 'objects'
        hashpath /= Path( hash[0] + hash[1] ) / hash
        # Path (relative) to in-game asset file
        path = Path( name )

        if opts.filter:
            match = False
            for pattern in opts.filter:
                if path.match( pattern ):
                    match = True
                if path.is_relative_to( pattern ):
                    match = True
        else:   
            match = True

        if match:
            if targetpath:
                # Directory of target file
                targetdir = targetpath / path.parent
                # Path to target file
                if opts.no_subdirs:
                    targetfile = targetpath / path.name
                else:
                    targetfile = targetpath / path
                if not hashpath.exists():
                    perror( f'Skipped {path.name}: Hash file does not exist' )
                elif targetfile.exists() and not opts.force:
                    perror( f'Skipped {path.name}: File already exists' )
                else:
                    print( f'{targetfile} <-- {hashpath}' )
                    if not opts.test:
                        targetfile.parent.mkdir( parents=True, exist_ok=True )
                        copy( hashpath, targetfile )
            else:
                print( f'{path}' )


def perror( *args ):
    """Print a message to stderr"""

    print( *args, file=stderr )

def die( *args, status=1 ):
    """Print an error end exit"""

    perror( *args )
    exit( status )

if __name__ == "__main__":
    main()



