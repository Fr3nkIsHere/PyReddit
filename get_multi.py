from os import system
import json, time, os, random
from redvid import Downloader
import requests,ascii_magic
import pygame
import moviepy.editor as mp 
import threading, cv2, platform
import sys, re, tempfile

if(sys.platform == "win32"):
    import ctypes
    from ctypes import wintypes
else:
    import termios

if platform.system() == 'Windows':
    TEMP = "C:\\Windows\\Temp"
else:
    TEMP = "/tmp"

class Video:
    def download(url):
        reddit = Downloader(min_q=True)
        reddit.overwrite =True
        reddit.log = False
        reddit.url = url
        data = reddit.download()
        title = data.title()
        if os.path.exists("last_video.mp4"):
            os.remove("last_video.mp4")
        os.rename(f"{title}", "last_video.mp4")
        
        vidObj = cv2.VideoCapture("last_video.mp4")
        number_of_frames = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))
        Video.audio_extracting()
        Video.launch(number_of_frames)
    
    def audio_extracting():
        if os.path.exists("last_audio.wav"):
            os.remove("last_audio.wav")
        try:
            clip = mp.VideoFileClip(r"last_video.mp4")
            clip.audio.write_audiofile(r"last_audio.wav",verbose = False)
            clip.close()
        except:
            pass
            
        
        
    def convertion():
        if not os.path.exists(f"{TEMP}\\images"):
            tempfile.mkdtemp(f"{TEMP}\\images")
        vidObj = cv2.VideoCapture("last_video.mp4")
        count = 0 
        flag = 1
        while flag:
            flag, image = vidObj.read()
            try:
                cv2.imwrite(f"{TEMP}\\images\\frame{count}.jpg", image)
            except:
                break
            count += 1
        

    def getpos():
        if(sys.platform == "win32"):
            OldStdinMode = ctypes.wintypes.DWORD()
            OldStdoutMode = ctypes.wintypes.DWORD()
            kernel32 = ctypes.windll.kernel32
            kernel32.GetConsoleMode(kernel32.GetStdHandle(-10), ctypes.byref(OldStdinMode))
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0)
            kernel32.GetConsoleMode(kernel32.GetStdHandle(-11), ctypes.byref(OldStdoutMode))
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        else:
            OldStdinMode = termios.tcgetattr(sys.stdin)
            _ = termios.tcgetattr(sys.stdin)
            _[3] = _[3] & ~(termios.ECHO | termios.ICANON)
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, _)
        try:
            _ = ""
            sys.stdout.write("\x1b[6n")
            sys.stdout.flush()
            while not (_ := _ + sys.stdin.read(1)).endswith('R'):
                True
            res = re.match(r".*\[(?P<y>\d*);(?P<x>\d*)R", _)
        finally:
            if(sys.platform == "win32"):
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), OldStdinMode)
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), OldStdoutMode)
            else:
                termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, OldStdinMode)
        if(res):
            return (res.group("x"), res.group("y"))
        return (-1, -1)

    def output(count):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.4)
        try:
            pygame.mixer.music.load("last_audio.wav")
            pygame.mixer.music.play()
        except: pass
        y = Video.getpos()[1]
        for i in range(count):
            image = f"{TEMP}\\images\\frame{i}.jpg"
            ascii_magic.init_terminal()
            output = ascii_magic.from_image_file(image, columns=144, width_ratio= 3, mode=ascii_magic.Modes.TERMINAL)
            print(f"\x1b[{y};0H")
            time.sleep(1/30)
            ascii_magic.to_terminal(output)
            
        

    def launch(count):
        Video.convertion()
        Video.output(count)
        pygame.mixer.music.unload()
        print(f"\x1b[{Video.getpos()[1]};{Video.getpos()[0]}H")
        try:
            for i in range(27000):
                os.remove(f"{TEMP}\\images\\frame{i}.jpg")
        except: pass
            


class Image:

    def download(url):
        f = open('last_pic.jpg','wb')
        response = requests.get(url)
        f.write(response.content)
        f.close()
        Image.out()
    
    def out():
        image = ascii_magic.from_image_file('last_pic.jpg')
        ascii_magic.to_terminal(image)


