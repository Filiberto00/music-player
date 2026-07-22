"""
Simple offline music player built with Tkinter and Pygame.
Reads .mp3 files from the songs/ folder and lets you play, pause, stop
and adjust the volume. Press M to minimize it to the taskbar while the
music keeps playing.
"""
import tkinter
from tkinter import messagebox
import pygame
import os

pygame.init()

# --- Window setup: full and on top by default, so it's easy to pick songs ---
root = tkinter.Tk()
root.title("music")
root.geometry('300x250')
root.resizable(width=False, height=False)
root.attributes('-topmost', 1)   # keep the window above others by default
root.attributes('-alpha', 1)     # fully opaque by default


# Press M to minimize to the taskbar; playback keeps going in the background.
# Reopen it from the taskbar (it restores itself on top again).
def hide_window(event=None):
    root.attributes('-topmost', 0)   # drop always-on-top so it sinks to the back
    root.iconify()                   # minimize to taskbar; music keeps playing


def show_window(event=None):
    root.deiconify()                 # bring the window back
    root.attributes('-topmost', 1)   # put it on top again


root.bind('<m>', hide_window)
root.bind('<Map>', show_window)      # <Map> fires when the window is restored

# --- Load the song list dynamically from the songs/ folder ---
# The folder is created if missing, so the app never crashes on first run.
SONGS_FOLDER = 'songs'
if not os.path.exists(SONGS_FOLDER):
    os.makedirs(SONGS_FOLDER)
song_files = [f for f in os.listdir(SONGS_FOLDER) if f.endswith('.mp3')]

# --- Menu bar (Info / Exit) ---
menubar = tkinter.Menu(root)
root.config(menu=menubar)

info_message = 'Here you can listen and play songs completely free offline'


def information():
    tkinter.messagebox.showinfo(title='information', message=info_message)


def close_app():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    root.destroy()


filemenu = tkinter.Menu(menubar)
filemenu.add_command(label="Info", command=information)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=close_app)
menubar.add_cascade(label="File", menu=filemenu)

# --- Song list on the left, made scrollable with a Canvas + Scrollbar ---
# (a plain Frame can't scroll, so the songs go inside a Canvas that can.)
canvas = tkinter.Canvas(root, background="dark gray", width=150)
scrollbar = tkinter.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side='left', fill='y')
canvas.pack(side='left', expand=True, fill='both')

song_frame = tkinter.Frame(canvas, background="dark gray")
canvas.create_window((0, 0), window=song_frame, anchor='nw')


def load_song(filename):
    pygame.mixer.music.unload()
    try:
        pygame.mixer.music.load(filename)
    except pygame.error:              # file missing or unreadable: don't crash
        print("File not found:", filename)


selected_song = tkinter.StringVar()   # shared variable: keeps the radio buttons exclusive

# Build one radio button per song found in the folder.
row = 0
for song in song_files:
    btn = tkinter.Radiobutton(
        song_frame,
        text=song,
        variable=selected_song,
        value=song,
        # s=song "freezes" the current name, otherwise every button would
        # end up loading the last song of the loop.
        command=lambda s=song: load_song(SONGS_FOLDER + '/' + s),
        background="dark gray"
    )
    btn.grid(column=1, row=row, padx=10, pady=7, sticky=tkinter.W)
    row += 1

# Tell the canvas how big the scrollable area is (after the buttons exist).
song_frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

# --- Playback controls on the right ---
functions = tkinter.Frame(root, background="black")
functions.pack(side='left', expand=True, fill='both')


def play():
    position = pygame.mixer.music.get_pos()
    if position >= 0.00:             # already started before: resume it
        pygame.mixer.music.unpause()
    else:                            # nothing playing yet: start from the beginning
        pygame.mixer.music.play(loops=-1)


play_btn = tkinter.Button(functions, text='play', command=play, background="green")
play_btn.pack(expand=True, fill='both')


def pause():
    pygame.mixer.music.pause()


pause_btn = tkinter.Button(functions, text='pause', command=pause, background="grey")
pause_btn.pack(expand=True, fill='both')


def stop():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()


stop_btn = tkinter.Button(functions, text='stop', command=stop, background="red")
stop_btn.pack(expand=True, fill='both')

# --- Volume, kept between 0.0 and 1.0 (values pygame accepts) ---
volume = 0.5


def increase_volume():
    global volume
    volume = min(1.0, volume + 0.1)   # never above 1.0
    pygame.mixer.music.set_volume(volume)


def decrease_volume():
    global volume
    volume = max(0.0, volume - 0.1)   # never below 0.0
    pygame.mixer.music.set_volume(volume)


volume_increase_button = tkinter.Button(functions, text='+', command=increase_volume)
volume_increase_button.pack(side='right', expand=True, fill='both', ipady=10)
volume_decrease_button = tkinter.Button(functions, text='-', command=decrease_volume)
volume_decrease_button.pack(side='left', expand=True, fill='both', ipady=10)

root.mainloop()
