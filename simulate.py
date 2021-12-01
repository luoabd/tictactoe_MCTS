import random

from main import *
from mcts import *

print("Starting the simulation")

# how many games should play
NUM_SIM = 100
# Choose whther player 2 plays optimally or randomly
# True: optimal, False: random
player2_optimal = True

# Choose initial move you want:
possible_steps = [[0, 0], [0, 2], [2, 0], [2, 1], [2, 2]]
for possible_step in possible_steps:
    board = Board()
    board.restrict_board()
    mcts = MCTS()

    # set the first step condition for MCTS
    first_step = 1

    # To see the probability
    turn = 0
    count = 0
    wins = 0
    losses = 0
    ties = 0

    print(
        f"Calculating the probability of victory for action: {possible_step}")
    while count < NUM_SIM:
        if first_step == 0:
            if player2_optimal:
                try:
                    best_move = mcts.search(board)
                    board = best_move.board
                except:
                    pass
            else:
                # Rand player
                try:
                    random_move = random.choice(board.generate_states())
                    board = random_move
                except:
                    pass

            # AI player
            try:
                best_move = mcts.search(board)
                board = best_move.board
            except:
                pass

        elif first_step == 1:
            # restrict the first step of MCTS
            board = board.make_move(possible_step[0], possible_step[1])
            first_step = 0
        # Evaluate the result
        if board.is_win() or board.is_draw():
            if board.is_win():
                if board.player_2 == 'o':
                    losses += 1
                elif board.player_2 == 'x':
                    wins += 1
            elif board.is_draw():
                ties += 1

            count += 1
            # Reset the board to init state
            board.__init__()
            board.restrict_board()

            first_step = 1

            # if count % 25 == 0:
            #     expected_r = (wins - losses)/count
            #     print(count, " Step")
            #     print(" win probability : ", wins/count)
    print(f'wins: {wins}')
    print(f'losses: {losses}')
    print(f'ties: {ties}')
    print(f'winning probability: {wins/count}')
