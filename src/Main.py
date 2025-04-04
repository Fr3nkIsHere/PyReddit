"""
*****************************************************************************************
*                                                                                       *
*    '########::'##:::'##:'########::'########:'########::'########::'####:'########:   *
*     ##.... ##:. ##:'##:: ##.... ##: ##.....:: ##.... ##: ##.... ##:. ##::... ##..::   *
*     ##:::: ##::. ####::: ##:::: ##: ##::::::: ##:::: ##: ##:::: ##:: ##::::: ##::::   *
*     ########::::. ##:::: ########:: ######::: ##:::: ##: ##:::: ##:: ##::::: ##::::   *
*     ##.....:::::: ##:::: ##.. ##::: ##...:::: ##:::: ##: ##:::: ##:: ##::::: ##::::   *
*     ##::::::::::: ##:::: ##::. ##:: ##::::::: ##:::: ##: ##:::: ##:: ##::::: ##::::   *
*     ##::::::::::: ##:::: ##:::. ##: ########: ########:: ########::'####:::: ##::::   *
*    ..::::::::::::..:::::..:::::..::........::........:::........:::....:::::..:::::   *
*                                                                                       *
*                                                                                       *
*                             Use Reddit in your Terminal!                              *
*                                          by                                           *
*                                     Fr3nkIsHere                                       *
*                                                                                       *
*                Software Usable under MIT License (read the file LICENSE)              *
*                                                                                       *
*                                                                                       *
*                            PyReddit Main Source Code                                  *
*                                                                                       *
*                                                                                       *
*****************************************************************************************
"""

from sys import argv, stdout
from typing import Self, Final
from os import getenv
from dotenv import load_dotenv

from textual.app import App, ComposeResult
from textual.widgets import Header
from textual.widgets._header import HeaderClock, HeaderTitle
from textual.widget import Reactive
from textual import log

from praw import Reddit

# Graphics
from Widgets.image.ImageViewer import ImageViewer
from Widgets.Header import Header
from Code.Subreddit.Post.Post import PostViewer

# Code
from Code.PyReddit.Login import Login
from Code.Subreddit.Post.Post import PostFetcher


class Main(App):
    """
        The Main Application, where everything is displayed
        (well... depends of the needing of course)
    """

    # Setting the CSS
    CSS_PATH: Final[str] = "Main.tcss"
    SCREENS = {"seePost": PostViewer}
    BINDINGS = [("p", "showPost", "Post")]

    def __init__(self: Self, 
                 argv: list[str] = argv) -> None:
        
        super().__init__()

        self.argv: list[str] = argv
        self.argc: int = len(argv)

        # TODO: Data Check

        # Checking the file .env (you need to supply one by yourself under the section Login of the README)
        if(not load_dotenv(".env")):
            print("Error: Unable to load the file .env. Make sure i can open it!")
            exit(1)

        # Check for the Login
        self.redditIstance: Reddit = Login(clientID=getenv("CLIENT_ID"), clientSecret=getenv("CLIENT_SECRET"), Token=None).getIstance() if not self._is_logged() else Login(clientID=getenv("CLIENT_ID"), clientSecret=getenv("CLIENT_SECRET"), Token=getenv("TOKEN")).getIstance()

        # TODO: Widget Check
        #self.imageViewer: ImageViewer = ImageViewer(path="debugImages/Test.bmp")
        
        
        # App Execution
        self.title: str = "PyReddit Alpha 0.5 "
        self.sub_title: str =  " Home"
        self.id: str = "Main"
        stdout.write(f"\x1b]2;{self.title}-{self.sub_title}\x07")
        stdout.flush()
        self.run()

        exit(0)
        return


    def _is_logged(self: Self) -> bool:
        """
            Check if the user is logged or not by checking the Refresh Token
        """
        if(getenv("TOKEN") is None): return False
        return True

    def _on_resize(self: Self) -> None:
        #self.imageViewer.resize(self.size.width, self.size.height)
        ...

    def action_showPost(self: Self) -> None:
        self.push_screen(PostViewer(PostFetcher(self.redditIstance.submission(id="1jni1s3"))))

    def compose(self: Self) -> ComposeResult:
        log("Header() >>> Loading the Header Widget!")
        yield Header(show_clock=True, id="Header") 
        
        # ! Test of the ImageViewer
        #log("Main() >>> Loading the ImageViewer Widget!")
        #yield self.imageViewer

        # ! Test of the PostViewer
        log("Main() >>> Loading the PostViewer Screen!")



if __name__ == "__main__":
    # ! Test of the Post method
    Main()