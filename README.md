# Music Player

A simple offline music player built with Python, Tkinter and Pygame.
It reads `.mp3` files from a local folder and lets you play, pause, stop
and adjust the volume, with a scrollable song list.

## Requirements

- Python 3
- Pygame

Install the dependency with:

```
pip install pygame
```

(`tkinter` and `os` are part of the Python standard library, no install needed.)

## How to use

1. Put your `.mp3` files inside the `songs/` folder
   (the folder is created automatically on first run).
2. Run the program:

```
python music_player.py
```

3. Select a song from the list and use the play / pause / stop buttons.
   Use `+` and `-` to change the volume.
   Press `M` to minimize the window to the taskbar while the music keeps playing.

## Features

- Loads songs dynamically from a folder (no hard-coded file names)
- Scrollable song list
- Volume control kept within a valid range
- Graceful handling of missing files

## Notes

This is a learning project built to practice GUI programming and
event handling in Python.
