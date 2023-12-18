#######################################################
#                                                     #
#  ux.py - Library used to have a nice responsive UX  #
#         with bubble, image printing, colors         #
#                                                     #
#######################################################

# author : Grégoire Badiche
# sources : Wikipedia (https://en.wikipedia.org/wiki/ANSI_escape_code)
#           My big brain 🧠 🧠 🧠

from os import get_terminal_size

# CSI
ESC = "\u001b["

COLORS_FG = {
    "black": "30m",
    "red": "31m",
    "green": "32m",
    "yellow": "33m",
    "blue": "34m",
    "magenta": "35m",
    "cyan": "36m",
    "white": "37m"
}

COLORS_BG = {
    "black": "40m",
    "red": "41m",
    "green": "42m",
    "yellow": "43m",
    "blue": "44m",
    "magenta": "45m",
    "cyan": "46m",
    "white": "47m"
}

def write(text:str) -> None:
    """ Shorthand to print text without automatic newline """
    print(text, end='')

def setcode(code:str|int) -> None:
    """ Shorthand to set ANSI code """
    write(f"{ESC}{code}")

def resetcolors()-> None:
    """ Resets the terminal colors back to default """
    setcode("39m")
    setcode("49m")

def clear() -> None:
    """ Clears the terminal """
    write("\033c")

class Bubble:
    def __init__(self, width:int, orientation:bool, text:str = "", error:bool = 0, _s:int = 0) -> None:
        self.width = width
        self.error = error
        self.text = text
        self.parsedtext = []
        self.orientation = orientation
        self._s = _s
        self.parse()
    
    def draw(self, padding:int = 0, consolewidth:int = 0) -> None:
        """ Draws the bubble """
        consolewidth = consolewidth if consolewidth else get_terminal_size()[0]
        c = lambda: (setcode(COLORS_FG["red"]) if self.error else setcode(COLORS_FG["cyan"])) if self.orientation else (setcode(COLORS_FG["red"]) if self.error else setcode(COLORS_FG["green"]))
        d = lambda: setcode("39m") # Reset FG color
        if(self._s):
            w = self._s
        else:
            if(len(self.parsedtext) == 1):
                w = len(self.parsedtext[0].strip()) + 2
            else:
                w = max([len(l.strip()) for l in self.parsedtext]) + 2
        pad = " " * padding if not(self.orientation) else " " * (consolewidth - w - padding - 2)
        # Sets the cursor at the beginnig of the line, and draws the box
        setcode("G")
        c()
        write(pad + "╭")
        write("─" * w)
        write("╮")
        d()
        write('\n')
        for line in self.parsedtext:
            l = line.strip()
            c()
            write(pad + '│ ')
            d()
            write(l)
            write(" " * (w - 2 -len(l)))
            c()
            write(' │''\n')
            d()
        c()
        if(self.orientation):
            write(pad + "╰")
            write("─" * w)
            write("┴")
        else:
            write(pad + "┴")
            write("─" * w)
            write("╯")
        d()
        write('\n')
    
    def parse(self) -> None:
        """ 
        Parses the text into an array, stored inside self.parsedtext 
        in order to print the text without any overflow
        """
        self.parsedtext = []
        width = self.width - 4 # Removes border and padding
        phrases = self.text.split('\n')
        # If special (e.g an image), we don't parse it
        if(self._s):
            self.parsedtext = phrases
            return
        for phrase in phrases:
            if(phrase.strip() == ""): continue
            words = phrase.split(' ')
            line = ""
            for w in words:
                if(len(w) > width):
                    if(len(line) == 0):
                        cut = width
                    else:
                        if(width - 1 - len(line) == 0):
                            self.parsedtext.append(line)
                            line = ""
                            cut = width
                        else:
                            cut = width - 1 - len(line)
                            line += " "
                    line += w[:cut]
                    self.parsedtext.append(line)
                    line = w[cut:]
                else:
                    if(len(line) + len(w) + 1 <= width):
                        if(line != ""):
                            line += " "
                        line += w
                    else:
                        self.parsedtext.append(line)
                        line = w
            if(line != ""):
                self.parsedtext.append(line)
    
    def resize(self, width:int, padding:int = 0, consolewidth:int = 0) -> None:
        self.width = width
        self.parse()
        self.draw(padding, consolewidth)

class Scene:
    """ Scene object regroups all the Bubbles and updates them automatically """
    def __init__(self) -> None:
        """ Creates constants, clears the terminal """
        self.bubbles:list[Bubble] = []
        self.consolewidth = get_terminal_size()[0]
        self.width = int(self.consolewidth * 2 / 3)
        self.padding = 3
        clear()
    
    def update(self, *args) -> None:
        """ Resizes all the Bubbles if the terminal has been resized """
        if(self.consolewidth == get_terminal_size()[0]): return
        clear()
        self.consolewidth = get_terminal_size()[0]
        self.width = int(self.consolewidth * 2 / 3)

        for bubble in self.bubbles:
            bubble.resize(self.width, self.padding, self.consolewidth)
    
    def new(self, text:str, orientation:bool = 0, error:bool = 0, _s:int = 0) -> None:
        """ Creates a new text Bubble """
        self.bubbles.append(Bubble(self.width, orientation, text, error, _s=_s))
        self.bubbles[-1].draw(self.padding, self.consolewidth)
    
    def handle(self) -> str:
        """ Handles and return input() in a pretty manner, and create new Bubble for the text input """
        write("> ")
        txt = input()
        if(txt == ""):
            write(f"{ESC}1A")
            write(f"{ESC}2K")
            return ""
        for _ in range(len(txt) // self.consolewidth + 1):
            write(f"{ESC}1A")
            write(f"{ESC}2K")
        self.new(txt, 1)
        self.update()
        return txt
    
    def exit(self) -> None:
        """ Prints exit message """
        self.new("Bye!")
