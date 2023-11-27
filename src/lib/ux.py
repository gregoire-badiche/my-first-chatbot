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

class Bubble():
    def __init__(self, width:int, orientation:bool, text:str = "") -> None:
        self.width = width
        self.text = text
        self.parsedtext = []
        self.orientation = orientation
        self.parsetext()
    
    def draw(self, consolewidth:int = 0) -> None:
        if(len(self.parsedtext) == 1):
            w = len(self.parsedtext[0].strip()) + 4
        else:
            w = self.width
        write("╭")
        write("─" * (w - 2))
        write("╮")
        write('\n')
        for line in self.parsedtext:
            l = line.strip()
            write('│ ')
            write(l)
            write(" " * (w - 4 -len(l)))
            write(' │\n')
        if(self.orientation):
            write("╰")
            write("─" * (w - 2))
            write("┴")
        else:
            write("┴")
            write("─" * (w - 2))
            write("╯")
        write('\n')
    
    def parsetext(self) -> None:
        width = self.width - 4 # Removes border and padding
        words = self.text.split(' ')
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
    
    def resize(self, width, consolewidth:int = 0):
        self.width = width
        self.parsetext()
        self.draw(consolewidth)

bubble = Bubble(20, 0, "Hello!")
bubble.draw()
b2 = Bubble(20, 0, "How may I help you today?")
b2.draw()
