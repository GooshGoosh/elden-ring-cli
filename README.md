# elden-ring-cli
This project allows users to simulate fighting bosses from the Elden Ring game.

The game can be played with 1 to 3 players (1 host and 2 summons) locally. Players choose their starting class and name their character for the journey to begin.
Players then engage in 4 boss fights starting with the Soldier of Godrick in the tutorial fight followed by a field, mini, and main boss fight.

Boss fights are performed with a D&D style approach with each player taking turns rolling a D20 die to check if they hit the boss and a D10 die to check how much damage they dealt.
The boss fights players in the same way; The boss rolls a D20 die to check if they hit the player and a D10 die to check how much damage they dealt.
The turn order is as follows: Host > Boss > Summon One > Boss > Summon Two > Boss.

If either summon dies, then they are out of the boss fight until the next battle starts. If the host dies, then the defeat screen is shown and the program is exited.
If the boss dies, then the host and summons are healed at a grace and prepared for the next battle. If the boss is a main boss, then the victory screen is shown and the program is exited.
