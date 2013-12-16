import random
import copy

class Item(object):
    """"Represents an item in the dungeon. Each Item takes up one tile and
    can be a quest objective.

    attributes: x, y, is_quest"""
    def __init__(self, x, y, is_quest=False):
        """Initializes the Item.
        
        x: int
        y: int
        is_quest: boolean"""
        self.x = x
        self.y = y
        self.is_quest = is_quest

class Room(object):
    """Represents a room in a map grid.
    
    attributes: x, y, w, h"""

    def __init__(self, w=None, h=None, x=None, y=None):
        """Initializes the Room.
        
        w: int, width of Room
        h: int, height of Room
        x: int, indicates position in map
        y: int, indicates position in map"""
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

class Dungeon(dict):
    """Map of (x,y) coordinates to tiles and items.

    attributes: w, h, connections, start_room, items
    w: int, width of Dungeon
    h: int, height of Dungeon
    start_room: Room object, the room the player starts in
    connections: dictionary of Rooms to adjacent Rooms
    items: Item objects within the dungeon"""

    # Bit values of cell type
    WALL = 0x0000
    ROOM = 0x0001
    PERIMETER = 0x0002
    TUNNEL = 0x0004
    QUEST = 0x0008
    ITEM = 0x000F

    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)] # (dx, dy)
    TUNNEL_LENGTH = 5  # Length of each tunnel section before changing direction

    def __init__(self, w=20, h=20):
        """Initializes the dungeon map.
        
        w: int
        h: int"""
        self.w = w
        self.h = h
        self.start_room = None
        self.connections = {}
        self.items = []
        for i in range(w):
            for j in range(h):
                self[i, j] = self.WALL

    def __str__(self):
        """Prints graphical representation of map"""
        layout = ""
        for y in range(self.h):
            for x in range(self.w):
                if self[x, y] == self.WALL:
                    layout += 'x'
                elif self[x, y] == self.PERIMETER:
                    layout += 'x'
                elif self[x, y] == self.ROOM:
                    layout += ' '
                elif self[x, y] == self.TUNNEL:
                    layout += '-'
                elif self[x, y] == self.ITEM:
                    layout += '@'
                elif self[x, y] == self.QUEST:
                    layout += '#'
            layout += '\n'

        return layout



    def get_valid_position(self, room):
        """Generates x and y position for bottom left corner of room. Rooms
        cannot intersect or be adjacent to each other.
        
        Returns: tuple of ints, (x,y)"""
        # Prevents rooms from extending out of the dungeon
        x_pos = random.randint(0, self.w - room.w - 1)
        y_pos = random.randint(0, self.h - room.h - 1)

        # Check to make sure rooms don't intersect and are not adjacent.
        for i in range(room.w + 1):
            for j in range(room.h + 1):
                if self[x_pos + i, y_pos + j] != self.WALL:
                    return self.get_valid_position(room)

        return (x_pos, y_pos)


    def place_rooms(self, rooms):
        """Places a list of rooms into the dungeon map.
        
        rooms: list of Room objects"""
        for k in range(len(rooms)):
            rooms[k].id = k
            self.connections[rooms[k]] = set() # Initialize the set of adjacent rooms
            rooms[k].x, rooms[k].y = self.get_valid_position(rooms[k])
            for i in range(-1, rooms[k].w + 1):
                for j in range(-1, rooms[k].h + 1):
                    if i == -1 or j == -1 or i == rooms[k].w or j == rooms[k].h:
                        self[rooms[k].x + i, rooms[k].y + j] = self.PERIMETER
                    else:
                        self[rooms[k].x + i, rooms[k].y + j] = self.ROOM

    def place_items(self, num_items):
        """Places items into the dungeon map.
        
        num_items: int"""
        for k in range(num_items):
            room = random.choice(self.connections.keys()) # pick a random room
            x, y = self.place_in_room(room)
            self[x,y] = self.ITEMS
            self.items.append(Item(x,y,False))

    def generate_quests(self):
        """Places quest items at three locations at three distances away from
        the starting room. Distance refers to the number of rooms a player must
        traverse to get to the quest location. The distances depend on how many
        rooms are in the dungeon."""
        adjacent = self.connections[self.start_room]
        curr = random.sample(adjacent,1) # equivalent of random.choice() for a set
                                         # but returns a list
        num_rooms = len(self.connections)
        distances = [num_rooms * .1, num_rooms * .25, num_rooms * .5]
        distances = [int(d) for d in distances]
        for k in range(max(distances)):
            if k + 1 in distances:
                x, y = self.place_in_room(curr[0])
                self[x,y] = self.QUEST
                self.items.append(Item(x,y,True))
            adjacent = self.connections[curr[0]]
            adjacent = adjacent - set(curr) # don't go back into the room you just came from
            curr = random.sample(adjacent,1) 


    def place_in_room(self, room):
        """Returns a random coordinate within a room
        
        room: Room object within the dungeon
        return: tuple of ints (x,y)"""
        x = random.randint(room.x, room.x + room.w)
        y = random.randint(room.y, room.y + room.h)

        while self[x, y] != self.ROOM:
            x = random.randint(room.x, room.x + room.w)
            y = random.randint(room.y, room.y + room.h)
        return x, y


    def make_connection(self, room):
        """Maps the last room visited to the current room.

        room: Room object"""
        # Don't make the connection if this is the first room you've hit or if
        # you're still in the same room as last time
        if (hasattr(self.make_connection, 'last_room') and 
            self.make_connection.last_room != room):
            self.connections[self.make_connection.last_room].add(room)
            self.connections[room].add(self.make_connection.last_room)
        self.make_connection.__func__.last_room = room

    def print_connections(self):
        """Prints our the room connections within the dungeon based on room ID."""
        for room, adjacent in self.connections.items():
            print str(room.id) + ': ',
            for adj_room in adjacent:
                print str(adj_room.id) + ' ',
            print

    def which_room(self, coord):
        """Checks if a coordinate is inside a room

        coord: tuple of ints, (x,y) coordinate
        returns: Room object that coord is within or False if not inside a room"""
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
        for n in range(self.TUNNEL_LENGTH):
            coord = tuple(sum(k) for k in zip(coord, direction))
            x, y = coord
            if x < 0 or y < 0 or x >= self.w or y >= self.h:
                return False
            if self[coord] == self.TUNNEL:
                return False
            if self[coord] == self.ROOM or self[coord] == self.PERIMETER: 
                room = self.connections.keys()[self.which_room(coord)]
                self.make_connection(room)
                try:
                    self.tunnel.unconnected.remove(room)
                except ValueError:
                    pass
            new_dungeon[coord] = self.TUNNEL
        return new_dungeon


    def tunnel(self, coord):
        """Recursively draw tunnels to connect all the rooms.

        coord: tuple of ints, (x,y) of current position"""
        # Uses method attributes to keep track of unconnected rooms between
        # function calls
        if not hasattr(self.tunnel, 'unconnected'):
            self.tunnel.__func__.unconnected = self.connections.keys()
        if self.tunnel.unconnected == []: # Stop if every room has been connected
            return self
        # Try to open tunnels in every direction, with depth-first tunneling
        # Shuffle the list of directions between each call, so it doesn't just
        # make a square 
        random.shuffle(self.DIRECTIONS)
        for direction in self.DIRECTIONS:
            new_dungeon = self.valid_tunnel(coord, direction)
            if new_dungeon:
                self = new_dungeon
                new_coord = tuple(
                    n + self.TUNNEL_LENGTH * dn for n, dn in zip(coord, direction))
                self = self.tunnel(new_coord)
        return self


    def connect_rooms(self):
        """Selects a random room to start and tunnels to connect all the other
        rooms."""
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
