import sys
import tty
from typing import NamedTuple


class Stem(NamedTuple):
    keyword: str
    description: str
    completions: list = []


shrub = [Stem('reboot', 'Reboot the system', [Stem('now', 'Reboot the system without confirmation')]),
         Stem('set', 'Set operational options'),
         Stem('show', 'Show system information', [Stem('date', 'Show system time and date'),
                                                      Stem('system', 'Show system information')])]


def prompt(command_prompt: str) -> None:
    input = ''
    tty.setraw(sys.stdin)
    sys.stdout.write(command_prompt)
    sys.stdout.flush()

    stems = shrub

    while True:
        char = ord(sys.stdin.read(1))
        if char == 3:  # CTRL-C
            break
        elif char == 9:  # TAB
            count = 0
            print_line = True
            for stem in stems:
                if (stem.keyword.startswith(input)):
                    count += 1
                    # if print_line is True:
                    #     print()
                    #     print_line = False
                    # sys.stdout.write(u"\u001b[1000D")
                    # sys.stdout.flush()
                    # print('%s - %s' % (stem.keyword, stem.description))
            sys.stdout.write(u"\u001b[1000D")
            print("\n%d possible completion(s)" % count)
            sys.stdout.write(u"\u001b[1000D")
            sys.stdout.write(command_prompt + input)
            sys.stdout.flush()

        elif char in {10, 13}:  # LF or CR
            break
        elif 32 <= char <= 126:  # ASCII printable character
            if char == 32:
                pass  # record path
            input += chr(char)
            sys.stdout.write(u"\u001b[1000D")
            sys.stdout.write(command_prompt + input)
            sys.stdout.flush()
        elif char == 127:  # BACKSPACE
            if len(input) > 0:
                input = input[:-1]
                sys.stdout.write(u"\u001b[1000D")  # Move all the way left
                sys.stdout.write(u"\u001b[0K")  # Clear the line
                sys.stdout.write(command_prompt + input)
                sys.stdout.flush()
        else:
            pass


# for stem in shrub:
#     print(stem.keyword, stem.description)
#
# sys.exit(0)

prompt("> ")
