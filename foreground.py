import pygame as pg

# initializing pygame and the background surface
pg.init()

# initializing surfaces
foreground_surface_1 = pg.Surface((1440, 900))
foreground_surface_2 = pg.Surface((1440, 900))
# default black surface
default = pg.Surface((1440, 900))
default.set_colorkey((0, 0, 0))

# layer foreground surface 1
purple_bush = pg.image.load("Fantasy Game Assets/objects/fg_bush_purple.png")
purple_bush = pg.transform.scale(purple_bush, (500, 181))
orange_bush = pg.image.load("Fantasy Game Assets/objects/orange_bush.png")
orange_bush = pg.transform.scale(orange_bush, (500, 181))
statue = pg.image.load("Fantasy Game Assets/objects/statue.png")
statue = pg.transform.scale(statue, (165, 390))
foreground_surface_1.blit(statue, (50, 425))
foreground_surface_1.blit(purple_bush, (-50, 720))
foreground_surface_1.blit(orange_bush, (50, 790))
foreground_surface_1.blit(purple_bush, (1190, 700))
foreground_surface_1.blit(orange_bush, (1040, 730))
foreground_surface_1.set_colorkey((0, 0, 0))  # png

# layer foreground surface 2
bush = pg.image.load("Fantasy Game Assets/objects/fg_bush.png")
statue = pg.image.load("Fantasy Game Assets/objects/statue.png")
statue = pg.transform.scale(statue, (165, 390))
foreground_surface_2.blit(statue, (50, 425))
bush = pg.transform.scale(bush, (500, 181))
foreground_surface_2.blit(bush, (-50, 720))
foreground_surface_2.blit(bush, (50, 790))
foreground_surface_2.blit(bush, (1190, 700))
foreground_surface_2.blit(bush, (1040, 730))
foreground_surface_2.set_colorkey((0, 0, 0))  # png


def get_fg(surface_number):
    # transform into a png, then return the according surface depending on the map/player location
    if surface_number == 1:
        return foreground_surface_1
    elif surface_number == 2:
        return foreground_surface_2
    else:
        return default
