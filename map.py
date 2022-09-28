# (0,0) --> 50

start_y = 0
start_x = 0
x = start_x
y = start_y
start_coordinates = (start_x, start_y)
current_coordinates = start_coordinates
start_location = 1
current_location = start_location

MAP_HEIGHT = 4
MAP_WIDTH = 20

locations = []


def coordinates_to_location(coordinates):
    for l in range(0, len(locations)):
        if (locations[l][0], locations[l][1]) == coordinates:
            return locations[l][2]


def create_map():
    count = 0
    for i in range(0, MAP_HEIGHT):
        for j in range(0, MAP_WIDTH):
            locations.append(((j - MAP_WIDTH / 2), (i - MAP_HEIGHT / 2), count))
            count += 1


def get_current_location():
    return current_location


def navigate_map(flag):  # flag will return "left", "right", "up", or "down
    global current_coordinates
    global current_location
    global x, y
    if flag == "up":
        x += 1
    elif flag == "down":
        x -= 1
    elif flag == "left":
        x -= 1
    elif flag == "right":
        x += 1
    else:
        return start_location
    current_coordinates = (x, y)
    current_location = coordinates_to_location(current_coordinates) - 49
    return current_location
