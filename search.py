

'''
*****************************************
*            Beta Software              *
*         Use only at your risk         *
*                Fr3nk                  *
***************************************** 
Search Engine
'''
      


import json, time, os, random
import requests, praw, pyfiglet, ascii_magic
from rich import console
from rich.markdown import Markdown
import linecache, parse_sub

reddit= praw.Reddit(client_id="dpCFcO5NCMP4Xa7ZqQP6rA",         
                                client_secret="eHOQOtGHXfg8xLX9drgIlhQxi5dnHQ",     
                                user_agent="Mozilla/5.0 (Windows NT 10.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.35")
Console = console.Console()

def search(nsfw):
    result = True
    while result:
        os.system("cls")
        search = pyfiglet.figlet_format("Search")
        Console.print(f"[dark_orange3]{search}[/dark_orange3]\n\n",markup=True)
        try:
            if nsfw:
                Console.print("[deep_pink4]Search A subreddit[/deep_pink4]")
                Console.print("[orange_red1]r/", end="")
                search = Console.input()
                Console.print("[spring_green3]Searching[/spring_green3]", end=" ")
                time.sleep(0.3)
                Console.print(f"[slate_blue1]r/{search}[/slate_blue1]")
                subreddit = reddit.subreddit(search)
                time.sleep(1)
                reading = True
                name = pyfiglet.figlet_format(subreddit.display_name)
                Console.print("[spring_green3]Subreddit Found! receiving Data...[/spring_green3]")
                time.sleep(1)
                while reading:
                    os.system("cls")
                    name = pyfiglet.figlet_format(subreddit.display_name)
                    for post in subreddit.top(time_filter="month"):
                        Console.print(f"[dark_orange3]{name}[/dark_orange3]\n[salmon1]Description: {subreddit.title}[/salmon1]\n\n",markup=True)
                        Console.print(f"[blue3]Title:[/blue3] {post.title} \n[deep_sky_blue3]Description: [/deep_sky_blue3]")
                        Console.print(Markdown(post.selftext))
                        if post.url.endswith(".png") or post.url.endswith(".jpg") or post.url.endswith(".gif"):
                            Console.print(f"\n[green_yellow]Image:[/green_yellow]")
                            f = open('last_pic.jpg','wb')
                            response = requests.get(post.url)
                            f.write(response.content)
                            f.close()
                            image = ascii_magic.from_image_file('last_pic.jpg')
                            ascii_magic.to_terminal(image)
                            Console.print(f"\n[purple4]Url:[/purple4] {post.url}")
                        else:
                            Console.print(f"\n[purple4]Url:[/purple4] {post.url}")
                        qui = Console.input("")
                        if qui.lower() == ":q": #Quit into main
                            reading = False
                            result = False
                            break
                        elif qui.lower() == ":n" or qui.lower() == "": #Next post in the sub
                            Console.print(f"\n[blue_violet]Next Post...[/blue_violet]")
                            time.sleep(1)
                            Console.clear()
                            os.system("cls")
                            continue
                        elif qui.lower() == ":s": #Search another sub
                            reading = False
                            break
                            
            else:
                Console.print("[deep_pink4]Search A subreddit [/deep_pink4]")
                Console.print("[orange_red1]r/", end="")
                search = Console.input()
                subreddit = reddit.subreddit(search)
                time.sleep(1)
                reading = True
                name = pyfiglet.figlet_format(subreddit.display_name)
                Console.print("[spring_green3]Subreddit Found! receiving Data...[/spring_green3]")
                time.sleep(1)
                if subreddit.over18:
                    Console.print(f"[red1]NSFW subs disabled. Please enable into settings.[/red1]")
                    Console.input()
                else:
                    while reading:
                        os.system("cls")
                        name = pyfiglet.figlet_format(subreddit.display_name)
                        for post in subreddit.top(time_filter="month"):
                            Console.print(f"[dark_orange3]{name}[/dark_orange3]\n[salmon1]Description: {subreddit.title}[/salmon1]\n\n",markup=True)
                            Console.print(f"[blue3]Title:[/blue3] {post.title} \n[deep_sky_blue3]Description: [/deep_sky_blue3]")
                            Console.print(Markdown(post.selftext))
                            if post.url.endswith(".png") or post.url.endswith(".jpg") or post.url.endswith(".gif"):
                                Console.print(f"\n[green_yellow]Image:[/green_yellow]")
                                f = open('last_pic.jpg','wb')
                                response = requests.get(post.url)
                                f.write(response.content)
                                f.close()
                                image = ascii_magic.from_image_file('last_pic.jpg')
                                ascii_magic.to_terminal(image)
                                Console.print(f"\n[purple4]Url:[/purple4] {post.url}")
                            else:
                                Console.print(f"\n[purple4]Url:[/purple4] {post.url}")
                            qui = Console.input("")
                            if qui.lower() == ":q": #Quit into main
                                reading = False
                                result = False
                                break
                            elif qui.lower() == ":n" or qui.lower() == "": #Next post in the sub
                                Console.print(f"\n[blue_violet]Next Post...[/blue_violet]")
                                time.sleep(1)
                                Console.clear()
                                os.system("cls")
                                continue
                            elif qui.lower() == ":s": #Search another sub
                                reading = False
                                break
        except Exception as e:
            Console.print(f"[red1]Error Searching r/{search}: {e}[/red1]")
            Console.input()