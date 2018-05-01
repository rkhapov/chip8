#!/usr/bin/env python3
import curses
from virtualmachine.consolescreen import ConsoleScreen
from virtualmachine.consolekeyboard import ConsoleKeyboard
from virtualmachine.interpreter import Interpreter
import sys
import logging


def main(stdscr):
    logging.basicConfig(filename='log.log', level=logging.DEBUG)

    if curses.LINES < 32 or curses.COLS < 64:
        stdscr.addstr(0, 0, 'Too little display')
        stdscr.refresh()
        stdscr.getch()
        return

    if len(sys.argv) < 2:
        stdscr.addstr(0, 0, 'Expected program file name')
        stdscr.refresh()
        stdscr.getch()
        return

    screen = ConsoleScreen(stdscr)
    keyboard = ConsoleKeyboard(screen)
    interpreter = Interpreter(screen, keyboard)

    interpreter.load_program(sys.argv[1])
    # interpreter.load_program('./games/MAZE')
    interpreter.run_program()


if __name__ == "__main__":
    curses.wrapper(main)
