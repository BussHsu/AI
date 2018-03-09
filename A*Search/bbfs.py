import state
class Search:
    def __init__(self, in_ini, in_env):
        self.frontier = [in_ini]
        self.cache = []
        self.back_frontier = [state.State(in_env.end_x, in_env.end_y)]
        self.env = in_env
        self.frontier_visited = []
        self.backf_visited = []

    def bfs_extend(self, openlist,  visited, backtrack):
        for curr_state in openlist:
            visited.append(curr_state)
            children_list = self.env.get_children_states(curr_state,backtrack)

            for node in children_list:
                if node.cost_so_far<= self.env.energy_budget:
                    if node in visited:
                        a = next(t for t in visited if t == node)
                        if node.cost_so_far < a.cost_so_far:
                            # remove the node from visited to maintain the lowest cost
                            visited.remove(a)
                        else:
                            continue
                    if node in self.cache:
                        a = next(t for t in self.cache if t == node)
                        if node.cost_so_far < a.cost_so_far:
                              self.cache.remove(a)
                        else:
                            continue
                    self.cache.append(node)


    def create_solution_state(self,intersect):
        state_from_goal=next(x for x in self.back_frontier if x == intersect)

        sol = state.State(self.env.end_x,self.env.end_y)
        sol.cost_so_far=intersect.cost_so_far+state_from_goal.cost_so_far
        sol.moves_so_far=list(intersect.moves_so_far)
        sol.moves_so_far.extend(reversed(state_from_goal.moves_so_far))
        return sol

    def get_cost(self,state):
        return state.cost_so_far


    def search(self):
        # get rid of the trivial case where goal = start
        if self.env.is_goal(self.frontier[0]):
            return self.frontier.pop(0), self.frontier, self.visited

        solution = None

        # Extend the frontier alternatively
        counter = 0;
        while(self.frontier or self.back_frontier):

            if((counter%2 is 0 and self.frontier) or not self.back_frontier):
                self.bfs_extend(self.frontier,self.frontier_visited,False)
                self.frontier = self.cache
                self.cache = []
            else:
                self.bfs_extend(self.back_frontier,self.backf_visited,True)
                self.back_frontier = self.cache
                self.cache = []

            intersect_list=[x for x in self.frontier if x in self.back_frontier]
            if intersect_list:
                intersect_list = sorted(intersect_list,key= self.get_cost)
                intersect = intersect_list[0]
                solution = self.create_solution_state(intersect)
                return solution, list(set().union(self.back_frontier,self.frontier)), list(set().union(self.frontier_visited,self.backf_visited))

            counter+=1


        return None, [], list(set().union(self.frontier_visited,self.backf_visited))

