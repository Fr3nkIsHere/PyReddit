'''
*****************************************
*            Beta Software              *
*         Use only at your risk         *
*                Fr3nk                  *
***************************************** 

SubReddit Widget
'''

from rich.text import TextType
from textual.app import  RenderResult
from textual.widgets import Label, Button, Input
from textual.containers import Horizontal
from textual.widget import Widget
from typing import Self, Type
import sys
from rich import console
from pyfiglet import Figlet, FigletString


class SubReddit(Widget):
    def __init__(self: Self,):

        self.Title: str = "Subreddit - pass"
        super().__init__()
        

    def compose(self: Self) -> RenderResult:
        yield Label("Hello", classes="SubTitle")
        yield Input(placeholder="r/ {Not Implemented Yet!}", disabled=False)
        