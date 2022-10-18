import json
import os
import sys
import socket
import threading
import ursina
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import json



class Enemy(ursina.Entity):
    def __init__(self, position: ursina.Vec3, identifier: str, username: str):
        super().__init__(
            position=position,
            model="cube",
            origin_y=-0.5,
            collider="box",
            texture="white_cube",
            color=ursina.color.color(0, 0, 1),
            scale=ursina.Vec3(1, 2, 1)
        )

        self.gun=ursina.Entity(
            parent=self,
            position=ursina.Vec3(0.55, 0.5, 0.6),
            scale=ursina.Vec3(0.1, 0.2, 0.65),
            model="cube",
            texture="white_cube",
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
            color_saturation=1-self.health / 100
        except AttributeError:
            self.health=100
            color_saturation=1-self.health / 100

        self.color=ursina.color.color(0, color_saturation, 1)

        if self.health <= 0:
            ursina.destroy(self)

class Player(FirstPersonController):
    def __init__(self, position: ursina.Vec3):
        super().__init__(
            position=position,
            model="cube",
            jump_height=2.5,
            jump_duration=0.4,
            origin_y=-2,
            collider="box",
            speed=7
        )
        self.cursor.color=ursina.color.rgb(255, 0, 0, 122)

        self.gun=ursina.Entity(
            parent=ursina.camera.ui,
            position=ursina.Vec2(0.6, -0.45),
            scale=ursina.Vec3(0.1, 0.2, 0.65),
            rotation=ursina.Vec3(-20, -20, -5),
            model="cube",
            texture="white_cube",
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

        ursina.Text(
            text="You are dead!",
            origin=ursina.Vec2(0, 0),
            scale=3
        )

    def update(self):
        self.healthbar.scale_x=self.health / 100 * self.healthbar_size.x

        if self.health <= 0:
            if not self.death_message_shown:
                self.death()
        else:
            super().update()

class Bullet(ursina.Entity):
    def __init__(self, position: ursina.Vec3, direction: float, x_direction: float, network, damage: int=random.randint(5, 20), slave=False):
        speed=50
        dir_rad=ursina.math.radians(direction)
        x_dir_rad=ursina.math.radians(x_direction)

        self.velocity=ursina.Vec3(
            ursina.math.sin(dir_rad) * ursina.math.cos(x_dir_rad),
            ursina.math.sin(x_dir_rad),
            ursina.math.cos(dir_rad) * ursina.math.cos(x_dir_rad)
        ) * speed

        super().__init__(
            position=position+self.velocity / speed,
            model="sphere",
            collider="box",
            scale=0.2
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
        self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr=server_addr
        self.port=server_port
        self.username=username
        self.recv_size=2048
        self.id=0

    def settimeout(self, value):
        self.client.settimeout(value)

    def connect(self):

        self.client.connect((self.addr, self.port))
        self.id=self.client.recv(self.recv_size).decode("utf8")
        self.client.send(self.username.encode("utf8"))

    def receive_info(self):
        try:
            msg=self.client.recv(self.recv_size)
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
            "position": (player.world_x, player.world_y, player.world_z),
            "rotation": player.rotation_y,
            "health": player.health,
            "joined": False,
            "left": False
        }
        player_info_encoded=json.dumps(player_info).encode("utf8")

        try:
            self.client.send(player_info_encoded)
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
            self.client.send(bullet_info_encoded)
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
            self.client.send(health_info_encoded)
        except socket.error as e:
            print(e)

class Wall(ursina.Entity):
    def __init__(self, position):
        super().__init__(
            position=position,
            scale=2,
            model="cube",
            texture=os.path.join("assets", "wall.png"),
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

class FloorCube(ursina.Entity):
    def __init__(self, position):
        super().__init__(
            position=position,
            scale=2,
            model="cube",
            texture=os.path.join("assets", "floor.png"),
            collider="box"
        )
        self.texture.filtering=None


class Floor:
    def __init__(self):
        dark1=True
        for z in range(-20, 20, 2):
            dark2=not dark1
            for x in range(-20, 20, 2):
                cube=FloorCube(ursina.Vec3(x, 0, z))
                if dark2:
                    cube.color=ursina.color.color(0, 0.2, 0.8)
                else:
                    cube.color=ursina.color.color(0, 0.2, 1)
                dark2=not dark2
            dark1=not dark1



username=input("Enter your username: ")

while True:
    server_addr=input("Enter server IP: ")
    server_port=input("Enter server port: ")

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
ursina.window.title="Ursina FPS"
ursina.window.exit_button.visible=False

floor=Floor()
map=Map()
sky=ursina.Entity(
    model="sphere",
    texture=os.path.join("assets", "sky.png"),
    scale=9999,
    double_sided=True
)
player=Player(ursina.Vec3(0, 1, 0))
prev_pos=player.world_position
prev_dir=player.world_rotation_y
enemies=[]


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

        elif info["object"]=="bullet":
            b_pos=ursina.Vec3(*info["position"])
            b_dir=info["direction"]
            b_x_dir=info["x_direction"]
            b_damage=info["damage"]
            new_bullet=Bullet(b_pos, b_dir, b_x_dir, n, b_damage, slave=True)
            ursina.destroy(new_bullet, delay=2)

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

        if prev_pos!=player.world_position or prev_dir!=player.world_rotation_y:
            n.send_player(player)

        prev_pos=player.world_position
        prev_dir=player.world_rotation_y


def input(key):
    if key=="left mouse down" and player.health > 0:
        b_pos=player.position+ursina.Vec3(0, 2, 0)
        bullet=Bullet(b_pos, player.world_rotation_y, -player.camera_pivot.world_rotation_x, n)
        n.send_bullet(bullet)
        ursina.destroy(bullet, delay=2)


def main():
    msg_thread=threading.Thread(target=receive, daemon=True)
    msg_thread.start()
    app.run()


if __name__=="__main__":
    main()