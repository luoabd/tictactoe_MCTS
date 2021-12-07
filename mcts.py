# Originally written By Code Monkey King
# Source: https://github.com/maksimKorzh/tictactoe-mtcs/tree/master/src/tutorials/game_loop
# Edited by Abdellah Lahnaoui and Ben Platten from group 24
#
# MCTS algorithm implementation
#

# packages
import math
import random
import pandas as pd

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

# MCTS class


class MCTS():
    # combine steps of algorithm
    def tree_search(self, initial_state, minimax=False):
        # initialise tree
        self.root = TreeNode(initial_state, None)

        # iterations
        for iteration in range(1000):
            # print(f"iteration:{iteration}")
            # tree traversal step
            node = self.tree_traversal(self.root, iteration)

            # simulation step
            score = self.rollout(node.board)

            # backpropagate step to update nodes
            self.backpropagate(node, score, minimax)

        # make a move
        try:
            return self.get_best_move(self.root, 0)

        except:
            pass

    # taking the action that maximises the UCB score
    def tree_traversal(self, node, iteration=None):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_move(node, 2, iteration)

            # if not fully expanded
            else:
                return self.expand(node)

        return node

    # explore
    def expand(self, node):
        # generate legal states (moves) for the given node
        states = node.board.generate_states()

        for state in states:
            if str(state.position) not in node.children:
                # create node for new states
                new_node = TreeNode(state, node)

                # save as child
                node.children[str(state.position)] = new_node

                # if fully expanded
                if len(states) == len(node.children):
                    node.is_fully_expanded = True

                return new_node

    # simulate step

    def rollout(self, board):
        # simulate game until end
        while not board.is_win():
            try:
                # random move
                board = random.choice(board.generate_states())

            except:
                # draw
                return 0

        # score dependent on player
        if board.player_2 == 'x':
            return 1
        elif board.player_2 == 'o':
            return -1

    # backpropagate step
    def backpropagate(self, node, score, minimax=False):
        while node is not None:
            # add visit
            node.visits += 1

            # update score
            if minimax == False:
                node.score += score

            elif minimax == True:
                if node.board.player_2 == 'x':
                    node.score += score
                elif node.board.player_2 == 'o':
                    node.score += -abs(score)

            # move up tree
            node = node.parent

    # apply the UCB formula
    def get_best_move(self, node, exploration_constant, iteration=None):
        # function to help label the child nodes
        def generate_states(child):
            # define states list (move list - list of available actions to consider)
            actions = []

            # loop over board rows
            for col in range(3):
                # loop over board columns
                for row in range(3):
                    # make sure that current square is empty
                    if child.board.position[col, row] == child.board.empty_square:
                        # append available action/board state to action list
                        actions.append((col+1, row+1))

            # return the list of available actions (board class instances)
            return actions

        best_score = float('-inf')
        best_moves = []

        # df = pd.read_csv("convergence_minimax.csv")
        # temp = pd.DataFrame(columns=('iteration', 'move', 'score', 'empties'))
        # for all potential moves
        for i, child_node in enumerate(node.children.values()):
            empties = generate_states(child_node)
            # temp.loc[i] = [iteration, i, child_node.score, str(empties)]

            # score dependent on player
            if child_node.board.player_2 == 'x':
                current_player = 1
            elif child_node.board.player_2 == 'o':
                current_player = -1

            # UCB
            move_score = current_player * child_node.score / child_node.visits + \
                exploration_constant * \
                math.sqrt(math.log(node.visits / child_node.visits))

            # store best move
            if move_score > best_score:
                best_score = move_score
                best_moves = [child_node]

            elif move_score == best_score:
                best_moves.append(child_node)

        # save scores for plotting policy convergence
        # df = pd.concat([df, temp])
        # df.to_csv("convergence_minimax.csv", index=False)
        # random choice of best move
        return random.choice(best_moves)
