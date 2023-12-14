import math
import json
import os
import random
import time
import sys
import pyinputplus as pyip


def roll_d10():
    # Roll a number in the range 1-10 and return it.
    return random.randrange(1,11)


# The class for the the player character.
class Character:
    # Paths for the directory/file that contains the classes and
    # the starter weapons for each class.
    __classesPath = os.path.abspath(f'./classes/')
    __starterWeaponsPath = os.path.abspath(f'./weapons/starter-weapons.json')

    def __init__(self):
        self.__playerMaxHealth = 0
        self.__playerCurrentHealth = 0
        self.__playerAttack = 0
        self.__playerArmor = 11

        self.__stats = {
            'Vig:': 0,
            'Mnd:': 0,
            'End:': 0,
            'Str:': 0,
            'Dex:': 0,
            'Int:': 0,
            'Fth:': 0,
            'Arc:': 0
        }   # Dictionary to store the player's stats.

        self.__equipment = {
            'Right Hand:': "",
            'Left Hand:': "",
            'Helm:': "",
            'Torso:': "",
            'Wrists:': "",
            'Legs:': ""
        }   # Dictionary to store the player's currently equipped gear.

        # __self.inventory = {}    # TODO: Dictionary to track the player's inventory.

        # Clear the screen for the terminal.
        os.system('cls' if os.name == 'nt' else 'clear')

        # Create a menu of the classes for the player to choose from:
        self.__character = pyip.inputMenu(['Astrologer', 'Bandit','Confessor',
                                    'Hero', 'Prisoner', 'Prophet', 'Samurai',
                                    'Vagabond', 'Warrior', 'Wretch', 'Quit'],
                                   numbered=True)

        # Exit the program if the player chooses the 'Quit' option.
        if self.__character == 'Quit':
            sys.exit()

        # Get a name for the player.
        self.__playerName = pyip.inputStr(
                            prompt='\nEnter a name for your character: ')

        # "Load" the class and clear the screen.
        print('Loading class...')
        time.sleep(0.5)
        os.system('cls' if os.name == 'nt' else 'clear')

        # Join the path to the classes .json files and the chosen class to get
        # the .json file for the chosen class and load the json file data into
        # classData.
        try:
            jsonFile = open(os.path.join(Character.__classesPath,
                                        self.__character.lower() + '.json'), 'r')
            self.__classData = json.load(jsonFile)
            jsonFile.close()
        except FileNotFoundError:
            print('\nFile {} not found! Exiting...'
                  .format(os.path.join(Character.__classesPath,
                                       self.__character.lower() + '.json')))
            sys.exit(1)

        for k, v in self.__classData['Stats'].items():
            # Store the player's stats in the __stats dict.
            self.__stats[k] = v

        for k, v in self.__classData['Equipment'].items():
            # Fill the slots for the player's equipment in the
            # __equipment dict.
            self.__equipment[k] = v

        # Search through the starter weapons file to find the weapon that is
        # in the player's right hand and give the player that weapon's attack
        # rating.
        try:
            with open(Character.__starterWeaponsPath, 'r') as jsonFile:
                self.__weaponReader = json.load(jsonFile)
        except FileNotFoundError:
            print('\nFile {} not found! Exiting...'
                  .format(Character.__starterWeaponsPath))
            sys.exit(1)

        for k, v in self.__weaponReader.items():
            if k == self.__equipment['Right Hand:']:
                self.__playerAttack = int(v)
            # If the player is holding another weapon in their left hand, then
            # increase the player's attack rating by half of the left-handed
            # weapon.
            if k == self.__equipment['Left Hand:']:
                self.__playerAttack += (int(v) // 2)

        # Get the player's max health and set their current health equal to
        # their max health.
        self.__playerMaxHealth = (self.__stats['Vig:'] * 10)
        self.__playerCurrentHealth = self.__playerMaxHealth

        # Determine if the player has a shielf in their left hand.
        if "shield" or "buckler" in self.__equipment['Left Hand:'].lower():
            self.__playerArmor = 13
        
    def print_stats(self):
        # Print the player's class and stats.
        print('Name: {}\n'.format(self.__playerName))
        print('Class: {}\n'.format(self.__character))
        for k, v in self.__stats.items():
            print(k.ljust(7, ' ') + str(v))
        print('\nHP: {}'.format(self.__playerMaxHealth))
        print('Attack: {}'.format(self.__playerAttack))
        print('-' * 30)

        # Print the player's currently equipped items.
        for k, v in self.__equipment.items():
            print(k.ljust(12, ' ') + v)
        print('-' * 30)

        # Let the player read the chosen class' stats.
        time.sleep(3)
        # Wait for the player to hit 'ENTER' to initiate the first battle.
        input("Press 'ENTER' to continue...")

    def print_health(self):
        # Print the player's current health.
        print('\n{}'.format(self.__playerName))
        print('HP: {}'.format(self.__playerCurrentHealth))

    def get_name(self):
        # Return the player's name.
        return self.__playerName

    def get_armor(self):
        # Return the player's armor rating for boss damage rolls.
        return self.__playerArmor

    def get_health(self):
        # Return the player's current health.
        return self.__playerCurrentHealth

    def grace(self):
        print('\nRest...') # Rest and prepare for the next battle.
        # Heal the player's current health to their max health.
        self.__playerCurrentHealth = self.__playerMaxHealth
        print('Fully healed and preparing for next battle...')
        time.sleep(0.70)
        print('-' * 30)

    def reduce_health(self, damage = 0):
        # Reduce the player's current health by the damage amount.
        self.__playerCurrentHealth -= damage
        
        # If the player's health is reduced below 0, then set the
        # health value at 0 instead.
        if self.__playerCurrentHealth < 0:
            self.__playerCurrentHealth = 0

    def attack(self):
        # Perform a d10 die roll to determine the player's damage done to the
        # boss. The damage dealt is equal to a percentage of player's current
        # attack rating. The percentage is based off the results of the d10
        # die roll. For example, a roll of 4 will do 40% of the player's
        # attack rating in damage.
        # Round the damage number up to nearest whole number.
        return math.ceil(self.__playerAttack * (roll_d10() / 10))