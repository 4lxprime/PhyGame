class player():
    jump_height=2
    jump_duration=0.25
    speed=10
    fov=120
    snipe_fov=40
    scope_texture="assets/scope.png"
    gun_texture="assets/USP45.obj"

class bullet():
    speed=100
    scale=1

class map():
    scale=9999
    texture="assets/sky.png"
    floor_texture="white_cube" #"assets/floor.png"
    wall_texture="white_cube" #"assets/wall.png"

class game():
    exit_key="escape"