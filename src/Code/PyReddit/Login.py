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

#from pydub import AudioSegment
#import simpleaudio

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
        
        if(Token is not None):
            # Login with the Token
            try:
                self.redditIstance: Reddit = Reddit(
                    client_id=clientID,
                    client_secret=clientSecret,
                    refresh_token=Token,
                    user_agent="PyReddit/0.5"
                )
                print(f"PyRedit is now Logged! User: {self.redditIstance.user.me()}.")
                return
            except:
                print("Not a valid Token, re-authenticating...")

                # First of all: Deleting the old Token
                with open(".env", 'r') as file:
                    lines: list[str] = file.readlines()
                with open(".env", 'w') as file:
                    for line in lines:
                        if not line.startswith(f"TOKEN="):
                            file.write(line)

        #Login Without Token
        self.redditIstance: Reddit = Reddit(
            client_id=clientID,
            client_secret=clientSecret,
            redirect_uri="http://localhost:8080",
            user_agent="PyReddit/0.5"
        )

        STATE: Final[str] = f"pyReddiUniqueStateLoL{randint(9, 4_294_967_296)}"

        # Authorization URL
        print(f"This is your first time logging in: Please authorize the app using this link -> {self.redditIstance.auth.url(scopes=["*"], state=STATE, duration="permanent")}")

        # Code obtainer
        #self.token: str = input("!Debug! Inserire Code: ")
        self.client: socket = self.createConnection()
        data: str = self.client.recv(8192).decode("utf-8", errors="replace")
        param_tokens: list[str] = data.split(" ", 2)[1].split("?", 1)[1].split("&")
        self.params: dict[str: str] = {
            key: value for (key, value) in [token.split("=") for token in param_tokens]
        }
        
        # State Check
        if(self.params.get("state") != STATE):
            print("Error: the State of the request is not equal to the State of PyReddit!")
            print("Please Try Again Later!")
            exit(32)
        
        # Error Check
        if(self.params.get("error") is not None):
            print(f"Error: an Error during the login happened! The response: {self.params.get("error")}")
            print("Please Try Again Later!")
            exit(31)

        # Code Check
        self.refreshToken: str = self.redditIstance.auth.authorize(self.params.get("code"))
        print(f"PyRedit is now Logged! User: {self.redditIstance.user.me()}.")
        self.sendMessage()

        # Saving the Token
        with open(".env", "a") as file:
            file.write(f"\nTOKEN={self.refreshToken}")

        return

    def getIstance(self: Self) -> Reddit:
        """
            Return the Reddit Istance after the Login
            Return:
                Reddit -> The Reddit Istance after the login
        """
        return self.redditIstance

    def createConnection(self: Self) -> socket:
        """Wait for and then return a connected socket..

        Opens a TCP connection on port 8080, and waits for a single client.

        """
        server: socket = socket(AF_INET, SOCK_STREAM)
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind(("localhost", 8080))
        server.listen(1)
        client: socket = server.accept()[0]
        return client


    def sendMessage(self:Self) -> None:
        """Send message to client and close the connection."""
        html: str = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PyReddit - Login</title>
            <style>
                /* Imposta il corpo della pagina per usare Flexbox */
                body {
                    display: flex;
                    justify-content: center; /* Centra orizzontalmente */
                    align-items: center;     /* Centra verticalmente */
                    height: 100vh;           /* Altezza viewport per la centratura verticale */
                    margin: 0;               /* Rimuove i margini predefiniti del body */
                    font-family: Arial, sans-serif; /* Imposta il font del testo */
                    background-color: #f0f0f0; /* Colore di sfondo per contrastare il testo */
                }

                /* Stile per l'elemento h1 */
                h1 {
                    font-size: 2em;          /* Dimensione del testo */
                    color: #333;             /* Colore del testo */
                    text-align: center;      /* Allineamento del testo */
                }
            </style>
        </head>
        <body>
            <h1>You can now close this Page.</h1>
        </body>
        </html>
        """
        self.client.send(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(html)}\r\n\r\n{html}".encode("utf-8"))
        self.client.close()
        return


