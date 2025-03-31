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

from praw.reddit import Submission
from typing import Self, Final
from os import stat
from os.path import getsize, exists
import requests

from textual.app import App, ComposeResult, RenderResult
from textual.strip import Strip
from textual.screen import Screen
from textual.events import MouseMove
from textual import log

class PostViewer(Screen):
    """
        This is the Screen used to view a post
    """
    ...


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

        
