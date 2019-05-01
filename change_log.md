Still to do / ideas to try:

full motion movement calls - such as my_tank.turn_right(# of degrees) etc
destructible walls
call to detect shots in play
auto-tournament play


These are things changed or implemented since we last talked:

Can now use from two to four players, blue, green, orange and red. If a control script assigns an AI level it assigned to ALL other tanks.  Can set a hardcoded number of players or user input.

Added Player() class.  This track lives and kills and also allows complete destruction of a killed tank (to prevent invisible corpses) while maintain continuity of the player.  Currently a tank respawning could intersect with another tank if it moves into the dead tanks location ...

Improvements to calculating line of sight.  Better intersection detection and only walls inside a bounding rectangle defined by the line between tanks are checked.  Faster.

Left your sensors alone completely

Changes to the names of some tank method calls ... sorry!

Added point sensors (8 in total) that move and rotate with tank

added getter for weapon cooldown remaining

clear shot and enemy location calls gone, replaced with enemy_tanks() which returns a list of coordinate tuples for the location of any visible enemies.  The closest is listed as element 0 of the list.  No visible tanks returns empty list

added reverse()

cleaned up damage code and speed and turn rates are now actually affected by damage

lives and kills are displayed with name and health bar

cleaned up maze set-up a little

moved countdown out of game loop to its own function

cleaned up main and moved code out of game loop that really belonged elsewhere

currently gives each player three lives and quits when only one player left.  All on same maze.