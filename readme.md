MCAssRip
========

This script will copy the files from the Minecraft assets directory, restoring their in-game paths.

It requires Python 3.

Also included is a tangentially related tool, `metaunite`, which will restore
the missing metadata for the music files.

Background
----------

A number of Minecraft assets (the music and sounds in particular) are not located in the Minecraft .jar files; instead, the launcher downloads them into a separate directory.

On Windows, they are stored in the `Users\<username>\AppData\Roaming\.minecraft\assets` directory.

The layout of these files is a bit ... odd. In the assets directory, there is a `objects` directory and an `indexes` directory. The `objects` directory contains the actual files, but they are named by hexadecimal hashes, rather than the original file name and path. The `indexes` directory contains a series of JSON files, which map the hash files to their in-game name. There appears to be one index file for each major Minecraft version. Most of them seem to be named obviously, however this seems to not be universal; for example, the index for version 1.20.x seems to simply be called `8.json`.

This script will read an index file, find the hash files for the requested objects, and copy them to a new directory with the original name.

Usage
-----

```
mcassrip [-h] [-f] [-s] [-t] index [target] [filter ...]
```

* index  
  Path to a .json file in the indexes directory. MCAssRip will find the
  corresponding hash files based on the location of this file.
* target  
  Directory to save the renamed files to. If not specified, MCAssRip will list
  all files referenced in the index.
* filter  
  The files that should be copied. This could be a single file, a directory, or
  a wildcard.

By default, MCAssRip will recreate the directory structure of the files as
listed in the index. The `-s` option will instead copy all files directly to
the given `target`, without creating any subdirectories.

By default, MCAssRip will not overwrite existing files. Use `-f` to override this.

If you would like to see what files will be copied where before actually doing
it , use the `-t` option.

Examples
--------

The following examples assume you're running them from the `assets` directory.

```
mcassrip indexes/8.json
```

Display all resources indexed in `8.json`

```
mcassrip indexes/8.json ~/stuff minecraft/sounds/ambient/cave/cave1.ogg
```

Copy the single file `cave1.ogg` to
`~/stuff/minecraft/sounds/ambient/cave`, creating directories as needed.

```
mcassrip indexes/8.json ~/stuff cave1.ogg
```

Copy any file named `cave1.ogg` to `~/stuff`, recreating the directories it was
found in

```
mcassrip -s indexes/8.json ~/stuff cave1.ogg
```

Copy any file named `cave1.ogg` directly into `~/stuff`

```
mcassrip indexes/8.json ~/stuff minecraft/sounds/ambient/cave
```

Copy the entire directory tree `minecraft/sounds/ambient/cave` into `~/stuff`

```
mcassrip -s indexes/8.json ~/stuff "*.ogg"
```

Copy any and all ogg files into `~/stuff`

MetaUnite
=========

MetaUnite will tag a set of `.ogg` files with metadata provided by a `.csv`
file. This can in particular, tag the Minecraft soundtrack files with their
title and artist tags.

It requires Python 3 with the `mutagen` package.

Usage
-----

`metaunite [-h] [-v] index files [files ...]`

* index  
  Path to a .csv file containing the metadata information
* files...
  The files to tag

The `-v` switch will display information as each file is tagged. By default, no
output is displayed unless an error or warning occurs.

MetaUnite will display a warning if it couldn't find the metadata for a specified file.

The `.csv` file contains the filename, title, and artist, in that order. It is
expeted to be comma-delimited, with strings enclosed in double quotes. The
first line is expected to be a heading, and is ignored.

The file `1-20.csv` contains the metadata for the soundtrack as included in
Minecraft 1.20.x. There are also index files in the `mods` folder for a
selection of Minecraft mods that include their own soundtracks. In the latter
case, some of the metadata is guesswork, as reliable information is sometimes
lacking.

Example
-------

```
metaunite 1-20.json *.ogg
```

Tag all .ogg files in the current directory based on metadata in 1-20.json

