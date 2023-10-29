'''
*****************************************
*            Beta Software              *
*         Use only at your risk         *
*                Fr3nk                  *
***************************************** 

Menu Widget
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
from ScreenInit import Screen

class RandomButton(Button):
    def __init__(self, label: TextType | None = None, *, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False):
        super().__init__(label, "default", name=name, id=id, classes=classes, disabled=disabled)
    
    def press(self) -> Self:
        super().press()
        Screen().setValue(2)


        

class Menu(Widget):
    def __init__(self: Self,):

        self.PyReddit: FigletString = Figlet().renderText("PyReddit")
        self.Random: str = "Random SubReddit"
        super().__init__()
        

    def compose(self: Self) -> RenderResult:
        yield Label(self.PyReddit, classes="Title")
        yield Input(placeholder="r/ {Not Implemented Yet!}", classes="Search", disabled=True)
        yield Horizontal(
            Button("Search SubReddit", variant="success", disabled=True, classes="ButtonSearch"),
            RandomButton(self.Random,classes="Random"),
            classes="Buttons"
        )
        