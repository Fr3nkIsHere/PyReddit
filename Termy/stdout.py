import sys, re, pickle, numpy
from rich import console, style
from typing import Self, Type, Optional, Union, IO, TextIO
from time import sleep


if (sys.platform == "linux"):
    import sounddevice as sd
else:
    import winsound



class stdout:
    """
    The new stdout created for Termy! 
    Based on the Rich Library.
    So, it can be possibly reused in other programs.


    Args:
        @OutType (int): The Output type of stdout (can be Terminal[1], a File[2])
        @Path (str): The output name of stdout                          |
            ! Required only if you aren't using a Terminal for stdout <-┘
        @Color (bool): If The output need to ave Color or not       | 
            ! Required only if you're using a Terminal for stdout <-┘
    
    Returns:
        Nothing
        
    """
    def __init__(self: Self, 
                 OutType: Optional[int] = 1, 
                 Path: Optional[str | None] = None,
                 Color: bool = True) -> Self:
        self.TERMINAL: int = 1
        self.FILE: int = 2
        self.Type: int  = OutType
        self.Path: str | None = Path
        self.StdoutPath = "stdout.dat"

        if(self.Type == self.TERMINAL):
            self.Path: str | None = None 
            self.FileStream: IO = None
        else:
            self.FileStream: IO = open(self.Path, "w")
            
        with open(self.StdoutPath, "wb"):{}
            

        self.Console: console.Console = console.Console(file=self.FileStream ,no_color=(not Color))
        
 

    class ConsoleInfo:
        """
            TODO: A better Implementation
        """
        def __init__(self: Self):
            self.ConsoleWidth: int = console.Console.width
            self.ConsoleHeight: int = console.Console.height
            self.ConsoleColor: str = console.Console.color_system

    
    def ClearScr(self: Self, 
                CurPosX: Optional[int] = -1,
                CurPosY: Optional[int] = -1) -> None:
        """
        Clear the Terminal and set the cursor in every terminal position

        Args:
            @CurPosX (int): The X position to go after clearing the screen  |
                ! Leave -1 or set a number <0 for no cursor movement      <-┘
            @CurPosY (int): The Y position to go after clearing the screen  |
                ! Leave -1 or set a number <0 for no cursor movement      <-┘
            
        Return:
            Nothing
        """
        sys.stdout.write(f"\x1b[{CurPosY};{CurPosX}H")
        self.Home: bool = True if(CurPosX and  CurPosY < 0) else False 
        with open(self.StdoutPath, "wb"):{}
        self.Console.clear(home=self.Home)

    def Beep(self: Self,
             Freq: int = 37,
             Duration: int = 1000) -> None:
        
        """
        Create a Beep from the speaker with differet duration and tune

        Args:
            @Freq (int): The Frequency of the beep within a Range from 32 trought 32767|
                ! If Freq is <32 or >32767 make the default terminal beep            <-┘
            @Duration (int): The Beep duration in milliseconds
            
        Return:
            Nothing
        """

        if(Freq > 32 and Freq < 32767):
            if (sys.platform != "linux"):
                winsound.Beep(Freq, Duration) 
            else:
                camp: float = numpy.sin(2 * numpy.pi * Freq *\
                                          numpy.arange(int(Duration * 44_000)) / \
                                          44_000)
                sd.play(camp, samplerate=44_000)
                sleep(Duration/1000)
                sd.stop()
                
        else:
            self.Console.bell()

    def StdOutBackupRefresh(self: Self, OutFile: str = "stdout.dat", Text: str = "") -> list[list[str]]:
        #Internal Method
        with open(OutFile, 'ab') as file:
            pickle.dump(Text, file)

    def Println(self: Self,
                *Prompt: Type,
                Style: Optional[Union[str, style.Style]] = None,
                PosX: Optional[int] = -1,
                PosY: Optional[int] = -1,
                Delay: float = 0,
                Type: Optional[str] = "Text",
                WithSaveguard: Optional[bool] = True,
                Separator: str = ' ',
                End: str = '\n') -> None:
        """
            ! For not esage of Positioned Text, set PosX & PosY == -1 or any number < 0
        """
        
        
        
        with self.Console.capture() as capture:
            if(Type == "Text"):
                self.Console.print(*Prompt, 
                                sep=Separator, 
                                style=Style, 
                                end=End)
            elif(Type == "JSON"):
                self.Console.print_json(*Prompt)

        
        TrueOut: str = capture.get()
        TrueOut: str = re.sub(r'\x1b\[.*?m', '', TrueOut)

        if(WithSaveguard):
            self.StdOutBackupRefresh(Text=TrueOut)

        sleep(Delay)

        if(PosX, PosY > 0):
            sys.stdout.write(f"\x1b[{PosY};{PosX}H")

        self.Console.print(TrueOut, style=Style)
    
    def CreateBackup(self: Self, Name: str = "stdout_back.dat") -> None:
        """
        Create a Backup copy of the file "stdout.dat"

        Args:
            @Name (str): The name of the file to save the backup
            
        Return:
            Nothing
        """
        with open(self.StdoutPath, 'rb') as file:
            Output: str  = pickle.load(file)
        
        with open(Name, 'wb') as file:
            pickle.dump(Output, file)


    def PrintBack(self: Self, Style: Optional[Union[str, style.Style]] = None,
                Separator: str = ' ',
                End: str = '\n',
                Name: str = "stdout.dat") -> None:
        
        """
        Restore a Backup of the stdout

        Args:
            @Name (str): The name of the file to get the backup
            @Separator (str): go to Println for the definition
            @Style (str | rich.style.Style): same here
            @End (str): and here
            
        Return:
            Nothing
        """

        with open(Name, 'rb') as file:
            Output: str  = pickle.load(file)
        self.ClearScr()
        self.Println(Output, Style=Style, Separator=Separator, End=End)

class stderr:
    NotImplemented