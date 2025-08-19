from colored import Fore, Style
from time import sleep
from random import choice

RESET = Style.reset
BOLD = Style.BOLD


def setup(tube: str) -> None:
    # NOTE:
    # These are the fiber colors
    BLUE = f"{Fore.rgb(83, 83, 255)}{BOLD}BLUE{RESET}"
    ORANGE = f"{Fore.rgb(255, 128, 0)}{BOLD}ORANGE{RESET}"
    GREEN = f"{Fore.rgb(0, 204, 0)}{BOLD}GREEN{RESET}"
    BROWN = f"{Fore.rgb(128, 64, 0)}{BOLD}BROWN{RESET}"
    SLATE = f"{Fore.rgb(128, 128, 128)}{BOLD}SLATE{RESET}"
    WHITE = f"{Fore.rgb(255, 255, 255)}{BOLD}WHITE{RESET}"
    RED = f"{Fore.rgb(255, 0, 0)}{BOLD}RED{RESET}"
    BLACK = f"{Fore.rgb(100, 100, 100)}BLACK{RESET}"
    YELLOW = f"{Fore.rgb(255, 255, 0)}{BOLD}YELLOW{RESET}"
    VIOLET = f"{Fore.rgb(128, 0, 255)}{BOLD}VIOLET{RESET}"
    ROSE = f"{Fore.rgb(255, 128, 192)}{BOLD}ROSE{RESET}"
    AQUA = f"{Fore.rgb(0, 255, 255)}{BOLD}AQUA{RESET}"
    # NOTE:
    # These are the fiber colors that get printed out
    _1 = f"{BLUE} {BLUE}"
    _2 = f"{BLUE} {ORANGE}"
    _3 = f"{BLUE} {GREEN}"
    _4 = f"{BLUE} {BROWN}"
    _5 = f"{BLUE} {SLATE}"
    _6 = f"{BLUE} {WHITE}"
    _7 = f"{BLUE} {RED}"
    _8 = f"{BLUE} {BLACK}"
    _9 = f"{BLUE} {YELLOW}"
    _10 = f"{BLUE} {VIOLET}"
    _11 = f"{BLUE} {ROSE}"
    _12 = f"{BLUE} {AQUA}"
    _13 = f"{ORANGE} {BLUE}"
    _14 = f"{ORANGE} {ORANGE}"
    _15 = f"{ORANGE} {GREEN}"
    _16 = f"{ORANGE} {BROWN}"
    _17 = f"{ORANGE} {SLATE}"
    _18 = f"{ORANGE} {WHITE}"
    _19 = f"{ORANGE} {RED}"
    _20 = f"{ORANGE} {BLACK}"
    _21 = f"{ORANGE} {YELLOW}"
    _22 = f"{ORANGE} {VIOLET}"
    _23 = f"{ORANGE} {ROSE}"
    _24 = f"{ORANGE} {AQUA}"
    _25 = f"{GREEN} {BLUE}"
    _26 = f"{GREEN} {ORANGE}"
    _27 = f"{GREEN} {GREEN}"
    _28 = f"{GREEN} {BROWN}"
    _29 = f"{GREEN} {SLATE}"
    _30 = f"{GREEN} {WHITE}"
    _31 = f"{GREEN} {RED}"
    _32 = f"{GREEN} {BLACK}"
    _33 = f"{GREEN} {YELLOW}"
    _34 = f"{GREEN} {VIOLET}"
    _35 = f"{GREEN} {ROSE}"
    _36 = f"{GREEN} {AQUA}"
    blue_blue = 1
    blue_orange = 2
    blue_green = 3
    blue_brown = 4
    blue_slate = 5
    blue_white = 6
    blue_red = 7
    blue_black = 8
    blue_yellow = 9
    blue_violet = 10
    blue_rose = 11
    blue_aqua = 12
    orange_blue = 13
    orange_orange = 14
    orange_green = 15
    orange_brown = 16
    orange_slate = 17
    orange_white = 18
    orange_red = 19
    orange_black = 20
    orange_yellow = 21
    orange_violet = 22
    orange_rose = 23
    orange_aqua = 24
    green_blue = 25
    green_orange = 26
    green_green = 27
    green_brown = 28
    green_slate = 29
    green_white = 30
    green_red = 31
    green_black = 32
    green_yellow = 33
    green_violet = 34
    green_rose = 35
    green_aqua = 36
    blue = [_1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12]
    orange = [_13, _14, _15, _16, _17, _18, _19, _20, _21, _22, _23, _24]
    green = [_25, _26, _27, _28, _29, _30, _31, _32, _33, _34, _35, _36]
    blue_fiber = [
        blue_blue,
        blue_orange,
        blue_green,
        blue_brown,
        blue_slate,
        blue_white,
        blue_red,
        blue_black,
        blue_yellow,
        blue_violet,
        blue_rose,
        blue_aqua,
    ]
    orange_fiber = [
        orange_blue,
        orange_orange,
        orange_green,
        orange_brown,
        orange_slate,
        orange_white,
        orange_red,
        orange_black,
        orange_yellow,
        orange_violet,
        orange_rose,
        orange_aqua,
    ]
    green_fiber = [
        green_blue,
        green_orange,
        green_green,
        green_brown,
        green_slate,
        green_white,
        green_red,
        green_black,
        green_yellow,
        green_violet,
        green_rose,
        green_aqua,
    ]
    blue_tube = {color: fiber for color, fiber in zip(blue, blue_fiber)}
    orange_tube = {color: fiber for color, fiber in zip(orange, orange_fiber)}
    green_tube = {color: fiber for color, fiber in zip(green, green_fiber)}
    # brown_tube = {color: fiber for color, fiber in zip(brown, brown_fiber)}
    # slate_tube = {color: fiber for color, fiber in zip(slate, slate_fiber)}
    # white_tube = {color: fiber for color, fiber in zip(white, white_fiber)}
    # red_tube = {color: fiber for color, fiber in zip(red, red_fiber)}
    # black_tube = {color: fiber for color, fiber in zip(black, black_fiber)}
    # yellow_tube = {color: fiber for color, fiber in zip(yellow, yellow_fiber)}
    # violet_tube = {color: fiber for color, fiber in zip(violet, violet_fiber)}
    # rose_tube = {color: fiber for color, fiber in zip(rose, rose_fiber)}
    # aqua_tube = {color: fiber for color, fiber in zip(aqua, aqua_fiber)}
    if tube == "blue":
        return blue, blue_tube
    elif tube == "orange":
        return orange, orange_tube
    elif tube == "green":
        return green, green_tube
    # elif tube == 'brown':
    #    return brown, brown_tube
    # elif tube == 'slate':
    #    return slate, slate_tube
    # elif tube == 'white':
    #    return white, white_tube
    # elif tube == 'red':
    #    return red, red_tube
    # elif tube == 'black':
    #    return black, black_tube
    # elif tube == 'yellow':
    #    return yellow, yellow_tube
    # elif tube == 'violet':
    #    return violet, violet_tube
    # elif tube == 'rose':
    #    return rose, rose_tube
    # elif tube == 'aqua':
    #    return aqua, aqua_tube


def main():
    colors = [
        "blue",
        "orange",
        "green",
        "brown",
        "slate",
        "white",
        "red",
        "black",
        "yellow",
        "violet",
        "rose",
        "aqua",
    ]
    color_practice = input("Choose a color tube to practice on: ")
    sleep(1)
    if isinstance(color_practice, str) is False:
        print("Please use a color from the 12 fiber colors, ex: blue")
        sleep(1)
        main()
    elif color_practice not in colors:
        print("Please use a color from the 12 fiber colors, ex: blue")
    fiber_num, tube = setup(color_practice)
    count = 0
    while count < 10:
        question = choice(fiber_num)
        print(question)
        guess = int(input("Fiber: "))
        if guess == tube[question]:
            print(f"{Fore.rgb(0, 204, 0)}{BOLD}CORRECT!!{RESET}\n")
        else:
            print(f"{Fore.rgb(255, 0, 0)}{BOLD}WRONG!!{RESET}\n")
        sleep(1)
        count += 1


if __name__ == "__main__":
    main()
