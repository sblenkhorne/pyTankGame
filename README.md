# pyTankGame
A Tank Game Battle Tournament System built in Python

You are a tank commander in a one on one battle in the maze arena.  You must code an AI for your tank.  Your AI function will be called once per frame.

You control your tank by issuing orders to your driver and your gunner.

You driver can be commanded to drive forwards or turn the tank using these commands:

my_tank.forward() - moves the tank forward approximately 8 pixels in the heading direction
my_tank.turn_left() - turns the tank 5 degrees to the left
my_tank.turn_right() - turns the tank 5 degrees to the right

only one forward and one turn command can be issued each frame.  If multiple calls are made to forward or turns they will be ignored.

You gunner can be commanded to turn the gun turret or fire the gun using these commands:

my_tank.fire() - fires a shell in the current turret direction.  Has an approximate one second cool down
my_tank.rotate_left() - turns the turret 5 degrees to the left
my_tank.rotate_right() - turns the turret 5 degrees to the right

only one fire and one rotate command can be issued each frame.  Multiple calls will be ignored.

As the commander you are able to determine some things about your environment.  

You have a GPS and compass which can pinpoint your tank and the enemy tank using these commands:

my_tank.my_position() - returns the x and y coordinates of your tank
my_tank.enemy_position() - returns the x and y coordinates of the enemy tank
my_tank.my_heading() - returns your tank heading in degrees (0 is north, 90 is east, 180 is south, 270 is west)
my_tank.turret_direction() - returns the direction (in degrees) that your gun turret is pointed

You also have view windows which allow a minimal view of your surroundings. You can only see the immediate area  using this command:

my_tank.get_walls() - returns a dictionary with keys 'n','s','e','w'.  The values for these keys are True if there is a close wall in that direction and False if not.

You have a somewhat better gunsight.  It allows you to see if the other tank is visible from your position, at any distance, using this command:

my_tank.clear_shot() - returns True if the other tank is visible from your position

Keep in mind that these commands are all relative to the center of your tank and the center of the enemy tank.  You may not see a wall in a certain direction but this doesn't guarentee that some part of your tank won't hit if you travel in that direction.  You gun sight may see the other tank but that doesn't guarantee that a shot made will reach it, your shell has size and may clip a wall even if it doesn't block your view.  Give your driver and gunner a margin of error to be sure things work the way you intend!

