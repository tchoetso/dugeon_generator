###To Do: Tunnels cannot intersect rooms that they are not connecting to.


import random
import copy

class Room(object):
    """Represents a room in a map grid"""

    def __init__ (self, w=3, h=3, x='None', y='None'):
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def __str__ (self):
        return 'Room object with top left corner at %d,%d, width %d, and height %d' % (self.x, self.y, self.w, self.h)


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

                elif self.__dict__[(x+1,y+1)] == 'not blocked': # showing rooms
                    print ' ',
                elif self.__dict__[(x+1,y+1)] == 'unblocked': # showing tunnels
                    print '-',
                else:
                    print ' ',

        return ''




def generate_position(room, maps):
    """Generates x and y position for bottom left corner of room"""
    x_pos=random.randint(1, maps.w-room.w)
    y_pos=random.randint(1, maps.h-room.h)

    #Check to make sure rooms don't intersect and are not adjacent. Conditions are necessary to ensure no errors on edge cases.
    if x_pos == 1 and y_pos == 1:
        for i in range(room.w+1):
            for j in range(room.h+1):
                if maps[x_pos + i,y_pos + j] != 'blocked':
                    return generate_position(room,maps)
    elif x_pos == 1 and y_pos == maps.h-room.h:
        for i in range(room.w+1):
            for j in range(room.h+1):
                if maps[x_pos + i,y_pos + j-1] != 'blocked':
                    return generate_position(room,maps)
    elif x_pos == 1:
        for i in range(room.w+1):
            for j in range(room.h+2):
                if maps[x_pos + i,y_pos + j-1] != 'blocked':
                    return generate_position(room,maps)
    elif x_pos == maps.w-room.w and y_pos == 1:
        for i in range(room.w+1):
            for j in range(room.h+1):
                if maps[x_pos + i-1,y_pos + j] != 'blocked':
                    return generate_position(room,maps)
    elif x_pos == maps.w-room.w and y_pos == maps.h-room.h:
        for i in range(room.w+1):
            for j in range(room.h+1):
                if maps[x_pos + i-1,y_pos + j-1] != 'blocked':
                    return generate_position(room,maps)
    elif x_pos == maps.w-room.w:
        for i in range(room.w+1):
            for j in range(room.h+2):
                if maps[x_pos + i-1,y_pos + j-1] != 'blocked':
                    return generate_position(room,maps)
    elif y_pos == 1:
        for i in range(room.w+2):
            for j in range(room.h+1):
                if maps[x_pos-1 + i,y_pos + j] != 'blocked':
                    return generate_position(room,maps)
    elif y_pos == maps.h-room.h:
         for i in range(room.w+2):
            for j in range(room.h+1):
                if maps[x_pos + i-1,y_pos + j-1] != 'blocked':
                    return generate_position(room,maps)
    else:
        for i in range(room.w+2):
            for j in range(room.h+2):
                if maps[x_pos + i-1,y_pos + j-1] != 'blocked':
                    return generate_position(room,maps)
      
    return (x_pos,y_pos)

def update_map(rooms, map):
    for room in rooms:
        x_pos,y_pos =generate_position(room, map)
        room.x= x_pos
        room.y= y_pos
        for i in range(room.w):
            for j in range(room.h):
                map[x_pos+i,y_pos+j]='not blocked'


def horizontal_tunnel(x1,x2,y, y2, maps, d):#khkjhkjhkjh
    for x in range (min(x1,x2), max(x1,x2)+1):
        if (x,y) in d:
            if (x,y-1) not in d and (x,y-1) in maps and maps[x,y-2] != 'unblocked' and maps[x,y] != 'unblocked':
                maps[x,y-1]='unblocked'
                maps[max(x1,x2),y-1]='unblocked'
                horizontal_tunnel (x,max(x1,x2),y-1,y2,maps,d)
            elif (x,y+1) not in d and (x,y+1) in maps and maps[x,y ] != 'unblocked' and maps[x,y+2] != 'unblocked':
                maps[x,y+1]='unblocked'
                maps[max(x1,x2),y+1]='unblocked'
                horizontal_tunnel(x,max(x1,x2),y+1,y2,maps,d)
            elif (x-1,y-1) not in d and (x-1,y-1) in maps and maps[x-1,y-2] != 'unblocked'and maps[x,y] != 'unblocked':
                maps[x-1,y-1]='unblocked'
                maps[max(x1,x2),y-1]='unblocked'
                horizontal_tunnel(x-1,max(x1,x2),y-1,y2,maps,d)
            elif (x-1,y+1) not in d and (x-1,y+1) in maps and maps[x-1,y] != 'unblocked' and maps[x,y+22] != 'unblocked':
                maps[x-1,y+1]='unblocked'
                maps[max(x1,x2),y+1]='unblocked'
                horizontal_tunnel(x-1,max(x1,x2),y+1,y2,maps,d)

def horizontal_tunnel(x1,x2,y, y2, maps, d):
    for x in range (min(x1,x2), max(x1,x2)+1):
        if (x,y) in d:
            if (x,y-1) not in d and (x,y-1) in maps:
                maps[x,y-1]='unblocked'
                maps[max(x1,x2),y-1]='unblocked'
                horizontal_tunnel (x,max(x1,x2),y-1,y2,maps,d)
            elif (x,y+1) not in d and (x,y+1) in maps:
                maps[x,y+1]='unblocked'
                maps[max(x1,x2),y-1]='unblocked'
                horizontal_tunnel(x,max(x1,x2),y+1,y2,maps,d)
            elif (x-1,y-1) not in d and (x-1,y-1) in maps:
                maps[x-1,y-1]='unblocked'
                maps[max(x1,x2),y-1]='unblocked'
                horizontal_tunnel(x-1,max(x1,x2),y-1,y2,maps,d)
            elif (x-1,y+1) not in d and (x-1,y+1) in maps:
                maps[x-1,y+1]='unblocked'
                maps[max(x1,x2),y+1]='unblocked'
                horizontal_tunnel(x-1,max(x1,x2),y+1,y2,maps,d)  

        else:
            maps[x,y] = "unblocked"
           
def vertical_tunnel(y1,y2,x, x2, maps, d):
    for y in range(min(y1,y2),max(y1,y2)+1):
        if (x,y) in d:
            if (x-1,y) not in d and (x-1,y) in maps:
                maps[x-1,y]='unblocked'
                maps[x-1,max(y1,y2)]='unblocked'
                vertical_tunnel(y,max(y1,y2),x-1,x2,maps,d)
            elif (x+1,y) not in d and (x+1,y) in maps:
                maps[x+1,y]='unblocked'
                maps[x+2,max(y1,y2)]='unblocked'
                vertical_tunnel(y,max(y1,y2),x+1,x2,maps,d)
            elif (x-1,y) not in d and (x-1,y) in maps:
                maps[x-1,y-1]='unblocked'
                maps[x-1,max(y1,y2)]='unblocked'
                vertical_tunnel(y-1,max(y1,y2),x-1,x2,maps,d)
            elif (x+1,y-1) not in d and (x+1,y-1) in maps:
                maps[x+1,y-1]='unblocked'
                maps[x+2,max(y1,y2)]='unblocked'
                vertical_tunnel(y-1,max(y1,y2),x+1,x2,maps,d)
        else:
            maps[x,y] = "unblocked"

def draw_tunnels (rooms, maps):
    connected=dict()
    for n in range(len(rooms)):
        room = rooms[n]
        dontconnect=copy.deepcopy(rooms)
        d=dict()
        i=random.randint(0,len(rooms)-1)
        if i == n:
            if i == 0:
                i+=1
            else:
                i-=1
                
        if n+1 in connected:
            if i+1 not in connected[n+1]:
                connected[n+1].append(i+1)
        else:
            connected[n+1]=[i+1]
            
        if i+1 in connected:
            if n+1 not in connected[i+1]:
                connected[i+1].append(n+1)
        else:
            connected[i+1]=[n+1]
            
        if n>i:
            dontconnect.pop(n)
            dontconnect.pop(i)
        if i>n:
            dontconnect.pop(i)
            dontconnect.pop(n)
            
        for item in dontconnect:
            for x in range(item.w+2):
                for y in range(item.h+2):
                    d[item.x+x-1,item.y+y-1]='dontconnect'
                    
        j=random.randint(0,1)
        if j == 0:
            horizontal_tunnel(room.x, rooms[i].x, room.y, rooms[i].y, maps, d)
            vertical_tunnel(room.y, rooms[i].y, rooms[i].x, room.x, maps, d)

        if j == 1:
            vertical_tunnel(room.y, rooms[i].y, room.x, rooms[i].x, maps, d)
            horizontal_tunnel(room.x, rooms[i].x, rooms[i].y, room.y, maps, d)

    return connected

           
def main():
    maps=Map()
    room=Room()
    room2=Room(6,4)
    room3=Room(6,6)
    rooms=[room, room2, room3]
    update_map(rooms,maps)
    connected=draw_tunnels(rooms, maps)
    
    print maps
    print room
    print room2
    print room3
    print connected
    
if __name__ == '__main__':
    main()

