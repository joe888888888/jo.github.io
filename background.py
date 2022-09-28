import pygame as pg

# initializing pygame and the background surface
pg.init()
background_surface = pg.Surface((1440, 900))

# initializing surfaces
background_surface_1 = pg.Surface((1440, 900))
background_surface_2 = pg.Surface((1440, 900))
# default surface
default = pg.Surface((1440, 900))

# layer background surface # 1 (purple trees, stone ground) ------------------------------------------------------------
background_1 = pg.image.load("Fantasy Game Assets/forest_background_layers/parallax_forest_back_trees.png")
background_1 = pg.transform.scale(background_1, (1440, 900))
background_surface.blit(background_1, (0, 0))
background_4 = pg.image.load("Fantasy Game Assets/forest_background_layers/parallax_forest_middle_trees.png")
background_4 = pg.transform.scale(background_4, (1440, 900))
background_surface.blit(background_4, (0, 0))
background_2 = pg.image.load("Fantasy Game Assets/forest_background_layers/parallax_forest_front_trees.png")
background_2 = pg.transform.scale(background_2, (1440, 900))
background_surface.blit(background_2, (0, 0))
stone_ground = pg.image.load("Fantasy Game Assets/objects/stone_ground.png")
stone_ground = pg.transform.scale(stone_ground, (360 + 25, 144))
background_surface.blit(stone_ground, (-15, 800))
background_surface.blit(stone_ground, (345, 800))
background_surface.blit(stone_ground, (705, 800))
background_surface.blit(stone_ground, (1065, 800))
# set this background to background surface 1
background_surface_1.blit(background_surface, (0, 0))

# layer background surface # 2 (orange trees/grass) ----------------------------------------------------------------------------
background_1 = pg.image.load("Fantasy Game Assets/forest_background_layers/orange-back-trees.png")
background_1 = pg.transform.scale(background_1, (1440, 900))
background_surface.blit(background_1, (0, 0))
background_2 = pg.image.load("Fantasy Game Assets/forest_background_layers/orange-middle-trees.png")
background_2 = pg.transform.scale(background_2, (1440, 1100))
background_surface.blit(background_2, (0, 0))
background_4 = pg.image.load("Fantasy Game Assets/forest_background_layers/orange-front-trees.png")
background_4 = pg.transform.scale(background_4, (1440, 900))
background_surface.blit(background_4, (0, 0))
ground = pg.image.load("Fantasy Game Assets/objects/grass_floor.png")
ground = pg.transform.scale(ground, (1440 + 25, 144))
background_surface.blit(ground, (-15, 800))
# set this background to background surface 1
background_surface_2.blit(background_surface, (0, 0))


def get_bg(surface_number):
    if surface_number == 1:
        return background_surface_1
    elif surface_number == 2:
        return background_surface_2
    else:
        return default
