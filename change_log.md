Full tournament and practice setup:


Tournament vs Practice is selected by a global boolean (line 10)


For practice:

The student AI must be in a .py file in the main directory and have "control" in the filename

The AI they are practicing against must be called enemy_AI.py and be in the main directory

The student will be asked for a number of players (2-4), all enemies use the enemy_AI.py file and the AI level set by them

Each tank has one life only and every time a single tank remains the session is reset with a new map

will play until pygame window closed



For tournament:

each contestant AI script (2-4 players) must be placed in the "tank_AI" directory and be in a file of any name ending in .py

No other .py files can be in this directory

each player is given 2 lives, when a tank is killed it will respawn in a random spawn location that is not currently occupied

when only one tank remains the winner is declared

the winner declaration will display until the pygame window is closed



NOTE:

I know we disucssed having the undestroyed tank respawn on a kill as well but that didn't work well or make much sense with more than two tanks so I just implemented having the dead tank respawn at a random valid spawn point

