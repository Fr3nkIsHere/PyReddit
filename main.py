
'''
*****************************************
*            Beta Software              *
*         Use only at your risk         *
*                Fr3nk                  *
***************************************** 

The main program
'''


from os import system
import argparse

parser = argparse.ArgumentParser(prog="PyReddit 0.4")

#Library Installation
try: 
    import requests, praw, pyfiglet, ascii_magic, redvid, pygame, ffmpeg, moviepy
except ModuleNotFoundError:
    with open("requirements.txt", 'w') as file:
        file.write("rich\nrequests\npraw\npyfiglet\nascii_magic\nredvid\nopencv-python\npygame==2.1.3.dev8\nmoviepy\nffmpeg")
    system("pip install -r requirements.txt")
    import requests, praw, pyfiglet, ascii_magic, redvid
    

import time, os
from rich import console
import linecache
import search, parse_sub
import sys, platform
 
reddit = None               
Console = console.Console() #Console Initialitation
running = True  

if platform.system() == 'Windows':
    CLS = "system(\"cls\")"
    TEMP = "C:\\Windows\\Temp"
else:
    CLS = "system(\"clear\")"
    TEMP = "/tmp"

#Preflight Operations
def get_started():
    global reddit
    time.sleep(0.3)
    sys.stdout.write("\x1b]2;PyReddit - Starting...\x07\n")
    Console.print("[spring_green3]Installing Required Libraries...✓[/spring_green3]")
    time.sleep(1)
    Console.print("[spring_green3]Testing Internet Connection...[/spring_green3]",end=" ")
    time.sleep(0.3)
    try:
        requests.request("GET","https://reddit.com")
        Console.print("[spring_green3]✓[/spring_green3]")
    except:
        Console.print("[red1]X[/red1]")
        Console.print("[bright_red]Error Connecting to the internet, Please Try Later. [/bright_red]")
        time.sleep(1)
        exit()
    time.sleep(0.3)
    Console.print("[spring_green3]Connection with Reddit... ✓[/spring_green3]")
    time.sleep(0.3)
    Console.print("[spring_green3]Starting PyReddit 0.4... [/spring_green3]")
    time.sleep(3)



#Random Place               
def random_place():
    global reddit
    Console.print("[spring_green3]Connection with Reddit... ✓[/spring_green3]")
    time.sleep(0.5)
    Console.print("[spring_green3]Checking Settings...[/spring_green3]",end=" ")
    time.sleep(0.5)
    
    if os.path.exists('settings.cfg') == False:
        Console.print("[red1]X[/red1]")
        Console.print("[bright_red]Error Checking Settings, Please run Settings from the main menu.[/bright_red]")
        nsfw = False
        Video = False
        Time = 1
    else:
        Console.print("[spring_green3]✓[/spring_green3]")

        NsfwSetting = linecache.getline('settings.cfg', 1)
        NsfwCheck = NsfwSetting.replace("NSFW= ", "")
        if NsfwCheck.__contains__("1"):
            nsfw = True
        else:
            nsfw = False

        VideoSetting = linecache.getline('settings.cfg', 2)
        VideoCheck =VideoSetting.replace("VIDEO_PLAY= ", "")
        if VideoCheck.__contains__("1"):
            Video = True
        else:
            Video = False

        TimeSetting = linecache.getline('settings.cfg', 3)
        Time = TimeSetting.replace("POST_UPDATES= ", "")
        print(Time, nsfw, Video)
        time.sleep(1)
    
    stop = False
    Console.clear()
    
    while not stop:
        Console.clear()
        eval(CLS)
        Times = parse_sub.Subreddit.time_index(Time)
        stop = parse_sub.Subreddit.get(nsfw, Times, Video)


#credits
def credits():
    sys.stdout.write("\x1b]2;PyReddit - Credits\x07")
    eval(CLS)
    PyReddit = pyfiglet.figlet_format("Credits")
    Console.print(f"[dark_orange3]{PyReddit}[/dark_orange3]\n\n",markup=True)   
    Console.print("PyReddit Created By: Fr3nkIsHere") 
    Console.input()  

#help
def help():
    sys.stdout.write("\x1b]2;PyReddit - Help\x07")
    eval(CLS)
    PyReddit = pyfiglet.figlet_format("Help")
    Console.print(f"[dark_orange3]{PyReddit}[/dark_orange3]\n\n",markup=True)
    Console.print("- Global Commands:")
    Console.print(":q Return to main menu")
    Console.print(":n/Enter Go to the next post")
    Console.print(":t Change Post listing")
    Console.print("Possible Post listings and their code:")
    Console.print("1 = Top of the Day\n2 = Top of the Week\n3 = Top of the Month\n4 = Top of the Year\n5 = Top of All\n6 = Hot\n7 = Newest Post")
    Console.print("Possible Post listings and their code:")
    Console.print("Possible Post listings and their code:")
    Console.print("- Random Subreddit Commands:")
    Console.print(":r Go to another Subredit")
    Console.print("- Search Commands:")
    Console.print(":s Search to another Subredit")
    Console.input("")

#Settings 
def settings():
    sett = 1
    sex = "n"
    sys.stdout.write("\x1b]2;PyReddit - Settings\x07")
    while sett: #Global Settings
        Console.clear()
        eval(CLS)
        Settings = pyfiglet.figlet_format("Settings")
        Console.print(f"[dark_orange3]{Settings}[/dark_orange3]\n\n",markup=True)
        Console.print("[red1]0) Exit[/red1]")
        Console.print("[red1]1) Subreddit Settings[/red1]")
        Console.print("[orange1]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/orange1]")
        sel = Console.input("Select: ")
        match int(sel):
            case 0: #Exit Settings
                sett = 0
            case 1: #Subreddit Settings
                Console.clear()
                eval(CLS)
                Settings = pyfiglet.figlet_format("Settings")
                Console.print(f"[dark_orange3]{Settings}[/dark_orange3]\n\n",markup=True)
                sex   = Console.input("- Enable +18 (Default: N)[y/n]: ")
                vid   = Console.input("- Enable Video playback (Default: y)[y/n]: ")
                times = Console.input("- Post Update Index (Defualt 2:Top Of The Week): ")
                try:
                    if int(times) < 1 or int(times) > 7:
                        Console.print("[bright_red]Input Not Valid, setted 7[/bright_red]")
                        Console.input()
                        times = '7'
                except:
                    times = '2'
    
    #Writing Settings
    Console.print("[bright_red]Saving Settings...[/bright_red]")
    with open("settings.cfg","w") as setting:
        if sex.lower() == "y":
            setting.writelines(f"NSFW= 1\n")
        else:
            setting.writelines(f"NSFW= 0\n")

        if vid.lower() == "y":
            setting.writelines(f"VIDEO_PLAY= 1\n")
        else:
            setting.writelines(f"VIDEO_PLAY= 0\n")
        
        setting.writelines(f"POST_UPDATES= {2 if times == '' or times == ' ' else times}")
    time.sleep(0.5)
    Console.print("[spring_green2]Done![/spring_green2]")
    time.sleep(0.5)


#Main Program
def main(): 
    global running
    get_started()
    while running:
        linecache.checkcache()
        sys.stdout.write("\x1b]2;PyReddit - Home\x07") 
        eval(CLS)
        PyReddit = pyfiglet.figlet_format("PyReddit")
        Console.print(f"[dark_orange3]{PyReddit}[/dark_orange3]\n\n",markup=True)
        Console.print("[orange_red1]0) Exit[/orange_red1]")
        Console.print("[red1]1) Start Navigating Randomly[/red1]")
        Console.print("[deep_pink4]2) Search some Subreddits[/deep_pink4]")
        Console.print("[bright_red]3) Help[/bright_red]")
        Console.print("[bright_red]4) Settings[/bright_red]")
        Console.print("[red3]5) Credits[/red3]")
        Console.print("[orange1]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/orange1]")
        sel = Console.input("Select: ")
        Console.bell()
        match sel:
            case '0': #Shutting Down
                Console.clear()
                Console.print("[bright_red]Shutting Down...[/bright_red]")
                time.sleep(0.5)
                running = False
            case '1': #Randome Place
                random_place()
            case '2': #Search
                Console.print("[spring_green3]Checking Settings...[/spring_green3]",end=" ")
                time.sleep(0.5)
                if os.path.exists('settings.cfg') == False:
                    Console.print("[red1]X[/red1]")
                    Console.print("[bright_red]Error Checking Settings, Please run Settings from the main menu.[/bright_red]")
                    nsfw = False
                else:
                    Console.print("[spring_green3]✓[/spring_green3]")
                    NsfwSetting = linecache.getline('settings.cfg', 1)
                    NsfwCheck = NsfwSetting.replace("NSFW= ", "")
                    if NsfwCheck.__contains__("1"):
                        nsfw = True
                    else:
                        nsfw = False

                    VideoSetting = linecache.getline('settings.cfg', 2)
                    VideoCheck =VideoSetting.replace("VIDEO_PLAY= ", "")
                    if VideoCheck.__contains__("1"):
                        Video = True
                    else:
                        Video = False

                    TimeSetting = linecache.getline('settings.cfg', 3)
                    Time = TimeSetting.replace("POST_UPDATES= ", "")

                time.sleep(0.5)
                search.search(nsfw, Video, Time)
            case '3': #Help
                help()
            case '4': #Settings
                settings()
            case '5': #Credits
                credits()
            case _:   #None Of Them
                Console.bell()
                eval(CLS)
                Console.print("[bright_red]Not A Valid Input[/bright_red]")
                Console.input("[bright_red]Press Any key to continue...[/bright_red]")
            



if __name__ == "__main__":
    main()          #Run the Program

