import random

class Room(object):
    """Represents a room in a map grid"""

    def __init__ (self, w=3, h=3, x='None', y='None'):
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def __str__ (self):
        return 'Room object with bottom left corner at %d,%d, width %d, and height %d' % (self.x, self.y, self.w, self.h)


class Map(object):
    """Represents a map in points"""


    def __init__ (self, w=20, h=20):
        
        self.w = w
        self.h = h
        init=dict()
        for i in range(w):
            for j in range(h):
                init[i+1,j+1]='blocked'
        self.__dict__.update(init)

        
    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__
    
    def __len__(self):
        return len(self.__dict__)

    def __str__ (self):
        """prints graphical representation of map"""
        d=dict()
        for y in range(self.h):
            print ''
            for x in range(self.w):
                if self.__dict__[(x+1,y+1)] == 'blocked':
                    print 'x',
                else:
                    print ' ',
        return ''




def generate_position(room, map):
    """Generates x and y position for bottom left corner of room"""
    x_pos=random.randint(1, map.w-room.w)
    y_pos=random.randint(1, map.h-room.h)

    for i in range(room.w):
        for j in range(room.h):
            if map[x_pos + i,y_pos + j] != 'blocked':
                return generate_position(room,map)
    return (x_pos,y_pos)

def update_map(rooms, map):
    for room in rooms:
        x_pos,y_pos =generate_position(room, map)
        room.x= x_pos
        room.y= y_pos
        for i in range(room.w):
            for j in range(room.h):
                map[x_pos+i,y_pos+j]='not blocked'
    


def main():
    maps=Map()
    room=Room()
    room2=Room(6,4)
    room3=Room(2,8)
    rooms=[room, room2, room3]
    update_map(rooms,maps)
    print maps
    print room
    print room2
    print room3
    
if __name__ == '__main__':
    main()
