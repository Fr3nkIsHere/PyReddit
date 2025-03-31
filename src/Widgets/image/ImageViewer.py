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
from textual.strip import Strip
from textual.widget import Widget, Size
from textual.events import MouseMove
from textual import log

from PIL import Image
from rich_pixels import Pixels

from rich.align import Align


class ImageInfo:
    """
        A simple Class to save Information about an Image

        TODO:
            - Implement a decent Zoom
            - Speed up the Rendering Process
            - Add more function
            - Add a "Low performance method"
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

        self.width: int = 80               # Some Default values
        self.height: int = 60              #
        self.mouseX: int | None = 0        #
        self.mouseY: int | None = 0        #

        self.iwidth: int = self.width           # Image width
        self.iheight: int = self.height         # Image height
        self.zoom: int = 2                      # Zoom factor
        self.origin: Tuple[int, int] = (0, 0)   # Image origin

        # Acquire Image info
        self.imageInfo: ImageInfo = self.acquire()

        self.iheight: int = self.imageInfo.height   # Image height
        self.iwidth: int = self.imageInfo.width     # Image width
        

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

    def _on_mouse_scroll_up(self: Self, event: MouseMove) -> None:
        """
            Zoom in the image
        """
        
        log(f"ImageViewer()._on_mouse_scroll_up() >>> Debug! X: {self.mouseX} || Y: {self.mouseY}")

        self.zoom: int = self.zoom + 0.2
        self.refresh()

    def _on_mouse_scroll_down(self: Self, event: MouseMove) -> None:
        """
            DeZoom in the image
        """

        log(f"ImageViewer()._on_mouse_scroll_down() >>> Debug! X: {self.mouseX} || Y: {self.mouseY}")

        if self.zoom >= 1:
            self.zoom: int = self.zoom - 0.2
        self.refresh()
    
    def on_mouse_move(self: Self, event: MouseMove) -> None:
        """
            Get the mouse position relative to the widget
        """
        self.mouseX: int = event.x
        self.mouseY: int = event.y
        
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

    def render(self: Self) -> Strip:
        """
            Render the Image built
        """

        orig_width, orig_height = self.imageInfo.width, self.imageInfo.height
        widget_width, widget_height = self.size.width, self.size.height

        max_scale = min(widget_width / orig_width, widget_height / orig_height)
        scale_factor = max(self.zoom, max_scale)

        new_width = int(orig_width * scale_factor)
        new_height = int(orig_height * scale_factor)

        if(new_width >= new_height):
            missing: int = self.size.width - new_width
            new_width += missing
            aspect_ratio = new_width / new_height
            new_height = int((orig_height * new_width) / orig_width)
        else:
            missing: int = self.size.height - new_height
            new_height += missing
            aspect_ratio = new_height / new_width
            new_height *= 2
            new_width = int((orig_width * new_height) / orig_height)

        pixel = Pixels.from_image(self.imageInfo.data, resize=(new_width, new_height))
        return pixel

