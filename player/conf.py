class player():
    jump_height=2
    jump_duration=0.25
    speed=12
    fov=120
    snipe_fov=40
    gun_texture="white_cube"
    gun_anim=False
    random_spawn=True
    texture="" #"assets\player.png"

class bullet():
    speed=100
    scale=1

class map():
    scale=9999
    texture="assets/sky.png"
    floor_texture="white_cube" #"assets/floor.png"
    wall_texture="white_cube" #"assets/wall.png"

class game():
    exit_key="p"
    reload_key="escape"
    limit_fps=False
    max_fps=120
    auto_restart=True
    discord_rpc_server=True