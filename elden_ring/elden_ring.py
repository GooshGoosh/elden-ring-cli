# Author: Alex Grecinger
# Copyright (C) 2023 Alex Grecinger


"""
elden_ring.py - Mini Elden Ring-based game that lets the user
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
"""


import random
import sys
import time
import os
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


PATH = os.path.abspath(__file__)    # Current directory of the executing file.
PLAYER_REST_TIME = 2.5              # Amount of time to wait for players to rest.

def roll_d20(advantage=False, disadvantage=False):
    """roll_d20 Generate a random number in the range 1-20 (inclusive) and
    return it. If the roller has advantage, then generate two numbers and return
    the higher number. If the roller has disadvantage, then generate two numbers
    and return the lower number.

    Args:
        advantage (bool, optional): Determines if the greater of two numbers
        should be returned. Defaults to False.
        disadvantage (bool, optional): Determines if the less of two numbers
        should be returned. Defaults to False.

    Returns:
        int: The number to determine if the player/boss successfully land an
        attack.
    """
    if advantage:
        return max(random.randrange(1,21), random.randrange(1,21))

    if disadvantage:
        return min(random.randrange(1,21), random.randrange(1,21))

    return random.randrange(1,21)


def player_attack_phase(player_obj, boss_obj):
    """player_attack_phase Allows the player to perform an attack on the boss.
    Uses input() so the fight is more interactive for the user.

    Args:
        player_obj (character.Character): Object of the player performing
        the attack.
        boss_obj (boss.Boss): Object of the boss being targeted by the attack.
    """
    print(f'\n{player_obj.get_name()} attack phase.')
    input("Press 'ENTER' to roll for attack...")
    if roll_d20() < boss_obj.get_armor():    # Attack roll fails if the boss'
        print('Attack roll failed!')        # armor is higher than the roll.
        time.sleep(1.5)   # Pause for the player to read the roll result.
    else:
        print('Attack roll success!')
        time.sleep(0.5)
        input("Press 'ENTER' to roll for damage...")
        time.sleep(0.5)
        # Get the damage done to the boss, reduce the boss' health, and let
        # the player know how much damage was done to the boss.
        dmg = player_obj.attack()
        boss_obj.reduce_health(dmg)
        print(f'Hit {boss_obj.get_name()} for {dmg} damage!')
        time.sleep(1.5)


def boss_attack_phase(player_obj, boss_obj):
    """boss_attack_phase Allows the boss to perform an attack on the player.

    Args:
        player_obj (character.Character): Object of the player being targeted by
        the attack.
        boss_obj (boss.Boss): Object of the boss performing the attack.
    """
    print('\nBoss attack phase.')
    if roll_d20() < player_obj.get_armor():  # Attack roll fails if the
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
        dmg = boss_obj.attack()
        player_obj.reduce_health(dmg)
        print(f'Hit {player_obj.get_name()} for {dmg} damage!')
        # Allow the player to interactively proceed to the next phase.
        input("\nPress 'ENTER' to continue...")


def tutorial_boss_fight(player_obj, boss_obj):
    """tutorial_boss_fight Function to fight the tutorial boss
    "Soldier of Godrick". This should be the first fight performed by the player
    and should only occur once in the program. This version is to be used for
    one player.

    Args:
        player_obj (character.Character): Object of the player in the fight.
        boss_obj (boss.Boss): Object of the boss in the fight.
    """
    # Set the boss' runes to drop if defeated.
    runes = boss_obj.get_runes()
    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print(f'Begin fight VS {boss_obj.get_name()}')
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while player_obj.get_health() > 0 and boss_obj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        player_obj.print_health()   # Display the player's current hp.
        boss_obj.print_stats()      # Display the boss' current hp.
        time.sleep(0.75)

        # Begin player attack phase.
        player_attack_phase(player_obj, boss_obj)
        if boss_obj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(player_obj, boss_obj)

    # If the player has no hp, then show a defeat screen and exit the program.
    if player_obj.get_health() <= 0:
        print('\nYOU DIED\n')
        time.sleep(1)
        sys.exit(0)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)

    # Update the player's runes value.
    print(f'You gained {runes} runes.\n')
    player_obj.add_runes(runes)
    print(f'You currently have {player_obj.get_runes()} runes.')
    time.sleep(1)

    # Make the rest action interactive for the player.
    input("\nPress'ENTER' to rest...")


def two_player_tutorial_boss_fight(player_list, boss_obj):
    """two_player_tutorial_boss_fight Function fight the tutorial boss
    "Soldier of Godrick". This should be the first fight performed by the player
    and should only occur once in the program. This version is to be used for
    two players.

    Args:
        player_list (list): List of player objects in the fight.
        boss_obj (boss.Boss): Object of the boss in the fight.
    """
    # Set the players from the list to separate variables.
    host_obj = player_list[0]
    summon_one = player_list[1]

    # Set the boss' runes to drop if defeated.
    runes = boss_obj.get_runes()
    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print('Begin fight VS {boss_obj.get_name()}')
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while host_obj.get_health() > 0 and boss_obj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        host_obj.print_health()     # Display the player's current hp.
        summon_one.print_health()   # Display the first summon's hp.
        boss_obj.print_stats()      # Display the boss' current hp.
        time.sleep(0.75)

        # Begin host attack phase.
        player_attack_phase(host_obj, boss_obj)
        if boss_obj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(host_obj, boss_obj)
        else:
            # Break from the loop if the boss dies from the host's attack.
            break

        # If the host has no hp, then show a defeat screen and exit the program.
        if host_obj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)

        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summon_one.get_health() != 0 and boss_obj.get_health() > 0:
            player_attack_phase(summon_one, boss_obj)
            if boss_obj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summon_one, boss_obj)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)

    # Update the player's runes value.
    print(f'You gained {runes} runes.\n')
    host_obj.add_runes(runes)
    summon_one.add_runes(runes)
    print(f'{host_obj.get_name()} currently has {host_obj.get_runes()} runes.')
    print(f'{summon_one.get_name()} currently has {summon_one.get_runes()} runes.')
    time.sleep(1)

    # Make the rest action interactive for the player.
    input("\nPress'ENTER' to rest...")


def three_player_tutorial_boss_fight(player_list, boss_obj):
    """three_player_tutorial_boss_fight Function to fight the tutorial boss
    "Soldier of Godrick". This should be the first fight performed by the player
    and should only occur once in the program. This version is to be used for
    three players.

    Args:
        player_list (list): List of player objects in the fight.
        boss_obj (boss.Boss): Object of the boss in the fight.
    """
    # Set the players from the list to separate variables.
    host_obj = player_list[0]
    summon_one = player_list[1]
    summon_two = player_list[2]

    # Set the boss' runes to drop if defeated.
    runes = boss_obj.get_runes()
    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print(f'Begin fight VS {boss_obj.get_name()}')
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while host_obj.get_health() > 0 and boss_obj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        host_obj.print_health()     # Display the player's current hp.
        summon_one.print_health()   # Display the first summon's hp.
        summon_two.print_health()   # Display the second summon's hp.
        boss_obj.print_stats()      # Display the boss' current hp.
        time.sleep(0.75)

        # Begin host attack phase.
        player_attack_phase(host_obj, boss_obj)
        if boss_obj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(host_obj, boss_obj)
        else:
            # Break from the loop if the boss dies from the host's attack.
            break

        # If the host has no hp, then show a defeat screen and exit the program.
        if host_obj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)

        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summon_one.get_health() != 0 and boss_obj.get_health() > 0:
            player_attack_phase(summon_one, boss_obj)
            if boss_obj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summon_one, boss_obj)

        # Begin second summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summon_two.get_health() != 0 and boss_obj.get_health() > 0:
            player_attack_phase(summon_two, boss_obj)
            if boss_obj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summon_two, boss_obj)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)

    # Update the player's runes value.
    print(f'You gained {runes} runes.\n')
    host_obj.add_runes(runes)
    summon_one.add_runes(runes)
    summon_two.add_runes(runes)
    print(f'{host_obj.get_name()} currently has {host_obj.get_runes()} runes.')
    print(f'{summon_one.get_name()} currently has {summon_one.get_runes()} runes.')
    print(f'{summon_two.get_name()} currently has {summon_two.get_runes()} runes.')
    time.sleep(1)

    # Make the rest action interactive for the player.
    input("\nPress'ENTER' to rest...")


def field_boss_fight(player_obj, boss_obj):
    """field_boss_fight Function to fight a random field boss from the field
    boss list file. This version is to be used for one player.

    Args:
        player_obj (character.Character): Object of the player in the fight.
        boss_obj (boss.Boss): Object of the boss in the fight.
    """
    # Set the boss stats to the stats appropriate for a field boss.
    boss_obj.set_field_boss()
    runes = boss_obj.get_runes()    # Set the boss' runes to drop if defeated.

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print(f'Begin fight VS {boss_obj.get_name()}')
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while player_obj.get_health() > 0 and boss_obj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        player_obj.print_health()   # Display the player's current hp.
        boss_obj.print_stats()      # Display the boss' current hp.
        time.sleep(0.75)

        # Begin player attack phase.
        player_attack_phase(player_obj, boss_obj)
        if boss_obj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(player_obj, boss_obj)

    # If the player has no hp, then show a defeat screen and exit the program.
    if player_obj.get_health() <= 0:
        print('\nYOU DIED\n')
        time.sleep(1)
        sys.exit(0)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)

    # Update the player's runes value.
    print(f'You gained {runes} runes.\n')
    player_obj.add_runes(runes)
    print(f'You currently have {player_obj.get_runes()} runes.')
    time.sleep(1)

    # Make the rest action interactive for the player.
    input("\nPress'ENTER' to rest...")


def two_player_field_boss_fight(player_list, boss_obj):
    """two_player_field_boss_fight Function to fight a random field boss from the
    field boss list file. This version is to be used for two players.

    Args:
        player_list (list): List of the player objects in the fight.
        boss_obj (boss.Boss): Object of the boss in the fight.
    """
    # Set the players from the list to separate variables.
    host_obj = player_list[0]
    summon_one = player_list[1]

    # Set the boss stats to the stats appropriate for a field boss.
    boss_obj.set_field_boss()
    runes = boss_obj.get_runes()    # Set the boss' runes to drop if defeated.

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print(f'Begin fight VS {boss_obj.get_name()}')
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while host_obj.get_health() > 0 and boss_obj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        host_obj.print_health()     # Display the player's current hp.
        summon_one.print_health()   # Display the first summon's current hp.
        boss_obj.print_stats()      # Display the boss' current hp.
        time.sleep(0.75)

        # Begin player attack phase.
        player_attack_phase(host_obj, boss_obj)
        if boss_obj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(host_obj, boss_obj)
        else:
            # Break out of the loop if the boss dies to the host's attack.
            break

        # If the host has no hp, then show a defeat screen and exit the program.
        if host_obj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)

        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summon_one.get_health() != 0 and boss_obj.get_health() > 0:
            player_attack_phase(summon_one, boss_obj)
            if boss_obj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summon_one, boss_obj)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)

    # Update the player's runes value.
    print(f'You gained {runes} runes.\n')
    host_obj.add_runes(runes)
    summon_one.add_runes(runes)
    print(f'{host_obj.get_name()} currently has {host_obj.get_runes()} runes.')
    print(f'{summon_one.get_name()} currently has {summon_one.get_runes()} runes.')
    time.sleep(1)

    # Make the rest action interactive for the player.
    input("\nPress'ENTER' to rest...")


def three_player_field_boss_fight(player_list, boss_obj):
    """three_player_field_boss_fight Function to fight a random field boss from the
    field boss list file. This version is to be used for three players.

    Args:
        player_list (list): List of the player objects in the fight.
        boss_obj (boss.Boss): Object of the boss in the fight.
    """
    # Set the players from the list to separate variables.
    host_obj = player_list[0]
    summon_one = player_list[1]
    summon_two = player_list[2]

    # Set the boss stats to the stats appropriate for a field boss.
    boss_obj.set_field_boss()
    runes = boss_obj.get_runes()    # Set the boss' runes to drop if defeated.

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print(f'Begin fight VS {boss_obj.get_name()}')
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while host_obj.get_health() > 0 and boss_obj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        host_obj.print_health()     # Display the player's current hp.
        summon_one.print_health()   # Display the first summon's current hp.
        summon_two.print_health()   # Display the second summon's current hp.
        boss_obj.print_stats()      # Display the boss' current hp.
        time.sleep(0.75)

        # Begin player attack phase.
        player_attack_phase(host_obj, boss_obj)
        if boss_obj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(host_obj, boss_obj)
        else:
            # Break out of the loop if the boss dies to the host's attack.
            break

        # If the host has no hp, then show a defeat screen and exit the program.
        if host_obj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)

        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summon_one.get_health() != 0 and boss_obj.get_health() > 0:
            player_attack_phase(summon_one, boss_obj)
            if boss_obj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summon_one, boss_obj)

        # Begin the second summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summon_two.get_health() != 0 and boss_obj.get_health() > 0:
            player_attack_phase(summon_two, boss_obj)
            if boss_obj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summon_two, boss_obj)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)

    # Update the player's runes value.
    print(f'You gained {runes} runes.\n')
    host_obj.add_runes(runes)
    summon_one.add_runes(runes)
    summon_two.add_runes(runes)
    print(f'{host_obj.get_name()} currently has {host_obj.get_runes()} runes.')
    print(f'{summon_one.get_name()} currently has {summon_one.get_runes()} runes.')
    print(f'{summon_two.get_name()} currently has {summon_two.get_runes()} runes.')
    time.sleep(1)

    # Make the rest action interactive for the player.
    input("\nPress'ENTER' to rest...")


def mini_boss_fight(player_obj, boss_obj):
    """mini_boss_fight Function to fight a random mini boss from the mini boss
    list file. This version is to be used for one player.

    Args:
        player_obj (character.Character): Object of the player in the fight.
        boss_obj (boss.Boss): Object of the boss in the fight.
    """
    # Set the boss stats to the stats appropriate for a mini boss.
    boss_obj.set_mini_boss()
    runes = boss_obj.get_runes()    # Set the boss' runes to drop if defeated.

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print(f'Begin fight VS {boss_obj.get_name()}')
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while player_obj.get_health() > 0 and boss_obj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        player_obj.print_health()   # Display the player's current hp.
        boss_obj.print_stats()      # Display the boss' current hp.
        time.sleep(0.75)

        # Begin player attack phase.
        player_attack_phase(player_obj, boss_obj)
        if boss_obj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(player_obj, boss_obj)

    # If the player has no hp, then show a defeat screen and exit the program.
    if player_obj.get_health() <= 0:
        print('\nYOU DIED\n')
        time.sleep(1)
        sys.exit(0)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)

    # Update the player's runes value.
    print(f'You gained {runes} runes.\n')
    player_obj.add_runes(runes)
    print(f'You currently have {player_obj.get_runes()} runes.')
    time.sleep(1)

    # Make the rest action interactive for the player.
    input("\nPress'ENTER' to rest...")


def two_player_mini_boss_fight(player_list, boss_obj):
    """two_player_mini_boss_fight Function to fight a random mini boss from the
    mini boss list file. This version is to be used for two players.

    Args:
        player_list (list): List of player objects in the fight.
        boss_obj (boss.Boss): Object of the boss in the fight.
    """
    # Set the players from the list to separate variables.
    host_obj = player_list[0]
    summon_one = player_list[1]

    # Set the boss stats to the stats appropriate for a mini boss.
    boss_obj.set_mini_boss()
    runes = boss_obj.get_runes()    # Set the boss' runes to drop if defeated.

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print(f'Begin fight VS {boss_obj.get_name()}')
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while host_obj.get_health() > 0 and boss_obj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        host_obj.print_health()     # Display the player's current hp.
        summon_one.print_health()   # Display the first summon's current hp.
        boss_obj.print_stats()      # Display the boss' current hp.
        time.sleep(0.75)

        # Begin player attack phase.
        player_attack_phase(host_obj, boss_obj)
        if boss_obj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(host_obj, boss_obj)
        else:
            # Break from the loop if the boss dies from the host's attack.
            break

        # If the host has no hp, then show a defeat screen and exit the program.
        if host_obj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)

        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summon_one.get_health() != 0 and boss_obj.get_health() > 0:
            player_attack_phase(summon_one, boss_obj)
            if boss_obj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summon_one, boss_obj)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)

    # Update the player's runes value.
    print(f'You gained {runes} runes.\n')
    host_obj.add_runes(runes)
    summon_one.add_runes(runes)
    print(f'{host_obj.get_name()} currently has {host_obj.get_runes()} runes.')
    print(f'{summon_one.get_name()} currently has {summon_one.get_runes()} runes.')
    time.sleep(1)

    # Make the rest action interactive for the player.
    input("\nPress'ENTER' to rest...")


def three_player_mini_boss_fight(player_list, boss_obj):
    """three_player_mini_boss_fight Function to fight a random mini boss from
    the mini boss list file. This version is to be used for three players.

    Args:
        player_list (list): List of player objects in the fight.
        boss_obj (boss.Boss): Object of the boss in the fight.
    """
    # Set the players from the list to separate variables.
    host_obj = player_list[0]
    summon_one = player_list[1]
    summon_two = player_list[2]

    # Set the boss stats to the stats appropriate for a mini boss.
    boss_obj.set_mini_boss()
    runes = boss_obj.get_runes()    # Set the boss' runes to drop if defeated.

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print(f'Begin fight VS {boss_obj.get_name()}')
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while host_obj.get_health() > 0 and boss_obj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        host_obj.print_health()     # Display the player's current hp.
        summon_one.print_health()   # Display the first summon's current hp.
        summon_two.print_health()   # Display the second summon's current hp.
        boss_obj.print_stats()      # Display the boss' current hp.
        time.sleep(0.75)

        # Begin player attack phase.
        player_attack_phase(host_obj, boss_obj)
        if boss_obj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(host_obj, boss_obj)
        else:
            # Break from the loop if the boss dies from the host's attack.
            break

        # If the host has no hp, then show a defeat screen and exit the program.
        if host_obj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)

        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summon_one.get_health() != 0 and boss_obj.get_health() > 0:
            player_attack_phase(summon_one, boss_obj)
            if boss_obj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summon_one, boss_obj)

        # Begin second summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summon_two.get_health() != 0 and boss_obj.get_health() > 0:
            player_attack_phase(summon_two, boss_obj)
            if boss_obj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summon_two, boss_obj)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)

    # Update the player's runes value.
    print(f'You gained {runes} runes.\n')
    host_obj.add_runes(runes)
    summon_one.add_runes(runes)
    summon_two.add_runes(runes)
    print(f'{host_obj.get_name()} currently has {host_obj.get_runes()} runes.')
    print(f'{summon_one.get_name()} currently has {summon_one.get_runes()} runes.')
    print(f'{summon_two.get_name()} currently has {summon_two.get_runes()} runes.')
    time.sleep(1)

    # Make the rest action interactive for the player.
    input("\nPress'ENTER' to rest...")


def main_boss_fight(player_obj, boss_obj):
    """main_boss_fight Function to fight a random main boss from the main boss
    list file. This version is to be used for one player.

    Args:
        player_obj (character.Character): Object of the player in the fight.
        boss_obj (boss.Boss): Object of the boss in the fight.
    """
    # Set the boss stats to the stats appropriate for a main boss.
    boss_obj.set_main_boss()
    runes = boss_obj.get_runes()    # Set the boss' runes to drop if defeated.

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print(f'Begin fight VS {boss_obj.get_name()}')
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while player_obj.get_health() > 0 and boss_obj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        player_obj.print_health()   # Display the player's current hp.
        boss_obj.print_stats()      # Display the boss' current hp.
        time.sleep(0.75)

        # Begin player attack phase.
        player_attack_phase(player_obj, boss_obj)
        if boss_obj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(player_obj, boss_obj)

    # If the player has no hp, then show a defeat screen and exit the program.
    if player_obj.get_health() <= 0:
        print('\nYOU DIED\n')
        time.sleep(1)
        sys.exit(0)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)

    # Update the player's runes value.
    print(f'You gained {runes} runes.\n')
    player_obj.add_runes(runes)
    print(f'You currently have {player_obj.get_runes()} runes.')
    time.sleep(1)

    # Make the exit action interactive for the player.
    input("\nPress'ENTER' to end journey...")


def two_player_main_boss_fight(player_list, boss_obj):
    """two_player_main_boss_fight Function to fight a random main boss from the
    main boss list file. This version is to be used for two players.

    Args:
        player_list (list): List of player objects in the fight.
        boss_obj (boss.Boss): Object of the boss in the fight.
    """
    # Set the players from the list to separate variables.
    host_obj = player_list[0]
    summon_one = player_list[1]

    # Set the boss stats to the stats appropriate for a main boss.
    boss_obj.set_main_boss()
    runes = boss_obj.get_runes()    # Set the boss' runes to drop if defeated.

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print(f'Begin fight VS {boss_obj.get_name()}')
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while host_obj.get_health() > 0 and boss_obj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        host_obj.print_health()     # Display the player's current hp.
        summon_one.print_health()   # Display the first summon's current hp.
        boss_obj.print_stats()      # Display the boss' current hp.
        time.sleep(0.75)

        # Begin player attack phase.
        player_attack_phase(host_obj, boss_obj)
        if boss_obj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(host_obj, boss_obj)
        else:
            # Break from the loop if the boss dies from the host's attack.
            break

        # If the host has no hp, then show a defeat screen and exit the program.
        if host_obj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)

        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summon_one.get_health() != 0 and boss_obj.get_health() > 0:
            player_attack_phase(summon_one, boss_obj)
            if boss_obj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summon_one, boss_obj)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)

    # Update the player's runes value.
    print(f'You gained {runes} runes.\n')
    host_obj.add_runes(runes)
    summon_one.add_runes(runes)
    print(f'{host_obj.get_name()} currently has {host_obj.get_runes()} runes.')
    print(f'{summon_one.get_name()} currently has {summon_one.get_runes()} runes.')
    time.sleep(1)

    # Make the rest action interactive for the player.
    input("\nPress'ENTER' to end journey...")


def three_player_main_boss_fight(player_list, boss_obj):
    """three_player_main_boss_fight Function to fight a random boss from the
    main boss list file. This version is to be used for three players.

    Args:
        player_list (list): List of players in the fight.
        boss_obj (boss.Boss): Object of the boss in the fight.
    """
    # Set the players from the list to separate variables.
    host_obj = player_list[0]
    summon_one = player_list[1]
    summon_two = player_list[2]

    # Set the boss stats to the stats appropriate for a main boss.
    boss_obj.set_main_boss()
    runes = boss_obj.get_runes()    # Set the boss' runes to drop if defeated.

    # Introduce the boss to the player and begin the boss fight.
    print('\nA CHALLENGER APPROACHES\n')
    print(f'Begin fight VS {boss_obj.get_name()}')
    time.sleep(1)

    # Loop until either the player or the boss run out of health.
    while host_obj.get_health() > 0 and boss_obj.get_health() > 0:
        # Separate the attack phases for easier readability.
        print('\n' + ('-' * 30))
        host_obj.print_health()     # Display the player's current hp.
        summon_one.print_health()   # Display the first summon's current hp.
        summon_two.print_health()   # Display the second summon's current hp.
        boss_obj.print_stats()      # Display the boss' current hp.
        time.sleep(0.75)

        # Begin player attack phase.
        player_attack_phase(host_obj, boss_obj)
        if boss_obj.get_health() > 0:
            # Begin boss attack phase if the boss is still alive.
            boss_attack_phase(host_obj, boss_obj)
        else:
            # Break from the loop if the boss dies from the host's attack.
            break

        # If the host has no hp, then show a defeat screen and exit the program.
        if host_obj.get_health() == 0:
            print('\nYOU DIED\n')
            time.sleep(1)
            sys.exit(0)

        # Begin first summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summon_one.get_health() != 0 and boss_obj.get_health() > 0:
            player_attack_phase(summon_one, boss_obj)
            if boss_obj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summon_one, boss_obj)

        # Begin second summon attack phase.
        # If the summon's hp reaches 0 or the boss' hp reaches 0,
        # then skip this phase.
        if summon_two.get_health() != 0 and boss_obj.get_health() > 0:
            player_attack_phase(summon_two, boss_obj)
            if boss_obj.get_health() > 0:
                # Begin boss attack phase if the boss is still alive.
                boss_attack_phase(summon_two, boss_obj)

    # If the boss has no hp, then show a victory screen and proceed.
    print('\nENEMY FELLED\n')
    time.sleep(1)

    # Update the player's runes value.
    print(f'You gained {runes} runes.\n')
    host_obj.add_runes(runes)
    summon_one.add_runes(runes)
    summon_two.add_runes(runes)
    print(f'{host_obj.get_name()} currently has {host_obj.get_runes()} runes.')
    print(f'{summon_one.get_name()} currently has {summon_one.get_runes()} runes.')
    print(f'{summon_two.get_name()} currently has {summon_two.get_runes()} runes.')
    time.sleep(1)

    # Make the rest action interactive for the player.
    input("\nPress'ENTER' to end journey...")


def single_player_game():
    """single_player_game Function for a single player version of the program.
    Includes the tutorial boss fight as well as a single field, mini and main
    boss fight.
    """
    player_one = character.Character(PATH) # Create the player object.
    boss_one = boss.Boss(PATH)             # Create the boss object.
    player_one.print_stats() # Display the player's stats.

    tutorial_boss_fight(player_one, boss_one) # Begin the tutorial boss fight.
    player_one.grace()   # Rest and heal the player.
    time.sleep(PLAYER_REST_TIME)

    field_boss_fight(player_one, boss_one)    # Begin the field boss fight.
    player_one.grace()
    time.sleep(PLAYER_REST_TIME)

    mini_boss_fight(player_one, boss_one) # Begin the mini boss fight.
    player_one.grace()
    time.sleep(PLAYER_REST_TIME)

    main_boss_fight(player_one, boss_one) # Begin the main boss fight.


def two_player_game():
    """two_player_game Function for a two player version of the program.
    Includes the tutorial boss fight as well as a single field, mini and main
    boss fight. This version will exit the program early if the host object
    reaches 0 hp.
    """
    host = character.Character(PATH)          # Create the host object.
    summon_one = character.Character(PATH)     # Create the first summon object.
    players = [host, summon_one] # Create the player list.
    boss_one = boss.Boss(PATH)    # Create the boss object.

    host.print_stats()          # Display the host's stats.
    print()
    summon_one.print_stats()     # Display the first summon's stats.

    # Begin the tutorial boss fight.
    two_player_tutorial_boss_fight(players, boss_one)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(PLAYER_REST_TIME)

    # Begin the field boss fight.
    two_player_field_boss_fight(players, boss_one)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(PLAYER_REST_TIME)

    # Begin the mini boss fight.
    two_player_mini_boss_fight(players, boss_one)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(PLAYER_REST_TIME)

    # Begin the main boss fight.
    two_player_main_boss_fight(players, boss_one)


def three_player_game():
    """three_player_game Function for a three player version of the program.
    Includes the tutorial boss fight as well as a single field, mini and main
    boss fight. This version will exit the program early if the host object
    reaches 0 hp.
    """
    host = character.Character(PATH)            # Create the host object.
    summon_one = character.Character(PATH)       # Create the first summon object.
    summon_two = character.Character(PATH)       # Create the second summon object.
    players = [host, summon_one, summon_two]  # Create the player list.
    boss_one = boss.Boss(PATH)    # Create the boss object.

    host.print_stats()          # Display the host's stats.
    print()
    summon_one.print_stats()     # Display the first summon's stats.
    print()
    summon_two.print_stats()     # Display the second summon's stats.

    # Begin the tutorial boss fight.
    three_player_tutorial_boss_fight(players, boss_one)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(PLAYER_REST_TIME)

    # Begin the field boss fight.
    three_player_field_boss_fight(players, boss_one)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(PLAYER_REST_TIME)

    # Begin the mini boss fight.
    three_player_mini_boss_fight(players, boss_one)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(PLAYER_REST_TIME)

    # Begin the main boss fight.
    three_player_main_boss_fight(players, boss_one)


def main():
    """main Main function to call when running the program. This will get the
    number of players and run the appropriate game mode based on the number
    of players joining the fight(s).
    """
    # Get the number of players for the game. There can be a minimum
    # of 1 player (the host) and a maximum of 3 players (2 summons).
    num_of_players = pyip.inputInt(prompt="Enter the number of players. Max 3: ",
                                   min=1, max=3)

    # Start the correct game based on the number of players.
    if num_of_players == 1:
        single_player_game()
    elif num_of_players == 2:
        two_player_game()
    else:
        three_player_game()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print('\nTHANKS FOR PLAYING!')
