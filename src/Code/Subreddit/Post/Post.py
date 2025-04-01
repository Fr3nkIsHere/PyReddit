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
*                       PyReddit Post Parser & Viewer Source Code                       *
*                                                                                       *
*                                                                                       *
*****************************************************************************************
"""

from praw.reddit import Submission, Redditor, Subreddit
from typing import Self, Final
from os import stat
from os.path import getsize, exists
import requests

from textual.app import App, ComposeResult, RenderResult
from textual.strip import Strip
from textual.screen import Screen
from textual.widgets import Static
from textual import log

from Widgets.Header import Header
from Widgets.image.ImageViewer import ImageViewer




class PostFetcher():
    """
        This is the Backend for the screen PostViewer used to fetch a reddit post
    """
    
    def __init__(self: Self, post: Submission):
        self.post: Submission = post
        self.id: str = self.post.id
        self.name: str = self.post.title
        self.url: str = self.post.url
        self.imagePath: str = self.obtainImage()
        self.author: Redditor = self.post.author
        self.authorFlar: str = self.post.author_flair_text
        self.subreddit: Subreddit = self.post.subreddit

    def obtainImage(self: Self) -> str:
        file_name = f'cache/{self.id}.jpg'

        if(exists(file_name)):
            return file_name

        # Richiesta GET all'URL dell'immagine
        response = requests.get(self.url, stream=True)

        # Verifica se la richiesta ha avuto successo
        if response.status_code == 200:
            # Apertura del file in modalità scrittura binaria
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return self.id
        else:
            exit()

        
class PostViewer(Screen):
    """
        This is the Screen used to view a post
    """
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def __init__(self: Self, fetcher: PostFetcher):
        super().__init__()
        self.fetcher: PostFetcher  = fetcher
        self.imageViewer: ImageViewer = ImageViewer(path=self.fetcher.imagePath, id="image")
        self.title: str = "PyReddit Alpha 0.5 "
        self.sub_title: str =  f" {self.fetcher.name} : r/{self.fetcher.subreddit.display_name}"
    
    def _on_resize(self: Self) -> None:
        self.imageViewer.resize(self.size.width, self.size.height)

    def compose(self: Self) -> ComposeResult:
        yield Header(show_clock=True, id="Header")
        
        yield self.imageViewer
