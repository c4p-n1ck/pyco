if __import__('sys').platform == "linux":
	import tty, termios, sys
	def getch():
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch
else:
	import msvcrt
	def getch():
		return msvcrt.getch()
