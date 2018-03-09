from state import *
import Heuristics as heu

class Search:
    def __init__(self, in_ini, in_env):
        self.frontier = [in_ini]
        self.env = in_env
        self.visited = []
        self.heu_calc = heu.AltHeuristic(self.env)
        # self.ini = in_ini

    def search(self):
        # if self.env.is_goal(self.ini):
        #     return self.ini

        # frontier.append(self.ini)
        solution = None
        # solution_flag = False
        while(self.frontier):

            curr_state = self.frontier.pop(0)

            if self.env.is_goal(curr_state):
                solution = curr_state
                self.visited.append(solution)
                break

            self.visited.append(curr_state)
            list = self.env.get_children_states(curr_state)
            self.frontier.extend(list)
            self.frontier = self.remove_dup(self.sort_by_astar(self.frontier))
            self.frontier = [x for x in self.frontier if x.cost_so_far<self.env.energy_budget]

        return solution, reversed(self.frontier), self.visited


    # def heuristic(self, state):
    #     start = state.pos
    #     end = Point(self.env.end_x, self.env.end_y)
    #     return (end-start).abs_sum()+abs(self.env.get_elevation(end.x,end.y) - self.env.get_elevation(start.x,start.y))

    def astar_value(self, state):
        astar_val= self.heu_calc.heuristic(state,len(self.visited))+state.cost_so_far
        if state.astar_val is not astar_val:
            state.astar_val = astar_val
        return astar_val;

    def sort_by_astar(self, list):
        newlist = [x for x in list if x not in self.visited]
        return sorted(newlist, key = self.astar_value)

    ## copy from stack_overflow
    #  remove duplicate in list while preserving order
    def remove_dup(self, seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]
