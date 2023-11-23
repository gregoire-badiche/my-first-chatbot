ESCAPE = "\u001b["

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
    write(f"{ESCAPE}{code}")

def resetcolors():
    setcode("39m")
    setcode("49m")

def createselector(choices: list[str]) -> int:
    pass

setcode(COLORS_FG["blue"])
write("Hello ")
setcode(COLORS_FG['magenta'])
write('World')
setcode(COLORS_FG['yellow'])
write('!')
resetcolors()
write('\n')