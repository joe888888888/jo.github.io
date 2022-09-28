import sys
from player import *
from background import *
from foreground import *
from map import *

pg.init()

width, height = (1440, 900)
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

clock = pg.time.Clock()
start_time = pg.time.get_ticks()

center_position = width / 2, height / 2
mouse = center_position
ticks = 0
elapsed_time = 0

# create player
player = Player(width - 250)
player_group = pg.sprite.Group()
player_group.add(player)

# player control
player_flipped = True
animation = "idle"
player_move = False
acceleration_control = 0
current_screen = 1


def control_surfaces():
    global current_screen

    if not 0 <= player.get_player_position()[0] <= width:
        if player.get_player_position()[0] <= 0:  # player moved off the screen to the left
            player.set_player_position(width, player.get_player_position()[1])
            current_screen = navigate_map("left")
        else:
            player.set_player_position(0, player.get_player_position()[1])
            current_screen = navigate_map("right")
    elif not 0 <= player.get_player_position()[1] <= height:
        if player.get_player_position()[0] <= 0:  # top
            player.set_player_position(player.get_player_position()[0], height)
            current_screen = navigate_map("up")
        else:
            player.set_player_position(player.get_player_position()[0], 0)
            current_screen = navigate_map("down")


def display_bg():
    screen.blit(background, (0, 0))


def display_fg():
    screen.blit(foreground, (0, 0))


def draw_hud():
    # pg.mouse.set_visible(False)
    # health bar
    player_health = player.get_health()
    pg.draw.rect(screen, (200, 0, 0), (10, 10, (player_health * 3), 30))
    pg.draw.rect(screen, (0, 0, 0), (10, 10, 300, 30), 3)


def calc_dist(x1, y1, x2, y2):
    d = sqrt((x1 - x2) ** 2) + ((y1 - y2) ** 2)
    return d


def _exit():
    pg.quit()
    sys.exit()


def negative_acceleration():
    global acceleration_control
    deceleration = False
    if 0 < acceleration_control <= NEGATIVE_ACCELERATION_FRAMES:
        deceleration = True
        acceleration_control = 0
    return deceleration


def player_control():
    global player_flipped
    global animation
    global acceleration_control
    global NEGATIVE_ACCELERATION_FRAMES
    NEGATIVE_ACCELERATION_FRAMES = 15
    relative_position = player.get_dx()

    # running actions
    if not player.get_space_pressed():
        if relative_position != 0:
            animation = "run"
            player.switch_player_animation(animation)
        elif relative_position == 0:
            if animation == "run" or negative_acceleration():
                animation = "decelerate"
                acceleration_control += 1
            else:
                animation = "idle"
                acceleration_control = 0
                NEGATIVE_ACCELERATION_FRAMES = 0
            player.switch_player_animation(animation)

    # jump action
    elif player.get_space_pressed():
        animation = "jump"
        player.switch_player_animation(animation)
        if player.get_space_pressed():
            if player.get_dy() <= 0:
                animation = "fall"
                player.switch_player_animation(animation)

    # attack 1 and 2 action
    if player.get_attack_1_pressed():
        if animation == "idle":
            player.attack(1)
        else:
            player.set_attack_1_pressed(False)

    elif player.get_attack_2_pressed():
        if animation == "idle":
            player.attack(2)
        else:
            player.set_attack_2_pressed(False)

    if player_flipped:
        player.flip_sprites()

    if player.get_last_arrow_pressed() == "left" or not player_move:
        player_flipped = True
    else:
        player_flipped = False

    player_group.draw(screen)

    player.update(negative_acceleration())


def user_inputs():
    global elapsed_time
    global ticks
    global player_move
    for event in pg.event.get():
        if event.type == pg.QUIT: _exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE: _exit()

            if event.key == pg.K_RIGHT:
                player.set_right_pressed(True)
                player_move = True
            if event.key == pg.K_LEFT:
                player.set_left_pressed(True)
            if event.key == pg.K_a:
                player.set_left_pressed(True)
            if event.key == pg.K_d:
                player.set_right_pressed(True)
                player_move = True
            if event.key == pg.K_SPACE:
                player.set_space_pressed(True)
            if event.key == pg.K_UP:
                player.set_space_pressed(True)
            if event.key == pg.K_q:
                player.set_attack_1_pressed(True)
            if event.key == pg.K_e:
                player.set_attack_2_pressed(True)

        elif event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                player.set_right_pressed(False)
            if event.key == pg.K_LEFT:
                player.set_left_pressed(False)
            if event.key == pg.K_a:
                player.set_left_pressed(False)
            if event.key == pg.K_d:
                player.set_right_pressed(False)


create_map()

while True:
    control_surfaces()
    # set the background and foreground
    background = get_bg(current_screen)
    foreground = get_fg(current_screen)
    user_inputs()

    clock.tick(60)
    display_bg()

    player_control()

    display_fg()
    draw_hud()

    pg.display.update()
