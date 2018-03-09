class Point:
    def __init__(self,pos_x,pos_y):
        self.x = pos_x;
        self.y = pos_y;

    def __add__(self,other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self,other):
        return Point(self.x-other.x, self.y - other.y)

    def __str__(self):
        return '('+str(self.x)+', '+str(self.y)+')'

    def __eq__(self,other):
        return self.x==other.x and self.y == other.y

    def abs_sum(self):
        return abs(self.x)+abs(self.y)

    def to_tuple(self):
        return (self.x,self.y)


class State:
    'Map-based environment'

    # Member data
    # elevations: raw data for each position, stored in a list of lists
    #             (each outer list represents a single row)
    # height: number of rows
    # width: number of elements in each row
    # end_x, end_y: location of goal

    def __init__(self, x_pos, y_pos):
        self.pos = Point(x_pos, y_pos)
        self.moves_so_far = []
        self.cost_so_far = 0
        self.astar_val = 0

    def __str__(self):
        return "Pos="+str(self.pos)+' Moves='+str(self.moves_so_far)+' Cost='+str(self.cost_so_far) #+' A*='+str(self.astar_val)

    def __eq__( self, other ):
        # print "A __eq__ called: "+str(self.pos)+" == "+str(other.pos)+"? " +str(self.pos==other.pos)
        return self.pos==other.pos

    def __hash__(self):
        return hash(self.pos.to_tuple())

