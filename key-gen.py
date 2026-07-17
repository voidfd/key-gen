#!/usr/bin/env python3
import argparse
import os
import secrets
import shutil
import string
import sys
import time

APP_NAME = "key-gen"
VERSION = "1.1.0"
ASCII_ART = r"""
                                                                                               
                            * - : . .--::  =- @@- ##-@ +#  +  .: -- :                          
                              - -:: - -:: --- *=-+@.: %= :--  . -.  - *                        
                              .: .  : =::.-+*-.... .#-*@ - + %. -=                             
                           *  .  -:  -=--: * #*+-==++   : :  ..- --=-                          
                             * .- . - * --. @  .%* -:-.:-. @   ---    %                        
                             = - :@ --   .- @%    @-*:--=.. @.-  - -.   .                      
                         -     ::   .-. .:=. ::*: . : -- -   . :.- - -  :                      
                         .  -   :.  -:= #..:--- --=.--  . + .: ...    =                        
                           .. : .. -. -             :.= - - .:-.  =-     .                     
                         .  : ..::* :.     @@@@@@@@     :: .:-       - -::                     
                        -  .  -:  :.    @@@  @@@ @@@@@@    :   :.-= :   -                      
                        =  - :  .:   @@: @ @      @  @ @@    -.. -  .    :                     
                          - =:.-   @ @   @-@ @@@      @@@ @@    - -                            
                          . --   @ @   @@@@@    @@@@@    @+ @   :+  :=   -                     
                  @   . =-:-=  @    @@                 @@  @ @@    -.                          
                       * -    @ @@@      @           -+   @ @  @  - :-*                        
                     -= =    @@@         =      @  @        @ @ @       =:                     
                            @ @        @=-          :@@@@     @ @@ --   .                      
                    .--:.:  @   @@@@@@                           @   -                         
                     .  -. @  @:  @   @       -.                       - -.-                   
                      :       - . .%*@   @      -         .       @#                           
                   : .  @      @@..#    : +  #-:               -   @@ -  .                     
                 * .                  .+@@   - :.@= -    - -.%           -                     
                               =   @     @   =  -.@: -* ##            +                        
                      @          @@@@@%@+@ @+%*  #=  @:= =-                                    
                  @          =   @= @#%@%@@-%#@@@@-@#@ -=  -           @                       
                     @        @  @ --%=+--:@+==+ @ -==  :*-:*  +=*                             
                              @  +=+* #-+=--:-=#.:.-+  @-. =    @       @                      
                    .         *@ *==-. -*=:@:-*#- @-*--  - = .: -+                             
                    .         :% - +#+@ *=-@%-+#= :-:. *-+=:    =                              
                    .*         @@ :%-@=@#*+--=*.-*:* := --.- ##@                               
                                  *:-= -  - **-+-*-*=%+-    .                                  
                     =            -@ =@:@=*+* # @.= :  = -:=                                   
                     @             =-.-.*-+=#@#.=*% -%:*  -                                    
                                   .+ @-@.**@ @@ @ :+. * :-                                    
                      :             =:  @.@*: %= +---=* .=                                     
                                     #@ =  -+ @@ @ - - .-                                      
                                     . @@#=+=.@@ . : .--                                       
                                         =.# :@  -::*.   :                                     
                                        # .*:@@   -    .-           :@                         
                         @@           -     @@=@ +.  .-             +.@                        
                       @@ @#          .* -  @ :=                    .#-@@                      
                     @@@@  .               --  .@@@@@%.  -           - * :                     
              .=@@@@@.   @@-              @@@@@=      #  *@               @@                   
          +@@@%%  - +  =-       :        @-    @@@@@@@ : +            *-@  *@=@                
        *+  +- ++ %+@@@   ##             @@ ..=        @ @            - .   @+ +@ @            
       * == @  @:@    ::@                % @@@@@@@@@@@=               +@-%    *+*# @@@         
     * @ -+ -.. # +@*- .  @*            :@ - .        +-                   @:-@-    @ @=       
    *=. . *  -+         @.              %=@-+- .     %:                 @ @@  -  @*+  - @      
   #  %#% .#  +@          @             @-%   @+ -  @+               *          : @  @         
   #   %+  %  :            -          +.@@ @ @ = -:%                            =-     @-:%    
   %    +                  *        :    *-%@*#  =*=                                  -  *     
    =    *                          :       * =-                              : *:  .   @      
      @    @                      -          .:*                    =        :-#     %:    +   
        @                       -            -.                                       #        
        =+-=           #      #% +                                                        -    
 :           @             * #                                                      -     =    
          -%              -       @                                                @     %     
   -        # *          - . . @+                                          .             -     
 #**.#:#*%            %  =                                                              @      
 -                  :.                                                                         
                   %                                                                  @        
                                                                                               

""".strip("\n")
ASCII_SIGNATURE = "@voidfd"
MIN_LENGTH, MAX_LENGTH = 8, 32
MIN_COUNT, MAX_COUNT = 1, 75
LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGITS = string.digits
BASIC = "!@#$%_-"
SYMBOLS = "!@#$%^&*()-_=+[]{}:,.?"
ALL = LOWER + UPPER + DIGITS + SYMBOLS
MEMORABLE_WORDS = (
    "acorn amber anchor apple apron arctic arrow ash atlas autumn azure badge bamboo basil bayberry beacon",
    "beagle berry biscuit blossom bluebird brook button cactus candle canyon captain caramel cedar cherry",
    "cinder citrus cloud clover comet coral cricket crimson crown crystal daisy dandelion dawn desert",
    "diamond dragon drift eagle earth echo eclipse ember falcon feather fern field firefly flame forest",
    "fossil fox galaxy garden glacier golden harbor hazel honey horizon island ivy jade jasmine juniper",
    "kestrel kitten lagoon lantern lavender leaf lemon library lilac linen lion lotus maple marina meadow",
    "meteor midnight mint moon morning moss mountain nectar night north oak ocean olive opal orchid otter",
    "panda paper pebble pepper phoenix pine planet plum pocket pollen pond prairie prism pumpkin quartz",
    "quill rabbit rain raven reef river robin rose ruby saffron sail sandal sapphire scarlet sea shadow",
    "silver sky snow solar sparrow spice spring star stone summer sun sunrise sunset swift thunder tiger",
    "timber toast tomato topaz trail tulip valley velvet violet walnut water willow wind winter wolf wood",
    "wren yellow zephyr zinc alpine birch breeze bronze cabin cascade chestnut copper cove creek dawnfire",
    "dolphin evergreen finch frost granite grove heron iris kingfisher lake lark meadowlark mist orchard",
    "pearl pinecone ripple seaglass shore starlight tide wildflower woodland yarrow"
)
MEMORABLE_WORDS = tuple(" ".join(MEMORABLE_WORDS).split())
LEVELS = {
    1: ("Lowercase", "a-z only.", LOWER, [], 0, False),
    2: ("Mixed letters", "a-z and A-Z.", LOWER + UPPER, [], 0, False),
    3: ("Lowercase + digits", "a-z and 0-9.", LOWER + DIGITS, [], 0, False),
    4: ("Letters + digits", "a-z, A-Z, and 0-9.", LOWER + UPPER + DIGITS, [], 0, False),
    5: ("Basic symbols", "Letters, digits, and ! @ # $ % _ -.", LOWER + UPPER + DIGITS + BASIC, [], 0, False),
    6: ("Full symbols", "Letters, digits, and a broad safe-symbol set.", ALL, [], 0, False),
    7: ("Four classes", "Full set; guarantees 1 lowercase, uppercase, digit, and symbol.", ALL, [LOWER, UPPER, DIGITS, SYMBOLS], 0, False),
    8: ("Balanced", "Full set; guarantees 2 of each of the 4 character classes.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 0, False),
    9: ("Balanced + varied", "Level 8 plus at least 8 distinct characters.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 8, False),
    10: ("Balanced + no doubles", "Level 9 and never repeats a character immediately.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 8, True),
    11: ("Strong 10", "Four classes (2 each), 10+ distinct characters, no adjacent repeats.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 10, True),
    12: ("Strong 11", "Four classes (2 each), 11+ distinct characters, no adjacent repeats.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 11, True),
    13: ("Strong 12", "Four classes (2 each), 12+ distinct characters, no adjacent repeats.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 12, True),
    14: ("Strong 13", "Four classes (2 each), 13+ distinct characters, no adjacent repeats.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 13, True),
    15: ("Strong 14", "Four classes (2 each), 14+ distinct characters, no adjacent repeats.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 14, True),
    16: ("Strong 15", "Four classes (2 each), 15+ distinct characters, no adjacent repeats.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 15, True),
    17: ("Strong 16", "Four classes (2 each), 16+ distinct characters, no adjacent repeats.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 16, True),
    18: ("Strong 17", "Four classes (2 each), 17+ distinct characters, no adjacent repeats.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 17, True),
    19: ("Strong 18", "Four classes (2 each), 18+ distinct characters, no adjacent repeats.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 18, True),
    20: ("Strong 19", "Four classes (2 each), 19+ distinct characters, no adjacent repeats.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 19, True),
    21: ("Strong 20", "Four classes (2 each), 20+ distinct characters, no adjacent repeats.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 20, True),
    22: ("Strong 21", "Four classes (2 each), 21+ distinct characters, no adjacent repeats.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 21, True),
    23: ("Strong 22", "Four classes (2 each), 22+ distinct characters, no adjacent repeats.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 22, True),
    24: ("Strong 23", "Four classes (2 each), 23+ distinct characters, no adjacent repeats.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 23, True),
    25: ("Maximum", "Four classes (2 each), 24+ distinct characters, no adjacent repeats.", ALL, [LOWER, LOWER, UPPER, UPPER, DIGITS, DIGITS, SYMBOLS, SYMBOLS], 24, True),
}

USE_COLOR = True
RESET = "\033[0m"
WHITE = "\033[97m"
GREY = "\033[90m"
RED = "\033[91m"
BLACK_BG = "\033[40m"
BOLD = "\033[1m"


def color(text, code):
    return f"{code}{text}{RESET}" if USE_COLOR else text


def terminal_width():
    return max(40, shutil.get_terminal_size(fallback=(80, 24)).columns)


def center(text="", code=WHITE):
    width = terminal_width()
    # Never trim passwords or ASCII artwork: overlong text is printed unchanged.
    padding = max(0, (width - len(text)) // 2)
    print(" " * padding + color(text, code))


def clear_screen():
    if sys.stdout.isatty():
        print("\033[2J\033[H", end="")


def header(clear=True):
    if clear:
        clear_screen()
    if USE_COLOR:
        print(BLACK_BG, end="")
    for line in ASCII_ART.splitlines() or [""]:
        center(line, RED)
    center(ASCII_SIGNATURE, GREY)
    center("─" * min(58, terminal_width() - 4), GREY)


def abort_if_exit(value):
    if value.strip().lower() == "/exit":
        raise KeyboardInterrupt


def ask(prompt):
    center(prompt, WHITE)
    try:
        value = input(color(" " * max(0, (terminal_width() - 3) // 2) + "> ", RED))
    except EOFError:
        raise KeyboardInterrupt
    abort_if_exit(value)
    return value.strip()


def ask_int(label, minimum, maximum):
    while True:
        value = ask(f"{label} [{minimum}-{maximum}]  (/exit to quit)")
        try:
            number = int(value)
        except ValueError:
            center("Please enter a whole number.", RED)
            continue
        if minimum <= number <= maximum:
            return number
        center(f"Choose a value from {minimum} to {maximum}.", RED)


def random_character(pool, previous, no_adjacent):
    choices = pool if not no_adjacent else pool.replace(previous, "")
    return secrets.choice(choices)


def generate_password(length, level):
    _, _, charset, required, unique_min, no_adjacent = LEVELS[level]
    if length < len(required):
        raise ValueError(f"Level {level} needs a password length of at least {len(required)}.")
    if unique_min > length:
        raise ValueError(f"Level {level} needs a password length of at least {unique_min}.")
    for _ in range(10000):
        chars = [secrets.choice(pool) for pool in required]
        while len(chars) < length:
            chars.append(random_character(charset, chars[-1] if chars else "", no_adjacent))
        secrets.SystemRandom().shuffle(chars)
        candidate = "".join(chars)
        if no_adjacent and any(a == b for a, b in zip(candidate, candidate[1:])):
            continue
        if len(set(candidate)) < unique_min:
            continue
        return candidate
    raise RuntimeError("Could not satisfy this policy; choose a longer password or lower level.")


def generate_memorable_key(word_count, separator):
    return separator.join(secrets.SystemRandom().sample(MEMORABLE_WORDS, word_count))


def loading_screen(label):
    header()
    center(label, WHITE)
    for filled in range(16):
        bar = "#" * min(15, filled) + "." * (15 - min(15, filled))
        center(f"[{bar}] {min(100, filled * 7):3d}%", RED)
        if filled < 15:
            time.sleep(0.035)


def level_table():
    lines = [
        "Password levels",
        "Level  Name                Policy",
        "─────  ──────────────────  ─────────────────────────────────────────────────────",
    ]
    for number, (name, policy, _, _, _, _) in LEVELS.items():
        lines.append(f"{number:>5}  {name:<18}  {policy}")
    lines += [
        "",
        "All passwords use Python's secrets module (cryptographically secure randomness).",
        "Levels 11-25 require a length at least equal to their distinct-character number.",
    ]
    return "\n".join(lines)


def interactive():
    header()
    center("Secure password and memorable-key generator", BOLD + WHITE)
    center("Press Ctrl+C or type /exit at any prompt to leave.", GREY)
    center("Use key-gen --help to view all 25 password-level policies.", GREY)
    print()
    mode = ask_int("Choose mode: 1 = password   2 = memorable key", 1, 2)

    if mode == 1:
        length = ask_int("Password length", MIN_LENGTH, MAX_LENGTH)
        level = ask_int("Security level", 1, 25)
        count = ask_int("Number of passwords", MIN_COUNT, MAX_COUNT)
        required = max(len(LEVELS[level][3]), LEVELS[level][4])
        while length < required:
            center(f"Level {level} requires a length of at least {required}.", RED)
            length = ask_int("Password length", required, MAX_LENGTH)

        loading_screen("Generating secure passwords…")
        print()
        title, policy, *_ = LEVELS[level]
        center(f"{count} password(s) • {length} characters • Level {level}: {title}", GREY)
        center(policy, GREY)
        print()
        for index in range(1, count + 1):
            center(f"{index:02d}.  {generate_password(length, level)}", WHITE)
    else:
        word_count = ask_int("Words per memorable key", 4, 12)
        separator_choice = ask_int("Separator: 1 = hyphen   2 = dot   3 = underscore", 1, 3)
        count = ask_int("Number of memorable keys", MIN_COUNT, MAX_COUNT)
        separator = {1: "-", 2: ".", 3: "_"}[separator_choice]

        loading_screen("Generating memorable keys…")
        print()
        center(f"{count} memorable key(s) • {word_count} random words • separator: {separator}", GREY)
        if word_count < 8:
            center("Tip: use 8+ random words for important accounts; fewer words are easier to guess.", RED)
        else:
            center("Randomly selected words; 8+ words is recommended for important accounts.", GREY)
        print()
        for index in range(1, count + 1):
            center(f"{index:02d}.  {generate_memorable_key(word_count, separator)}", WHITE)
    print()
    center("Keep these private. Anyone with a displayed password or key can use it.", RED)


def main():
    global USE_COLOR
    if sys.platform != "linux":
        print("key-gen is intended for Linux.", file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description="Interactive, cryptographically secure Linux password and memorable-key generator.",
        epilog=level_table(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"{APP_NAME} {VERSION}")
    parser.add_argument("--no-color", action="store_true", help="disable ANSI terminal colors")
    args = parser.parse_args()
    USE_COLOR = not args.no_color and sys.stdout.isatty()
    try:
        interactive()
    except KeyboardInterrupt:
        print()
        center("Goodbye.", GREY)
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
