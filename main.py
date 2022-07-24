__author__ = "Benjamin Mickler"
__copyright__ = "Copyright 2022, Benjamin Mickler"
__credits__ = ["Benjamin Mickler"]
__license__ = "GPLv3 or later"
__version__ = "230720222"
__maintainer__ = "Benjamin Mickler"
__email__ = "ben@benmickler.com"

"""
Number Guessing Game is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

Number Guessing Game is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
Number Guessing Game. If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import random
import tkinter as tk
import tkinter.messagebox
from tkinter import simpledialog
from help_message import HELP_MESSAGE

class game:
    def __init__(self, rand_num=random.randint(1, 100)):
        self.rand_num = rand_num
        self.attempts = 0
    def guess(self, num):
        self.attempts += 1
        res = []
        if num == self.rand_num:
            res.append(0)
        if self.rand_num-10 <= num <= self.rand_num+10:
            res.append(1)
        if num > self.rand_num:
            res.append(2)
        if num < self.rand_num:
            res.append(3)
        return res

class cli_if:
    def __init__(self):
        self.game = game()
    def start(self):
        self.name = input("Name: ")
        print()
        while True:
            guess = input("Guess: ")
            if guess == "exit":
                break
            else:
                guess = int(guess)
            guess_result = self.game.guess(guess)
            if 0 in guess_result:
                print(f"\033[92mCongratulations {self.name}, you guessed the number in {self.game.attempts} attempts\033[0m")
                break
            if 1 in guess_result:
                print("It's close, your guess was 10 or less off")
            if 2 in guess_result:
                print(f"The number is less than {guess}")
            if 3 in guess_result:
                print(f"The number is greater than {guess}")
            print()

class gui_if:
    def __init__(self):
        self.game = game()
        self.game_done = False
        self.window = tk.Tk()
        self.window.title("Number Guessing Game")
        self.window.tk.call('wm', 'iconphoto', self.window._w, tk.PhotoImage(file='logo.png'))
        self.window.minsize(400, 200)
        self.window.bind('<Return>', self.check)
        guess_label = tk.Label(text="Guess:")
        self.guess_entry = tk.Entry()
        guess_label.pack()
        self.guess_entry.pack()
        self.check_button = tk.Button(text="Check")
        self.check_button.pack()
        self.help_button = tk.Button(text="Help", command=self.show_help_dialog)
        self.help_button.pack()
        self.check_button.bind("<Button-1>", self.check)
        self.label = tk.Label()
        self.label.pack()
        self.name = simpledialog.askstring(title="Number Guessing Game", prompt="What's your name?")
        if self.name == None:
            raise SystemExit
        self.guess_entry.focus()
        self.window.mainloop()
    def check(self, event):
        if self.game_done == True:
            self.game.rand_num = random.randint(1, 100)
            self.game.attempts = 0
            self.label.config(text="")
            self.guess_entry["state"] = "normal"
            self.guess_entry.delete(0, 'end')
            self.check_button.config(text="Check")
            self.game_done = False
        else:
            guess = self.guess_entry.get()
            guess = self.check_to_int(guess)
            if guess == 0 or guess == False or guess > 100 or guess < 1:
                tkinter.messagebox.showerror("Invalid guess", "Please enter a number between 1 and 100.")
            else:
                guess_result = self.game.guess(guess)
                lbl_txt = ""
                if 1 in guess_result:
                    lbl_txt += "It's close, your guess was 10 or less off\n"
                if 2 in guess_result:
                    lbl_txt += f"The number is less than {guess}\n"
                if 3 in guess_result:
                    lbl_txt += f"The number is greater than {guess}\n"
                if 0 in guess_result:
                    lbl_txt = f"Congratulations {self.name}, you guessed the number in {self.game.attempts} attempts\n"
                    self.guess_entry["state"] = "disabled"
                    self.check_button.config(text="Reset")
                    self.game_done = True
                self.label.config(text=lbl_txt)
                self.guess_entry.delete(0, 'end')
    def check_to_int(self, num):
        try:
            num = int(num)
            return num
        except:
            return False
    def show_help_dialog(self):
        aboutdialog = AboutDialog(self.window)
        self.window.wait_window(aboutdialog.top)

class AboutDialog:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        self.about_text = tk.Text(top)
        self.about_text.pack()
        self.about_text.config(state='normal')
        self.about_text.insert('end', HELP_MESSAGE)
        self.about_text.config(state='disabled')
        self.close_button = tk.Button(top, text='Close', command=self.top.destroy)
        self.close_button.pack()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ["-h", "--help", "help"]:
            print(HELP_MESSAGE)
            raise SystemExit
        elif sys.argv[1].lower() in ["-g", "--gui", "gui"]:
            gui_if()
        elif sys.argv[1].lower() in ["-c", "--cli", "cli"]:
            cli_if().start()
        else:
            print("Invalid arguments, use --help for help")
    else:
        print("Not enough arguments, use --help for help")