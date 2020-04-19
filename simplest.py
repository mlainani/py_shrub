import sys
import tty
from typing import List, NamedTuple, Optional


class Stem(NamedTuple):
    keyword: str
    description: str
    stems: List['Stem'] = []


class Token(NamedTuple):
    parameter: Optional[str]
    stem: Stem = None


shrub = [Stem('reboot', 'Reboot the system', [Stem('now', 'Reboot the system without confirmation')]),
         Stem('set', 'Set operational options'),
         Stem('show', 'Show system information', [Stem('date', 'Show system time and date'),
                                                  Stem('system', 'Show system information')])]


def print_raw(line: str) -> None:
    sys.stdout.write('\u001b[1000D')  # Move all the way left
    sys.stdout.write(line)
    sys.stdout.flush()


# Two different orthogonal states must be maintained for a command. The first one is_valid indicates if the ordered
# sequence of tokens as entered by user is valid. The second one is_complete indicates if the same sequence
# represents an executable command.


def prompt(command_prompt: str) -> None:
    # command_str: str = ''  # command line as displayed
    keyword_str: str = ''  # current keyword as displayed
    command_tokens: List['Stem'] = []  # list of Token object instances comprising the command

    stems: List['Stem'] = shrub

    is_keyword_complete: bool = False

    is_command_valid: bool = False
    is_command_complete: bool = False

    tty.setraw(sys.stdin)

    print_raw(command_prompt)

    while True:
        char = ord(sys.stdin.read(1))
        if char == 3:  # CTRL-C
            break
        elif char == 9:  # TAB
            possible_completions: List['Stem'] = []
            print_line = True
            for stem in stems:
                if stem.keyword.startswith(keyword_str):
                    possible_completions.append(stem)  # record possible completions
                    if print_line is True:
                        print()
                        print_line = False
                    sys.stdout.write('\u001b[1000D')
                    sys.stdout.flush()
                    print('%s - %s' % (stem.keyword, stem.description))

            num_completions = len(possible_completions)

            if num_completions == 1:
                command_tokens.append(possible_completions[0])
                command_str = ' '.join([token.keyword for token in command_tokens]) + ' '
                stems = possible_completions[0].stems
                keyword_str = ''
                print_raw(command_prompt + command_str)
                # print(completions)
                # sys.exit(0)
            else:
                sys.stdout.write('\u001b[1000D')
                print('\n{} possible completion(s)'.format(num_completions))
                sys.stdout.write('\u001b[1000D')
                sys.stdout.write(command_prompt + ' '.join([token.keyword for token in command_tokens]) + keyword_str)
                sys.stdout.flush()

        elif char in {10, 13}:  # LF or CR
            if is_command_complete is True:
                break

        elif char == 32:  # SP
            command_str = ' '.join([token.keyword for token in command_tokens])
            if len(command_str) == 0:
                continue
            else:
                command_str += ' '

            # token = command_str.split()[-1]  # last command token
            # if token in stems:
            #     command_tokens.append(Token(token, None))  # TODO: parameter handling
            #     for completion in completions:
            #         command_str += chr(char)
            # TODO: update 'completions'
            print_raw(command_prompt + command_str)

        elif 33 <= char <= 126:  # ASCII printable character other than SP - TODO: select relevant subset
            keyword_str += chr(char)
            command_str = ' '.join([token.keyword for token in command_tokens])
            if len(command_str) == 0:
                command_str += keyword_str
            else:
                command_str += ' ' + keyword_str
            for stem in stems:
                if keyword_str is stem.keyword:
                    is_keyword_complete = True
                    command_tokens.append(stem)
                    is_command_valid = True
                    print_raw(command_prompt + command_str)
                    break
            print_raw(command_prompt + command_str)

        elif char == 127:  # BACKSPACE

            if len(keyword_str) > 0:
                keyword_str = keyword_str[:-1]  # NOTE: empty keyword is a valid value
                if is_keyword_complete is True:
                    is_keyword_complete = False
                    is_command_valid = False
                    command_tokens.pop()
                    # TODO: update 'stems'
                    if not command_tokens:
                        stems = shrub
                    else:
                        stems = command_tokens[-1].stems

                command_str = ' '.join([token.keyword for token in command_tokens])
                if len(command_str) == 0:
                    command_str += keyword_str
                else:
                    command_str += ' ' + keyword_str

                sys.stdout.write('\u001b[1000D')  # Move all the way left
                sys.stdout.write('\u001b[0K')  # Clear the line
                sys.stdout.write(command_prompt + command_str)
                sys.stdout.flush()

        else:
            pass


# for stem in shrub:
#     print(stem.keyword, stem.description)
#
# sys.exit(0)

prompt('> ')
