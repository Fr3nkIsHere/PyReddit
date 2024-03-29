'''
*****************************************
*            Beta Software              *
*         Use only at your risk         *
*                Fr3nk                  *
***************************************** 

The Subreddit Parser
'''
from os import system
import json, time, os, random
import requests, praw, pyfiglet, ascii_magic, platform
from rich import console
from rich.markdown import Markdown
import get_multi
import sys

Console = console.Console()

if platform.system() == 'Windows':
    CLS = "system(\"cls\")"
    TEMP = "C:\\Windows\\Temp"
else:
    CLS = "system(\"clear\")"
    TEMP = "/tmp"

reddit= praw.Reddit(client_id="dpCFcO5NCMP4Xa7ZqQP6rA",         
                                client_secret="eHOQOtGHXfg8xLX9drgIlhQxi5dnHQ",     
                                user_agent="Mozilla/5.0 (Windows NT 10.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.35")


class Subreddit:
    def time_index(Time):
        match int(Time):
            case 1:
                return "subreddit.top(time_filter=\"day\")"
            case 2:
                return "subreddit.top(time_filter=\"week\")"
            case 3:
                return "subreddit.top(time_filter=\"month\")"
            case 4:
                return "subreddit.top(time_filter=\"year\")"
            case 5:
                return "subreddit.top(time_filter=\"all\")"
            case 6:
                return "subreddit.hot()"
            case 7:
                return "subreddit.new()"

    def get(nsfw_setting: bool = True, Times: str = "subreddit.top(time_filter=\"week\")", video_settings: bool = True, search_mode: bool = False, search: str = None):
        if not search_mode:
            if nsfw_setting:
                if random.randint(1,5) == 1:
                    subreddit = reddit.random_subreddit(nsfw_setting)
                else: 
                    subreddit = reddit.random_subreddit()
            else:
                subreddit = reddit.random_subreddit()
        else:   
            if nsfw_setting:
                subreddit = reddit.subreddit(search)
            else:
                subreddit = reddit.subreddit(search)
                if subreddit.over18:
                    Console.print(f"[red1]NSFW subs disabled. Please enable into settings.[/red1]")
                    Console.input()
                    return False 
        
        
        name = pyfiglet.figlet_format(subreddit.display_name)
        sys.stdout.write(f"\x1b]2;PyReddit - {subreddit.display_name}\x07")
        for post in eval(Times):
            Subreddit.out(post.title, post.selftext, post.url, name, subreddit.title, video_settings)
            qui = Console.input("")
            if qui.lower() == ":n" or qui.lower() == "": #Next post in the sub
                Console.print(f"\n[blue_violet]Next Post...[/blue_violet]")
                time.sleep(1)
                continue            
                '''if qui.lower().__contains__(":t"):  #Change Post listing of the same subreddit (Note: Only in this instance, to change globally you need to go into settings)
                Console.print(f"\n[blue_violet]Changing Listing type of the subreddit...[/blue_violet]")
                time.sleep(1)
                time_code = int(qui.replace(":t", ""))
                Times = Subreddit.time_index(time_code)  
                continue'''
            elif qui.lower() == ":q":  #Quit into the menu
                return True
            elif qui.lower() == ":r" and search_mode == False:  #Get a new Subreddit
                Console.print(f"\n[blue_violet]Next Subreddit...[/blue_violet]")
                time.sleep(1)
                break
            elif qui.lower() == ":s" and search_mode == True:  #Search Again 
                break
            else:
                Console.print(f"\n[blue_violet]There's a time and place for everything, but not now! Next Post...[/blue_violet]")
                time.sleep(1)
                continue 
                   

    def out(title, desc, link, subname, subdesc, video_sett):
        eval(CLS)
        Console.print(f"[dark_orange3]{subname}[/dark_orange3]\n[salmon1]Description: {subdesc}[/salmon1]\n\n",markup=True)
        Console.print(f"[blue3]Title:[/blue3] {title} \n[deep_sky_blue3]Description: [/deep_sky_blue3]")
        Console.print(Markdown(desc))
        if link.__contains__("i."):
            Console.print(f"\n[green_yellow]Image:[/green_yellow]")
            get_multi.Image.download(link)
            Console.print(f"\n[purple4]Url:[/purple4] {link}")
        elif link.__contains__("v.") and video_sett:
            Console.print(f"\n[green_yellow]Video (might be taking long):[/green_yellow]")
            get_multi.Video.download(link)
            Console.print(f"\n[purple4]Url:[/purple4] {link}")
        else:
            Console.print(f"\n[purple4]Url:[/purple4] {link}")
        
        
