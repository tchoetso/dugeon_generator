# To Do: Tunnels cannot intersect rooms that they are not connecting to.
import random
import copy

# Bit values of cell type
WALL = 0x0000
ROOM = 0x0001
PERIMETER = 0x0002
TUNNEL = 0x0004
QUEST = 0x0008
ITEM = 0x000F

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)] # (dx, dy)
TUNNEL_LENGTH = 5  # Length of each tunnel section before changing direction


class Item(object):
    def __init__(self, x, y, is_quest=False):
        self.x = x
        self.y = y
        self.is_quest = is_quest

class Room(object):

    """Represents a room in a map grid"""

    def __init__(self, w=None, h=None, x=None, y=None):
        if w == None:
            self.w = random.randint(3, 10)
        else:
            self.w = w
        if h == None:
           self.h = random.randint(3, 10)
        else:
            self.h = h
        self.x = x
        self.y = y
        self.id = None

    def __str__(self):
        return 'At (%d,%d), with width %d, and height %d' % (self.x, self.y, self.w, self.h)


class Dungeon(dict):
    """Represents a map in points"""

    def __init__(self, w=20, h=20, connections=None, start_room=None):
        self.w = w
        self.h = h
        self.start_room = None
        self.connections = {}
        self.items = []
        for i in range(w):
            for j in range(h):
                self[i, j] = WALL

    def __str__(self):
        """prints graphical representation of map"""
        layout = ""
        for y in range(self.h):
            for x in range(self.w):
                if self[x, y] == WALL:
                    layout += 'x'
                elif self[x, y] == PERIMETER:
                    layout += 'x'
                elif self[x, y] == ROOM:
                    layout += ' '
                elif self[x, y] == TUNNEL:
                    layout += '-'
                elif self[x, y] == ITEM:
                    layout += '@'
                elif self[x, y] == QUEST:
                    layout += '#'
            layout += '\n'

        return layout



    def get_valid_position(self, room):
        """Generates x and y position for bottom left corner of room"""
        # Prevents rooms from extending out of the dungeon
        x_pos = random.randint(0, self.w - room.w - 1)
        y_pos = random.randint(0, self.h - room.h - 1)

        # Check to make sure rooms don't intersect and are not adjacent.
        for i in range(room.w + 1):
            for j in range(room.h + 1):
                if self[x_pos + i, y_pos + j] != WALL:
                    return self.get_valid_position(room)

        return (x_pos, y_pos)


    def place_rooms(self, rooms):
        for k in range(len(rooms)):
            rooms[k].id = k
            self.connections[rooms[k]] = set()
            rooms[k].x, rooms[k].y = self.get_valid_position(rooms[k])
            for i in range(-1, rooms[k].w + 1):
                for j in range(-1, rooms[k].h + 1):
                    if i == -1 or j == -1 or i == rooms[k].w or j == rooms[k].h:
                        self[rooms[k].x + i, rooms[k].y + j] = PERIMETER
                    else:
                        self[rooms[k].x + i, rooms[k].y + j] = ROOM

    def place_items(self, num_items):
        for k in range(num_items):
            room = random.choice(self.connections.keys())
            x, y = self.place_in_room(room)
            self[x,y] = ITEM
            self.items.append(Item(x,y,False))

    def generate_quests(self):
        adjacent = self.connections[self.start_room]
        curr = random.sample(adjacent,1) # equivalent of random.choice() for a set
        num_rooms = len(self.connections)
        distances = [num_rooms * .1, num_rooms * .25, num_rooms * .5]
        distances = [int(d) for d in distances]
        for k in range(max(distances)):
            if k + 1 in distances:
                x, y = self.place_in_room(curr[0])
                self[x,y] = QUEST
                self.items.append(Item(x,y,True))
            adjacent = self.connections[curr[0]]
            adjacent = adjacent - set(curr) # don't go back into the room you just came from
            curr = random.sample(adjacent,1) 


    def place_in_room(self, room):
        """Returns a random coordinate within a room
        room: Room object within self
        return: tuple of ints (x,y)"""
        x = random.randint(room.x, room.x + room.w)
        y = random.randint(room.y, room.y + room.h)

        while self[x, y] != ROOM:
            x = random.randint(room.x, room.x + room.w)
            y = random.randint(room.y, room.y + room.h)
        return x, y


    def make_connection(self, room):
        if hasattr(self.make_connection, 'last_room') and self.make_connection.last_room != room:
            self.connections[self.make_connection.last_room].add(room)
            self.connections[room].add(self.make_connection.last_room)
        self.make_connection.__func__.last_room = room

    def print_connections(self):
        for room, adjacent in self.connections.items():
            print str(room.id) + ': ',
            for adj_room in adjacent:
                print str(adj_room.id) + ' ',
            print

    def which_room(self, coord):
        x, y = coord
        rooms = self.connections.keys()
        for k in range(len(rooms)):
            left_edge = rooms[k].x - 1
            right_edge = rooms[k].x + rooms[k].w + 1
            top_edge = rooms[k].y - 1 
            bottom_edge = rooms[k].y + rooms[k].h + 1
            if left_edge <= x <= right_edge and top_edge <= y <= bottom_edge:
                return k
        return False


    def valid_tunnel(self, coord, direction):
        """"Tries to open a new section of tunnel, which cannot 
        collide with other tunnels or run off the map.
        
        dungeon: map of (x,y) coordinates to cell typeru
        coord: tuple of int (x,y),  start of the tunnel
        direction: tuple of int (dx,dy), direction of tunnel
        return: new map with tunnel if successful, False,
        otherwise"""

        new_dungeon = copy.copy(self)
        for n in range(TUNNEL_LENGTH):
            coord = tuple(sum(k) for k in zip(coord, direction))
            x, y = coord
            if x < 0 or y < 0 or x >= self.w or y >= self.h:
                return False
            if self[coord] == TUNNEL:
                return False
            if self[coord] == ROOM or self[coord] == PERIMETER: 
                room = self.connections.keys()[self.which_room(coord)]
                self.make_connection(room)
                try:
                    self.tunnel.unconnected.remove(room)
                except ValueError:
                    pass
            new_dungeon[coord] = TUNNEL
        return new_dungeon


    def tunnel(self, coord):
        if not hasattr(self.tunnel, 'unconnected'):
            self.tunnel.__func__.unconnected = self.connections.keys()
        if self.tunnel.unconnected == []:
            return self
        global DIRECTIONS
        random.shuffle(DIRECTIONS)
        for direction in DIRECTIONS:
            new_dungeon = self.valid_tunnel(coord, direction)
            if new_dungeon:
                self = new_dungeon
                new_coord = tuple(
                    n + TUNNEL_LENGTH * dn for n, dn in zip(coord, direction))
                self = self.tunnel(new_coord)
        return self


    def connect_rooms(self):
        self.start_room = random.choice(self.connections.keys())
        x, y = self.place_in_room(self.start_room)
        self = self.tunnel((x, y))
        return self


def main():
    dungeon = Dungeon(50, 50)
    rooms = [Room() for k in range(10)]
    dungeon.place_rooms(rooms)
    dungeon = dungeon.connect_rooms()
    dungeon.generate_quests()
    dungeon.place_items(10)
    f = open('map.txt', 'w')
    f.write(str(dungeon))
if __name__ == '__main__':
    main()
