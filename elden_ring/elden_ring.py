"""
elden_ring.py

Listen up, brother! This is the main module for the Elden Ring CLI game, where you get to face off against
the toughest bosses from Elden Ring. You'll be battling the tutorial boss Soldier of Godrick and a majority
of the field, mini, and main bosses. The game uses a random die roll of 1-20 to decide if the Tarnished
was able to attack the boss and dodge/block the boss' attack.

You'll start by selecting your class using the pyinputplus module and a list of .json files stored in
elden_ring/classes. Each .json file contains the class name followed by each stat and their values for
each Elden Ring starting class (e.g. Vig: 0). The stats are followed by the 6 equipment slots for the
character including Right Hand, Left Hand, Helm, Torso, Wrists, and Legs.

Get ready to step into the ring and show those bosses what you're made of, brother!

Functions:
    single_player_game():
        Function for a single player version of the program. Includes the tutorial boss fight as well as
        a single field, mini, and main boss fight.

    two_player_game():
        Function for a two player version of the program. Includes the tutorial boss fight as well as
        a single field, mini, and main boss fight. This version will exit the program early if the host
        object reaches 0 hp.

    three_player_game():
        Function for a three player version of the program. Includes the tutorial boss fight as well as
        a single field, mini, and main boss fight. This version will exit the program early if the host
        object reaches 0 hp.

    main():
        Main function to call when running the program. This will get the number of players and run the
        appropriate game mode based on the number of players joining the fight(s).
"""

import sys
import time

try:
    import pyinputplus as pyip
except ImportError:
    print("\nPlease install the missing module: pyinputplus.")
    sys.exit(1)
try:
    import character
    import boss
    import battles
except ImportError:
    print("\nPlease ensure the following modules are available:\n\
        - character.py\n\
        - boss.py\n\
        - battles.py")
    sys.exit(1)


PLAYER_REST_TIME = 2.5              # Amount of time to wait for players to rest.

def single_player_game():
    """single_player_game Function for a single player version of the program.
    Includes the tutorial boss fight as well as a single field, mini and main
    boss fight.
    """
    player_one = character.Character() # Create the player object.
    boss_one = boss.Boss()             # Create the boss object.
    player_one.print_stats() # Display the player's stats.

    battles.tutorial_boss_fight(player_one, boss_one) # Begin the tutorial boss fight.
    player_one.grace()   # Rest and heal the player.
    time.sleep(PLAYER_REST_TIME)

    battles.field_boss_fight(player_one, boss_one)    # Begin the field boss fight.
    player_one.grace()
    time.sleep(PLAYER_REST_TIME)

    battles.mini_boss_fight(player_one, boss_one) # Begin the mini boss fight.
    player_one.grace()
    time.sleep(PLAYER_REST_TIME)

    battles.main_boss_fight(player_one, boss_one) # Begin the main boss fight.


def two_player_game():
    """two_player_game Function for a two player version of the program.
    Includes the tutorial boss fight as well as a single field, mini and main
    boss fight. This version will exit the program early if the host object
    reaches 0 hp.
    """
    host = character.Character()          # Create the host object.
    summon_one = character.Character()     # Create the first summon object.
    players = [host, summon_one] # Create the player list.
    boss_one = boss.Boss()    # Create the boss object.

    host.print_stats()          # Display the host's stats.
    print()
    summon_one.print_stats()     # Display the first summon's stats.

    # Begin the tutorial boss fight.
    battles.two_player_tutorial_boss_fight(players, boss_one)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(PLAYER_REST_TIME)

    # Begin the field boss fight.
    battles.two_player_field_boss_fight(players, boss_one)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(PLAYER_REST_TIME)

    # Begin the mini boss fight.
    battles.two_player_mini_boss_fight(players, boss_one)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(PLAYER_REST_TIME)

    # Begin the main boss fight.
    battles.two_player_main_boss_fight(players, boss_one)


def three_player_game():
    """three_player_game Function for a three player version of the program.
    Includes the tutorial boss fight as well as a single field, mini and main
    boss fight. This version will exit the program early if the host object
    reaches 0 hp.
    """
    host = character.Character()            # Create the host object.
    summon_one = character.Character()       # Create the first summon object.
    summon_two = character.Character()       # Create the second summon object.
    players = [host, summon_one, summon_two]  # Create the player list.
    boss_one = boss.Boss()    # Create the boss object.

    host.print_stats()          # Display the host's stats.
    print()
    summon_one.print_stats()     # Display the first summon's stats.
    print()
    summon_two.print_stats()     # Display the second summon's stats.

    # Begin the tutorial boss fight.
    battles.three_player_tutorial_boss_fight(players, boss_one)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(PLAYER_REST_TIME)

    # Begin the field boss fight.
    battles.three_player_field_boss_fight(players, boss_one)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(PLAYER_REST_TIME)

    # Begin the mini boss fight.
    battles.three_player_mini_boss_fight(players, boss_one)
    for player in players:  # Rest and heal each of the players
        player.grace()
    time.sleep(PLAYER_REST_TIME)

    # Begin the main boss fight.
    battles.three_player_main_boss_fight(players, boss_one)


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
