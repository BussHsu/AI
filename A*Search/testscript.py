import environment
import state
import sys
import astar
import bbfs
import  altastar

map_name = './tests/bbfs-1-jhsu.map'
energy = 247
start_x=2
start_y=1
end_x = 4
end_y=4

env = environment.TEnvironment(map_name,energy,
                              (end_x, end_y))
initial_state = state.State(start_x, start_y)
search = bbfs.Search(initial_state, env)
(solution, frontier, visited) = search.search()

if solution:
    print "Solution steps: " + str(solution.moves_so_far)
    print "Solution cost: %d" % solution.cost_so_far
else:
    print "No solution found"

# if not args.minimal_display:
print "Number of states considered: %d" % len(visited)
print
print "Frontier:"
for state in frontier:
    print state
print
print "Closed List:"
for state in visited:
    print state
