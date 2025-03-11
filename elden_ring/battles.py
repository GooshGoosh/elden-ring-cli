"""
battles.py

Listen up, brother! This module contains the functions to handle all the epic battles in the Elden Ring CLI game.
We're talking player and boss attack phases, and different types of boss fights like tutorial, field, mini,
and main boss fights.
Whether you're going solo or teaming up with your buddies (up to three players), this module has got you covered!

Functions:
    roll_d20(advantage=False, disadvantage=False) -> int:
        Generates a random number between 1 and 20, with optional advantage or disadvantage, brother!

    player_attack_phase(player_obj, boss_obj):
        Handles the player's attack phase against the boss, brother!

    boss_attack_phase(player_obj, boss_obj):
        Handles the boss's attack phase against the player, brother!

    tutorial_boss_fight(player_obj, boss_obj):
        Manages the tutorial boss fight for a single player, brother!

    two_player_tutorial_boss_fight(player_list, boss_obj):
        Manages the tutorial boss fight for two players, brother!

    three_player_tutorial_boss_fight(player_list, boss_obj):
        Manages the tutorial boss fight for three players, brother!

    field_boss_fight(player_obj, boss_obj):
        Manages a field boss fight for a single player, brother!

    two_player_field_boss_fight(player_list, boss_obj):
        Manages a field boss fight for two players, brother!

    three_player_field_boss_fight(player_list, boss_obj):
        Manages a field boss fight for three players, brother!

    mini_boss_fight(player_obj, boss_obj):
        Manages a mini boss fight for a single player, brother!

    two_player_mini_boss_fight(player_list, boss_obj):
        Manages a mini boss fight for two players, brother!

    three_player_mini_boss_fight(player_list, boss_obj):
        Manages a mini boss fight for three players, brother!

    main_boss_fight(player_obj, boss_obj):
        Manages a main boss fight for a single player, brother!

    two_player_main_boss_fight(player_list, boss_obj):
        Manages a main boss fight for two players, brother!

    three_player_main_boss_fight(player_list, boss_obj):
        Manages a main boss fight for three players, brother!
"""

import time
import secrets
import sys


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
        return max(secrets.SystemRandom().randrange(1,21), secrets.SystemRandom().randrange(1,21))

    if disadvantage:
        return min(secrets.SystemRandom().randrange(1,21), secrets.SystemRandom().randrange(1,21))

    return secrets.SystemRandom().randrange(1,21)


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
        input("\nPress 'ENTER' to roll for damage...")
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
        print('\nRolling for damage...')
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
    # Set the boss' runes and weapon to drop if defeated.
    runes = boss_obj.get_runes()
    dropped_weapon = boss_obj.drop_weapon(chance=10)

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

    # Give the player the chance to equip the dropped weapon.
    print(f'Boss dropped {dropped_weapon.iloc[0,0]}!')
    time.sleep(1.5)
    player_obj.change_weapon(dropped_weapon)

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

    # Set the boss' runes and weapon to drop if defeated.
    runes = boss_obj.get_runes()
    dropped_weapon = boss_obj.drop_weapon(chance=10)

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

    # Give the player the chance to equip the dropped weapon.
    print(f'Boss dropped {dropped_weapon.iloc[0,0]}!')
    time.sleep(1.5)
    host_obj.change_weapon(dropped_weapon)
    summon_one.change_weapon(dropped_weapon)

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

    # Set the boss' runes and weapon to drop if defeated.
    runes = boss_obj.get_runes()
    dropped_weapon = boss_obj.drop_weapon(chance=10)

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

    # Give the player the chance to equip the dropped weapon.
    print(f'Boss dropped {dropped_weapon.iloc[0,0]}!')
    time.sleep(1.5)
    host_obj.change_weapon(dropped_weapon)
    summon_one.change_weapon(dropped_weapon)
    summon_two.change_weapon(dropped_weapon)

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
    dropped_weapon = boss_obj.drop_weapon(chance=5) # Set the boss' dropped weapon.

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

    # Give the player the chance to equip the dropped weapon.
    print(f'Boss dropped {dropped_weapon.iloc[0,0]}!')
    time.sleep(1.5)
    player_obj.change_weapon(dropped_weapon)

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
    dropped_weapon = boss_obj.drop_weapon(chance=5) # Set the boss' dropped weapon.

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

    # Give the player the chance to equip the dropped weapon.
    print(f'Boss dropped {dropped_weapon.iloc[0,0]}!')
    time.sleep(1.5)
    host_obj.change_weapon(dropped_weapon)
    summon_one.change_weapon(dropped_weapon)

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
    dropped_weapon = boss_obj.drop_weapon(chance=5) # Set the boss' dropped weapon.

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

    # Give the player the chance to equip the dropped weapon.
    print(f'Boss dropped {dropped_weapon.iloc[0,0]}!')
    time.sleep(1.5)
    host_obj.change_weapon(dropped_weapon)
    summon_one.change_weapon(dropped_weapon)
    summon_two.change_weapon(dropped_weapon)

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
    dropped_weapon = boss_obj.drop_weapon(chance=1) # Set the boss' dropped weapon.

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

    # Give the player the chance to equip the dropped weapon.
    print(f'Boss dropped {dropped_weapon.iloc[0,0]}!')
    time.sleep(1.5)
    player_obj.change_weapon(dropped_weapon)

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
    dropped_weapon = boss_obj.drop_weapon(chance=1) # Set the boss' dropped weapon.

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

    # Give the player the chance to equip the dropped weapon.
    print(f'Boss dropped {dropped_weapon.iloc[0,0]}!')
    time.sleep(1.5)
    host_obj.change_weapon(dropped_weapon)
    summon_one.change_weapon(dropped_weapon)

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
    dropped_weapon = boss_obj.drop_weapon(chance=1) # Set the boss' dropped weapon.

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

    # Give the player the chance to equip the dropped weapon.
    print(f'Boss dropped {dropped_weapon.iloc[0,0]}!')
    time.sleep(1.5)
    host_obj.change_weapon(dropped_weapon)
    summon_one.change_weapon(dropped_weapon)
    summon_two.change_weapon(dropped_weapon)

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
