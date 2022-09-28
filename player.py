from math import *
import pygame as pg

pg.init()

# "constants"
PLAYER_SPEED = 3.75
PLAYER_FLOOR_LOCATION = 682
NEGATIVE_ACCELERATION_FRAMES = 7
FRAME_RATE = .15
count = NEGATIVE_ACCELERATION_FRAMES
frame_step = PLAYER_SPEED / NEGATIVE_ACCELERATION_FRAMES
jump_height = 21

# constants - don't change. You will break something, Joe
gravity = 1
width, height = (1440, 900)
center_position = width / 2, height / 2
player_img_res = 250
acceleration_control = 0

idle_sheet = pg.image.load("Fantasy Game Assets/idle.png")
run_sheet = pg.image.load("Fantasy Game Assets/run.png")
attack_1_sheet = pg.image.load("Fantasy Game Assets/Attack1.png")
attack_2_sheet = pg.image.load("Fantasy Game Assets/Attack2.png")
death_sheet = pg.image.load("Fantasy Game Assets/Death.png")
fall_sheet = pg.image.load("Fantasy Game Assets/Fall.png")
jump_sheet = pg.image.load("Fantasy Game Assets/Jump.png")
take_hit_sheet = pg.image.load("Fantasy Game Assets/take_hit.png")

ATTACK = False


def get_image(sheet, frame):
    global player_img_res
    scale = 2.9
    image = pg.Surface((player_img_res, player_img_res))
    image.blit(sheet, (0, 0), ((frame * player_img_res), 0, player_img_res, player_img_res))
    image = pg.transform.scale(image, (player_img_res * scale, player_img_res * scale))
    image.set_colorkey((0, 0, 0))
    return image


def calc_distance(x1, y1, x2, y2):
    di = sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
    return di


# sliced idle sprites
idle_frame_0 = get_image(idle_sheet, 0)
idle_frame_1 = get_image(idle_sheet, 1)
idle_frame_2 = get_image(idle_sheet, 2)
idle_frame_3 = get_image(idle_sheet, 3)
idle_frame_4 = get_image(idle_sheet, 4)
idle_frame_5 = get_image(idle_sheet, 5)
idle_frame_6 = get_image(idle_sheet, 6)
idle_frame_7 = get_image(idle_sheet, 7)

# sliced run sprites
run_frame_0 = get_image(run_sheet, 0)
run_frame_1 = get_image(run_sheet, 1)
run_frame_2 = get_image(run_sheet, 2)
run_frame_3 = get_image(run_sheet, 3)
run_frame_4 = get_image(run_sheet, 4)
run_frame_5 = get_image(run_sheet, 5)
run_frame_6 = get_image(run_sheet, 6)
run_frame_7 = get_image(run_sheet, 7)

# sliced attack 1 sprites
attack_1_frame_0 = get_image(attack_1_sheet, 0)
attack_1_frame_1 = get_image(attack_1_sheet, 1)
attack_1_frame_2 = get_image(attack_1_sheet, 2)
attack_1_frame_3 = get_image(attack_1_sheet, 3)
attack_1_frame_4 = get_image(attack_1_sheet, 4)
attack_1_frame_5 = get_image(attack_1_sheet, 5)
attack_1_frame_6 = get_image(attack_1_sheet, 6)
attack_1_frame_7 = get_image(attack_1_sheet, 7)

# sliced attack 2 sprites
attack_2_frame_0 = get_image(attack_2_sheet, 0)
attack_2_frame_1 = get_image(attack_2_sheet, 1)
attack_2_frame_2 = get_image(attack_2_sheet, 2)
attack_2_frame_3 = get_image(attack_2_sheet, 3)
attack_2_frame_4 = get_image(attack_2_sheet, 4)
attack_2_frame_5 = get_image(attack_2_sheet, 5)
attack_2_frame_6 = get_image(attack_2_sheet, 6)
attack_2_frame_7 = get_image(attack_2_sheet, 7)

# sliced death sprites
death_frame_0 = get_image(death_sheet, 0)
death_frame_1 = get_image(death_sheet, 1)
death_frame_2 = get_image(death_sheet, 2)
death_frame_3 = get_image(death_sheet, 3)
death_frame_4 = get_image(death_sheet, 4)
death_frame_5 = get_image(death_sheet, 5)
death_frame_6 = get_image(death_sheet, 6)

# sliced fall sprites
fall_frame_0 = get_image(fall_sheet, 0)
fall_frame_1 = get_image(fall_sheet, 1)

# sliced jump sprites (for jump)
jump_frame_0 = get_image(jump_sheet, 0)
jump_frame_1 = get_image(jump_sheet, 1)

# sliced taking hit sprites
take_hit_frame_0 = get_image(take_hit_sheet, 0)
take_hit_frame_1 = get_image(take_hit_sheet, 1)
take_hit_frame_2 = get_image(take_hit_sheet, 2)


class Player(pg.sprite.Sprite):
    def __init__(self, x):
        super(Player, self).__init__()
        # movement
        self.x = int(x)
        self.y = PLAYER_FLOOR_LOCATION
        self.dx = 0
        self.dy = jump_height
        self.left_pressed = False
        self.right_pressed = False
        self.space_pressed = False
        self.attack_1_pressed = False
        self.attack_2_pressed = False
        self.speed = PLAYER_SPEED
        self.last_arrow_pressed = ""
        self.player_health = 100
        # animation
        self.current_animation = "idle"
        self.sprites = []
        self.current_sprite = 0
        self.sprites.append(idle_frame_0)
        self.sprites.append(idle_frame_1)
        self.sprites.append(idle_frame_2)
        self.sprites.append(idle_frame_3)
        self.sprites.append(idle_frame_4)
        self.sprites.append(idle_frame_5)
        self.sprites.append(idle_frame_6)
        self.sprites.append(idle_frame_7)
        self.animation_finished = False
        self.image = idle_frame_0
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

    def flip_sprites(self):
        for i in range(0, len(self.sprites)):
            self.sprites[i] = pg.transform.flip(self.sprites[i], True, False)

    def switch_player_animation(self, switch):
        if switch == "idle" or "run" or "attack_1" or "attack_2" or "death" \
                or "fall" or "jump" or "take_hit" or "decelerate":
            self.current_animation = switch
            del self.sprites[:]
            if self.current_animation == "idle":
                self.sprites.append(idle_frame_0)
                self.sprites.append(idle_frame_1)
                self.sprites.append(idle_frame_2)
                self.sprites.append(idle_frame_3)
                self.sprites.append(idle_frame_4)
                self.sprites.append(idle_frame_5)
                self.sprites.append(idle_frame_6)
                self.sprites.append(idle_frame_7)
            elif self.current_animation == "run":
                self.sprites.append(run_frame_0)
                self.sprites.append(run_frame_1)
                self.sprites.append(run_frame_2)
                self.sprites.append(run_frame_3)
                self.sprites.append(run_frame_4)
                self.sprites.append(run_frame_5)
                self.sprites.append(run_frame_6)
                self.sprites.append(run_frame_7)
            elif self.current_animation == "attack_1":
                self.sprites.append(attack_1_frame_0)
                self.sprites.append(attack_1_frame_1)
                self.sprites.append(attack_1_frame_2)
                self.sprites.append(attack_1_frame_3)
                self.sprites.append(attack_1_frame_4)
                self.sprites.append(attack_1_frame_5)
                self.sprites.append(attack_1_frame_6)
                self.sprites.append(attack_1_frame_7)
            elif self.current_animation == "attack_2":
                self.sprites.append(attack_2_frame_0)
                self.sprites.append(attack_2_frame_1)
                self.sprites.append(attack_2_frame_2)
                self.sprites.append(attack_2_frame_3)
                self.sprites.append(attack_2_frame_4)
                self.sprites.append(attack_2_frame_5)
                self.sprites.append(attack_2_frame_6)
                self.sprites.append(attack_2_frame_7)
            elif self.current_animation == "death":
                self.sprites.append(death_frame_0)
                self.sprites.append(death_frame_1)
                self.sprites.append(death_frame_2)
                self.sprites.append(death_frame_3)
                self.sprites.append(death_frame_4)
                self.sprites.append(death_frame_5)
                self.sprites.append(death_frame_6)
            elif self.current_animation == "fall":
                self.sprites.append(fall_frame_0)
                self.sprites.append(fall_frame_1)
            elif self.current_animation == "jump":
                self.sprites.append(jump_frame_0)
                self.sprites.append(jump_frame_1)
            elif self.current_animation == "take_hit":
                self.sprites.append(take_hit_frame_0)
                self.sprites.append(take_hit_frame_1)
                self.sprites.append(take_hit_frame_2)
            elif self.current_animation == "decelerate":
                self.sprites.append(run_frame_0)
                self.sprites.append(run_frame_1)
                self.sprites.append(run_frame_2)
                self.sprites.append(run_frame_3)
                self.sprites.append(run_frame_4)
                self.sprites.append(run_frame_5)
                self.sprites.append(run_frame_6)
                self.sprites.append(run_frame_7)

    def set_left_pressed(self, torf):
        self.left_pressed = torf

    def set_right_pressed(self, torf):
        self.right_pressed = torf

    def set_space_pressed(self, torf):
        self.space_pressed = torf

    def get_space_pressed(self):
        return self.space_pressed

    def get_dx(self):
        return self.dx

    def get_dy(self):
        return self.dy

    def set_attack_1_pressed(self, torf):
        self.attack_1_pressed = torf

    def set_attack_2_pressed(self, torf):
        self.attack_2_pressed = torf

    def get_attack_1_pressed(self):
        return self.attack_1_pressed

    def get_attack_2_pressed(self):
        return self.attack_2_pressed

    def get_last_arrow_pressed(self):
        return self.last_arrow_pressed

    def set_health(self, value):
        self.player_health = value

    def get_health(self):
        return self.player_health

    def get_player_position(self):
        return self.x, self.y

    def set_player_position(self, x_value, y_value):
        if 0 <= x_value <= width and 0 <= y_value <= height:
            self.x = x_value
            self.y = y_value
            return self.x, self.y
        else:
            print("oh ok ")

    def reset_current_sprite(self):
        self.current_sprite = 0
        return self.current_sprite

    def attack(self, attack_type):
        global ATTACK
        if self.current_sprite != 0 and not ATTACK:
            self.current_sprite = 0
        if attack_type == 1:
            self.switch_player_animation("attack_1")
        else:
            self.switch_player_animation("attack_2")
        ATTACK = True
        if int(self.current_sprite) == 7:  # a single animation loop has been completed
            # here lies pret plese. Your were a real one who will be missed dearly.
            self.set_attack_1_pressed(False)
            self.set_attack_2_pressed(False)
            ATTACK = False

    def run(self, direction):
        global acceleration_control
        if direction == "left":
            if acceleration_control <= 8:
                self.dx = (self.speed * (acceleration_control / 8)) * -1
            else:
                self.dx = -self.speed
        else:
            if acceleration_control <= 8:
                self.dx = self.speed * (acceleration_control / 8)
            else:
                self.dx = self.speed
        self.last_arrow_pressed = direction
        acceleration_control += 1

    # def navigate_map(self):

    def update(self, n_a):  # negative acceleration is a bool telling if ht player is slowing down or not
        global acceleration_control
        global count
        self.dx = 0
        if self.left_pressed and not self.right_pressed:
            self.run("left")
        elif self.right_pressed and not self.left_pressed:
            self.run("right")
        else:
            acceleration_control = 0

        if self.space_pressed:  # jumping (set to false later in function even if space is still pressed)
            self.y -= self.dy
            self.dy -= gravity
            if self.dy < -jump_height:
                self.dy = jump_height
                self.space_pressed = False

        if not n_a:
            self.x += self.dx
        else:
            if self.last_arrow_pressed == "right":
                self.dx = frame_step * count
            elif self.last_arrow_pressed == "left":
                self.dx = frame_step * -count
            self.x += self.dx
            count -= 1
            if count < 0:
                count = NEGATIVE_ACCELERATION_FRAMES

        self.rect.center = (self.x, self.y)

        self.current_sprite += FRAME_RATE
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
