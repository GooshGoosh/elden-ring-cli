import random
import math
import sys
import os
import pandas as pd
import time


def roll_d10():
    # Roll a number in the range 1-10 and return it.
    return random.randrange(1,11)


# Class for the boss character.
class Boss():
    __bossesPath = os.path.abspath(f'./bosses/') 

    def __init__(self):
        # Set the starter/tutorial boss name, health, attack, and armor.
        self.__bossHpDivisor = 2
        self.__bossName = 'Soldier of Godrick'
        self.__bossHealth = math.ceil(384 / self.__bossHpDivisor)
        self.__bossAttack = 10
        self.__bossArmor = 7

    def set_field_boss(self):
        # Set the boss stats for a field boss.
        self.__filePath = os.path.join(Boss.__bossesPath,
                                       'field-boss-list.csv')
        self.__bossHpDivisor = 4
        self.__bossHealth = 500
        self.__bossAttack = 15
        self.__bossArmor = 9

        # Read the field boss list file and create a list of field bosses.
        try:
            self.__df = pd.read_csv(self.__filePath,sep=';')
            self.__bossData = self.__df.sample()
            self.__bossName = self.__bossData.iloc[0,0]
            self.__bossHealth = math.ceil(self.__bossData.iloc[0,1]
                                          / self.__bossHpDivisor)
        except FileNotFoundError:
            print('\nFile {} not found! Exiting...'.format(self.__filePath))
            time.sleep(1.5)
            sys.exit(1)
        except IndexError:
            print('\nError: Index out of range in boss data! Exiting...')
            time.sleep(1.5)
            sys.exit(1)

    def set_mini_boss(self):
        # Set the boss stats for a mini boss.
        self.__filePath = os.path.join(Boss.__bossesPath,
                                       'mini-boss-list.csv')
        self.__bossHpDivisor = 6
        self.__bossHealth = 800
        self.__bossAttack = 20
        self.__bossArmor = 11

        # Read the mini boss list file and create a list of mini bosses.
        try:
            self.__df = pd.read_csv(self.__filePath,sep=';')
            self.__bossData = self.__df.sample()
            self.__bossName = self.__bossData.iloc[0,0]
            self.__bossHealth = math.ceil(self.__bossData.iloc[0,1]
                                          / self.__bossHpDivisor)
        except FileNotFoundError:
            print('\nFile {} not found! Exiting...'.format(self.__filePath))
            time.sleep(1.5)
            sys.exit(1)
        except IndexError:
            print('\nError: Index out of range in boss data! Exiting...')
            time.sleep(1.5)
            sys.exit(1)

    def set_main_boss(self):
        # Set the boss stats for the main boss.
        self.__filePath = os.path.join(Boss.__bossesPath,
                                       'main-boss-list.csv')
        self.__bossHpDivisor = 8
        self.__bossHealth = 1200
        self.__bossAttack = 25
        self.__bossArmor = 13

        # Read the main boss list file and create a list of main bosses.
        try:
            self.__df = pd.read_csv(self.__filePath,sep=';')
            self.__bossData = self.__df.sample()
            self.__bossName = self.__bossData.iloc[0,0]
            self.__bossHealth = math.ceil(self.__bossData.iloc[0,1]
                                          / self.__bossHpDivisor)
        except FileNotFoundError:
            print('\nFile {} not found! Exiting...'.format(self.__filePath))
            time.sleep(1.5)
            sys.exit(1)
        except IndexError:
            print('\nError: Index out of range in boss data! Exiting...')
            time.sleep(1.5)
            sys.exit(1)

    def print_stats(self):
        # Print the boss' name and health.
        print('\n{}'.format(self.__bossName))
        print('HP: {}'.format(self.__bossHealth))

    def get_health(self):
        # Return the boss' health.
        return self.__bossHealth

    def get_armor(self):
        # Return the boss' armor for player damage rolls.
        return self.__bossArmor

    def get_name(self):
        # Return the boss' name.
        return self.__bossName

    def reduce_health(self, damage = 0):
        # Reduce the boss' health by the damage amount.
        self.__bossHealth -= damage

    def attack(self):
        # Perform a d10 die roll to determine the boss' damage done to the
        # player. The damage dealt is equal to a percentage of the boss'
        # current attack rating. The percentage is based off the results of
        # the d10 die roll. For example, a roll of 4 will do 40% of the boss'
        # attack rating in damage.
        # Round the damage number up to nearest whole number.
        return math.ceil(self.__bossAttack * (roll_d10() / 10))