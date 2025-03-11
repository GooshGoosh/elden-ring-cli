"""
character.py

Listen up, brother! This module is responsible for the Character object in the elden_ring.py program.
The character's stats and actions are controlled through this module, via the Character class and
its powerful attributes and methods. Get ready to step into the ring and show those bosses what you're made of!

Classes:
    Character:
        A class used to represent and manage a player for the elden_ring.py program file.

Functions:
    roll_d10() -> int:
        Generates a random number between 1 and 10 (inclusive), brother!
"""

import math
import json
import os
import time
import sys
import secrets
import pyinputplus as pyip
import pandas as pd


CLASSES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'classes'))
WEAPONS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'weapons'))
WEAPON_TYPES = ['Dagger', 'Straight Sword', 'Greatsword', 'Colossal Weapon',
                'Thrusting Sword', 'Heavy Thrusting Sword', 'Curved Sword',
                'Curved Greatsword', 'Katana', 'Twinblade', 'Axe', 'Greataxe',
                'Hammer', 'Flail', 'Great Hammer', 'Colossal Weapon', 'Spear',
                'Great Spear', 'Halberd', 'Reaper', 'Whip', 'Fist', 'Claw',
                'Light Bow', 'Bow', 'Greatbow', 'Crossbow', 'Ballista',
                'Glintstone Staff', 'Sacred Seal', 'Torches']
SHIELD_TYPES = ['Small Shield', 'Medium Shield', 'Great Shield']


def roll_d10():
    """roll_d10 Generates a random number from 1-10 (inclusive).

    Returns:
        int: Returns a number from 1-10 (inclusive).
    """
    # Roll a number in the range 1-10 and return it.
    return secrets.SystemRandom().randrange(1,11)


# The class for the the player character.
class Character:
    """ A class used to represent and manage a player for the eldenRing.py
    program file.

    Attributes
    ----------
    _player_max_health: int
        The maximum health value of the player.
    _player_current_health: int
        The current health value of the player.
    _player_attack: int
        The attack value of the player.
    _player_armor: int
        The armor rating/value of the player.
    _player_runes: int
        The number of runes in the player's possession.
    _stats: dict
        A dictionary of the player's stats and values.
    _equipment: dict
        A dictionary of the player's equipment slots.
    _character: str
        The chosen character class of the player.
    _player_name: str
        The name of the player.
    _player_level: int
        The level of the player's character.

    Methods
    -------
    update_stats()
        Reads the player's stats and updates their max health and attack.
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
    get_runes()
        Returns the player's current runes.
    increase_player_level()
        Increase the player's chosen stat.
    change_weapon(weapon_data)
        Give the player the opportunity to equip the new weapon dropped from the
        previous boss fight.
    grace()
        Sets the player's current health value to the player's max health value.
    reduce_health(damage=0)
        Subtracts the player's current health value by the given to the
        damage parameter.
    add_runes(runes=0)
        Adds to the player's current runes by the value given to the runes
        parameter.
    reduce_runes(runes=0)
        Subtracts the player's current runes by the value given to the runes
        parameter.
    attack()
        Perform a d10 die roll to determine the player's damage done to the
        boss. Round the damage number up to the nearest whole number.
    """

    def __init__(self):
        # Path for the file that contains the starter weapons for each class.
        unupgraded_weapons_path = os.path.join(WEAPONS_PATH, 'unupgraded-weapons.csv')

        self._player_max_health = 0
        self._player_current_health = 0
        self._player_attack = 0
        self._player_armor = 11
        self._player_runes = 0

        self._stats = {
            'Vig': 0,
            'Mnd': 0,
            'End': 0,
            'Str': 0,
            'Dex': 0,
            'Int': 0,
            'Fth': 0,
            'Arc': 0
        }   # Dictionary to store the player's stats.

        self._equipment = {
            'Right Hand': "",
            'Left Hand': "",
            'Helm': "",
            'Torso': "",
            'Wrists': "",
            'Legs': ""
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
        character_path = os.path.join(CLASSES_PATH,
                                      self._character.lower() + '.json')
        try:
            with open(character_path, 'r', encoding="UTF-8") as file:
                class_data = json.load(file)
        except FileNotFoundError:
            print(f'\nFile {character_path} not found! Exiting...')
            sys.exit(1)

        self._player_level = class_data['Level']

        for k, v in class_data['Stats'].items():
            # Store the player's stats in the _stats dict.
            self._stats[k] = v

        for k, v in class_data['Equipment'].items():
            # Fill the slots for the player's equipment in the _equipment dict.
            self._equipment[k] = v

        try:
            weapons_df = pd.read_csv(unupgraded_weapons_path, sep=';')

            # Get the data for the weapon in the player's right hand and set the
            # player's attack to that weapon's attack.
            right_hand = weapons_df[weapons_df["Name"] == self._equipment['Right Hand']]
            self._player_attack = int(right_hand.iloc[0,2])

            # Get the data for the weapon in the player's left hand.
            left_hand = weapons_df[weapons_df["Name"] == self._equipment['Left Hand']]
            if left_hand.iloc[0,1] in WEAPON_TYPES:
                # Add half its attack to the player's attack if it is a weapon.
                self._player_attack += int(left_hand.iloc[0,2]) // 2
            elif left_hand.iloc[0,1] in SHIELD_TYPES:
                # Increase the player's armor if it is a shield.
                self._player_armor = 13
        except FileNotFoundError:
            print(f'\nFile {unupgraded_weapons_path} not found! Exiting...')
            time.sleep(1.5)
            sys.exit(1)
        except IndexError:
            print('\nError: Index out of range for weapon data! Exiting...')
            time.sleep(1.5)
            sys.exit(1)

        # Increase the player's attack by their Str and Dex stat.
        self._player_attack += (self._stats['Str'] + self._stats['Dex'])

        # Get the player's max health and set their current health equal to
        # their max health.
        self._player_max_health = self._stats['Vig'] * 10
        self._player_current_health = self._player_max_health

    def update_stats(self):
        """update_stats Reads the player's stats and updates their max health and
        attacked based on their Vig, Str, and Dex.
        """
        unupgraded_weapons_path = os.path.join(WEAPONS_PATH, 'unupgraded-weapons.csv')
        upgraded_weapons_path = os.path.join(WEAPONS_PATH, 'full-upgraded-weapons.csv')

        # Set the player's health based on their Vig stat.
        self._player_max_health = self._stats['Vig'] * 10

        try:
            # Get the data for the weapon in the player's right hand and set the
            # player's attack to that weapon's attack.
            if 'MAX' in self._equipment['Right Hand']:
                try:
                    weapons_df = pd.read_csv(upgraded_weapons_path, sep=';')
                except FileNotFoundError:
                    print(f'\nFile {upgraded_weapons_path} not found! Exiting...')
                    time.sleep(1.5)
                    sys.exit(1)
            else:
                try:
                    weapons_df = pd.read_csv(unupgraded_weapons_path, sep=';')
                except FileNotFoundError:
                    print(f'\nFile {unupgraded_weapons_path} not found! Exiting...')
                    time.sleep(1.5)
                    sys.exit(1)

            right_hand = weapons_df[weapons_df["Name"] == self._equipment['Right Hand']]
            self._player_attack = int(right_hand.iloc[0,2])

            # Get the data for the weapon in the player's left hand.
            if 'MAX' in self._equipment['Left Hand']:
                try:
                    weapons_df = pd.read_csv(upgraded_weapons_path, sep=';')
                except FileNotFoundError:
                    print(f'\nFile {upgraded_weapons_path} not found! Exiting...')
                    time.sleep(1.5)
                    sys.exit(1)
            else:
                try:
                    weapons_df = pd.read_csv(unupgraded_weapons_path, sep=';')
                except FileNotFoundError:
                    print(f'\nFile {unupgraded_weapons_path} not found! Exiting...')
                    time.sleep(1.5)
                    sys.exit(1)

            left_hand = weapons_df[weapons_df["Name"] == self._equipment['Left Hand']]
            if left_hand.iloc[0,1] in WEAPON_TYPES:
                # Add half its attack to the player's attack if it is a weapon.
                self._player_attack += int(left_hand.iloc[0,2]) // 2
            elif left_hand.iloc[0,1] in SHIELD_TYPES:
                # Increase the player's armor if it is a shield.
                self._player_armor = 13
        except IndexError:
            print('\nError: Index out of range for weapon data! Exiting...')
            time.sleep(1.5)
            sys.exit(1)

        # Increase the player's attack by their Str and Dex stat.
        self._player_attack += (self._stats['Str'] + self._stats['Dex'])

    def print_stats(self):
        """print_stats Prints the player's class, stats and current equipment.
        """
        # Print the player's class and stats.
        print('-' * 30)
        print(f'Name: {self._player_name}\n')
        print(f'Class: {self._character}')
        print(f'Level: {self._player_level}\n')
        for k, v in self._stats.items():
            print((k +":").ljust(7, ' ') + str(v))
        print(f'\nHP: {self._player_max_health}')
        print(f'Attack: {self._player_attack}')
        print(f'Runes: {self._player_runes}')
        print('-' * 30)

        # Print the player's currently equipped items.
        for k, v in self._equipment.items():
            print((k + ":").ljust(12, ' ') + v)
        print('-' * 30)

        # Let the player read the chosen class' stats.
        time.sleep(3)
        # Wait for the player to hit 'ENTER' to initiate the first battle.
        input("\nPress 'ENTER' to continue...")

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

    def get_runes(self):
        """get_runes Return the player's current runes.

        Returns:
            int: The player's current runes.
        """
        # Return the player's current runes.
        return self._player_runes

    def increase_player_level(self):
        """increase_player_level Lets the player choose a stat to increase to
        level up their character if they have sufficient runes. The formula for
        the rune cost is taken from eldenring.wiki.fextralife.com/Level
        """
        # Formula for calculating the rune cost.
        x = ((self._player_level + 81) - 92) * 0.02
        # Change x to 0 if the above expression results in x below 0.
        x = max(x, 0)
        rune_cost = int(((x + 0.1) * ((self._player_level + 81) ** 2)) + 1)

        if self._player_runes < rune_cost:
            print("\nInsufficient runes to level up.")
            print(f'Need {rune_cost} runes to level up.')
            time.sleep(0.75)    # Allow player time to read message.
            return

        stats = ['Vig', 'Mnd', 'End', 'Str', 'Dex', 'Int', 'Fth', 'Arc']
        stat_to_inc = pyip.inputMenu(stats, prompt='\nSelect a stat to increase:\n',
                                     numbered=True)
        # Increase the player's chosen stat and reduce their current runes.
        print(f'\n{stat_to_inc} increased from {self._stats[stat_to_inc]}',
              f'to {self._stats[stat_to_inc] + 1}\n')

        self._stats[stat_to_inc] += 1
        self._player_runes -= rune_cost
        self._player_level += 1
        self.update_stats()

        print(f'Current runes: {self._player_runes}')
        time.sleep(0.75)

    def change_weapon(self, weapon_data):
        """change_weapon Ask the player if they would like to change the weapon in
        once of their hands with the new weapon that was dropped from the previous
        boss fight. Updates the stats after the player has to chosen to either equip
        the new weapon or not.

        Args:
            weapon_data (pandas.core.frame.DataFrame): DataFrame of the weapon data
            dropped from the previous boss fight that should follow the format of:
            Name;Type;Attack.
        """
        unupgraded_weapons_path = os.path.join(WEAPONS_PATH, 'unupgraded-weapons.csv')
        upgraded_weapons_path = os.path.join(WEAPONS_PATH, 'full-upgraded-weapons.csv')
        try:
            weapon_name = weapon_data.iloc[0,0]
            weapon_type = weapon_data.iloc[0,1]
            weapon_attack = weapon_data.iloc[0,2]
        except IndexError:
            print('\nError: Index out of range for weapon data! Exiting...')
            time.sleep(1.5)
            sys.exit(1)

        # Get the data from the player's right hand weapon.
        if 'MAX' in self._equipment['Right Hand']:
            try:
                weapons_df = pd.read_csv(upgraded_weapons_path, sep=';')
            except FileNotFoundError:
                print(f'\nFile {upgraded_weapons_path} not found! Exiting...')
                time.sleep(1.5)
                sys.exit(1)
        else:
            try:
                weapons_df = pd.read_csv(unupgraded_weapons_path, sep=';')
            except FileNotFoundError:
                print(f'\nFile {unupgraded_weapons_path} not found! Exiting...')
                time.sleep(1.5)
                sys.exit(1)
        right_hand = weapons_df[weapons_df["Name"] == self._equipment['Right Hand']]

        # Get the data from the player's left hand weapon.
        if 'MAX' in self._equipment['Left Hand']:
            try:
                weapons_df = pd.read_csv(upgraded_weapons_path, sep=';')
            except FileNotFoundError:
                print(f'\nFile {upgraded_weapons_path} not found! Exiting...')
                time.sleep(1.5)
                sys.exit(1)
        else:
            try:
                weapons_df = pd.read_csv(unupgraded_weapons_path, sep=';')
            except FileNotFoundError:
                print(f'\nFile {unupgraded_weapons_path} not found! Exiting...')
                time.sleep(1.5)
                sys.exit(1)
        left_hand = weapons_df[weapons_df["Name"] == self._equipment['Left Hand']]

        # Print the player's weapon attack for each hand, the new weapon's attack
        # and ask if they would like to equip the new weapon.
        try:
            print(f'\nRight hand attack: {right_hand.iloc[0,2]}')
            print(f'Left hand attack: {left_hand.iloc[0,2]}')
        except IndexError:
            print('\nError: Index out of range for weapon data! Exiting...')
            time.sleep(1.5)
            sys.exit(1)
        print(f'\n{weapon_name} attack: {weapon_attack}')
        print('\nWeapons increase attack while shields increase your armor.')
        response = pyip.inputYesNo(prompt='Would you like to equip the new weapon? Y/N: ')

        if response == 'yes':
            if weapon_type in WEAPON_TYPES:
                hand = pyip.inputMenu(['Right Hand', 'Left Hand'],
                                      prompt='\nSelect a hand to equip the weapon:\n',
                                      numbered=True)
                self._equipment[hand] = weapon_name
                print(f'\n{weapon_name} equipped in the {hand}\n')
            elif weapon_type in SHIELD_TYPES:
                self._equipment['Left Hand'] = weapon_name
                print(f'\n{weapon_name} equipped in Left Hand\n')

        print('Updating stats...\n')
        time.sleep(1.5)
        self.update_stats()

    def grace(self):
        """grace Give the player a set of actions to choose from and perform the
        action chosen. Once the player is done performing actions other than 'Rest',
        set the player's current health value to the player's maximum health value.
        Use to heal the player between boss fights.
        """
        action = ""

        print(f'\nName: {self._player_name}')
        print(f'Current runes: {self._player_runes}')

        while action != 'Rest':
            action = pyip.inputMenu(['Show Stats', 'Level Up', 'Rest'],
                                    prompt='\nPick an action:\n',
                                    numbered=True)
            if action == 'Show Stats':
                print()
                self.print_stats()
            elif action == 'Level Up':
                self.increase_player_level()

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

    def add_runes(self, runes = 0):
        """add_runes Increases the player's current runes by the amount of the
        runes value passed.

        Args:
            runes (int, optional): The number of runes to add to the player's
            current runes. Defaults to 0.
        """
        # Increase the player's runes by the value given.
        self._player_runes += runes

    def reduce_runes(self, runes = 0):
        """reduce_runes Reduce the player's current runes by the amount of the
        runes value passed.

        Args:
            runes (int, optional): The number of runes to subtract from the
            player's current runes. Defaults to 0.
        """
        # Decrease the player's runes by the value given.
        self._player_runes -= runes

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
