from math import atan2, degrees, pi
from random import choice

state = 0   # 0 - get a target, 1 - move to target, 2 - tunnel north, 3 - tunnel south, 4 - west, 5 - east
grid = 0
last_choice = ''
target_position = (0,0)
targets = {'n':[(100,100),(300,100),(500,100),(700,-20),(900,100),(1100,100),(100,180),(300,180),(500,180),(700,180),(900,180),(1100,180),(100,380),(300,380),(500,380),(700,380),(900,380),(1100,380),(100,580),(300,580),(500,580),(700,580),(900,580),(1100,580),(0,0),(0,0),(0,0),(0,0)],'s':[(100,220),(300,220),(500,220),(700,220),(900,220),(1100,220),(100,420),(300,420),(500,420),(700,420),(900,420),(1100,420),(100,620),(300,620),(500,620),(700,620),(900,620),(1100,620),(100,700),(300,700),(500,700),(700,820),(900,700),(1100,700),(0,0),(0,0),(0,0),(0,0)],'w':[(100,100),(180,100),(380,100),(580,100),(780,100),(980,100),(-20,300),(180,300),(380,300),(580,300),(780,300),(980,300),(100,500),(180,500),(380,500),(580,500),(780,500),(980,500),(100,700),(180,700),(380,700),(580,700),(780,700),(980,700),(0,0),(0,0),(0,0),(0,0)],'e':[(220,100),(420,100),(620,100),(820,100),(1020,100),(1100,100),(220,300),(420,300),(620,300),(820,300),(1020,300),(1220,300),(220,500),(420,500),(620,500),(820,500),(1020,500),(1100,500),(220,700),(420,700),(620,700),(820,700),(1020,700),(1100,700),(0,0),(0,0),(0,0),(0,0)]}

def action(my_tank):
    if state == 0: get_target_position(my_tank)
    elif state == 1: move_to_target_position(my_tank)
    elif state == 2: traverse_tunnel_north(my_tank)
    elif state == 3: traverse_tunnel_south(my_tank)
    elif state == 4: traverse_tunnel_west(my_tank)
    elif state == 5: traverse_tunnel_east(my_tank)

def traverse_tunnel_north(my_tank):
    global state
    if get_grid(my_tank.my_position()) == 21:
        state = 0
        return
    heading = (my_tank.my_heading() + 180) % 360
    if heading >= 185: my_tank.turn_left()
    elif heading <= 175: my_tank.turn_right()
    my_tank.forward()

def traverse_tunnel_south(my_tank):
    global state
    if get_grid(my_tank.my_position()) == 3:
        state = 0
        return
    if my_tank.my_heading() >= 185: my_tank.turn_left()
    elif my_tank.my_heading() <= 175: my_tank.turn_right()
    my_tank.forward()

def traverse_tunnel_west(my_tank):
    global state
    if get_grid(my_tank.my_position()) == 11:
        state = 0
        return
    heading = (my_tank.my_heading() + 270) % 360
    if heading >= 185: my_tank.turn_left()
    elif heading <= 175: my_tank.turn_right()
    my_tank.forward()

def traverse_tunnel_east(my_tank):
    global state
    if get_grid(my_tank.my_position()) == 6:
        state = 0
        return
    heading = (my_tank.my_heading() + 90) % 360
    if heading >= 185: my_tank.turn_left()
    elif heading <= 175: my_tank.turn_right()
    my_tank.forward()

def get_target_position(my_tank):
    global target_position, state, grid, last_choice
    grid = get_grid(my_tank.my_position())
    
    # find open directions and pick one
    walls = my_tank.get_walls()
    choices = [key for key, value in walls.items() if not value]
    if len(choices) > 1:
        if last_choice == 'n': choices.remove('s')
        if last_choice == 's': choices.remove('n')
        if last_choice == 'w': choices.remove('e')
        if last_choice == 'e': choices.remove('w')
    target = choice(choices)
    last_choice = target
    target_position = targets[target][grid]
    target_grid = get_grid(target_position)
    state = 1

def move_to_target_position(my_tank):
    global grid, state
    if grid != get_grid(my_tank.my_position()):
        grid = get_grid(my_tank.my_position())
        if grid == 24: state = 4
        elif grid == 25: state = 5
        elif grid == 26: state = 2
        elif grid == 27: state = 3
        else: state = 0
        return
    
    # if there is a potential shot, take it
    if my_tank.clear_shot(): my_tank.fire()
    
    # keep turret aimed at enemy
    angle_to_enemy = get_angle(my_tank.my_position(),my_tank.enemy_position())
    aim_off = ((180 + angle_to_enemy - my_tank.turret_direction()) % 360) - 180
    if aim_off < -4: my_tank.rotate_left()
    elif aim_off > 4: my_tank.rotate_right()

    # turn and move tank towards target position
    angle_to_location = get_angle(my_tank.my_position(),target_position)
    steer_off = ((180 + angle_to_location - my_tank.my_heading()) % 360) - 180
    if steer_off < -4: my_tank.turn_left()
    elif steer_off > 4: my_tank.turn_right()
    if -90 < steer_off < 90: my_tank.forward()

def get_angle(start,finish):
    dx = start[0]-finish[0]
    dy = start[1]-finish[1]
    return int(degrees((atan2(-dx,dy))%(2*pi)))

def get_grid(position):
    if position[0] < 0: return 24
    if position[0] >= 1200: return 25
    if position[1] < 0: return 26
    if position[1] >= 800: return 27
    return 6 * (position[1]//200) + position[0]//200

