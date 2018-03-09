from state import *
class SimpleHeuristic:
    def __init__(self,env):
        self.env = env
        self.goal = Point(env.end_x,env.end_y)

    def heuristic(self, state, goal= None):
        if goal is None:
            goal = self.goal
        start = state.pos
        a=(goal-start).abs_sum()
        b=abs(self.env.get_elevation(goal.x,goal.y) - self.env.get_elevation(start.x,start.y))
        return a+b

class AltHeuristic:
    def __init__(self,env):
        self.env = env
        self.goal = Point(env.end_x,env.end_y)

    def heuristic(self, state, num_visited, goal= None):
        if goal is None:
            goal = self.goal
        start = state.pos
        a=(goal-start).abs_sum()

        # my alternate heuristics can provide better virtical estimation when goal is higher than target
        b=self.env.get_elevation(goal.x,goal.y) - self.env.get_elevation(start.x,start.y)
        if b>=0:
            max_remain_moves = self.env.width*self.env.height - num_visited
            c=(b/max_remain_moves)**2*max_remain_moves
            vertical_est = max(b,c)
        else:
            vertical_est = -b
        return a+vertical_est
