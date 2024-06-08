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
*                          PyReddit ImageViewer Source Code                             *
*                                                                                       *
*                                                                                       *
*****************************************************************************************
"""


from typing import Self, Final

from textual.app import App, ComposeResult, RenderResult
from textual.widget import Widget

from PIL import Image
from rich_pixels import Pixels


class ImageViewer(Widget):
    """
        This is A Widget to display an image with Textual & Rich Pixels
    """

    CSS_PATH: Final[str] = "ImageViewer.tcss"

    def __init__(self: Self, 
                 path: str = "src/Widgets/image/Test.bmp", 
                 name: str | None = None,
                 id: str | None = None,
                 classes: str | None = None) -> None:

        """Initialise the image viewer widget.

        Args:
            @path: The Image Path needed to be shown.
            @name: The name of the header widget.
            @id: The ID of the header widget in the DOM.
            @classes: The CSS classes of the header widget.
        """

        super().__init__(name=name, id=id, classes=classes)

        self.path: str = path

        # Opening the Image
        with Image.open(self.path) as image:
            self.data: Pixels = Pixels.from_image(image, resize=(80, 60))


    def render(self: Self) -> RenderResult:
        """
            Render the Image built
        """
        return self.data