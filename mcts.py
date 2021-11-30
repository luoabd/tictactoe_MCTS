# tree node class definition
class TreeNode():
    # class constructor (create tree node class instance)
    def __init__(self, board, parent):
        # init associated board state
        self.board = board

        # init is node terminal flag
        if self.board.is_win() or self.board.is_draw():
            # we have a terminal node
            self.is_terminal = True

        # otherwise
        else:
            # we have a non-terminal node
            self.is_terminal = False

        # init is fully expanded flag
        self.is_fully_expanded = self.is_terminal

        # init parent node if available
        self.parent = parent

        # init the number of node visits
        self.visits = 0

        # init the total score of the node
        self.score = 0

        # init current node's children
        self.children = {}

# MCTS class definition


class MCTS():
    # search for the best move in the current position
    def search(self, initial_state):
        pass
    # Selection
    def select(self, node):
        pass
    # Expansion
    def expand(self, node):
        pass
    # Simulation
    def simulate(self, board):
        pass
    # Backpropagation
    def backpropagate(self, node, score):
        pass
    # Choose in each node of the game tree the move corresponding to the highest UCB formula
    # this is the Exploration and exploitation step which will be used in search and select
    def choose_move(self, node):
        pass
