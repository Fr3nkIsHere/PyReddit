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
from praw.models.comment_forest import CommentForest
from typing import Self, Final
from os import stat
from os.path import getsize, exists
import requests

from textual.app import App, ComposeResult, RenderResult
from textual.strip import Strip
from textual.screen import Screen
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Markdown, Link, Input, Button
from textual import log

from Widgets.Header import Header
from Widgets.image.ImageViewer import ImageViewer
from Code.Subreddit.Post.Comments import CommentViewer



class PostFetcher():
    """
        This is the Backend for the screen PostViewer used to fetch a reddit post
    """
    
    def __init__(self: Self, post: Submission):
        self.post: Submission = post
        self.id: str = self.post.id
        self.name: str = self.post.title
        self.url: str = f"https://www.reddit.com{self.post.permalink}"
        self.imagePath: str = self.obtainImage()
        self.author: Redditor = self.post.author
        self.authorFlair: str | None = self.post.author_flair_text
        self.subreddit: Subreddit = self.post.subreddit
        self.locked: bool = not self.post.locked
        self.postFlair: str | None = self.post.link_flair_text
        self.description: str = self.post.selftext
        self.isSpoiler: bool = self.post.spoiler
        self.isNSFW: bool = self.post.over_18
        self.upvotes: int = self.post.score
        self.commentRoot: CommentForest = self.post.comments
        

    def obtainImage(self: Self) -> str:
        file_name = f'cache/{self.id}.jpg'

        if(exists(file_name)):
            return file_name

        # Richiesta GET all'URL dell'immagine
        response = requests.get(self.post.url, stream=True)

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
    CSS_PATH: Final[str] = "./PostViewer.tcss"
    #       &       

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
        yield Horizontal(
                self.imageViewer,
                Vertical(
                    Markdown(f"# {self.fetcher.name} [yellow]{'' if self.fetcher.locked else '' }", id="title"),
                    Horizontal(
                        Static(f"{self.fetcher.postFlair}"),
                        Link("See the original Post!", url=self.fetcher.url, tooltip=self.fetcher.url),
                        Static(f"u/{self.fetcher.author}\n{self.fetcher.authorFlair}"),
                        id="info"
                    ),
                    Horizontal(
                        Static(f"  {self.fetcher.upvotes} "),
                        #Link("See the original Post!", url=self.fetcher.url, tooltip=self.fetcher.url),
                        #Static(f"u/{self.fetcher}\n{self.fetcher.authorFlair}"),
                        id="data"
                    ),
                    Markdown(f"## {self.fetcher.description}", id="desc") if self.fetcher.description != '' else Static(id="desc"),
                    CommentViewer(commentRoot=self.fetcher.commentRoot, id="comments"),
                    Horizontal(
                        Input(placeholder="Create a Comment", type="text", id="commentCreate"),
                        Button("Send", id="sendButton"),
                        id="sender"
                    ),
                    
                )
        )
