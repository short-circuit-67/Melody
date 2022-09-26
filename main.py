import tkinter as tk
import fnmatch
import os
from turtle import bgcolor
from tkinter import ttk, messagebox
from ttkthemes import themed_tk
from pygame import mixer
from ttkthemes import themed_style
from mutagen.mp3 import MP3
import time

song=""
songLength=0
count = 0
first_time=False
favSongs = []
recentSongs = []
frequentSongs = []


def songStatus(x):
    global favSongs, recentSongs, frequentSongs
    curSong = ListBox.curselection() 
    curSongName = ListBox.get(curSong)

    if x == 1:
        if curSongName in recentSongs:
            recentSongs.remove(curSongName)
        temp = 0
        for key,value in frequentSongs:
            if value == curSongName:
                temp = key
                frequentSongs.remove((key,value))
                break
            
        frequentSongs.append((temp+1, curSongName))
        frequentSongs.sort()
        recentSongs.append(curSongName)
        
        

    if curSongName in favSongs:
        addToFavButton['image'] = add_fav_img
        addToFavButton['text'] = "Remove From Fav"
    
    else:
        addToFavButton['image'] = remove_fav_img
        addToFavButton['text'] = "Add To Fav"

def display_All():
    ListBox.delete(0,'end')
    global count
    for root, dir, files in os.walk(completepath):
        for filename in fnmatch.filter(files, pattern):
            count+=1
            ListBox.insert('end', filename)

def display_Favourites():
    ListBox.delete(0,'end')
    global favSongs,count
    count = 0
    for filename in favSongs:
        count+=1
        ListBox.insert('end', filename)

def display_Recents():
    ListBox.delete(0,'end')
    global recentSongs,count
    count = 0
    temp = recentSongs
    temp.reverse()
    for songs in temp:
        count+=1
        ListBox.insert('end', songs)

def display_Frequents():
    ListBox.delete(0,'end')
    global frequentSongs,count 
    count = 0
    temp = frequentSongs
    temp.reverse()
    for key,value in temp:
        count+=1
        ListBox.insert('end', value)



def add_remove_to_fav():
    
    songStatus(0)
    global favSongs
    curSong = ListBox.curselection()
    curSongName = ListBox.get(curSong)

    if addToFavButton['text'] == "Remove From Fav":
        favSongs.remove(curSongName)
        
    else:
        favSongs.append(curSongName)

    songStatus(0)          
   
def default_play(songPath):
    progress_scale['value']=0
    time_elasped_label['text']="00:00"
    mixer.music.load(songPath)
    mixer.music.play()
    song=MP3(songPath)
    songLength=int(song.info.length)
    music_duration_label['text']=time.strftime('%M:%S',time.gmtime(songLength))
    progress_scale['to']=songLength
    progress_scale.after_cancel(progress_scale.updater)
    pauseButton["text"] = "Pause"
    pauseButton['image'] = pause_img
    scale_update()

def select():
   
    global songLength,song,first_time
    if first_time==False:
        first_time=True
        label.config(text = ListBox.get("anchor"))
        progress_scale['value']=0
        time_elasped_label['text']="00:00"
        mixer.music.load(completepath + "/" + ListBox.get("anchor"))
        mixer.music.play()
        song=MP3(completepath + "/" + ListBox.get("anchor"))
        songLength=int(song.info.length)
        music_duration_label['text']=time.strftime('%M:%S',time.gmtime(songLength))
        progress_scale['to']=songLength
        pauseButton["text"] = "Pause"
        pauseButton['image'] = pause_img
        scale_update()
    else:
        label.config(text = ListBox.get("anchor"))
        default_play(completepath + "/" + ListBox.get("anchor"))
   
    

    songStatus(1)


def stop():
    progress_scale['value']=0
    time_elasped_label['text']="00:00" 
    ListBox.delete(0,'end')
    mixer.music.stop()
    ListBox.select_clear('active')
    messagebox.showinfo("See You Again!", "Thank You for using MELODY!")
    time.sleep(1)
    canvas.destroy()

def play_next():
    # progress_scale['value']=0
    # time_elasped_label['text']="00:00" 
    nextSong = ListBox.curselection()
    nextSong = nextSong[0] + 1
    if nextSong >= count :
        nextSong = 0
    nextSongName = ListBox.get(nextSong)
    label.config(text = nextSongName)

    songPath = completepath + "/" + nextSongName
    default_play(songPath)

    ListBox.select_clear(0, 'end')
    ListBox.activate(nextSong)
    ListBox.select_set(nextSong)

    songStatus(1)

def play_prev():
    prevSong = ListBox.curselection()
    prevSong = prevSong[0] - 1
    if prevSong < 0 :
        prevSong = count-1
    
    prevSongName = ListBox.get(prevSong)
    label.config(text = prevSongName)
    
    songPath = completepath + "/" + prevSongName
    default_play(songPath)
    
    ListBox.select_clear(0, 'end')
    ListBox.activate(prevSong)
    ListBox.select_set(prevSong)
    songStatus(1)

def pause():
    if pauseButton["text"] == "Pause":
        mixer.music.pause()
        progress_scale.after_cancel(progress_scale.updater)
        pauseButton["text"] = "Play"
        pauseButton['image'] = play_img

    else :
        mixer.music.unpause()
        pauseButton["text"] = "Pause"
        pauseButton['image'] = pause_img
        progress_scale.updater=progress_scale.after(1000,scale_update)

def repeat_song():
    if repeatButton['text'] == "single":
        repeatButton['text'] = "repeat"
        repeatButton.config(image = repeat_on_img)
    else:
        repeatButton['text'] = "single"   
        repeatButton.config(image = repeat_off_img)


# def repeat_song():
#     ok

def scale_set(x):  
        currSong = ListBox.curselection()
        currSongName = ListBox.get(currSong)
        scale_at=progress_scale.get()
        mixer.music.load(completepath + "/" + currSongName)
        mixer.music.play(0,scale_at)
        pauseButton["text"] = "Pause"
        pauseButton['image'] = pause_img
        time_elasped_label['text']=time.strftime('%M:%S',time.gmtime(progress_scale.get()))
        
def scale_update():
         global songLength,song
     
      
         if progress_scale['value']<songLength:
            progress_scale['value']+=1
            time_elasped_label['text']=time.strftime('%M:%S',time.gmtime(progress_scale.get()))
        
            progress_scale.updater=progress_scale.after(1000,scale_update)

         elif repeatButton['text']=="repeat" :

              select()
         else:
             progress_scale['value']=0
             time_elasped_label['text']="00:00" 
             play_next() 
          
    


canvas = tk.Tk()
canvas.title("Music Player")
canvas.geometry("600x700")
canvas.config( bg = '#8B8878')



style=themed_style.ThemedStyle()
style.theme_names()
style.theme_use('breeze')
style.configure("TScale",background="#8B6878")







toolbar = tk.Frame(canvas, bg = "#8B6878")
toolbar.pack(padx = 2, pady = 10)


allSongsButton = tk.Button(canvas, text = "All Songs", bg = "#8B8878", borderwidth = 0, command = display_All)
allSongsButton.pack(pady = 0,padx = 5, in_ = toolbar, side = 'left')

favSongsButton = tk.Button(canvas, text = "Favourite Songs", bg = "#8B8878", borderwidth = 0, command = display_Favourites)
favSongsButton.pack(pady = 0,padx = 5, in_ = toolbar, side = 'left')

recentSongsButton = tk.Button(canvas, text = "Recently Played", bg = "#8B8878", borderwidth = 0, command = display_Recents)
recentSongsButton.pack(pady = 0,padx = 5, in_ = toolbar, side = 'left')

frequentSongsButton = tk.Button(canvas, text = "Frequently Played", bg = "#8B8878", borderwidth = 0, command = display_Frequents)
frequentSongsButton.pack(pady = 0,padx = 5, in_ = toolbar, side = 'left')


TitleBox = tk.Label(canvas, text = "Song List : ", fg = "black", bg = "#8B8878", width = 100, anchor= 'w', font = ('Arial', 20))
TitleBox.pack(fill='both')



completepath = "/home/amit/projects/python_project/files"
pattern = "*.mp3"

mixer.init()

#images
prev_img = tk.PhotoImage( file = "icons/prev_img.png")
stop_img = tk.PhotoImage( file = "icons/stop_img.png")
next_img = tk.PhotoImage( file = "icons/next_img.png")
play_img = tk.PhotoImage( file = "icons/play_img.png")
pause_img = tk.PhotoImage( file = "icons/pause_img.png")
remove_fav_img = tk.PhotoImage( file = "icons/remove_fav_img.png")
add_fav_img = tk.PhotoImage( file = "icons/add_fav_img.png")
play_from_start_img = tk.PhotoImage( file = "icons/play_from_start_img.png")
repeat_off_img = tk.PhotoImage( file = "icons/repeat_off_img.png")
repeat_on_img = tk.PhotoImage( file = "icons/repeat_on_img.png")


DisplaySongsFrame = tk.Frame( canvas, bg = "#8B8878")
DisplaySongsFrame.pack(padx = 0, pady = 10)


ListBox = tk.Listbox(DisplaySongsFrame, fg = "black", bg = "#696969", width = 90, font = ('Comic Sans MS', 20))

scrolltool = tk.Scrollbar(DisplaySongsFrame, orient='vertical', command=ListBox.yview, bg='red', width=10)

ListBox['yscrollcommand']=scrolltool.set
scrolltool.pack(side = 'right', fill = 'y')
ListBox.pack(padx = 15, pady = 2, in_ = DisplaySongsFrame)


newFrame = tk.Frame(canvas, bg = '#8B7878')
newFrame.pack(padx = 2, pady = 10)

now_playingBox = tk.Label(canvas, text = "Now Playing : ", fg = "black", bg = "#8B7878", width = 10, anchor= 'w', font = ('Arial', 15))
now_playingBox.pack(fill='both', in_ = newFrame, side = 'left')

scale_bar = tk.Frame(canvas, bg = "#8B6878")
scale_bar.pack(padx = 2, pady = 10,anchor='center')

time_elasped_label=tk.Label(canvas,text="00:00", fg = "black", bg = "#8B8878",padx = 5)
time_elasped_label.pack(padx=10,pady=5,in_=scale_bar,side='left')


music_duration_label=tk.Label(canvas,text="00:00", fg = "black", bg = "#8B8878",padx = 5)
music_duration_label.pack(padx=10,pady=5,in_=scale_bar,side='right')
# progressframe = tk.Frame( canvas, bg = "black")
# progressframe.pack(padx=0,pady=0)

progress_scale=ttk.Scale(canvas,orient="horizontal",from_=0,length=380,command=scale_set,cursor='hand2',style="TScale")

progress_scale.pack(padx=10,pady=5,in_=scale_bar,side='left')

label = tk.Label(canvas, text = '', bg = "#8B8878", fg = 'yellow', width = 80, font = ('Comic Sans MS', 20))
label.pack(pady = 15, in_ = newFrame, side = 'left')

# play/pause user box (prev - pause - play - stop - next)

top = tk.Frame(canvas, bg = '#8B8878')
top.pack(padx = 10, pady = 10, anchor = 'center')

# button for prev song

prevButton = tk.Button(canvas, text = "Prev", image = prev_img, bg = "#8B8878", borderwidth = 0, command = play_prev)
prevButton.pack(pady = 0,padx = 5, in_ = top, side = 'left')

# button to pause the song

pauseButton = tk.Button(canvas, text = "Pause",image = pause_img, bg = "#8B8878", borderwidth = 0, command = pause)
pauseButton.pack(pady = 0,padx = 5, in_ = top, side = 'left')

# button to Play the song

playButton = tk.Button(canvas, text = "Play", image = play_from_start_img, bg = "#8B8878", borderwidth = 0, command = select)
playButton.pack(pady = 0,padx = 5, in_ = top, side = 'left')

# button to stop the song

stopButton = tk.Button(canvas, text = "Stop",image = stop_img, bg = "#8B8878", borderwidth = 0, command = stop)
stopButton.pack(pady = 0,padx = 5, in_ = top, side = 'left')


# button for next song

nextButton = tk.Button(canvas, text = "Next", image = next_img, bg = "#8B8878", borderwidth = 0, command = play_next)
nextButton.pack(pady = 0,padx = 5, in_ = top, side = 'left')


addToFavButton = tk.Button(canvas, text = "Add To Fav", image = remove_fav_img, bg = "#8B8878", borderwidth = "2", command = add_remove_to_fav)
addToFavButton.pack(pady = 0,padx = 5, side = 'right')

repeatButton = tk.Button(canvas, text = "single", image = repeat_off_img, bg = "#8B8878", borderwidth = "2", command = repeat_song)
repeatButton.pack(pady = 0,padx = 5, side = 'left')


canvas.mainloop()
 


# priority queue (most played)