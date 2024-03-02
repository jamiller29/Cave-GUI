"""
Program Name: The Cave Program 4
Author: Jeremy Miller
Date:3/1/24

Purpose: A high level single line statement
Requirements: See External Documentation

Pseudocode: See External Documentation
"""

import tkinter as tk
from tkinter import ttk
import sys
from model import Level
from hero import Hero
import webbrowser

hero = Hero()


class View(tk.Tk):
    """This is the Graphical User Interface """

    def __init__(self):
        super().__init__()

        # Window
        self.title("The Cave")
        self.geometry("900x450")

        # Variables
        self.txt = tk.StringVar(value="Select File: Load to begin game. Select Help: Game Manual for the Read Me.")
        # if Hero.FLAVOR_TEXT != " ":
        #     self.txt.set(Hero.FLAVOR_TEXT)


        # Layout
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1, uniform='a')
        self.grid_columnconfigure(index=1, weight=1, )
        self.grid_columnconfigure(index=2, weight=1)
        self.grid_columnconfigure(index=3, weight=1, uniform='a')

        self.left_control_frame = ttk.Frame()
        self.left_control_frame.grid(row=0, column=0)

        self.map_frame = tk.Frame()
        self.map_frame.grid(row=0, column=1, columnspan=2, sticky='nsew', pady=10)

        self.right_control_frame = tk.Frame()
        self.right_control_frame.grid(row=0, column=3)

        # Left Control Frame
        # movement_input = tk.StringVar
        self.up_button = ttk.Button(self.left_control_frame,
                                    text='Up', state='disabled',
                                    command=lambda: View.set_direction(self, direction='N'))
        self.down_button = ttk.Button(self.left_control_frame,
                                      text='Down', state='disabled',
                                      command=lambda: View.set_direction(self, direction='S'))
        self.right_button = ttk.Button(self.left_control_frame,
                                       text='Right', state='disabled',
                                       command=lambda: View.set_direction(self, direction='E'))
        self.left_button = ttk.Button(self.left_control_frame,
                                      text='Left', state='disabled',
                                      command=lambda: View.set_direction(self, direction='W'))

        self.up_button.grid(row=0, column=1)
        self.down_button.grid(row=2, column=1)
        self.right_button.grid(row=1, column=2)
        self.left_button.grid(row=1, column=0)

        # Map Frame
        self.game_map = tk.Canvas(self.map_frame, width=20 * 20, height=20 * 20, bg='white')
        self.game_map.pack()
        # draw_grid(canvas=game_map, rows=20, columns=20)
        self.game_output = tk.Label(self.map_frame, textvariable=self.txt)
        self.game_output.pack()

        # Right Control Frame
        self.attack_button = ttk.Button(self.right_control_frame, text='Attack', state='disabled',
                                        command=lambda: View.attack_button(self))
        self.aup_button = ttk.Button(self.right_control_frame, text='Up', state='disabled',
                                     command=lambda: View.attack_direction(self, atk_direction='N'))
        self.adown_button = ttk.Button(self.right_control_frame, text='Down', state='disabled',
                                       command=lambda: View.attack_direction(self, atk_direction='S'))
        self.aright_button = ttk.Button(self.right_control_frame, text='Right', state='disabled',
                                        command=lambda: View.attack_direction(self, atk_direction='E'))
        self.aleft_button = ttk.Button(self.right_control_frame, text='Left', state='disabled',
                                       command=lambda: View.attack_direction(self, atk_direction='W'))

        self.attack_button.grid(row=1, column=1)
        self.aup_button.grid(row=0, column=1)
        self.adown_button.grid(row=2, column=1)
        self.aright_button.grid(row=1, column=2)
        self.aleft_button.grid(row=1, column=0)

        # Menus
        self.menu = tk.Menu(self)
        file_menu = tk.Menu(self.menu, tearoff=False)
        file_menu.add_command(label='Load', command=lambda: View.start_game(self))
        file_menu.add_command(label='Exit', command=lambda: sys.exit())
        self.menu.add_cascade(label='File', menu=file_menu)

        self.help_menu = tk.Menu(self.menu, tearoff=False)
        self.help_menu.add_command(label='Game Manual', command=lambda: webbrowser.open('https://github.com/jamiller29/Cave-GUI.git'))
        self.menu.add_cascade(label='Help', menu=self.help_menu)

        self.config(menu=self.menu)

    def start_game(self):
        """A Function that will load the level into a list and do the initial display to the canvas."""
        Level.load_level(Level.select_file())
        Level.spawn_hero()
        View.display_level(canvas_to_draw_on=self.game_map, lst_to_display=Level.PLAYER_MAP)
        self.up_button['state'] = 'enabled'
        self.down_button['state'] = 'enabled'
        self.right_button['state'] = 'enabled'
        self.left_button['state'] = 'enabled'
        self.attack_button['state'] = 'enable'

    @staticmethod
    def display_level(canvas_to_draw_on, lst_to_display):
        """This Function takes in canvas and data. Data is a list. It then displays it on the Canvas.
        The canvas.delete('all') wipes the canvas before it updates.
        """
        canvas_to_draw_on.delete('all')
        for i, row in enumerate(lst_to_display):
            for j, element in enumerate(row):
                x = j * 20
                y = i * 20
                canvas_to_draw_on.create_text(x, y, text=element, anchor='nw')

    def set_direction(self, direction):
        """Sets the direction when a button is pressed to move the Hero."""
        _Direction_var = direction
        hero.move(d=_Direction_var)
        View.display_level(canvas_to_draw_on=self.game_map, lst_to_display=Level.PLAYER_MAP)
        View.update_flavor_text(self)


    def attack_button(self):
        """Enables the attack directional buttons to attack."""
        self.aup_button['state'] = 'enabled'
        self.adown_button['state'] = 'enabled'
        self.aleft_button['state'] = 'enabled'
        self.aright_button['state'] = 'enabled'

    def attack_direction(self, atk_direction):
        """Sets attack direction to call the Hero.Attack function. Then Disables the attack buttons."""
        hero.attack(direction=atk_direction)
        self.attack_button['state'] = 'disabled'
        self.aup_button['state'] = 'disabled'
        self.adown_button['state'] = 'disabled'
        self.aleft_button['state'] = 'disabled'
        self.aright_button['state'] = 'disabled'

    # def update_flavor_text(self):
    #     x = Hero.FLAVOR_TEXT
    #     y = Game_Logic.FLAVOR_TEXT
    #     self.txt.set(x)
    #     self.txt.set(y)
    #     print(x)


if __name__ == "__main__":
    window = View()

    window.mainloop()
