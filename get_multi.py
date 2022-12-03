from os import system
import json, time, os, random
from redvid import Downloader
import requests,ascii_magic
import threading, cv2, platform

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

        Video.launch(number_of_frames)
    
    def convertion():
        if not os.path.exists(f"{TEMP}\\images"):
            os.mkdir(f"{TEMP}\\images")
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
        

    def output(count):
        system("cls")
        for i in range(count):
            image = f"{TEMP}\\images\\frame{i}.jpg"
            ascii_magic.init_terminal()
            output = ascii_magic.from_image_file(image, columns=144, mode=ascii_magic.Modes.TERMINAL)
            ascii_magic.to_terminal(output)
            print("\x1b[0;0H")
    
    def launch(count):
        t1 = threading.Thread(target=Video.convertion(), name='t1')
        t2 = threading.Thread(target=Video.output(count), name='t2')
        t1.start()
        time.sleep(0.3)
        t2.start()
        t1.join()
        t2.join()
            


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


