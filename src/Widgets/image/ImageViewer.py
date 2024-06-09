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
from os import stat
from os.path import getsize

from textual.app import App, ComposeResult, RenderResult
from textual.widget import Widget, Size

from PIL import Image
from rich_pixels import Pixels


class ImageInfo:
    """
        A simple Class to save Information about an Image
    """
    def __init__(self: Self,
                 name: str = "name.bmp",
                 date: float = 0,
                 type: str = 'bmp',
                 width: int = 0,
                 height: int = 0,
                 size: float = 0,
                 colors: int = 2,
                 data: Image = None):
        """
            Initialize the Class.

            Args:
                @name: The File Name
                @date: The Date of creation expressed in UNIX time
                @type: Image type
                @width: Image width
                @height: Image height
                @size: Image size (in Byte)
                @colors: Number of Colors
                @data: Image data
        """
        self.name: str = name
        self.date: float = date
        self.type: str = type
        self.width: int = width
        self.height: int = height
        self.size: float = size
        self.colors: int = colors
        self.data: Image = data


class ImageViewer(Widget):
    """
        This is A Widget to display an image with Textual & Rich Pixels
    """

    DEFAULT_CSS: Final[str] = (lambda f: f.read())(open("src/Widgets/image/ImageViewer.tcss"))

    def __init__(self: Self, 
                 path: str = "src/Widgets/image/Test.bmp", 
                 name: str | None = None,
                 id: str | None = None,
                 classes: str | None = None) -> None:

        """
        Initialise the image viewer widget.

        Args:
            @path: The Image Path needed to be shown.
            @name: The name of the header widget.
            @id: The ID of the header widget in the DOM.
            @classes: The CSS classes of the header widget.
        """

        super().__init__(name=name, id=id, classes=classes)

        # Setting up some varaiables
        self.path: str = path

        self.width: int = 80        # Some Default values
        self.height: int = 60       #

        self.iwidth: int = self.width    # Image width
        self.iheight: int = self.height  # Image height

        # Acquire Image info
        self.imageInfo: ImageInfo = self.acquire()
        

    


    def resize(self: Self, width: int, height: int) -> None:
        """
        Resize the Widget with the appropriate width & height

        Args:
            @width: The width of the terminal
            @height: The height of the terminal
        
        ! This only resize the widget, doesn't zoom the image. For it there is the _on_scroll() methods
        +
        ! In this case it will (for simplicity) based of the position of the Widget for PyReddit (left)
        """
        self.width: int = int(width/3 * 2)
        self.height: int = height - 5

        
    
    def acquire(self: Self) -> ImageInfo:
        """
            Acquire Image info
        """

        try:
            info: ImageInfo = ImageInfo()
            modeToBpp: dict[str: int] = {
                "1": 1,
                "L": 8,
                "P": 8,
                "RGB": 24,
                "RGBA": 32,
                "CMYK": 32,
                "YCbCr": 24,
                "LAB": 24,
                "HSV": 24,
                "I": 32,
                "F": 32
            }
            with Image.open(self.path) as image:
                info.name: str = self.path
                info.date: float = stat(info.name).st_atime
                info.type: str = self.path.split('.')[-1]
                info.width: int = image.width
                info.height: int = image.height
                info.size: int = getsize(self.path)
                info.colors: int = modeToBpp.get(image.mode, 24)
                info.data: bytes = image.copy()

            return info

        except IOError:
            exit(20)
        
    def get_content_width(self: Self, container: Size, viewport: Size) -> int:
        """
            Obtaint the Widget width
        """
        return self.width

    def get_content_height(self: Self, container: Size, viewport: Size, width: int) -> int:
        """
            Obtaint the Widget height
        """
        return self.height

    def render(self: Self) -> RenderResult:
        """
            Render the Image built
        """
        
        imageScale: float = self.imageInfo.width / self.imageInfo.height 
        widgetScale: float = self.width / self.height
        if imageScale > widgetScale: 
            width: int = self.width
            height: int= int(self.width / imageScale)
        else:
            width: int = int(self.height * imageScale)
            height: int= self.height 
        
        return Pixels.from_image(self.imageInfo.data, resize=(width * 2, height * 2))