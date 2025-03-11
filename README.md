# Elden Ring CLI

Listen up, brother! This project lets you simulate fighting bosses from the Elden Ring game in a command-line interface (CLI) environment. Get ready to step into the ring and show those bosses what you're made of!

## Overview

The game can be played with 1 to 3 players (1 host and up to 2 summons) locally. Players choose their starting class and name their character to begin their journey. Players then engage in a series of 4 boss fights, starting with the Soldier of Godrick in the tutorial fight, followed by a field boss, a mini boss, and a main boss fight.

## Gameplay

Boss fights are performed with a Dungeons & Dragons (D&D) style approach, brother! Each player takes turns rolling a D20 die to check if they hit the boss and a D10 die to determine how much damage they dealt. The boss fights players in the same way, rolling a D20 die to check if they hit the player and a D10 die to determine how much damage they dealt.

### Turn Order

The turn order is as follows:
1. Host
2. Boss
3. Summon One (if present)
4. Boss
5. Summon Two (if present)
6. Boss

### Player Actions

- **Attack Phase**: Players roll a D20 die to determine if they hit the boss. If successful, they roll a D10 die to determine the damage dealt.
- **Boss Attack Phase**: The boss rolls a D20 die to determine if they hit the player. If successful, they roll a D10 die to determine the damage dealt.

### Game Flow

1. **Character Selection**: Players choose their starting class and name their character.
2. **Tutorial Boss Fight**: Players fight the Soldier of Godrick.
3. **Field Boss Fight**: Players fight a randomly selected field boss.
4. **Mini Boss Fight**: Players fight a randomly selected mini boss.
5. **Main Boss Fight**: Players fight a randomly selected main boss.

### Victory and Defeat Conditions

- **Summon Death**: If a summon dies, they are out of the boss fight until the next battle starts.
- **Host Death**: If the host dies, the defeat screen is shown, and the program exits.
- **Boss Death**: If the boss dies, the host and summons are healed at a grace and prepared for the next battle. If the boss is a main boss, the victory screen is shown, and the program exits.

## Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Running the Game

To start the game, run the following command:

```bash
python elden_ring.py
```

## Example

Here's an example of how the game might look in the terminal:

```
Welcome to Elden Ring CLI!

Choose your class:
1. Astrologer
2. Bandit
3. Confessor
...

Enter a name for your character: Tarnished

Loading class...
...

Press 'ENTER' to continue...

Battle Start!
Host's turn:
Rolling D20... Hit!
Rolling D10... 7 damage dealt to the boss!

Boss's turn:
Rolling D20... Miss!
...

Victory! The boss has been defeated!
```

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the GNU General Public License v3.0.

## Documentation Disclaimer
This README and the module docstrings for the .py files were written by Copilot.
```