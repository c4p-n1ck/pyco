#!/usr/bin/env python3

from utils import (
    getch,
    printable,
    StringIO,
    sys
);

# TODO: Using commented stuff for recovery feature.

class vTee(object):
    def __init__(self, name, mode):
        # self.file = open(name, mode)
        self.content = StringIO()
        self.stdout = sys.stdout
        sys.stdout = self
    def __del__(self):
        sys.stdout = self.stdout
        # self.file.close()
        self.content.close()
    def write(self, data):
        # self.file.write(data)
        self.stdout.write(data)
        if data != 'Enter filename: ':
            self.content.write(data)
    def flush(self):
        self.stdout.flush()
        self.content.flush()
        # self.file.flush()
    def getvalue(self):
        return self.content.getvalue()

def wprint(*args, **kwargs):
    with open('log.txt', 'a') as f:
        f.write(args[0])
    print(*args, **kwargs)

print("pyco - Press Alt + Enter to exit: ", end='\n'*2);

sys.stdout = vTee('self.stdout', 'w')

ESC = 0; ARR = 0
inp = '';
while 1:
    inp = getch()
    if inp == '\x7f':
        print('\b \b', end='', flush=True)
    elif inp == '\r':
        print('\n', end='', flush=True)
        if ESC:
            # print('\x04')
            filename = input('Enter filename: ')
            with open(filename, 'w') as f:
                f.write( sys.stdout.getvalue().encode().decode('unicode-escape') )
            break
    elif inp == '\x1b':
        ESC = 1
    elif inp == '[' and ESC:
        ESC = 0; ARR = 1
    elif inp in ('A', 'B', 'C', 'D') and ARR:
        # Arrow keys (A=up, B=down, C=right, D=left)
        print(f'\x1b[{inp}', end='', flush=True)
        ARR = 0
    elif inp == ';' and ARR:
        inp = getch()
    elif inp.isdigit() and ARR:
        if inp == '3':
            # Delete
            if getch() == '~':
                print(' \b \b ', end='', flush=True)
        elif inp == '1':
            if getch() == ';':
                # Ctrl/Alt + Arrow keys
                times = getch() # Number of times to repeat [3, 5, 7]
                key = getch() # Key to repeat [A, B, C, D]
                for _ in range(int(times)):
                    print(f'\x1b[{key}', end='', flush=True)
        ARR = 0
    elif inp in printable:
        if not ARR:
            print(inp, end='', flush=True)
    elif inp == '\x03':
        raise KeyboardInterrupt("Keyboard Interrupt in pyco")
    elif inp == '\x04':
        raise EOFError("EOF in pyco")
    else:
        print('\nTODO:', repr(inp))

