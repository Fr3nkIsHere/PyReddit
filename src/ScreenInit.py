'''
*****************************************
*            Beta Software              *
*         Use only at your risk         *
*                Fr3nk                  *
***************************************** 

Screen Rendering
'''

from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Footer, Header, _header
from textual.widget import Widget
from typing import Self, Type
from types import ModuleType
import sys, ctypes
from rich import console

import importlib, os, inspect

class RHeader(Header):
    def __init__(self: Self) -> None:
        super().__init__(show_clock=True)
    
    
    def compose(self):
        yield _header.HeaderTitle()
        yield _header.HeaderClock() if self._show_clock else _header.HeaderClockSpace()
    
    
class Screen(App):
    
    CSS_PATH = "css\\Screen.tcss"

    def __init__(self: Self, subtitle: str = "Menu"):
        super().__init__()
        self.Console: console.Console = console.Console()
        self.Console.set_window_title("PyReddit 0.4")
        self.title: str = "PyReddit 0.4"
        self._value: int = 1
        self.PageTable: dict[int : Widget] = self.generateLookupTable()
        self.sub_title: str = subtitle
        self.rederWidget: Widget = self.PageTable.get(self._value)

    def generateLookupTable(self: Self) -> dict:
        Table: dict[int : Widget] = {}
        count: int = 1
        files: list[str] = [file[:-3] for file in os.listdir("Widgets") if file.endswith(".py")]
        # Importa dinamicamente i moduli e crea il dizionario
        for file in files:
            module_name: str = f"{"Widgets"}.{file}"
            class_name: str = file.capitalize()  # Si suppone che il nome del file e della classe sia simile con la prima lettera maiuscola
    
            try:
                module: ModuleType = importlib.import_module(module_name)
                
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and obj.__module__ == module_name:
                        Table[count] = obj
                        count += 1
                        break
            except (AttributeError, ImportError):
                pass
        return Table

    def setValue(self: Self, value: int) -> None:
        self._value: int = value
        self.rederWidget: Widget = self.PageTable.get(self._value)
        print(self.rederWidget)
        self.compose()

    def compose(self: Self) -> ComposeResult:
        try:
            yield RHeader()
            yield self.rederWidget()
        except:
            pass

        

    

    
    
    