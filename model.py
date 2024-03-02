"""
Program Name: The Cave Program 4
Author: Jeremy Miller
Date:3/1/24
"""

import PySimpleGUI as psg
from random import choice


class Level:
    """Responsible for loading game files into the program and making the accessible to the rest of the game."""
    # Class Variables
    Master_Level = []
    PLAYER_MAP = []
    Wall_Loc = []
    Spawn_Loc = []
    TREASURE = []
    PIT = []
    MONSTER = []
    DM_Map = []

    def __init__(self):
        self.rows = 20
        self.cols = 20

    @classmethod
    # Load the game file.
    def load_level(cls, select_file):
        """Loads a text file and outputs it to the Master Level."""
        with open(select_file) as file:
            lvl = file.read()

        # Remove any white spaces inside the file.
        for i in range(0, len(lvl), 40):
            level_slice = list(lvl[i:i + 39])
            while ' ' in level_slice:
                level_slice.remove(' ')
            # print(level_slice)
            Level.Master_Level.append(level_slice)
            Level.DM_Map.append(level_slice)
        Level.initialize_game_locations()

    @classmethod
    def initialize_game_locations(cls):
        """Reads the game locations of all the objects on the map and outputs them for tracking."""
        Game_Logic.find_position(Level.Master_Level, Level.Wall_Loc, 'W')
        Game_Logic.find_position(Level.Master_Level, Level.Spawn_Loc, 'E')
        Game_Logic.find_position(Level.Master_Level, Level.MONSTER, 'M')
        Game_Logic.find_position(Level.Master_Level, Level.TREASURE, 'T')
        Game_Logic.find_position(Level.Master_Level, Level.PIT, 'P')
        Level.gen_player_map()

    @staticmethod
    def select_file():
        """The file selection function"""
        file = psg.popup_get_file('Select A File', title='File Selection')
        return file

    @staticmethod
    def gen_player_map():
        """Generates the Player Map"""
        for _ in range(20):
            row = []
            for _ in range(20):
                row.append(' ')
            Level.PLAYER_MAP.append(row)

    # @staticmethod
    # def player_map():
    #     for row in Level.PLAYER_MAP:
    #         print(' '.join(row))

    # @staticmethod
    # def DM_map():
    #     for row in Level.Master_Level:
    #         print(' '.join(row))

    @staticmethod
    def spawn_hero():
        """This function is responsible for randomly spawning the Hero. It does this by using game logic dmz function
        to create no spawn zones. It then chooses a location at random from the available spawn locations.
        """
        level_dmz = []
        monster_dmz = []
        pit_dmz = []
        treasure_dmz = []
        Game_Logic.dmz(Level.MONSTER[0][0], Level.MONSTER[0][1], Level.Master_Level, monster_dmz, 3)
        Game_Logic.dmz(Level.PIT[0][0], Level.PIT[0][1], Level.Master_Level, pit_dmz, 2)
        Game_Logic.dmz(Level.TREASURE[0][0], Level.TREASURE[0][1], Level.Master_Level, treasure_dmz, 2)
        level_dmz = monster_dmz + treasure_dmz + treasure_dmz
        for x, y in enumerate(level_dmz):
            for a, b in enumerate(Level.Spawn_Loc):
                if y == b:
                    Level.Spawn_Loc.remove(y)
        hero_location = choice(Level.Spawn_Loc)
        hero_location_x = hero_location[0]
        hero_location_y = hero_location[1]
        Level.Master_Level[hero_location_x][hero_location_y] = 'H'
        Level.PLAYER_MAP[hero_location[0]][hero_location[1]] = 'H'
        # Hero.Player_Map_visible[hero_location[0]][hero_location[1]] = 'H'


class Game_Logic:
    """Game Logic is where the functions that manage the game such as finding locations and win conditions."""
    monster_slain = False
    FLAVOR_TEXT = ''

    # flavor_text = tk.StringVar()
    def __init__(self):
        pass

    @staticmethod
    def find_position(lst, output_lst, tgt):
        """Takes a list, and output list and the target you wish to find."""
        for i, sublist in enumerate(lst):
            for j, element in enumerate(sublist):
                if element == tgt:
                    output_lst.append([i, j])

    @staticmethod
    def dmz(row, col, lst, out_put_lst, no_spawn_range):
        """Returns a list of adjacent locations in a list. Inputs a number of 1-3 to set the range. Then
        outputs the results to a list.
        """
        if no_spawn_range == 1:
            i, j = 1, 2
        elif no_spawn_range == 2:
            i, j = 2, 3
        else:
            i, j = 3, 4
        for x in range(row - i, row + j):
            for y in range(col - i, col + j):
                if 0 <= x < len(lst) and 0 <= y < len(lst[row]):
                    out_put_lst.append([x, y])

    @staticmethod
    def detect_collision(lst, tgt):
        """Takes in two lists and compares them for a collision in the lists."""
        for x, y in enumerate(tgt):
            for a, b in enumerate(lst):
                if y == b:
                    return True

    @staticmethod
    def listen():
        """Function Responsible for detecting what the Hero hears. Uses game logic dmz function to create bubbles around
        the player and the objects. When the players bubble enters an object bubble the Hero hears it.
        """
        hero_location = []
        Game_Logic.find_position(Level.Master_Level, hero_location, 'H')
        listen_for_monster = []
        listen_for_pit = []
        Game_Logic.dmz(hero_location[0][0], hero_location[0][1], Level.Master_Level, listen_for_monster, 2)
        Game_Logic.dmz(hero_location[0][0], hero_location[0][1], Level.Master_Level, listen_for_pit, 1)
        for a, b in enumerate(listen_for_pit):
            for c, d in enumerate(Level.PIT):
                if b == d:
                    print("You hear a howl of wind and feel it against your face as if you're standing on the ledge of "
                          "something.")
                    Game_Logic.FLAVOR_TEXT = ("You hear a how of wind and feel it against you're face as if you're on "
                                              "the ledge of something.")
        if not Game_Logic.monster_slain:
            for a, b in enumerate(listen_for_monster):
                for c, d in enumerate(Level.MONSTER):
                    if b == d:
                        print("You hear the snarl of a monster somewhere in the darkness.")
                        Game_Logic.FLAVOR_TEXT = '"You hear the snarl of a monster somewhere in the darkness."'

    @staticmethod
    def torch():
        """Responsible for what the Hero sees on the map. Uses game logic find position and dmz to compare locaitions
        and updates map accordingly.
        """
        hero_location = []
        visible = []
        Game_Logic.find_position(Level.Master_Level, hero_location, 'H')
        Game_Logic.dmz(hero_location[0][0], hero_location[0][1], Level.Master_Level, visible, 1)

        for a, b in enumerate(Level.PLAYER_MAP):
            for c, d in enumerate(b):
                if d in ['W', 'T', 'P', 'C']:
                    Level.PLAYER_MAP[a][c] = ' '

        for a, b in enumerate(visible):
            for c, d in enumerate(Level.Wall_Loc):
                if b == d:
                    Level.PLAYER_MAP[b[0]][b[1]] = 'W'
                    # Level.Player_Map_visible[b[0]][b[1]] = 'W'

        for a, b in enumerate(visible):
            for c, d in enumerate(Level.TREASURE):
                if b == d:
                    Level.PLAYER_MAP[b[0]][b[1]] = 'T'
                    # Level.Player_Map_visible[b[0]][b[1]] = 'T'

        # for a, b in enumerate(visible):
        #     for c, d in enumerate(Level.TREASURE):
        #         if b == d:
        #             Level.Player_Map[b[0]][b[1]] = 'C'
        #             Level.Player_Map_visible[b[0]][b[1]] = 'C'

        for a, b in enumerate(visible):
            for c, d in enumerate(Level.PIT):
                if b == d:
                    Level.PLAYER_MAP[b[0]][b[1]] = 'P'
                    # Level.Player_Map_visible[b[0]][b[1]] = 'P'

    @staticmethod
    def win_conditions():
        """Checks for win conditions by using game logic find location and dmz to compare lists and determine if
        win conditions are met.
        """
        h_loc = []
        monster_kill_box = []
        Game_Logic.dmz(Level.MONSTER[0][0], Level.MONSTER[0][1], Level.Master_Level, monster_kill_box, 1)
        Game_Logic.find_position(Level.Master_Level, h_loc, 'H')
        if h_loc == Level.TREASURE:
            print("You found the Treasure!")
            Game_Logic.FLAVOR_TEXT = 'YOU FOUND THE TREASURE! YOU WIN!'

        elif h_loc == Level.PIT:
            print("You fell in a pit")
            Game_Logic.FLAVOR_TEXT = ('You Fell into a pit. Both of your legs are now broken. You are going to die a '
                                      'slow and painful death. GAME OVER!')
        elif not Game_Logic.monster_slain:
            if Game_Logic.detect_collision(monster_kill_box, h_loc):
                print("The Monster Found You!")
                Game_Logic.FLAVOR_TEXT = ('The Monster has found you! It slashes at your face and ripes your arm off '
                                          'and beats you to death with it. GAME OVER!')
