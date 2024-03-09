"""
This module is responsible for the Boss object in the elden_ring.py program.
The boss' stats and actions are controlled through boss.py via the Boss class
and various attributes and methods.
"""

import random
import math
import sys
import os
import time
import pandas as pd


BOSSES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bosses'))
WEAPONS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'weapons'))


def roll_d10():
    """roll_d10 Generates a random number from 1-10 (inclusive).

    Returns:
        int: Returns a number from 1-10 (inclusive).
    """
    # Roll a number in the range 1-10 and return it.
    return random.randrange(1,11)


# Class for the boss character.
class Boss():
    """A class used to represent and manage an Elden Ring boss for the
    eldenRing.py program file.

    Attributes
    ----------
    _boss_name: str
        The name of the boss.
    _boss_health: int
        The boss' health value.
    _boss_attack: int
        The boss' attack value.
    _boss_armor: int
        The boss' armor value.
    _boss_runes: int
        The number of runes that the boss will drop upon defeat.

    Methods
    -------
    drop_weapon(chance=1)
        Allows the boss to drop a random weapon from one of two weapon lists
        when defeated.
    set_field_boss()
        Sets the stats for a boss from the field-boss-list.csv file.
    set_mini_boss()
        Sets the stats for a boss from the mini-boss-list.csv file.
    set_main_boss()
        Sets the stats for a boss from the main-boss-list.csv file.
    print_stats()
        Prints the name and health of the current boss object.
    get_health()
        Returns the health value of the boss object.
    get_armor()
        Returns the armor value of the boss object.
    get_name()
        Returns the name of the boss object.
    get_runes()
        Returns the runes value of the boss object.
    reduce_health(damage=0)
        Subtracts the current value of _boss_health by the value
        given to the damage parameter.
    attack()
        Perform a d10 die roll to determine the boss' damage done to the
        player. Round the damage number up to nearest whole number.

    """

    def __init__(self):
        # Set the starter/tutorial boss name, health, attack, armor and runes.
        self._boss_name = 'Soldier of Godrick'
        self._boss_health = math.ceil(384 / 2)
        self._boss_attack = 10
        self._boss_armor = 7
        self._boss_runes = 400

    def drop_weapon(self, chance = 1):
        """drop_weapon Allows the boss to drop a random weapon from one of two
        weapon lists when defeated. The boss can either drop a weapon from the
        list of unupgraded weapons or a weapon from the list of fully upgraded
        weapons.

        Args:
            chance (int, optional): Determines the possibility of getting a fully
            upgraded weapon to drop from the boss. The odds are "1 in 'chance'".
            For example, chance = 1 means there is a 100% chance of the boss dropping
            a fully upgraded weapon and chance = 2 is a 50% chance. Defaults to 1.

        Returns:
            pandas.core.frame.DataFrame: Sample DataFrame from one of the weapon lists.
        """
        # Ensure that chance is at least 1 so there is no error for randrange.
        if chance <= 0:
            chance = 1

        unupgraded_weapons_path = os.path.join(WEAPONS_PATH, 'unupgraded-weapons.csv')
        upgraded_weapons_path = os.path.join(WEAPONS_PATH, 'full-upgraded-weapons.csv')

        luck = random.randrange(0, chance)

        if luck == 0:
            weapon_drop = pd.read_csv(upgraded_weapons_path, sep=';').sample()
            return weapon_drop

        weapon_drop = pd.read_csv(unupgraded_weapons_path, sep=';').sample()
        return weapon_drop

    def set_field_boss(self):
        """set_field_boss Sets the stats for a boss from the field-boss-list
        CSV file. Creates a pandas DataFrame of the data and grabs a sample
        to use as the boss name and health.
        """
        # Set the boss file path, attack, and armor.
        boss_file_path = os.path.join(BOSSES_PATH, 'field-boss-list.csv')
        self._boss_attack = 15
        self._boss_armor = 9

        # Read the field boss list file and get a sample of boss data.
        # Set the boss name and health.
        try:
            boss_data = pd.read_csv(boss_file_path, sep=';').sample()
            self._boss_name = boss_data.iloc[0,0]
            self._boss_health = math.ceil(boss_data.iloc[0,1]
                                          / 4)
            self._boss_runes = boss_data.iloc[0,2]
        except FileNotFoundError:
            print(f'\nFile {boss_file_path} not found! Exiting...')
            time.sleep(1.5)
            sys.exit(1)
        except IndexError:
            print('\nError: Index out of range in boss data! Exiting...')
            time.sleep(1.5)
            sys.exit(1)

    def set_mini_boss(self):
        """set_mini_boss Sets the stats for a boss from the mini-boss-list
        CSV file. Creates a pandas DataFrame of the data and grabs a sample
        to use as the boss name and health.
        """
        # Set the boss file path, attack, and armor.
        boss_file_path = os.path.join(BOSSES_PATH, 'mini-boss-list.csv')
        self._boss_attack = 20
        self._boss_armor = 11

        # Read the mini boss list file and create a list of mini bosses.
        # Set the boss name and health.
        try:
            boss_data = pd.read_csv(boss_file_path, sep=';').sample()
            self._boss_name = boss_data.iloc[0,0]
            self._boss_health = math.ceil(boss_data.iloc[0,1]
                                          / 6)
            self._boss_runes = boss_data.iloc[0,2]
        except FileNotFoundError:
            print(f'\nFile {boss_file_path} not found! Exiting...')
            time.sleep(1.5)
            sys.exit(1)
        except IndexError:
            print('\nError: Index out of range in boss data! Exiting...')
            time.sleep(1.5)
            sys.exit(1)

    def set_main_boss(self):
        """set_main_boss Sets the stats for a boss from the main-boss-list
        CSV file. Creates a pandas DataFrame of the data and grabs a sample
        to use as the boss name and health.
        """
        # Set the boss file path, attack, and armor.
        boss_file_path = os.path.join(BOSSES_PATH, 'main-boss-list.csv')
        self._boss_attack = 25
        self._boss_armor = 13

        # Read the main boss list file and create a list of main bosses.
        # Set the boss name and health.
        try:
            boss_data = pd.read_csv(boss_file_path, sep=';').sample()
            self._boss_name = boss_data.iloc[0,0]
            self._boss_health = math.ceil(boss_data.iloc[0,1]
                                          / 8)
            self._boss_runes = boss_data.iloc[0,2]
        except FileNotFoundError:
            print(f'\nFile {boss_file_path} not found! Exiting...')
            time.sleep(1.5)
            sys.exit(1)
        except IndexError:
            print('\nError: Index out of range in boss data! Exiting...')
            time.sleep(1.5)
            sys.exit(1)

    def print_stats(self):
        """print_stats Prints the boss name and health.
        """
        print(f'\n{self._boss_name}')
        print(f'HP: {self._boss_health}')

    def get_health(self):
        """get_health Returns the boss' health value.

        Returns:
            int: The boss' health.
        """
        return self._boss_health

    def get_armor(self):
        """get_armor Returns the boss' armor value.

        Returns:
            int: The boss' armor.
        """
        return self._boss_armor

    def get_name(self):
        """get_name Return the boss' name.

        Returns:
            str: The boss' name.
        """
        return self._boss_name

    def get_runes(self):
        """get_runes Return the runes value of the boss

        Returns:
            int: The number of runes the boss will drop upon defeat.
        """
        return self._boss_runes

    def reduce_health(self, damage = 0):
        """reduce_health Reduce the boss' health value.

        Args:
            damage (int, optional): The amount to reduce the boss' health.
            Defaults to 0.
        """
        self._boss_health -= damage

    def attack(self):
        """attack Perform a d10 die roll to determine the boss' damage done to
        the player. The damage dealt is equal to a percentage of the boss'
        current attack rating. The percentage is based off the results of the
        d10 die roll. For example, a roll of 4 will do 40% of the boss' attack
        rating in damage.
        Round the damage number up to the nearest whole number.

        Returns:
            int: The amount of damage the boss will deal with its attack.
        """
        return math.ceil(self._boss_attack * (roll_d10() / 10))


if __name__ == "__main__":
    print("This module is to be imported by elden_ring.py.")
