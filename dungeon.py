# To Do: Tunnels cannot intersect rooms that they are not connecting to.
import random
import copy

# Bit values of cell type
WALL = 0x0000
ROOM = 0x0001
PERIMETER = 0x0002
TUNNEL = 0x0004

# Used to place tunnels, 1/3 chance changing directions
DIRECTIONS = [(0,1), (1,0), (0,-1), (-1,0)]
TUNNEL_LENGTH = 3 # Length of each tunnel section before changing direction

class Room(object):
    """Represents a room in a map grid"""
    def __init__(self, w=3, h=3, x='None', y='None'):
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def __str__(self):
        return 'Room object with top left corner at %d,%d, width %d, and height %d' % (self.x, self.y, self.w, self.h)


class Dungeon(dict):
    """Represents a map in points"""

    def __init__(self, w=20, h=20):
        self.w = w
        self.h = h
        for i in range(w):
            for j in range(h):
                self[i, j] = WALL

    def __str__(self):
        """prints graphical representation of map"""
        layout = ""
        for y in range(self.h):
            for x in range(self.w):
                if self[x, y] == WALL:
                    layout += 'x '
                elif self[x, y] == PERIMETER:
                    layout += 'x '
                elif self[x, y] == ROOM:
                    layout += '  '
                elif self[x, y] == TUNNEL:
                    layout += '- '
            layout += '\n'

        return layout


def get_valid_position(room, dungeon):
    """Generates x and y position for bottom left corner of room"""
    # Prevents rooms from extending out of the dungeon
    x_pos = random.randint(0, dungeon.w - room.w - 1)
    y_pos = random.randint(0, dungeon.h - room.h - 1)

    # Check to make sure rooms don't intersect and are not adjacent.
    for i in range(room.w + 1):
        for j in range(room.h + 1):
            if dungeon[x_pos + i, y_pos + j] != WALL:
                return get_valid_position(room, dungeon)

    return (x_pos, y_pos)


def place_rooms(rooms, dungeon):
    for room in rooms:
        room.x, room.y = get_valid_position(room, dungeon)
        for i in range(-1,room.w+1):
            for j in range(-1,room.h+1):
                if i == -1 or j == -1 or i == room.w or j == room.h:
                    dungeon[room.x + i, room.y + j] = PERIMETER
                else:
                    dungeon[room.x + i, room.y + j] = ROOM


def which_room(coord, rooms):
    x, y = coord
    for k in range(len(rooms)):
        left_edge = rooms[k].x
        right_edge = rooms[k].x + rooms[k].w
        top_edge = rooms[k].y
        bottom_edge = rooms[k].y + rooms[k].h
        if left_edge <= x <= right_edge and top_edge <= y <= bottom_edge:
            return k
    return False

def valid_tunnel(dungeon, coord, direction):
    """"Tries to open a new section of tunnel, which cannot 
    collide with other tunnels or run off the map.
    
    dungeon: map of (x,y) coordinates to cell typeru
    coord: tuple of int (x,y),  start of the tunnel
    direction: tuple of int (dx,dy), direction of tunnel
    return: new map with tunnel if successful, False,
    otherwise"""

    new_dungeon = copy.copy(dungeon)
    for n in range(TUNNEL_LENGTH):
        coord = tuple(sum(k) for k in zip(coord, direction))
        x, y = coord
        if x < 0 or y < 0 or x >= dungeon.w or y >= dungeon.h:
            return False
        if dungeon[coord] == TUNNEL:
            return False
        new_dungeon[coord] = TUNNEL
    return new_dungeon


def tunnel(dungeon, coord, unconnected):
    global DIRECTIONS
    random.shuffle(DIRECTIONS)
    if unconnected == []:
        return dungeon
    for direction in DIRECTIONS:
        print coord
        if dungeon[coord] == ROOM or dungeon[coord] ==PERIMETER:
            try: 
                unconnected.pop(which_room(coord, unconnected))
            except IndexError:
                pass
        new_dungeon = valid_tunnel(dungeon, coord, direction)
        if new_dungeon:
            dungeon = new_dungeon
            new_coord = tuple(n + TUNNEL_LENGTH * dn for n, dn in zip(coord, direction))
            dungeon = tunnel(dungeon, new_coord, unconnected)
    return dungeon


def connect_rooms(rooms, dungeon):
    start_room = random.choice(rooms)
    length = 3
    x = random.randint(start_room.x, start_room.x + start_room.w)
    y = random.randint(start_room.y, start_room.y + start_room.h)
    unconnected = copy.copy(rooms)
    dungeon = tunnel(dungeon, (x,y), unconnected)
        

def main():
    dungeon = Dungeon()
    room = Room()
    room2 = Room(6, 4)
    room3 = Room(6, 6)
    rooms = [room, room2, room3]
    place_rooms(rooms, dungeon)
    connect_rooms(rooms, dungeon)
    print dungeon


if __name__ == '__main__':
    main()
