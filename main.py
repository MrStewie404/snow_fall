from time import sleep
from random import randint
from os import system
import sys

try:
    from fcntl import ioctl
    from termios import TIOCGWINSZ
    from struct import unpack
    
    if "full" in sys.argv:
        Y_MAP, X_MAP = unpack('hh', ioctl(0, TIOCGWINSZ, '1234'))
        Y_MAP-=1
        X_MAP-=1
    else:
        X_MAP, Y_MAP = [20, 20]
except:
    X_MAP, Y_MAP = [20, 20]


time_sleep = None
if len(sys.argv) == 4:
    _, X_MAP, Y_MAP, time_sleep = sys.argv
    X_MAP, Y_MAP, time_sleep = int(X_MAP), int(Y_MAP), float(time_sleep)

if len(sys.argv) == 3:
    _, X_MAP, Y_MAP = sys.argv
    X_MAP, Y_MAP = int(X_MAP), int(Y_MAP)

# if len(sys.argv) == 2:
#     _, time_sleep = sys.argv
#     time_sleep = float(time_sleep)
# print(len(sys.argv))

# MAPPING = {0: " ", 1: "⠿", 2: "⠐", 3: "⠴", 4:"⠦", 5: "⠐", 6: "⠉"}
MAPPING = {i: "█" for i in range(0, 7)}
MAPPING[0] = " "

def place_on_map(map, place):
    """
    place = [\n
    X, Y | element\n
    [3,2,2],\n
    [1,1,1],\n
    . . .]
    """

    # Проходим по высоте карты. 
    # Если на n высоте есть элемент, 
    # добираемся до его позиции и вставляем его в карту
    for element in place:
        for y in range(Y_MAP):
            if y == element[1]:
                for x in range(X_MAP):
                    if x == element[0]:
                        map[y][x] = element[2]
    return map

def render(map):
    # system('clear')
    screen = ""
    for line in map:
        screen += "".join([MAPPING[place] for place in line]) + "|\n"
    screen += f"{'-' * int(X_MAP)}"
    print(screen)
    
    sleep(0.025 if time_sleep is None else time_sleep)

def start():
    map = [[0 for x in range(X_MAP)] for y in range(Y_MAP)]
    map_for_place = [[randint(0, X_MAP-1), 
                    randint(0, int(Y_MAP)-1),
                    1] for i in range(int((X_MAP*Y_MAP)/2))]

    place_on_map(map, map_for_place)
    render(map)
    sleep(1)
    return map

map = start()

while True:
    restart = 0
    for y in range(Y_MAP-1):
        for x in range(X_MAP):
            if (map[y][x] > 0):
                if (map[y+1][x] == 0):
                    # comment that for more
                    # map[y][x] = 0
                    # map[y+1][x] = 1
                    # restart = 1
                    ...

                else: 
                    if (randint(0, 1) == 0):
                        if (map[y+1][x-1] == 0) and (y < Y_MAP):
                            map[y][x] = 0
                            map[y+1][x-1] = 1
                            restart = 1

                    elif (x < X_MAP-1) and (y < Y_MAP):
                        if (map[y+1][x+1] == 0):
                            map[y][x] = 0
                            map[y+1][x+1] = 1
                            restart = 1

                    else:
                        map[y][x] = 0
                        map[y+1][x-1] = 1
                        restart = 1

                # if (0 < y < Y_MAP-1) and (0 < x < X_MAP-1) and (map[y][x] > 0):
                #     if      (map[y-1][x-1] == 0) and (map[y-1][x] == 0) and (map[y-1][x+1] == 0) \
                #         and (map[y][x-1] == 0)   and                        (map[y][x+1] == 0)  \
                #         and (map[y+1][x-1] == 0) and (map[y+1][x] == 0) and (map[y+1][x+1] == 0): 
                #         map[y][x] = 2 # .

                #     elif    (map[y-1][x-1] == 0) \
                #         and (map[y][x-1] == 0) \
                #         and (map[y+1][x-1] == 0) and (map[y+1][x] == 0) and (map[y+1][x+1] == 0): 
                #         map[y][x] = 3 # \

                #     elif                                                    (map[y-1][x+1] == 0) \
                #                                  and                        (map[y][x+1] == 0)  \
                #         and (map[y+1][x-1] == 0) and (map[y+1][x] == 0) and (map[y+1][x+1] == 0): 
                #         map[y][x] = 4 # /

                #     elif    (map[y-1][x-1] == 0) and (map[y-1][x] == 0) and (map[y-1][x+1] == 0) \
                #         and (map[y][x-1] == 0) \
                #         and (map[y+1][x-1] == 0): 
                #         map[y][x] = 4 # /

                #     elif    (map[y-1][x-1] == 0) and (map[y-1][x] == 0) and (map[y-1][x+1] == 0) \
                #                                                         and (map[y][x+1] == 0)  \
                #                                                         and (map[y+1][x+1] == 0): 
                #         map[y][x] = 5 # .

                #     elif\
                #         \
                #             (map[y+1][x-1] == 0) and (map[y+1][x] == 0) and (map[y+1][x+1] == 0): 
                #         map[y][x] = 6 # -

        y-=2

    render(map)
    if restart == 0:
        for y in range(Y_MAP):
            for x in range(X_MAP):
                if map[y][x] > 0:
                    map[y][x] = 0
            time_sleep = 0.01
            if y % 2 == 0:
                render(map)
        time_sleep = None
        map = start()