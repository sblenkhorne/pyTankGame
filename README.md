# pyTankGame
A Tank Game Battle Tournament System built in Python

You are a tank commander in a one on one battle in the maze arena.  You must code an AI for your tank.  Your AI function will be called once per frame.

You control your tank by issuing orders to your driver and your gunner.

To Run Practice Mode
-----------------------------------------------------------------
Create a .py file in the game folder. It can have any filename as long as 'control' is in the filename, but make sure NO other filename includes 'control'. You MUST have the action() function in your file. This is the function that gets called once per frame. Put all of your code, algorithms and logic in this function. Although, if you want to create helper functions that are called from within the action() function, that works just as well.

Include a call to set the enemy AI level in your code. (see below)

You will be asked how many (2-4) tanks you wish to practice with in the arena.

To run your program, simply open and run PyTank.py. 

Available Commands
-----------------------------------------------------------------

You can set the name of your tank that will be shown in the game by issuing the following command:  
my_tank.set_Name(yourName) - Where yourName is a string.

You can set the level of difficulty for your enemy AI to practice against.  
my_tank.set_enemy_lvl(1) - sets the enemy AI to the easiest level
All other tanks are set to this level if more than 2 players

1 - enemy just sits there; does not shoot  
2 - enemy drives in a circle; does not shoot  
3 - enemy navigates the map, but does not shoot  
4 - enemy navigates the map and tries to shoot you  


## Movement Commands
You driver can be commanded to drive forwards or turn the tank using these commands:

my_tank.forward() - moves the tank forward approximately 10 pixels in the heading direction
my_tank.reverse() - moves the tank backward approximately 10 pixels
my_tank.turn_left() - turns the tank 5 degrees to the left (turret does not turn with tank)
my_tank.turn_right() - turns the tank 5 degrees to the right

you can also execute multi-frame turns with these commands:

my_tank.turn_right_for(degrees) - turns the tank at its current rate of turn as close to 'degrees' as possible
my_tank.turn_left_for(degrees) - same but to the left
my_tank.turn_to(heading) - turns at the current rate of turn in the shortest direction to get to heading

only one forward and one turn command can be issued each frame.  If multiple calls are made to forward or turns they will be ignored.

forward() and reverse() both return False if the movement could not be completed because of a collision.

## Turret Control
Your gunner can be commanded to rotate the gun turret or fire the gun using these commands:

my_tank.fire() - fires a shell in the current turret direction.  Has an approximate two second cool down
my_tank.rotate_left() - turns the turret 3 degrees to the left
my_tank.rotate_right() - turns the turret 3 degrees to the right

you can also execute multi-frame aiming movements:

my_tank.turret_right_for(degrees)
my_tank.turret_left_for(degrees)
my_tank.turret_to(bearing)

only one fire and one rotate command can be issued each frame.  Multiple calls will be ignored.

If your tank is damaged movement is reduced to approximately 7 pixels, turn rate to 3 degrees and turret rotation to 2 degrees. If your tank is hit again it is destroyed.

## Position Information Commands
As the commander you are able to determine some things about your environment.  

You have a GPS and compass which can pinpoint your tank using these commands:

my_tank.my_position() - returns the x and y coordinates of your tank as a tuple
my_tank.my_heading() - returns your tank heading in degrees (0 is north, 90 is east, 180 is south, 270 is west)
my_tank.turret_direction() - returns the direction (in degrees) that your gun turret is pointed

## Sensors Commands
You also have proximity sensors, which allow you to check whether there are any obstacles in your immediate area, using this command:
my_tank.checkSensors() - returns a dictionary with keys 'n','s','e','w','fl','f','fr','r','br','b','bl','l'.  The values for these keys are True if there is a close wall or tank in that direction and False if not.
- example: mySensors = my_tank.checkSensors() -> returns {'n':True,'s':False,'w':False,'e':False} #This means there is an obstacle to the immediate north of your tank.

You can determine the exact position of any visible enemy tanks by calling: 
my_tank.enemy_tanks().  This returns a list of locations (eg [ ( 100,200 ) , ( 350,125 ) ] ) of all visible enemies. They are not listed in any order except that the closest is always the first one listed. If no enemies are visible an empty list is returned.

There are two other functions you can use:
my_tank.damaged() returns True if your tank has taken a hit
my_tank.cooldown() returns the number of frames before your weapon can be fired again

Keep in mind that these commands are all relative to the center of your tank and the center of the enemy tanks.  You may not see a wall in a certain direction but this doesn't guarentee that some part of your tank won't hit if you travel in that direction.  Your gun sight may see the other tank but that doesn't guarantee that a shot made will reach it, your shell has size and may clip a wall even if it doesn't block your view.  Give your driver and gunner a margin of error to be sure things work the way you intend!

Each tank in the arena has one life.  The number of lives remaining is shown to the left of the healthbar.  The number to the right is your total kills.  When only one player has any remaining lives the arena will reset with a new map.
