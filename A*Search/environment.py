#!/usr/bin/python

from state import *
import sys
import Heuristics


class Direction:
    N = 0
    E = 1
    S = 2
    W = 3

    def __init__(self,in_dir):
        self.code = in_dir
        if in_dir == Direction.N:
            self.move = Point(0,1)
        elif in_dir== Direction.E:
            self.move = Point(1,0)
        elif in_dir == Direction.S:
            self.move = Point(0,-1)
        else:
            self.move = Point(-1,0)

    def __str__(self):
        if self.code == Direction.N:
            return 'N'
        elif self.code == Direction.E:
            return 'E'
        elif self.code == Direction.S:
            return 'S'
        else:
            return 'W'

    def opposite(self):
        return Direction((self.code+2)%4)

class Environment:
    'Map-based environment'

    # Member data
    # elevations: raw data for each position, stored in a list of lists
    #             (each outer list represents a single row)
    # height: number of rows
    # width: number of elements in each row
    # end_x, end_y: location of goal

    directions = [Direction(Direction.N), Direction(Direction.E), Direction(Direction.S), Direction(Direction.W)]


    def __init__(self, mapfile, energy_budget, end_coords):
        self.elevations = []
        self.height = 0
        self.width = -1
        self.end_x, self.end_y = end_coords
        self.energy_budget = energy_budget
        # Read in the data
        for line in mapfile:
            nextline = [ int(x) for x in line.split() ]
            if self.width == -1:
                self.width = len(nextline)
            elif len(nextline) == 0:
                sys.stderr.write("No data (or parse error) on line %d\n"
                                 % (len(self.elevations) + 1))
                sys.exit(1)
            elif self.width != len(nextline):
                sys.stderr.write("Inconsistent map width in row %d\n"
                                 % (len(self.elevations) + 1))
                sys.stderr.write("Expected %d elements, saw %d\n"
                                 % (self.width, len(nextline)))
                sys.exit(1)
            self.elevations.insert(0, nextline)
        self.height = len(self.elevations)
        if self.end_x == -1:
            self.end_x = self.width - 1
        if self.end_y == -1:
            self.end_y = self.height - 1
        self.endpoint = Point(self.end_x,self.end_y)

    def get_elevation(self,x_pos,y_pos):
        return self.elevations[y_pos][x_pos]
    # is_goal
    #   in: state
    #   out:    True if reach goal, False if not
    def is_goal(self,in_state):
        if in_state.pos == self.endpoint:
            return True
        else:
            return False

    # step cost
    #   in:     position = (x,y)
    #           dir 0 = up(N), 1= right(E),2=down(S),3=left(W)
    #   out:    cost of the direction (-1 if not legal move)
    def step_cost(self,from_pos,dir,back_track = False):
        new_pos = from_pos+dir.move
        if new_pos.x<0 or new_pos.x>self.width-1 or new_pos.y<0 or new_pos.y>self.height-1:
            return -1
        if back_track:
            return self.calc_cost_from_diff(self.get_elevation(from_pos.x,from_pos.y)-self.get_elevation(new_pos.x,new_pos.y))
        return self.calc_cost_from_diff(self.get_elevation(new_pos.x,new_pos.y)-self.get_elevation(from_pos.x,from_pos.y))


    # calculate step cost from elevation difference
    #   in:     difference of elevation (to - from)
    #   out:    cost
    def calc_cost_from_diff(self,diff):
        if diff>0:
            return 1+diff*diff
        elif diff==0:
            return 1
        else:
            return 1-diff

    # get list of children from state
    #   in:     from_state
    #   out:    list of all children states
    def get_children_states(self, from_state, back_track = False):
        ret = [];

        #get all the children costs
        for dir in Environment.directions:
            cost = self.step_cost(from_state.pos,dir,back_track)
            if cost>-1:
                new_pos=from_state.pos+dir.move
                child = State(new_pos.x,new_pos.y)
                child.cost_so_far = from_state.cost_so_far+cost
                child.moves_so_far.extend(from_state.moves_so_far)
                if back_track:
                    child.moves_so_far.append(str(dir.opposite()))
                else:
                    child.moves_so_far.append(str(dir))
                ret.append(child)

        return ret


class TEnvironment:
    # The same as Environment, except reading data
    # Used for debugging in Pycharm

    directions = [Direction(Direction.N), Direction(Direction.E), Direction(Direction.S), Direction(Direction.W)]


    def __init__(self, mapfile, energy_budget, end_coords):
        self.elevations = []
        self.height = 0
        self.width = -1
        self.end_x, self.end_y = end_coords
        self.energy_budget = energy_budget
        mapobj = open(mapfile)
        # Read in the data
        for line in mapobj:
            nextline = [ int(x) for x in line.split() ]
            if self.width == -1:
                self.width = len(nextline)
            elif len(nextline) == 0:
                sys.stderr.write("No data (or parse error) on line %d\n"
                                 % (len(self.elevations) + 1))
                sys.exit(1)
            elif self.width != len(nextline):
                sys.stderr.write("Inconsistent map width in row %d\n"
                                 % (len(self.elevations) + 1))
                sys.stderr.write("Expected %d elements, saw %d\n"
                                 % (self.width, len(nextline)))
                sys.exit(1)
            self.elevations.insert(0, nextline)
        self.height = len(self.elevations)
        if self.end_x == -1:
            self.end_x = self.width - 1
        if self.end_y == -1:
            self.end_y = self.height - 1
        mapobj.close()
        self.endpoint = Point(self.end_x,self.end_y)

    def get_elevation(self,x_pos,y_pos):
        return self.elevations[y_pos][x_pos]
    # is_goal
    #   in: state
    #   out:    True if reach goal, False if not
    def is_goal(self,in_state):
        if in_state.pos == self.endpoint:
            return True
        else:
            return False

    # step cost
    #   in:     position = (x,y)
    #           dir 0 = up(N), 1= right(E),2=down(S),3=left(W)
    #   out:    cost of the direction (-1 if not legal move)
    def step_cost(self,from_pos,dir,back_track = False):
        new_pos = from_pos+dir.move
        if new_pos.x<0 or new_pos.x>self.width-1 or new_pos.y<0 or new_pos.y>self.height-1:
            return -1
        if back_track:
            return self.calc_cost_from_diff(self.get_elevation(from_pos.x,from_pos.y)-self.get_elevation(new_pos.x,new_pos.y))
        return self.calc_cost_from_diff(self.get_elevation(new_pos.x,new_pos.y)-self.get_elevation(from_pos.x,from_pos.y))


    # calculate one step cost from elevation difference
    #   in:     difference of elevation (to - from)
    #   out:    cost
    def calc_cost_from_diff(self,diff):
        if diff>0:
            return 1+diff*diff
        elif diff==0:
            return 1
        else:
            return 1-diff

    # get list of children from state
    #   in:     from_state
    #   out:    list of all children states
    def get_children_states(self, from_state, back_track = False):
        ret = [];

        #get all the children costs
        for dir in Environment.directions:
            cost = self.step_cost(from_state.pos,dir,back_track)
            if cost>-1:
                new_pos=from_state.pos+dir.move
                child = State(new_pos.x,new_pos.y)
                child.cost_so_far = from_state.cost_so_far+cost
                child.moves_so_far.extend(from_state.moves_so_far)
                if back_track:
                    child.moves_so_far.append(str(dir.opposite()))
                else:
                    child.moves_so_far.append(str(dir))
                ret.append(child)

        return ret
