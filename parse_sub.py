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
import requests, praw, pyfiglet, ascii_magic
from rich import console
from rich.markdown import Markdown
import linecache

Console = console.Console()

reddit= praw.Reddit(client_id="dpCFcO5NCMP4Xa7ZqQP6rA",         
                                client_secret="eHOQOtGHXfg8xLX9drgIlhQxi5dnHQ",     
                                user_agent="Mozilla/5.0 (Windows NT 10.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.35")


class Subreddit:
    def get(nsfw_setting: bool = True):
        if nsfw_setting:
            if random.randint(1,5) == 1:
                subreddit = reddit.random_subreddit(nsfw_setting)
            else: 
                subreddit = reddit.random_subreddit()
        else:
            subreddit = reddit.random_subreddit()
        name = pyfiglet.figlet_format(subreddit.display_name)
        for post in subreddit.top(time_filter="week"):
            Subreddit.out(post.title, post.selftext, post.url, name, subreddit.title)
            qui = Console.input("")
            if qui.lower() == ":n" or qui.lower() == "": #Next post in the sub
                Console.print(f"\n[blue_violet]Next Post...[/blue_violet]")
                time.sleep(1)
                continue            
            elif qui.lower() == ":q":  #Quit into the menu
                return True
            elif qui.lower() == ":r":  #Get a new Subreddit
                Console.print(f"\n[blue_violet]Next Subreddit...[/blue_violet]")
                time.sleep(1)
                break
                   

    def out(title, desc, link, subname, subdesc):
        system("cls")
        Console.print(f"[dark_orange3]{subname}[/dark_orange3]\n[salmon1]Description: {subdesc}[/salmon1]\n\n",markup=True)
        Console.print(f"[blue3]Title:[/blue3] {title} \n[deep_sky_blue3]Description: [/deep_sky_blue3]")
        Console.print(Markdown(desc))
        if link.endswith(".png") or link.endswith(".jpg") or link.endswith(".gif"):
            Console.print(f"\n[green_yellow]Image:[/green_yellow]")
            f = open('last_pic.jpg','wb')
            response = requests.get(link)
            f.write(response.content)
            f.close()
            image = ascii_magic.from_image_file('last_pic.jpg')
            ascii_magic.to_terminal(image)
            Console.print(f"\n[purple4]Url:[/purple4] {link}")
        else:
            Console.print(f"\n[purple4]Url:[/purple4] {link}")
        
        