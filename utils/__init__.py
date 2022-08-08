from .getch import getch
from string import printable
import sys, os
from io import StringIO

printable = printable.replace('\r', '')
path = os.path
