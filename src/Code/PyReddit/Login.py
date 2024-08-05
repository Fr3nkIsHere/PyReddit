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
*                            PyReddit Login Source Code                                 *
*                                                                                       *
*                                                                                       *
*****************************************************************************************
"""

from typing import Self, Final
from praw import Reddit
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from random import randint

from pydub import AudioSegment
import simpleaudio

class Login:
    """
        The Class that handles Login / Logout (why creating another class for Logout, :) 
        and other useful function for authenticating

        Args:
            @clientID: str -> The ClientID obtainable creating an script application in https://old.reddit.com/prefs/apps/
            @clientSecret: str -> The SecretID obtainable with the same method as the ClientID
            @Token: str -> The Refresh Token obtained after the first login
    """
    def __init__(self: Self, clientID: str, clientSecret: str, Token: str | None) -> None:
        self.redditIstance: Reddit = Reddit(
            client_id=clientID,
            client_secret=clientSecret,
            redirect_uri="https://localhost:8080",
            user_agent="PyReddit/0.5"
        )

        STATE: Final[str] = f"pyReddiUniqueStateLoL{randint(9, 4_294_967_296)}"
        WAITING_MUSIC: Final[str] = "music/waitingAhhMusic.mp3"

        # Authorization URL
        print(f"This is your first time logging in: Please authorize the app using this link -> {self.redditIstance.auth.url(scopes=["*"], state=STATE, duration="permanent")}\n(And in the meantime i'm gonna play some music for the waiting)")
        
        waiting: AudioSegment = AudioSegment.from_file(WAITING_MUSIC)
        raw_data = waiting.raw_data
        sample_rate = waiting.frame_rate
        num_channels = waiting.channels
        bytes_per_sample = waiting.sample_width
        play_obj = simpleaudio.play_buffer(raw_data, num_channels, bytes_per_sample, sample_rate)
        

        # Code obtainer
        #self.token: str = input("!Debug! Inserire Code: ")
        client = self.createConnection()
        data = client.recv(1024).decode("utf-8", errors="replace")
        param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
        params = {
            key: value for (key, value) in [token.split("=") for token in param_tokens]
        }
        print(self.params)

        # Refresh TOken creator
       #print(self.redditIstance.auth.authorize(self.token))
        #print(self.redditIstance.user.me())
        # Fermare la riproduzione
        play_obj.stop()

        return

    
    def createConnection(self: Self) -> socket:
        """Wait for and then return a connected socket..

        Opens a TCP connection on port 8080, and waits for a single client.

        """
        server: socket = socket(AF_INET, SOCK_STREAM)
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind(("localhost", 8080))
        server.listen(1)
        client: socket = server.accept()[0]
        server.close()
        return client


    def send_message(client, message):
        """Send message to client and close the connection."""
        print(message)
        client.send(f"HTTP/1.1 200 OK\r\n\r\n{message}".encode("utf-8"))
        client.close()