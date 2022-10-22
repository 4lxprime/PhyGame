import json
import os
import sys
import socket
import threading
import ursina
from ursina.prefabs.first_person_controller import FirstPersonController
import random
from conf import player as cplayer, bullet as cbullet, map as cmap, game as cgame
import time



class Enemy(ursina.Entity):
    def __init__(self, position: ursina.Vec3, identifier: str, username: str):
        super().__init__(
            position=position,
            model="cube",
            origin_y=-0.5,
            collider="box",
            texture=os.path.join("assets", "palyer.png"),
            color=ursina.color.color(0, 0, 1),
            scale=ursina.Vec3(1, 2, 1)
        )

        self.gun=ursina.Entity(
            parent=self,
            position=ursina.Vec3(0.55, 0.5, 0.6),
            scale=ursina.Vec3(0.1, 0.2, 0.65),
            model="cube",
            texture=os.path.join("assets", "USP45.obj"),
            color=ursina.color.color(0, 0, 0.4)
        )

        self.name_tag=ursina.Text(
            parent=self,
            text=username,
            position=ursina.Vec3(0, 1.3, 0),
            scale=ursina.Vec2(5, 3),
            billboard=True,
            origin=ursina.Vec2(0, 0)
        )

        self.health=100
        self.id=identifier
        self.username=username

    def update(self):
        try:
            color_saturation=1-self.health/100
        except AttributeError:
            self.health=100
            color_saturation=1-self.health/100

        self.color=ursina.color.color(0, color_saturation, 1)

        if self.health==0:
            ursina.destroy(self)

class Player(FirstPersonController):
    def __init__(self, position: ursina.Vec3):
        super().__init__(
            position=position,
            model="cube",
            jump_height=cplayer.jump_height,
            jump_duration=cplayer.jump_duration,
            origin_y=-2,
            collider="box",
            speed=cplayer.speed
        )
        self.cursor.color=ursina.color.rgb(255, 0, 0, 122)

        self.gun=ursina.Entity(
            parent=ursina.camera.ui,
            position=ursina.Vec2(0.6, -0.45),
            scale=ursina.Vec3(0.1, 0.2, 0.65),
            rotation=ursina.Vec3(-20, -20, -5),
            model="cube",
            texture=cplayer.gun_texture,
            color=ursina.color.color(0, 0, 0.4)
        )

        self.healthbar_pos=ursina.Vec2(0, 0.45)
        self.healthbar_size=ursina.Vec2(0.8, 0.04)
        self.healthbar_bg=ursina.Entity(
            parent=ursina.camera.ui,
            model="quad",
            color=ursina.color.rgb(255, 0, 0),
            position=self.healthbar_pos,
            scale=self.healthbar_size
        )
        self.healthbar=ursina.Entity(
            parent=ursina.camera.ui,
            model="quad",
            color=ursina.color.rgb(0, 255, 0),
            position=self.healthbar_pos,
            scale=self.healthbar_size
        )

        self.health=100
        self.death_message_shown=False

    def death(self):
        self.death_message_shown=True

        ursina.destroy(self.gun)
        self.rotation=0
        self.camera_pivot.world_rotation_x=-45
        self.world_position=ursina.Vec3(0, 7, -35)
        self.cursor.color=ursina.color.rgb(0, 0, 0, a=0)

        self.dtext=ursina.Text(
            text="You are dead!",
            origin=ursina.Vec2(0, 0),
            scale=4
        )
        
        # the spec mode crash
        """ursina.destroy(self.dtext)
        self.spectext=ursina.Text(
            text=f"You are in spectator mode if you want to restart, press {cgame.exit_key}",
            origin=ursina.Vec2(0, 0),
            scale=2
        )
        Player(ursina.Vec3(0, 3, 0)) # spec mode"""
        
        if cgame.auto_restart:
            os.execl(sys.executable, sys.executable, *sys.argv)
        
    def update(self):
        self.healthbar.scale_x=self.health/100 * self.healthbar_size.x

        if self.health <= 0:
            if not self.death_message_shown:
                self.death()
        else:
            super().update()

class Bullet(ursina.Entity):
    def __init__(self, position: ursina.Vec3, direction: float, x_direction: float, network, damage: int=random.randint(5, 20), slave=False):
        speed=cbullet.speed
        dir_rad=ursina.math.radians(direction)
        x_dir_rad=ursina.math.radians(x_direction)

        self.velocity=ursina.Vec3(
            ursina.math.sin(dir_rad) * ursina.math.cos(x_dir_rad),
            ursina.math.sin(x_dir_rad),
            ursina.math.cos(dir_rad) * ursina.math.cos(x_dir_rad)
        ) * speed

        super().__init__(
            position=position+self.velocity/speed,
            model="sphere",
            collider="box",
            scale=cbullet.scale,
        )

        self.damage=damage
        self.direction=direction
        self.x_direction=x_direction
        self.slave=slave
        self.network=network

    def update(self):
        self.position += self.velocity * ursina.time.dt
        hit_info=self.intersects()

        if hit_info.hit:
            if not self.slave:
                for entity in hit_info.entities:
                    if isinstance(entity, Enemy):
                        entity.health -= self.damage
                        self.network.send_health(entity)

            ursina.destroy(self)

class Network:

    def __init__(self, server_addr: str, server_port: int, username: str):
        self.DepSrv=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.BulSrv=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr=server_addr
        self.port=server_port
        self.baddr=bullet_server_addr
        self.bport=int(bullet_server_port)
        self.username=username
        self.recv_size=2048
        self.id=0

    def settimeout(self, value):
        self.DepSrv.settimeout(value)
        self.BulSrv.settimeout(value)

    def connect(self):

        self.DepSrv.connect((self.addr, self.port))
        self.id=self.DepSrv.recv(self.recv_size).decode("utf8")
        self.DepSrv.send(self.username.encode("utf8"))
        
        self.BulSrv.connect((self.baddr, self.bport))
        self.bid=self.BulSrv.recv(self.recv_size).decode("utf8")
        self.BulSrv.send(self.username.encode("utf8"))

    def receive_info(self):
        try:
            msg=self.DepSrv.recv(self.recv_size)
        except socket.error as e:
            print(e)

        if not msg:
            return None

        msg_decoded=msg.decode("utf8")

        left_bracket_index=msg_decoded.index("{")
        right_bracket_index=msg_decoded.index("}")+1
        msg_decoded=msg_decoded[left_bracket_index:right_bracket_index]

        msg_json=json.loads(msg_decoded)

        return msg_json

    def bullet_receive_info(self):
        try:
            msg=self.BulSrv.recv(self.recv_size)
        except socket.error as e:
            print(e)

        if not msg:
            return None

        msg_decoded=msg.decode("utf8")

        left_bracket_index=msg_decoded.index("{")
        right_bracket_index=msg_decoded.index("}")+1
        msg_decoded=msg_decoded[left_bracket_index:right_bracket_index]

        msg_json=json.loads(msg_decoded)

        return msg_json

    def send_player(self, player: Player):
        player_info={
            "object": "player",
            "id": self.id,
            "position": (round(player.world_x, 2), round(player.world_y), round(player.world_z, 2)),
            "rotation": round(player.rotation_y),
            "health": player.health,
            "joined": False,
            "left": False
        }
        player_info_encoded=json.dumps(player_info).encode("utf8")

        try:
            self.DepSrv.send(player_info_encoded)
        except socket.error as e:
            print(e)

    def send_bullet(self, bullet: Bullet):
        bullet_info={
            "object": "bullet",
            "position": (bullet.world_x, bullet.world_y, bullet.world_z),
            "damage": bullet.damage,
            "direction": bullet.direction,
            "x_direction": bullet.x_direction
        }

        bullet_info_encoded=json.dumps(bullet_info).encode("utf8")

        try:
            self.BulSrv.send(bullet_info_encoded)
        except socket.error as e:
            print(e)

    def send_health(self, player: Enemy):
        health_info={
            "object": "health_update",
            "id": player.id,
            "health": player.health
        }

        health_info_encoded=json.dumps(health_info).encode("utf8")

        try:
            self.DepSrv.send(health_info_encoded)
        except socket.error as e:
            print(e)

class Wall(ursina.Entity):
    def __init__(self, position):
        super().__init__(
            position=position,
            scale=2,
            model="cube",
            texture=cmap.wall_texture,
            origin_y=-0.5
        )
        self.texture.filtering=None
        self.collider=ursina.BoxCollider(self, size=ursina.Vec3(1, 2, 1))


class Map:
    def __init__(self):
        for y in range(1, 4, 2):
            Wall(ursina.Vec3(6, y, 0))
            Wall(ursina.Vec3(6, y, 2))
            Wall(ursina.Vec3(6, y, 4))
            Wall(ursina.Vec3(6, y, 6))
            Wall(ursina.Vec3(6, y, 8))

            Wall(ursina.Vec3(4, y, 8))
            Wall(ursina.Vec3(2, y, 8))
            Wall(ursina.Vec3(0, y, 8))
            Wall(ursina.Vec3(-2, y, 8))

            Wall(ursina.Vec3(4, y, 14))
            Wall(ursina.Vec3(2, y, 14))
            Wall(ursina.Vec3(0, y, 14))
            Wall(ursina.Vec3(-2, y, 14))

            Wall(ursina.Vec3(0, y, -8))
            Wall(ursina.Vec3(-2, y, -8))
            Wall(ursina.Vec3(-4, y, -8))
            Wall(ursina.Vec3(-6, y, -8))
            Wall(ursina.Vec3(-8, y, -8))

            Wall(ursina.Vec3(14, y, 2))
            Wall(ursina.Vec3(14, y, 4))
            Wall(ursina.Vec3(14, y, 6))
            Wall(ursina.Vec3(14, y, 8))
            Wall(ursina.Vec3(14, y, 10))

            Wall(ursina.Vec3(-14, y, 2))
            Wall(ursina.Vec3(-14, y, 4))
            Wall(ursina.Vec3(-14, y, 6))
            Wall(ursina.Vec3(-14, y, 8))
            Wall(ursina.Vec3(-14, y, 10))

            Wall(ursina.Vec3(-14, y, -4))
            Wall(ursina.Vec3(-14, y, -6))
            Wall(ursina.Vec3(-14, y, -8))
            Wall(ursina.Vec3(-14, y, -10))
            Wall(ursina.Vec3(-14, y, -12))


class FloorCube(ursina.Entity):
    def __init__(self, position):
        super().__init__(
            position=position,
            scale=2,
            model="cube",
            texture=cmap.floor_texture,
            collider="box"
        )
        self.texture.filtering=None


class Floor:
    def __init__(self):
        for z in range(-20, 20, 2):
            for x in range(-20, 20, 2):
                cube=FloorCube(ursina.Vec3(x, 0, z))
                cube.color=ursina.color.color(0, 0.2, 2)



username=sys.argv[1]

while True:
    server_addr=sys.argv[2]
    server_port=sys.argv[3]
    bullet_server_addr=sys.argv[4]
    bullet_server_port=sys.argv[5]

    try:
        server_port=int(server_port)
    except ValueError:
        print("\nThe port you entered was not a number, try again with a valid port...")
        continue

    n=Network(server_addr, server_port, username)
    n.settimeout(5)

    error_occurred=False

    try:
        n.connect()
    except ConnectionRefusedError:
        print("\nConnection refused! This can be because server hasn't started or has reached it's player limit.")
        error_occurred=True
    except socket.timeout:
        print("\nServer took too long to respond, please try again...")
        error_occurred=True
    except socket.gaierror:
        print("\nThe IP address you entered is invalid, please try again with a valid address...")
        error_occurred=True
    finally:
        n.settimeout(None)

    if not error_occurred:
        break

app=ursina.Ursina()
ursina.window.borderless=False
ursina.window.title="PhyGame 1.0"
ursina.window.exit_button.visible=False
ursina.camera.fov=cplayer.fov

if cgame.limit_fps:
    clock=app.clock
    clock.mode=clock.MLimited
    clock.setFrameRate(cgame.max_fps)
    
floor=Floor()
map=Map()
sky=ursina.Entity(
    model="sphere",
    texture=cmap.texture,
    scale=cmap.scale,
    double_sided=True
)
player=Player(ursina.Vec3(0, 1, 0))
prev_pos=player.world_position
prev_dir=player.world_rotation_y
enemies=[]


def bullet_receive():
    while True:
        try:
            info=n.bullet_receive_info()
        except Exception as e:
            print(e)
            continue

        if not info:
            print("Server has stopped! Exiting...")
            sys.exit()
        
        if info["object"]=="bullet":
            ursina.Audio("assets/gunshot.mp3")
            b_pos=ursina.Vec3(*info["position"])
            b_dir=info["direction"]
            b_x_dir=info["x_direction"]
            b_damage=info["damage"]
            new_bullet=Bullet(b_pos, b_dir, b_x_dir, n, b_damage, slave=True)
            ursina.destroy(new_bullet, delay=2)
        else:
            pass


def receive():
    while True:
        try:
            info=n.receive_info()
        except Exception as e:
            print(e)
            continue

        if not info:
            print("Server has stopped! Exiting...")
            sys.exit()

        if info["object"]=="player":
            enemy_id=info["id"]

            if info["joined"]:
                new_enemy=Enemy(ursina.Vec3(*info["position"]), enemy_id, info["username"])
                new_enemy.health=info["health"]
                enemies.append(new_enemy)
                continue

            enemy=None

            for e in enemies:
                if e.id==enemy_id:
                    enemy=e
                    break

            if not enemy:
                continue

            if info["left"]:
                enemies.remove(enemy)
                ursina.destroy(enemy)
                continue

            enemy.world_position=ursina.Vec3(*info["position"])
            enemy.rotation_y=info["rotation"]

        elif info["object"]=="health_update":
            enemy_id=info["id"]

            enemy=None

            if enemy_id==n.id:
                enemy=player
            else:
                for e in enemies:
                    if e.id==enemy_id:
                        enemy=e
                        break

            if not enemy:
                continue

            enemy.health=info["health"]


def update():
    if player.health > 0:
        global prev_pos, prev_dir

        if round(prev_pos[0])!=round(player.world_position[0]) or round(prev_dir)!=round(player.world_rotation_y) or round(prev_pos[1])!=round(player.world_position[1]) or round(prev_pos[2])!=round(player.world_position[2]):
            print(f"player: {str(player)}")
            n.send_player(player)

        prev_pos=player.world_position
        prev_dir=player.world_rotation_y


def input(key):
    if key=="left mouse down" and player.health > 0:
        ursina.Audio("assets/gunshot.mp3")
        b_pos=player.position+ursina.Vec3(0, 2, 0)
        bullet=Bullet(b_pos, player.world_rotation_y, -player.camera_pivot.world_rotation_x, n)
        n.send_bullet(bullet)
        ursina.destroy(bullet, delay=2)
        
    if key=="right mouse down" and player.health > 0:
        ursina.camera.fov=cplayer.snipe_fov
        
    if key=="right mouse up" and player.health > 0:
        ursina.camera.fov=cplayer.fov
    
    if key==cgame.reload_key:
        os.execl(sys.executable, sys.executable, *sys.argv)
    
    if key==cgame.exit_key:
        exit(0)


def main():
    msg_thread=threading.Thread(target=receive, daemon=True)
    msg_thread.start()
    bmsg_thread=threading.Thread(target=bullet_receive, daemon=True)
    bmsg_thread.start()
    app.run()


if __name__=="__main__":
    if len(sys.argv)==6:
        main()
    else:
        print("python3 game.py <username> <server_ip> <server_port> <bullet_server_ip> <bullet_server_port>")