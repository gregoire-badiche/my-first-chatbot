from os import get_terminal_size
from threading import Thread

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

def write(text):
    print(text, end='')

def setcode(code):
    write(f"{ESC}{code}")

def resetcolors():
    setcode("39m")
    setcode("49m")

def clear():
    write("\033c")

class Bubble:
    def __init__(self, width:int, orientation:bool, text:str = "", error:bool = 0) -> None:
        self.width = width
        self.error = error
        self.text = text
        self.parsedtext = []
        self.orientation = orientation
        self.parse()
    
    def draw(self, padding:int = 0, consolewidth:int = 0) -> None:
        consolewidth = consolewidth if consolewidth else get_terminal_size()[0]
        c = lambda: (setcode(COLORS_FG["red"]) if self.error else setcode(COLORS_FG["cyan"])) if self.orientation else (setcode(COLORS_FG["red"]) if self.error else setcode(COLORS_FG["green"]))
        d = lambda: setcode("39m") # Reset FG color
        if(len(self.parsedtext) == 1):
            w = len(self.parsedtext[0].strip()) + 2
        else:
            w = max([len(l.strip()) for l in self.parsedtext]) + 2
        pad = " " * padding if not(self.orientation) else " " * (consolewidth - w - padding - 2)
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
        self.parsedtext = []
        width = self.width - 4 # Removes border and padding
        phrases = self.text.split('\n')
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
    def __init__(self) -> None:
        self.bubbles:list[Bubble] = []
        self.consolewidth = get_terminal_size()[0]
        self.width = int(self.consolewidth * 2 / 3)
        self.padding = 3
        clear()
    
    def update(self, *args) -> None:
        clear()
        self.consolewidth = get_terminal_size()[0]
        self.width = int(self.consolewidth * 2 / 3)

        for bubble in self.bubbles:
            bubble.resize(self.width, self.padding, self.consolewidth)
    
    def new(self, text:str, orientation:bool = 0, error:bool = 0) -> None:
        self.bubbles.append(Bubble(self.width, orientation, text, error))
        self.bubbles[-1].draw(self.padding, self.consolewidth)
    
    def handle(self) -> None:
        write("> ")
        txt = input()
        for _ in range(len(txt) // self.consolewidth + 1):
            write(f"{ESC}1A")
            write(f"{ESC}2K")
        self.new(txt, 1)
        self.update()
        return txt
    
    def exit(self):
        self.new("Bye!")
