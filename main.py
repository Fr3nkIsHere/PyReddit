'''
*****************************************
*            Beta Software              *
*         Use only at your risk         *
*                Fr3nk                  *
***************************************** 
'''



import json
import requests, praw, pyfiglet, time, random, ascii_magic, os
from rich import console
from rich.markdown import Markdown
import linecache
from os import system
import base64

reddit = None
Console = console.Console()
running = True



def get_started():
    global reddit
    time.sleep(0.3)
    file = open("requirements.txt", 'w')
    file.write("rich\nrequests\npraw\npyfiglet\nascii_magic")
    file.close()
    system("pip install -r requirements.txt")
    Console.print("[spring_green3]Installing Required Libraries...✓[/spring_green3]")
    time.sleep(1)
    Console.print("[spring_green3]Creating random subs list...[/spring_green3]",end=" ")
    file = open("random.txt", 'w')
    file.write("memes\nanime\nanimememes\nsports\nfishing\neyebleach\nformula1\nnba\nFoodPorn\nfunny\nspace\nworldnews\ntechnology\ncringepics\nbetterCallSaul\nshitposting\npics\nPorn\nFreeKarma4U\nhentai\nPEDsR\nFiftyFifty")
    file.close()
    Console.print("[spring_green3]✓[/spring_green3]")
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
    reddit= praw.Reddit(client_id="dpCFcO5NCMP4Xa7ZqQP6rA",         
                                client_secret="eHOQOtGHXfg8xLX9drgIlhQxi5dnHQ",     
                                user_agent="Mozilla/5.0 (Windows NT 10.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.35")      

    time.sleep(1)
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
            
    while runningd:
        Console.clear()
        system("cls")
        if nsfw:
            subredditname = linecache.getline('random.txt', random.randint(1,22))
        else:
            subredditname = linecache.getline('random.txt', random.randint(1,17))
        
        subreddit = reddit.subreddit(subredditname)
        name = pyfiglet.figlet_format(subreddit.display_name)
        
        
        Console.print(f"[dark_orange3]{name}[/dark_orange3]\n[salmon1]Description: {subreddit.title}[/salmon1]\n\n",markup=True)
        for post in subreddit.hot(limit=1):
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
        if qui.lower() == ":q": #Quit
            runningd = False
        elif qui.lower() == ":n": #Next post in the sub
            visiting_sub()
            


def visiting_sub():
    global subreddit
    runningsd  = True
    while runningsd:
        for posts in subreddit.top(time_filter="week"):
            Console.print(f"\n[blue_violet]Next Post...[/blue_violet]")
            time.sleep(1)
            Console.clear()
            system("cls")
            
            
            name = pyfiglet.figlet_format(subreddit.display_name)
            Console.print(f"[dark_orange3]{name}[/dark_orange3]\n[salmon1]Description: {subreddit.title}[/salmon1]\n\n",markup=True)
            Console.print(f"[blue3]Title:[/blue3] {posts.title} \n[deep_sky_blue3]Description: [/deep_sky_blue3]")
            Console.print(Markdown(posts.selftext))
            if posts.url.endswith(".png") or posts.url.endswith(".jpg") or posts.url.endswith(".gif"):
                Console.print(f"\n[green_yellow]Image:[/green_yellow]")
                f = open('last_pic.jpg','wb')
                response = requests.get(posts.url)
                f.write(response.content)
                f.close()
                image = ascii_magic.from_image_file('last_pic.jpg')
                ascii_magic.to_terminal(image)
                Console.print(f"\n[purple4]Url:[/purple4] {posts.url}")
            else:
                Console.print(f"\n[purple4]Url:[/purple4] {posts.url}")
            
            
            qui = Console.input("")
            if qui.lower() == ":q": #Quit random
                runningsd = False
                break
            elif qui.lower() == ":n": #Next post
                continue
            elif qui.lower() == ":r": #Refresh random subs (not working lol)
                main()


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
        Console.print("[bright_red]2) Help[/bright_red]")
        #Console.print("[deep_pink4]2) See some Subreddit[/deep_pink4]")
        Console.print("[bright_red]3) Settings[/bright_red]")
        Console.print("[orange1]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/orange1]")
        sel = Console.input("Select: ")
        Console.bell()
        match int(sel):
            case 0:
                Console.clear()
                Console.print("[bright_red]Shutting Down..[/bright_red]")
                time.sleep(0.5)
                running = False
            case 1:
                random_place()
            case 2:
                help()
            case 3:
                settings()
            



if __name__ == "__main__":
    main()
