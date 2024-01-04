# Author: Alex Grecinger
# Copyright (C) 2023 Alex Grecinger

"""
This module is responsible for the Character object in the eldenRing.py program.
The character's stats and actions are controlled through character.py via the
Character class and various attributes and methods.
"""

import math
import json
import os
import random
import time
import sys
import pyinputplus as pyip


def roll_d10():
    """roll_d10 Generates a random number from 1-10 (inclusive).

    Returns:
        int: Returns a number from 1-10 (inclusive).
    """
    # Roll a number in the range 1-10 and return it.
    return random.randrange(1,11)


# The class for the the player character.
class Character:
    """ A class used to represent and manage a player for the eldenRing.py
    program file.

    Attributes
    ----------
    _classes_path: str
        A string formatted to be the absolute path of the given directory.
        The directory should always point to the classes directory in the
        elden_ring directory.
    _starter_weapons_path: str
        A string formatted to be the absolute path of the given directory/file.
        The path should always lead to the starter-weapons.json file in the
        weapons directory.
    _player_max_health: int
        The maximum health value of the player.
    _player_current_health: int
        The current health value of the player.
    _player_attack: int
        The attack value of the player.
    _player_armor: int
        The armor rating/value of the player.
    _stats: dict
        A dictionary of the player's stats and values.
    _equipment: dict
        A dictionary of the player's equipment slots.
    _character: str
        The chosen character class of the player.
    _player_name: str
        The name of the player.
    _character_path: str
        The path to the chosen character's class file.
    _class_data: dict
        The data from the file in the _character_path variable.
    _weapon_reader: dict
        The data from the file in the _starter_weapons_path variable.
        Used to get the attack of the starting weapons for the classes.

    Methods
    -------
    print_stats()
        Prints the player's stats.
    print_health()
        Prints the player's name and current health.
    get_name()
        Returns the player's name.
    get_armor()
        Returns the player's armor rating value.
    get_health()
        Returns the player's current health value.
    grace()
        Sets the player's current health value to the player's max health value.
    reduce_health(damage=0)
        Subtracts the player's current health value by the given to the
        damage parameter.
    attack()
        Perform a d10 die roll to determine the player's damage done to the
        boss. Round the damage number up to the nearest whole number.
    """

    def __init__(self):
        # Paths for the directory/file that contains the classes and
        # the starter weapons for each class.
        self._classes_path = os.path.abspath('./classes/')
        self._starter_weapons_path = os.path.abspath( \
            './weapons/starter-weapons.json')

        self._player_max_health = 0
        self._player_current_health = 0
        self._player_attack = 0
        self._player_armor = 11

        self._stats = {
            'Vig:': 0,
            'Mnd:': 0,
            'End:': 0,
            'Str:': 0,
            'Dex:': 0,
            'Int:': 0,
            'Fth:': 0,
            'Arc:': 0
        }   # Dictionary to store the player's stats.

        self._equipment = {
            'Right Hand:': "",
            'Left Hand:': "",
            'Helm:': "",
            'Torso:': "",
            'Wrists:': "",
            'Legs:': ""
        }   # Dictionary to store the player's currently equipped gear.

        # _self.inventory = {}   Dictionary to track the player's inventory.

        # Clear the screen for the terminal.
        os.system('cls' if os.name == 'nt' else 'clear')

        # Create a menu of the classes for the player to choose from:
        self._character = pyip.inputMenu(['Astrologer', 'Bandit','Confessor',
                                    'Hero', 'Prisoner', 'Prophet', 'Samurai',
                                    'Vagabond', 'Warrior', 'Wretch', 'Quit'],
                                   numbered=True)

        # Exit the program if the player chooses the 'Quit' option.
        if self._character == 'Quit':
            sys.exit()

        # Get a name for the player.
        self._player_name = pyip.inputStr(
                            prompt='\nEnter a name for your character: ')

        # "Load" the class and clear the screen.
        print('Loading class...')
        time.sleep(0.5)
        os.system('cls' if os.name == 'nt' else 'clear')

        # Join the path to the classes .json files and the chosen class to get
        # the .json file for the chosen class and load the json file data into
        # classData.
        self._character_path = os.path.join(self._classes_path, \
                                            self._character.lower() + '.json')
        try:
            with open(self._character_path, 'r', encoding="utf-8") as file:
                self._class_data = json.load(file)
        except FileNotFoundError:
            print(f'\nFile {self._character_path} not found! Exiting...')
            sys.exit(1)

        for k, v in self._class_data['Stats'].items():
            # Store the player's stats in the _stats dict.
            self._stats[k] = v

        for k, v in self._class_data['Equipment'].items():
            # Fill the slots for the player's equipment in the
            # _equipment dict.
            self._equipment[k] = v

        # Search through the starter weapons file to find the weapon that is
        # in the player's right hand and give the player that weapon's attack
        # rating.
        try:
            with open(self._starter_weapons_path, 'r', encoding="utf-8") as file:
                self._weapon_reader = json.load(file)
        except FileNotFoundError:
            print(f'\nFile {self._starter_weapons_path} not found! Exiting...')
            sys.exit(1)

        for k, v in self._weapon_reader.items():
            if k == self._equipment['Right Hand:']:
                self._player_attack = int(v)
            # If the player is holding another weapon in their left hand, then
            # increase the player's attack rating by half of the left-handed
            # weapon.
            if k == self._equipment['Left Hand:']:
                self._player_attack += (int(v) // 2)

        # Get the player's max health and set their current health equal to
        # their max health.
        self._player_max_health = self._stats['Vig:'] * 10
        self._player_current_health = self._player_max_health

        # Determine if the player has a shielf in their left hand.
        if "shield" or "buckler" in self._equipment['Left Hand:'].lower():
            self._player_armor = 13

    def print_stats(self):
        """print_stats Prints the player's class, stats and current equipment.
        """
        # Print the player's class and stats.
        print(f'Name: {self._player_name}\n')
        print(f'Class: {self._character}\n')
        for k, v in self._stats.items():
            print(k.ljust(7, ' ') + str(v))
        print(f'\nHP: {self._player_max_health}')
        print(f'Attack: {self._player_attack}')
        print('-' * 30)

        # Print the player's currently equipped items.
        for k, v in self._equipment.items():
            print(k.ljust(12, ' ') + v)
        print('-' * 30)

        # Let the player read the chosen class' stats.
        time.sleep(3)
        # Wait for the player to hit 'ENTER' to initiate the first battle.
        input("Press 'ENTER' to continue...")

    def print_health(self):
        """print_health Prints the player's name and current health value.
        """
        # Print the player's current health.
        print(f'\n{self._player_name}')
        print(f'HP: {self._player_current_health}')

    def get_name(self):
        """get_name Return the player's name.

        Returns:
            str: The player's name.
        """
        # Return the player's name.
        return self._player_name

    def get_armor(self):
        """get_armor Return the player's armor rating.

        Returns:
            int: The player's armor rating.
        """
        # Return the player's armor rating for boss damage rolls.
        return self._player_armor

    def get_health(self):
        """get_health Return the player's current health value.

        Returns:
            int: The player's current health value.
        """
        # Return the player's current health.
        return self._player_current_health

    def grace(self):
        """grace Set the player's current health value to the player's maximum
        health value. Use to heal the player between boss fights.
        """
        print('\nRest...') # Rest and prepare for the next battle.
        # Heal the player's current health to their max health.
        self._player_current_health = self._player_max_health
        print('Fully healed and preparing for next battle...')
        time.sleep(0.70)
        print('-' * 30)

    def reduce_health(self, damage = 0):
        """reduce_health Reduce the player's current health value by the amount
        of the damage value passed. Sets the player's current health to 0 if the
        player's health would be reduced below 0 by the damage value.

        Args:
            damage (int, optional): The amount of damage to dealt by the boss.
            Defaults to 0.
        """
        # Reduce the player's current health by the damage amount.
        self._player_current_health -= damage

        # If the player's health is reduced below 0, then set the
        # health value at 0 instead.
        self._player_current_health = max(self._player_current_health, 0)

    def attack(self):
        """attack Perform a d10 die roll to determine the player's damage done
        to the boss. The damage dealt is equal to a percentage of the player's
        current attack rating. The percentage is based off the results of the
        d10 die roll. For example, a roll of 4 will do 40% of the player's
        attack rating in damage.
        Round the damage number up to the nearest whole number.

        Returns:
            int: The amount of damage the player will deal with its attack.
        """
        return math.ceil(self._player_attack * (roll_d10() / 10))


if __name__ == "__main__":
    print("This module is to be imported by elden_ring.py.")
