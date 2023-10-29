

'''
*****************************************
*            Beta Software              *
*         Use only at your risk         *
*                Fr3nk                  *
***************************************** 
Search Engine
''' 
      

from os import system
import  time
import  praw, pyfiglet
from rich import console
import platform, parse_sub

reddit= praw.Reddit(client_id="dpCFcO5NCMP4Xa7ZqQP6rA",         
                                client_secret="eHOQOtGHXfg8xLX9drgIlhQxi5dnHQ",     
                                user_agent="Mozilla/5.0 (Windows NT 10.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.35")
Console = console.Console()

if platform.system() == 'Windows':
    CLS = "system(\"cls\")"
    TEMP = "C:\\Windows\\Temp"
else:
    CLS = "system(\"clear\")"
    TEMP = "/tmp"

def search(nsfw, video, Time):
    result = False
    while not result:
        try:
            eval(CLS)
            search = pyfiglet.figlet_format("Search")
            Console.print(f"[dark_orange3]{search}[/dark_orange3]\n\n",markup=True)
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
            Times = parse_sub.Subreddit.time_index(Time)
            result = parse_sub.Subreddit.get(nsfw, Times, video, True, search)
        except Exception as e:
            Console.print(f"[red1]Error Searching r/{search}: {e}[/red1]")
            Console.input()