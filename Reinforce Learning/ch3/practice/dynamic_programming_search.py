import util

_X_ = None

## future_dict
## state -> (min action, min cost, num visited)

class DynamicProgrammingSearch(util.SearchAlgorithm):
    def __init__(self, memory_use=True, verbose=0):
        self.memory_use = memory_use
        if memory_use:
            self.future_dict = {}
        self.verbose = verbose
        
    def future(self, problem, state):
        if self.memory_use and state in self.future_dict:
            actions, cost, _ = self.future_dict[state]  # use self.future_dict  ## 변경
            return actions, cost, 0

        num_visited = 1
        if problem.is_end(state):
            min_actions = util.LinkedList.create_list()
            min_cost = 0
        else:
            min_cost = float('inf')
            min_actions = None
            for action, successor, action_cost in problem.succ_and_cost(state):
                future_actions, future_cost, future_num_visited = self.future(problem, successor)
                num_visited += future_num_visited
                cost = action_cost + future_cost
                if cost < min_cost:
                    min_actions = future_actions.cons(action)
                    min_cost = cost
        if self.memory_use:
            self.future_dict[state] = min_actions, min_cost, num_visited
        return min_actions, min_cost, num_visited

    def solve(self, problem):
        actions, cost, num_visited = self.future(problem, problem.start_state())
        if self.verbose >= 1:
            print("numStatesVisited = {}".format(num_visited))
            print("totalCost = {}".format(cost))
            print("actions = {}".format(actions))
        return tuple(actions), cost, num_visited

