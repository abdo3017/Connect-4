from math import sqrt
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from csv import reader
from math import sqrt
import random
import pygame
import random
import sys
import math
import copy



# region Gaming
class Gaming:
    def __init__(self):
        self.COLOR_BLUE = (0, 0, 240)
        self.COLOR_BLACK = (0, 0, 0)
        self.COLOR_RED = (255, 0, 0)
        self.COLOR_YELLOW = (255, 255, 0)

        self.Y_COUNT = int(5)
        self.X_COUNT = int(8)

        self.PLAYER = 0
        self.AI = 1

        self.PLAYER_PIECE = 1
        self.AI_PIECE = 2

        self.WINNING_WINDOW_LENGTH = 3
        self.EMPTY = 0
        self.WINNING_POSITION = []
        self.SQUARESIZE = 80

        self.width = self.X_COUNT * self.SQUARESIZE
        self.height = (self.Y_COUNT + 1) * self.SQUARESIZE

        self.size = (self.width, self.height)

        self.RADIUS = int(self.SQUARESIZE / 2 - 5)

        self.screen = pygame.display.set_mode(self.size)

    def create_board(self):
        board = np.zeros((self.Y_COUNT, self.X_COUNT))
        return board

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(self, board, col):
        return board[self.Y_COUNT - 1][col] == 0

    def get_next_open_row(self, board, col):
        for r in range(self.Y_COUNT):
            if board[r][col] == 0:
                return r

    def print_board(self, board):
        print(np.flip(board, 0))

    def winning_move(self, board, piece):
        self.WINNING_POSITION.clear()
        for c in range(self.X_COUNT - 2):
            for r in range(self.Y_COUNT):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece:
                    self.WINNING_POSITION.append([r, c])
                    self.WINNING_POSITION.append([r, c + 1])
                    self.WINNING_POSITION.append([r, c + 2])
                    return True

        for c in range(self.X_COUNT):
            for r in range(self.Y_COUNT - 2):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece:
                    self.WINNING_POSITION.append([r, c])
                    self.WINNING_POSITION.append([r + 1, c])
                    self.WINNING_POSITION.append([r + 2, c])
                    return True

        for c in range(self.X_COUNT - 2):
            for r in range(self.Y_COUNT - 2):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece:
                    self.WINNING_POSITION.append([r, c])
                    self.WINNING_POSITION.append([r + 1, c + 1])
                    self.WINNING_POSITION.append([r + 2, c + 2])
                    return True

        for c in range(self.X_COUNT - 2):
            for r in range(2, self.Y_COUNT):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece:
                    self.WINNING_POSITION.append([r, c])
                    self.WINNING_POSITION.append([r - 1, c + 1])
                    self.WINNING_POSITION.append([r - 2, c + 2])
                    return True

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.PLAYER_PIECE
        if piece == self.PLAYER_PIECE:
            opp_piece = self.AI_PIECE

        if window.count(piece) == 3:
            score += 100
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 1:
            score += 5

        if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
            score -= 4

        return score

    def score_position(self, board, piece):
        score = 0

        center_array = [int(i) for i in list(board[:, self.X_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        for r in range(self.Y_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.X_COUNT - 3):
                window = row_array[c: c + self.WINNING_WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        for c in range(self.X_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.Y_COUNT - 3):
                window = col_array[r: r + self.WINNING_WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        for r in range(self.Y_COUNT - 3):
            for c in range(self.X_COUNT - 3):
                window = [board[r + i][c + i] for i in range(self.WINNING_WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(self.Y_COUNT - 3):
            for c in range(self.X_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(self.WINNING_WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def is_terminal_node(self, board):
        return self.winning_move(board, self.PLAYER_PIECE) or self.winning_move(board, self.AI_PIECE) or len(
            self.get_valid_locations(board)) == 0


    def AlphaBeta(self, board, depth, alpha, beta, currentPlayer):
        '''Implement here'''
        valid_locations = self.get_valid_locations(board)
        if depth == 0 or self.is_terminal_node(board):
            return None, self.score_position(board, self.AI_PIECE)

        if currentPlayer:
            column = random.choice(valid_locations)
            value = -math.inf
            for move in valid_locations:
                temp_board = board.copy()
                row = self.get_next_open_row(temp_board, move)
                self.drop_piece(temp_board, row, move, self.AI_PIECE)
                val = self.AlphaBeta(temp_board, depth - 1, alpha, beta, not currentPlayer)[1]
                if val > value:
                    column = move

                value = max(value, val)
                alpha = max(alpha, value)

                if alpha >= beta:
                    break

            return column, value
        else:
            column = random.choice(valid_locations)
            value = math.inf
            for move in reversed(valid_locations):
                templateBoard = board.copy()
                move = random.choice(valid_locations)
                row = self.get_next_open_row(templateBoard, move)
                self.drop_piece(templateBoard, row, move, self.PLAYER_PIECE)
                val = self.AlphaBeta(templateBoard, depth - 1, alpha, beta, not currentPlayer)[1]
                if val < value:
                    column = move

                value = min(value, val)
                beta = min(beta, value)

                if alpha >= beta:
                    break
            return column, value

    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(self.X_COUNT):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def pick_best_move(self, board, piece):
        best_score = -10000
        valid_locations = self.get_valid_locations(board)
        best_col = random.choice(valid_locations)

        for col in valid_locations:
            row = self.get_next_open_row(board, col)
            temp_board = board.copy()
            self.drop_piece(temp_board, row, col, piece)
            score = self.score_position(temp_board, piece)

            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    def draw_board(self, board):
        for c in range(self.X_COUNT):
            for r in range(self.Y_COUNT):
                pygame.draw.rect(self.screen, self.COLOR_BLUE,
                                 (c * self.SQUARESIZE, r * self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE,
                                  self.SQUARESIZE))
                pygame.draw.circle(self.screen, self.COLOR_BLACK, (
                    int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                    int(r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE / 2)),
                                   self.RADIUS)

        for c in range(self.X_COUNT):
            for r in range(self.Y_COUNT):
                if board[r][c] == self.PLAYER_PIECE:
                    pygame.draw.circle(self.screen, self.COLOR_RED, (
                        int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                        self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)),
                                       self.RADIUS)
                elif board[r][c] == self.AI_PIECE:
                    pygame.draw.circle(self.screen, self.COLOR_YELLOW, (
                        int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                        self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)),
                                       self.RADIUS)
        pygame.display.update()


# endregion



####################################  Main Functions #####################################

# region Gaming_Main_fn
def Gaming_Main():
    game = Gaming()
    board = game.create_board()
    game.print_board(board)
    game_over = False

    pygame.init()

    game.draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 50)

    turn = 1

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(game.screen, game.COLOR_BLACK, (0, 0, game.width, game.SQUARESIZE))
                posx = event.pos[0]
                if turn == game.PLAYER:
                    pygame.draw.circle(game.screen, game.COLOR_RED, (posx, int(game.SQUARESIZE / 2)), game.RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(game.screen, game.COLOR_BLACK, (0, 0, game.width, game.SQUARESIZE))

                if turn == game.PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / game.SQUARESIZE))

                    if game.is_valid_location(board, col):
                        row = game.get_next_open_row(board, col)
                        game.drop_piece(board, row, col, game.PLAYER_PIECE)

                        if game.winning_move(board, game.PLAYER_PIECE):
                            label = myfont.render("Player Human wins!", 1, game.COLOR_RED)
                            print(game.WINNING_POSITION)
                            game.screen.blit(label, (40, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        # game.print_board(board)
                        game.draw_board(board)

        if turn == game.AI and not game_over:

            col, minimax_score = game.AlphaBeta(board, 5, -math.inf, math.inf, True)

            if game.is_valid_location(board, col):
                row = game.get_next_open_row(board, col)
                game.drop_piece(board, row, col, game.AI_PIECE)

                if game.winning_move(board, game.AI_PIECE):
                    label = myfont.render("Player AI wins!", 1, game.COLOR_YELLOW)
                    print(game.WINNING_POSITION)
                    game.screen.blit(label, (40, 10))
                    game_over = True

                # game.print_board(board)
                game.draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)
            return game.WINNING_POSITION


# endregion



######################## MAIN ###########################33
if __name__ == '__main__':
    Gaming_Main()
   
