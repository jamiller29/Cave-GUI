"""
Program Name: The Cave Program 4
Author: Jeremy Miller
Date:3/1/24
"""

from model import Game_Logic, Level


class Hero:
    """Hero Class handles the hero controller."""
    FLAVOR_TEXT = ''
    def __init__(self):
        self.speed = 1
        self.attack_range = 2
        self.has_spear = True

    def move(self, d):
        """Gets direction from the GUI and moves the hero by changing his location on the map and in the list
        Level.Master_Level.
        """
        current_hero_location = []
        Game_Logic.find_position(Level.Master_Level, current_hero_location, 'H')
        row_adj, col_adj = {
            'N': [-self.speed, 0],
            'S': [self.speed, 0],
            'E': [0, self.speed],
            'W': [0, -self.speed],
        }.get(d)

        Level.Master_Level[current_hero_location[0][0] + row_adj][current_hero_location[0][1] + col_adj] = 'H'
        Level.Master_Level[current_hero_location[0][0]][current_hero_location[0][1]] = ' '
        Level.PLAYER_MAP[current_hero_location[0][0] + row_adj][current_hero_location[0][1] + col_adj] = 'H'
        Level.PLAYER_MAP[current_hero_location[0][0]][current_hero_location[0][1]] = '*'
        # Hero.Player_Map_visible[current_hero_location[0][0] + row_adj][current_hero_location[0][1] + col_adj] = 'H'
        # Hero.Player_Map_visible[current_hero_location[0][0]][current_hero_location[0][1]] = '*'
        Hero.wall_collision(self, direction=d)
        Game_Logic.listen()
        Game_Logic.win_conditions()
        Game_Logic.torch()
        # Hero.player_map()

    def wall_collision(self, direction):
        """Uses game logic to detect collision to determine if the player walks into a wall.
        The Hero is moved back to his original spot and the wall is recreated in the list.
        """
        current_hero_location = []
        Game_Logic.find_position(Level.Master_Level, current_hero_location, 'H')
        if Game_Logic.detect_collision(Level.Wall_Loc, current_hero_location):
            print("You ran into a wall!")
            Hero.FLAVOR_TEXT = 'You cannot walk through a wall!'
            row_adj, col_adj = {
                'N': [self.speed, 0],
                'S': [-self.speed, 0],
                'E': [0, -self.speed],
                'W': [0, self.speed],
            }.get(direction)

            Level.Master_Level[current_hero_location[0][0] + row_adj][current_hero_location[0][1] + col_adj] = 'H'
            Level.Master_Level[current_hero_location[0][0]][current_hero_location[0][1]] = 'W'
            Level.PLAYER_MAP[current_hero_location[0][0] + row_adj][current_hero_location[0][1] + col_adj] = 'H'
            Level.PLAYER_MAP[current_hero_location[0][0]][current_hero_location[0][1]] = 'W'

    def attack(self, direction):
        """Handles the attack action of the Hero. Determines if the Hero hits or misses the Monster by using game
        logic detect collision.
        """
        spear_location = []
        new_spear_location = []
        Game_Logic.find_position(Level.Master_Level, spear_location, 'H')
        # direction = input("Which way do you throw your spear? N, S, E, or W,: ").upper()

        throw_spear = {
            'N': [-self.attack_range, 0],
            'S': [self.attack_range, 0],
            'E': [0, self.attack_range],
            'W': [0, self.attack_range],
        }

        if direction in throw_spear:
            row_adj, col_adj = throw_spear[direction]
            spear_location[0][0] += row_adj
            spear_location[0][1] += col_adj

        if Game_Logic.detect_collision(Level.MONSTER, spear_location):
            print("You throw your spear. It slays the Monster!")
            Hero.FLAVOR_TEXT = 'You throw your spear. It slays the Monster!'
            Level.Master_Level[Level.MONSTER[0][0]][Level.MONSTER[0][1]] = 'E'
            self.has_spear = False
            Game_Logic.monster_slain = True
        else:
            print("You throw your spear it clangs of the cave floor and is lost in the darkness.")
            Hero.FLAVOR_TEXT = 'You throw your spear it clangs of the cave floor and is lost in the darkness.'
            self.has_spear = False