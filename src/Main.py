# CM3038 Artificial Intelligence for Problem Solving
# Sheepherding Puzzle — A* Search Implementation

import aips.informed.search as informedsearch
import aips.search as search


class ShepherdingState(search.State):
    def __init__(self, a_sheep, b_sheep, field_sheep, amax, bmax):
        self.a_sheep = a_sheep
        self.b_sheep = b_sheep
        self.field_sheep = field_sheep
        self.amax = amax
        self.bmax = bmax

    def __str__(self):
        return (
            f"Pen A: {self.a_sheep} (max:{self.amax}) "
            f"Pen B: {self.b_sheep} (max:{self.bmax})"
        )

    def __repr__(self):
        return (
            f"ShepherdingState(a={self.a_sheep}, b={self.b_sheep}, "
            f"field={self.field_sheep}, amax={self.amax}, bmax={self.bmax})"
        )

    def __eq__(self, other):
        return (
            isinstance(other, ShepherdingState)
            and self.a_sheep == other.a_sheep
            and self.b_sheep == other.b_sheep
            and self.amax == other.amax
            and self.bmax == other.bmax
        )

    def __hash__(self):
        return hash((self.a_sheep, self.b_sheep, self.amax, self.bmax))

    def successor(self):
        successors = []

        # Field -> Pen A
        if self.a_sheep < self.amax and self.field_sheep > 0:
            n = min(self.amax - self.a_sheep, self.field_sheep)
            successors.append(
                search.ActionStatePair(
                    MoveSheepToA(n),
                    ShepherdingState(
                        self.a_sheep + n,
                        self.b_sheep,
                        self.field_sheep - n,
                        self.amax,
                        self.bmax,
                    ),
                )
            )

        # Field -> Pen B
        if self.b_sheep < self.bmax and self.field_sheep > 0:
            n = min(self.bmax - self.b_sheep, self.field_sheep)
            successors.append(
                search.ActionStatePair(
                    MoveSheepToB(n),
                    ShepherdingState(
                        self.a_sheep,
                        self.b_sheep + n,
                        self.field_sheep - n,
                        self.amax,
                        self.bmax,
                    ),
                )
            )

        # Pen A -> Field
        if self.a_sheep > 0:
            n = self.a_sheep
            successors.append(
                search.ActionStatePair(
                    MoveSheepToField(n, "A"),
                    ShepherdingState(
                        0,
                        self.b_sheep,
                        self.field_sheep + n,
                        self.amax,
                        self.bmax,
                    ),
                )
            )

        # Pen B -> Field
        if self.b_sheep > 0:
            n = self.b_sheep
            successors.append(
                search.ActionStatePair(
                    MoveSheepToField(n, "B"),
                    ShepherdingState(
                        self.a_sheep,
                        0,
                        self.field_sheep + n,
                        self.amax,
                        self.bmax,
                    ),
                )
            )

        # Pen A -> Pen B
        if self.a_sheep > 0 and self.b_sheep < self.bmax:
            n = min(self.a_sheep, self.bmax - self.b_sheep)
            successors.append(
                search.ActionStatePair(
                    MoveSheepBetweenPens(n, "A", "B"),
                    ShepherdingState(
                        self.a_sheep - n,
                        self.b_sheep + n,
                        self.field_sheep,
                        self.amax,
                        self.bmax,
                    ),
                )
            )

        # Pen B -> Pen A
        if self.b_sheep > 0 and self.a_sheep < self.amax:
            n = min(self.b_sheep, self.amax - self.a_sheep)
            successors.append(
                search.ActionStatePair(
                    MoveSheepBetweenPens(n, "B", "A"),
                    ShepherdingState(
                        self.a_sheep + n,
                        self.b_sheep - n,
                        self.field_sheep,
                        self.amax,
                        self.bmax,
                    ),
                )
            )

        return successors


class MoveSheepToA(search.Action):
    def __init__(self, n):
        super().__init__()
        self.num_sheep_to_move = n
        self.cost = 60 * n

    def __str__(self):
        return f"Moving sheep from the field to Pen A. Cost: {self.cost}"


class MoveSheepToB(search.Action):
    def __init__(self, n):
        super().__init__()
        self.num_sheep_to_move = n
        self.cost = 60 * n

    def __str__(self):
        return f"Moving sheep from the field to Pen B. Cost: {self.cost}"


class MoveSheepToField(search.Action):
    def __init__(self, n, source_pen):
        super().__init__()
        self.num_sheep_to_move = n
        self.source_pen = source_pen
        self.cost = 5 * n

    def __str__(self):
        return f"Moving sheep from Pen {self.source_pen} to the field. Cost: {self.cost}"


class MoveSheepBetweenPens(search.Action):
    def __init__(self, n, source_pen, dest_pen):
        super().__init__()
        self.num_sheep_to_move = n
        self.source_pen = source_pen
        self.dest_pen = dest_pen
        self.cost = 30 * n

    def __str__(self):
        return (
            f"Moving sheep from Pen {self.source_pen} to Pen {self.dest_pen}. "
            f"Cost: {self.cost}"
        )


class ShepherdingSearch(informedsearch.BestFirstSearchProblem):
    def __init__(self, start_state, goal_state):
        super().__init__(start_state, goal_state)
        self.goal_state = goal_state

    def isGoal(self, state):
        return state == self.goal_state

    def evaluation(self, node):
        return node.getCost() + self.heuristic(node.state)

    def heuristic(self, state):
        # Conservative admissible lower bound:
        # each sheep still needing to change pen counts must cost at least 5 seconds
        a_distance = abs(state.a_sheep - self.goal_state.a_sheep)
        b_distance = abs(state.b_sheep - self.goal_state.b_sheep)
        return (a_distance + b_distance) * 5


def run_problem(amax, bmax, a0, b0, an, bn, field_sheep=99999):
    initial_state = ShepherdingState(a0, b0, field_sheep, amax, bmax)
    goal_state = ShepherdingState(an, bn, field_sheep, amax, bmax)

    problem = ShepherdingSearch(initial_state, goal_state)
    result = problem.search()

    print(f"Problem: {initial_state} -> {goal_state}")
    print(f"Node explored: {problem.nodeVisited}")

    if result is None:
        print("No solution found.")
    else:
        print(f"Cost: {result.cost}")
        print(result)


if __name__ == "__main__":
    # Basic problem from spec
    run_problem(9, 15, 0, 0, 0, 12)
    run_problem(9, 15, 0, 0, 9, 16)
    run_problem(10, 7, 0, 0, 0, 5)