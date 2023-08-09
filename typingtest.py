import curses
from curses import wrapper
import time
import random

def display_intro_screen(stdscr):
	stdscr.clear()
	stdscr.addstr("Welcome to the Typing Speed Trainer!")
	stdscr.addstr("\nPress any key to start!")
	stdscr.refresh()
	stdscr.getkey()

def display_typing_text(stdscr, target, current, typing_speed=0):
	stdscr.addstr(target)
	stdscr.addstr(1, 0, f"Typing Speed: {typing_speed} WPM")

	for i, char in enumerate(current):
		correct_char = target[i]
		text_color = curses.color_pair(1)
		if char != correct_char:
			text_color = curses.color_pair(2)

		stdscr.addstr(0, i, char, text_color)

def load_random_text():
	with open("text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip()

def typing_speed_test(stdscr):
	target_text = load_random_text()
	current_text = []
	typing_speed = 0
	start_time = time.time()
	stdscr.nodelay(True)

	while True:
		time_elapsed = max(time.time() - start_time, 1)
		typing_speed = round((len(current_text) / (time_elapsed / 60)) / 5)

		stdscr.clear()
		display_typing_text(stdscr, target_text, current_text, typing_speed)
		stdscr.refresh()

		if "".join(current_text) == target_text:
			stdscr.nodelay(False)
			break

		try:
			key = stdscr.getkey()
		except:
			continue

		if ord(key) == 27:
			break

		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)

def main(stdscr):
	curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	display_intro_screen(stdscr)
	while True:
		typing_speed_test(stdscr)
		stdscr.addstr(2, 0, "Text typing complete! Press any key to continue...")
		key = stdscr.getkey()
		
		if ord(key) == 27:
			break

wrapper(main)