
'''
*****************************************
*            Beta Software              *
*         Use only at your risk         *
*                Fr3nk                  *
***************************************** 

The main program
'''


from os import system


try: 
    import requests, praw, pyfiglet, ascii_magic
except ModuleNotFoundError:
    file = open("requirements.txt", 'w')
    file.write("rich\nrequests\npraw\npyfiglet\nascii_magic")
    file.close()
    system("pip install -r requirements.txt")
    import requests, praw, pyfiglet, ascii_magic
    

import json, time, os, random
from rich import console
from rich.markdown import Markdown
import linecache
import search, parse_sub


reddit = None
Console = console.Console()
running = True



def get_started():
    global reddit
    time.sleep(0.3)
    
    Console.print("[spring_green3]Installing Required Libraries...✓[/spring_green3]")
    time.sleep(1)
    Console.print("[spring_green3]Testing Internet Connection...[/spring_green3]",end=" ")
    time.sleep(0.3)
    try:
        requests.request("GET","https://reddit.com")
        Console.print("[spring_green3]✓[/spring_green3]")
    except:
        Console.print("[red1]X[/red1]")
        Console.print("[bright_red]Error Connecting to the internet, Please Try Later. [/right_red]")
        time.sleep(1)
        exit()
    time.sleep(0.3)
    Console.print("[spring_green3]Connection with Reddit... ✓[/spring_green3]")
    time.sleep(0.3)
    Console.print("[spring_green3]Starting PyReddit 0.1... [/spring_green3]")
    time.sleep(3)



#Random Place               
def random_place():
    global reddit, subreddit
    runningd = True
    Console.print("[spring_green3]Connection with Reddit... ✓[/spring_green3]")
    time.sleep(0.5)
    Console.print("[spring_green3]Checking Setings...[/spring_green3]",end=" ")
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
    time.sleep(0.5)
    stop = False
    Console.clear()
    while not stop:
        system("cls")
        stop = parse_sub.Subreddit.get(nsfw)
            

#help
def help():
    system("cls")
    PyReddit = pyfiglet.figlet_format("Help")
    Console.print(f"[dark_orange3]{PyReddit}[/dark_orange3]\n\n",markup=True)
    Console.print(":q Exit from the subreddit/return to main menù")
    Console.print(":n In the same subreddit go to the next post (of the week)")
    Console.print(":r Everything you did, this command bring you in the main menu")
    Console.print("Enter --> Change Random Subreddit")
    Console.input("")

#Settings 
def settings():
    sett = 1
    sex = "n"
    while sett: #Global Settings
        Console.clear()
        system("cls")
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
                system("cls")
                Settings = pyfiglet.figlet_format("Settings")
                Console.print(f"[dark_orange3]{Settings}[/dark_orange3]\n\n",markup=True)
                sex = Console.input("- Enable +18 (Default: N)[y/n]: ")
    
    #Writing Settings
    Console.print("[bright_red]Saving Settings...[/bright_red]")
    setting = open("settings.cfg","w")
    if sex.lower() == "y":
        setting.writelines(f"NSFW= 1")
    else:
        setting.writelines(f"NSFW= 0")
    setting.close()
    time.sleep(0.5)
    Console.print("[spring_green2]Done![/spring_green2]")
    time.sleep(0.5)


#Main Program
def main(): 
    global running
    get_started()
    while running: 
        system("cls")
        PyReddit = pyfiglet.figlet_format("PyReddit")
        Console.print(f"[dark_orange3]{PyReddit}[/dark_orange3]\n\n",markup=True)
        Console.print("[orange_red1]0) Exit[/orange_red1]")
        Console.print("[red1]1) Start Navigating Randomly[/red1]")
        Console.print("[deep_pink4]2) Search some Subreddits[/deep_pink4]")
        Console.print("[bright_red]3) Help[/bright_red]")
        Console.print("[bright_red]4) Settings[/bright_red]")
        Console.print("[orange1]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/orange1]")
        sel = Console.input("Select: ")
        Console.bell()
        match sel:
            case '0':
                Console.clear()
                Console.print("[bright_red]Shutting Down...[/bright_red]")
                time.sleep(0.5)
                running = False
            case '1':
                random_place()
            case '2':
                Console.print("[spring_green3]Checking Setings...[/spring_green3]",end=" ")
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
                time.sleep(0.5)
                search.search(nsfw)
            case '3':
                help()
            case '4':
                settings()
            case _:
                Console.bell()
                system("cls")
                Console.print("[bright_red]Not A Valid Input[/bright_red]")
                Console.input("[bright_red]Press Any key to continue...[/bright_red]")
            



if __name__ == "__main__":
    main()
