#!/usr/bin/env python

from typing import NamedTuple
import os
import sys
import time
import tty
import yaml


def loading():
    print("Loading...")
    for i in range(0, 100):
        time.sleep(0.1)
        sys.stdout.write(u"\u001b[1000D" + str(i + 1) + "%")
        sys.stdout.flush()
    print

def command_line():
    tty.setraw(sys.stdin)
    while True:
        sys.stdout.write('# ')
        sys.stdout.flush()
        char = sys.stdin.read(1)
        if ord(char) == 3: # CTRL-C
            break;
        print(ord(char))
        sys.stdout.write(u"\u001b[1000D") # Move all the way left

command_line()

# loading()

print(yaml.__version__)
sys.exit(1)

from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter

completer = NestedCompleter.from_nested_dict({
    'show': {
        'version': None,
        'clock': None,
        'ip': {
            'interface': {'brief'}
        },
    },
    'exit': None,
})

text = prompt('# ', completer=completer)
print('You said: %s' % text)
