#!/usr/bin/env python3

'''
eldenRingOOP.py - Mini Elden Ring-based game that lets the user
the tutorial boss Solder of Godrick and a majority of the field,
mini, and main bosses from Elden Ring. Uses a random die roll of
1-20 to decide if the Tarnished was able to attack the boss and
dodge/block the boss' attack.
Allows class selection via pyinputplus module and a list of .json
files stored in elden_ring/classes. The .json file contains the
class name followed by each stat and their values for each Elden
Ring starting class (e.g. Vig: 0).
The stats are followed by the 6 equipment slots for the character
including Right Hand, Left Hand, Helm, Torso, Wrists, and Legs.
'''


import random
import sys
import os
import time
import json
import math
try:
    import pyinputplus as pyip
except ImportError:
    print("\nPlease install the missing module: pyinputplus.")
    sys.exit(1)
try:
    import character
    import boss
except ImportError:
    print("\nPlease ensure the character.py & boss.py modules are available.")
    sys.exit(1)


def roll_d20(advantage=False, disadvantage=False):
    # Roll a number in the range 1-20 and return it. If the roller has
    # advantage, then roll twice and return the higher number. If the
    # roller has disadvantage, then roll twice and return the lower number.
    # Else, return a single roll of the 20-sided die.
    if advantage:
        return max(random.randrange(1,21), random.randrange(1,21))
    elif disadvantage:
        return min(random.randrange(1,21), random.randrange(1,21))
    else:
        return random.randrange(1,21)


def player_attack_phase(playerObj, bossObj):
    # Allows the player to perform an attack on the boss.
    # Use input() so the fight is interactive for the user.
    print('\n{} attack phase.'.format(playerObj.get_name()))
    input("Press 'ENTER' to roll for attack...")
    if roll_d20() < bossObj.get_armor():    # Attack roll fails if the boss'
        print('Attack roll failed!')        # armor is higher than the roll.
        time.sleep(1.5)   # Pause for the player to read the roll result.
    else:
        print('Attack roll success!')
        time.sleep(0.5)
        input("Press 'ENTER' to roll for damage...")
        time.sleep(0.5)
        # Get the damage done to the boss, reduce the boss' health, and let
        # the player know how much damage was done to the boss.
        dmg = playerObj.attack()
        bossObj.reduce_health(dmg)
        print('Hit {} for {} damage!'.format(bossObj.get_name(), dmg))
        time.sleep(1.5)


def boss_attack_phase(playerObj, bossObj):
    # Allows the boss to perform an attack on the player.
    print('\nBoss attack phase.')
    if roll_d20() < playerObj.get_armor():  # Attack roll fails if the
        print('Attack roll failed!')        # player's armor is higher than
        time.sleep(1.5)                       # the roll result.
    else:
        # Let the player know what steps are happening.
        print('Attack roll success!')
        time.sleep(0.5)
        print('Rolling for damage...')
        time.sleep(0.5)
        # Get the damage done to the player, reduce the player's health, and
        # let the player know how much damage was done to the player.
        dmg = bossObj.attack()
        playerObj.reduce_health(dmg)
        print('Hit {} for {} damage!'.format(playerObj.get_name(), dmg))
        # Allow the player to interactively proceed to the next phase.
        input("Press 'ENTER' to continue...")


# Function to fight the tutorial boss "Soldier of Godrick".
# This should be the first fight performed by the player and should only
# occur once in the program.
def tutorial_boss_fight(playerObj, bossObj):
    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print('Begin fight VS {}'.format(bossObj.get_name()))
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while playerObj.get_health() > 0 and bossObj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        playerObj.print_health()    # Display the player's current hp.
        bossObj.print_stats()       # Display the boss' current hp.

        # Begin player attack phase.
        player_attack_phase(playerObj, bossObj)
        if bossObj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(playerObj, bossObj)

    # If the player has no hp, then show a defeat screen and exit the program.
    if playerObj.get_health() <= 0:
        print('\nYOU DIED\n')
        time.sleep(1)
        sys.exit(0)
    
    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)
    # Make the rest action interactive for the player.
    input("Press'ENTER' to rest...")
    
    
# Function to fight the tutorial boss "Soldier of Godrick".
# This should be the first fight performed by the player and should only
# occur once in the program.
# This version of the function is to be used for two players.
def two_player_tutorial_boss_fight(playerList, bossObj):
    # Set the players from the list to separate variables.
    hostObj = playerList[0]
    summonOne = playerList[1]
    
    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print('Begin fight VS {}'.format(bossObj.get_name()))
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while hostObj.get_health() > 0 and bossObj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        hostObj.print_health()      # Display the player's current hp.
        summonOne.print_health()    # Display the first summon's hp.
        bossObj.print_stats()       # Display the boss' current hp.

        # Begin host attack phase.
        player_attack_phase(hostObj, bossObj)
        if bossObj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(hostObj, bossObj)
        else:
            # Break from the loop if the boss dies from the host's attack.
            break
        
        # If the host has no hp, then show a defeat screen and exit the program.
        if hostObj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)
        
        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summonOne.get_health() != 0 and bossObj.get_health() > 0:
            player_attack_phase(summonOne, bossObj)
            if bossObj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summonOne, bossObj)
    
    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)
    # Make the rest action interactive for the player.
    input("Press'ENTER' to rest...")
    
    
# Function to fight the tutorial boss "Soldier of Godrick".
# This should be the first fight performed by the player and should only
# occur once in the program.
# This version of the function is to be used for three players.
def three_player_tutorial_boss_fight(playerList, bossObj):
    # Set the players from the list to separate variables.
    hostObj = playerList[0]
    summonOne = playerList[1]
    summonTwo = playerList[2]
    
    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print('Begin fight VS {}'.format(bossObj.get_name()))
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while hostObj.get_health() > 0 and bossObj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        hostObj.print_health()      # Display the player's current hp.
        summonOne.print_health()    # Display the first summon's hp.
        summonTwo.print_health()    # Display the second summon's hp.
        bossObj.print_stats()       # Display the boss' current hp.

        # Begin host attack phase.
        player_attack_phase(hostObj, bossObj)
        if bossObj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(hostObj, bossObj)
        else:
            # Break from the loop if the boss dies from the host's attack.
            break
        
        # If the host has no hp, then show a defeat screen and exit the program.
        if hostObj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)
        
        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summonOne.get_health() != 0 and bossObj.get_health() > 0:
            player_attack_phase(summonOne, bossObj)
            if bossObj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summonOne, bossObj)
            
        # Begin second summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summonTwo.get_health() != 0 and bossObj.get_health() > 0:
            player_attack_phase(summonTwo, bossObj)
            if bossObj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summonTwo, bossObj)
    
    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)
    # Make the rest action interactive for the player.
    input("Press'ENTER' to rest...")


def field_boss_fight(playerObj, bossObj):
    # Set the boss stats to the stats appropriate for a field boss.
    bossObj.set_field_boss()

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print('Begin fight VS {}'.format(bossObj.get_name()))
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while playerObj.get_health() > 0 and bossObj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        playerObj.print_health()    # Display the player's current hp.
        bossObj.print_stats()       # Display the boss' current hp.

        # Begin player attack phase.
        player_attack_phase(playerObj, bossObj)
        if bossObj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(playerObj, bossObj)

    # If the player has no hp, then show a defeat screen and exit the program.
    if playerObj.get_health() <= 0:
        print('\nYOU DIED\n')
        time.sleep(1)
        sys.exit(0)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)
    # Make the rest action interactive for the player.
    input("Press'ENTER' to rest...")
    
    
def two_player_field_boss_fight(playerList, bossObj):
    # Set the players from the list to separate variables.
    hostObj = playerList[0]
    summonOne = playerList[1]
    
    # Set the boss stats to the stats appropriate for a field boss.
    bossObj.set_field_boss()

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print('Begin fight VS {}'.format(bossObj.get_name()))
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while hostObj.get_health() > 0 and bossObj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        hostObj.print_health()      # Display the player's current hp.
        summonOne.print_health()    # Display the first summon's current hp.
        bossObj.print_stats()       # Display the boss' current hp.

        # Begin player attack phase.
        player_attack_phase(hostObj, bossObj)
        if bossObj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(hostObj, bossObj)
        else:
            # Break out of the loop if the boss dies to the host's attack.
            break
        
        # If the host has no hp, then show a defeat screen and exit the program.
        if hostObj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)
        
        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summonOne.get_health() != 0 and bossObj.get_health() > 0:
            player_attack_phase(summonOne, bossObj)
            if bossObj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summonOne, bossObj)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)
    # Make the rest action interactive for the player.
    input("Press'ENTER' to rest...")
    
    
def three_player_field_boss_fight(playerList, bossObj):
    # Set the players from the list to separate variables.
    hostObj = playerList[0]
    summonOne = playerList[1]
    summonTwo = playerList[2]
    
    # Set the boss stats to the stats appropriate for a field boss.
    bossObj.set_field_boss()

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print('Begin fight VS {}'.format(bossObj.get_name()))
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while hostObj.get_health() > 0 and bossObj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        hostObj.print_health()      # Display the player's current hp.
        summonOne.print_health()    # Display the first summon's current hp.
        summonTwo.print_health()    # Display the second summon's current hp.
        bossObj.print_stats()       # Display the boss' current hp.

        # Begin player attack phase.
        player_attack_phase(hostObj, bossObj)
        if bossObj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(hostObj, bossObj)
        else:
            # Break out of the loop if the boss dies to the host's attack.
            break
        
        # If the host has no hp, then show a defeat screen and exit the program.
        if hostObj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)
        
        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summonOne.get_health() != 0 and bossObj.get_health() > 0:
            player_attack_phase(summonOne, bossObj)
            if bossObj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summonOne, bossObj)
            
        # Begin the second summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summonTwo.get_health() != 0 and bossObj.get_health() > 0:
            player_attack_phase(summonTwo, bossObj)
            if bossObj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summonTwo, bossObj)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)
    # Make the rest action interactive for the player.
    input("Press'ENTER' to rest...")


def mini_boss_fight(playerObj, bossObj):
    # Set the boss stats to the stats appropriate for a mini boss.
    bossObj.set_mini_boss()

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print('Begin fight VS {}'.format(bossObj.get_name()))
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while playerObj.get_health() > 0 and bossObj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        playerObj.print_health()    # Display the player's current hp.
        bossObj.print_stats()       # Display the boss' current hp.

        # Begin player attack phase.
        player_attack_phase(playerObj, bossObj)
        if bossObj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(playerObj, bossObj)

    # If the player has no hp, then show a defeat screen and exit the program.
    if playerObj.get_health() <= 0:
        print('\nYOU DIED\n')
        time.sleep(1)
        sys.exit(0)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)
    # Make the rest action interactive for the player.
    input("Press'ENTER' to rest...")
    
    
def two_player_mini_boss_fight(playerList, bossObj):
    # Set the players from the list to separate variables.
    hostObj = playerList[0]
    summonOne = playerList[1]
    
    # Set the boss stats to the stats appropriate for a mini boss.
    bossObj.set_mini_boss()

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print('Begin fight VS {}'.format(bossObj.get_name()))
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while hostObj.get_health() > 0 and bossObj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        hostObj.print_health()      # Display the player's current hp.
        summonOne.print_health()    # Display the first summon's current hp.
        bossObj.print_stats()       # Display the boss' current hp.

        # Begin player attack phase.
        player_attack_phase(hostObj, bossObj)
        if bossObj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(hostObj, bossObj)
        else:
            # Break from the loop if the boss dies from the host's attack.
            break
        
        # If the host has no hp, then show a defeat screen and exit the program.
        if hostObj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)
        
        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summonOne.get_health() != 0 and bossObj.get_health() > 0:
            player_attack_phase(summonOne, bossObj)
            if bossObj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summonOne, bossObj)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)
    # Make the rest action interactive for the player.
    input("Press'ENTER' to rest...")
    
    
def three_player_mini_boss_fight(playerList, bossObj):
    # Set the players from the list to separate variables.
    hostObj = playerList[0]
    summonOne = playerList[1]
    summonTwo = playerList[2]
    
    # Set the boss stats to the stats appropriate for a mini boss.
    bossObj.set_mini_boss()

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print('Begin fight VS {}'.format(bossObj.get_name()))
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while hostObj.get_health() > 0 and bossObj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        hostObj.print_health()      # Display the player's current hp.
        summonOne.print_health()    # Display the first summon's current hp.
        summonTwo.print_health()    # Display the second summon's current hp.
        bossObj.print_stats()       # Display the boss' current hp.

        # Begin player attack phase.
        player_attack_phase(hostObj, bossObj)
        if bossObj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(hostObj, bossObj)
        else:
            # Break from the loop if the boss dies from the host's attack.
            break
        
        # If the host has no hp, then show a defeat screen and exit the program.
        if hostObj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)
        
        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summonOne.get_health() != 0 and bossObj.get_health() > 0:
            player_attack_phase(summonOne, bossObj)
            if bossObj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summonOne, bossObj)
            
        # Begin second summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summonTwo.get_health() != 0 and bossObj.get_health() > 0:
            player_attack_phase(summonTwo, bossObj)
            if bossObj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summonTwo, bossObj)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)
    # Make the rest action interactive for the player.
    input("Press'ENTER' to rest...")


def main_boss_fight(playerObj, bossObj):
    # Set the boss stats to the stats appropriate for a main boss.
    bossObj.set_main_boss()

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print('Begin fight VS {}'.format(bossObj.get_name()))
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while playerObj.get_health() > 0 and bossObj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        playerObj.print_health()    # Display the player's current hp.
        bossObj.print_stats()       # Display the boss' current hp.

        # Begin player attack phase.
        player_attack_phase(playerObj, bossObj)
        if bossObj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(playerObj, bossObj)

    # If the player has no hp, then show a defeat screen and exit the program.
    if playerObj.get_health() <= 0:
        print('\nYOU DIED\n')
        time.sleep(1)
        sys.exit(0)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)
    # Make the exit action interactive for the player.
    input("Press'ENTER' to end journey...")
    
    
def two_player_main_boss_fight(playerList, bossObj):
    # Set the players from the list to separate variables.
    hostObj = playerList[0]
    summonOne = playerList[1]
    
    # Set the boss stats to the stats appropriate for a main boss.
    bossObj.set_main_boss()

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print('Begin fight VS {}'.format(bossObj.get_name()))
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while hostObj.get_health() > 0 and bossObj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        hostObj.print_health()      # Display the player's current hp.
        summonOne.print_health()    # Display the first summon's current hp.
        bossObj.print_stats()       # Display the boss' current hp.

        # Begin player attack phase.
        player_attack_phase(hostObj, bossObj)
        if bossObj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(hostObj, bossObj)
        else:
            # Break from the loop if the boss dies from the host's attack.
            break
        
        # If the host has no hp, then show a defeat screen and exit the program.
        if hostObj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)
        
        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summonOne.get_health() != 0 and bossObj.get_health() > 0:
            player_attack_phase(summonOne, bossObj)
            if bossObj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summonOne, bossObj)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)
    # Make the rest action interactive for the player.
    input("Press'ENTER' to end journey...")
    
    
def three_player_main_boss_fight(playerList, bossObj):
    # Set the players from the list to separate variables.
    hostObj = playerList[0]
    summonOne = playerList[1]
    summonTwo = playerList[2]
    
    # Set the boss stats to the stats appropriate for a main boss.
    bossObj.set_main_boss()

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print('Begin fight VS {}'.format(bossObj.get_name()))
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while hostObj.get_health() > 0 and bossObj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        hostObj.print_health()      # Display the player's current hp.
        summonOne.print_health()    # Display the first summon's current hp.
        summonTwo.print_health()    # Display the second summon's current hp.
        bossObj.print_stats()       # Display the boss' current hp.

        # Begin player attack phase.
        player_attack_phase(hostObj, bossObj)
        if bossObj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(hostObj, bossObj)
        else:
            # Break from the loop if the boss dies from the host's attack.
            break
        
        # If the host has no hp, then show a defeat screen and exit the program.
        if hostObj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)
        
        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summonOne.get_health() != 0 and bossObj.get_health() > 0:
            player_attack_phase(summonOne, bossObj)
            if bossObj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summonOne, bossObj)
            
        # Begin second summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summonTwo.get_health() != 0 and bossObj.get_health() > 0:
            player_attack_phase(summonTwo, bossObj)
            if bossObj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summonTwo, bossObj)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)
    # Make the rest action interactive for the player.
    input("Press'ENTER' to end journey...")


def single_player_game():
    playerOne = character.Character() # Create the player object.
    bossOne = boss.Boss()             # Create the boss object.
    playerOne.print_stats() # Display the player's stats.

    tutorial_boss_fight(playerOne, bossOne) # Begin the tutorial boss fight.
    playerOne.grace()   # Rest and heal the player.
    time.sleep(2.5)

    field_boss_fight(playerOne, bossOne)    # Begin the field boss fight.
    playerOne.grace()
    time.sleep(2.5)

    mini_boss_fight(playerOne, bossOne) # Begin the mini boss fight.
    playerOne.grace()
    time.sleep(2.5)

    main_boss_fight(playerOne, bossOne) # Begin the main boss fight.
    
    
def two_player_game():
    host = character.Character()          # Create the host object.
    summonOne = character.Character()     # Create the first summon object.
    players = [host, summonOne] # Create the player list.
    bossOne = boss.Boss()    # Create the boss object.

    host.print_stats()          # Display the host's stats.
    print()
    summonOne.print_stats()     # Display the first summon's stats.

    # Begin the tutorial boss fight.
    two_player_tutorial_boss_fight(players, bossOne)
    for player in players:  # Rest and heal each of the players
        player.grace()    
    time.sleep(2.5)
    
    # Begin the field boss fight.
    two_player_field_boss_fight(players, bossOne)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(2.5)
    
    # Begin the mini boss fight.
    two_player_mini_boss_fight(players, bossOne)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(2.5)
    
    # Begin the main boss fight.
    two_player_main_boss_fight(players, bossOne)
    
    
def three_player_game():
    host = character.Character()            # Create the host object.
    summonOne = character.Character()       # Create the first summon object.
    summonTwo = character.Character()       # Create the second summon object.
    players = [host, summonOne, summonTwo]  # Create the player list.
    bossOne = boss.Boss()    # Create the boss object.

    host.print_stats()          # Display the host's stats.
    print()
    summonOne.print_stats()     # Display the first summon's stats.
    print()
    summonTwo.print_stats()     # Display the second summon's stats.

    # Begin the tutorial boss fight.
    three_player_tutorial_boss_fight(players, bossOne)
    for player in players:  # Rest and heal each of the players
        player.grace()    
    time.sleep(2.5)
    
    # Begin the field boss fight.
    three_player_field_boss_fight(players, bossOne)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(2.5)
    
    # Begin the mini boss fight.
    three_player_mini_boss_fight(players, bossOne)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(2.5)
    
    # Begin the main boss fight.
    three_player_main_boss_fight(players, bossOne)


def main():
    # Get the number of players for the game. There can be a minimum
    # of 1 player (the host) and a maximum of 3 players (2 summons).
    numOfPlayers = pyip.inputInt(prompt="Enter the number of players. Max 3: ", min=1, max=3)
    
    # Start the correct game based on the number of players.
    if numOfPlayers == 1:
        single_player_game()
    elif numOfPlayers == 2:
        two_player_game()
    else:
        three_player_game()
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print('\nTHANKS FOR PLAYING!')

