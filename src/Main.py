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

from textual.app import App, ComposeResult
from textual.widgets import Header
from textual.widgets._header import HeaderClock, HeaderTitle
from textual.widget import Reactive

from Widgets.image.ImageViewer import ImageViewer

class Header(Header):
    """
        An Header replacement of the textual.widgets.Header implementation of an Header
    """

    def __init__(self: Self, 
                show_clock: bool = False,
                name: str | None = None,
                id: str | None = None,
                classes: str | None = None) -> None:
        """Initialise the header widget.

        Args:
            @show_clock: ``True`` if the clock should be shown on the right of the header.
            @name: The name of the header widget.
            @id: The ID of the header widget in the DOM.
            @classes: The CSS classes of the header widget.
        """
        super().__init__(show_clock=show_clock, name=name, id=id, classes=classes)

    def compose(self: Self) -> ComposeResult:
        yield HeaderTitle()
        yield HeaderClock() if self._show_clock else HeaderClockSpace()
        
    
    def _on_click(self: Self) -> None:
        return

class Main(App):
    """
        The Main Application, where everything is displayed
        (well... depends of the needing of course)
    """

    # Setting the CSS
    CSS_PATH: Final[str] = "Main.tcss"

    def __init__(self: Self, 
                 argv: list[str] = argv) -> None:
        
        super().__init__()

        self.argv: list[str] = argv
        self.argc: int = len(argv)

        # TODO: Data Check

        # TODO: Widget Check
        
        # App Execution
        self.title: str = "PyReddit Alpha 0.5 "
        self.sub_title: str =  " Home"
        self.id: str = "Main"
        stdout.write(f"\x1b]2;{self.title}-{self.sub_title}\x07")
        stdout.flush()

        self.run()

        exit(0)
        return
    
    def compose(self: Self) -> ComposeResult:
        yield Header(show_clock=True, id="Header") 
        yield ImageViewer()



if __name__ == "__main__":
    Main()