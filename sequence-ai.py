# pylint: disable=no-member
# imports
import pygame
import pygame.transform as transform
import pygame.image as image
import neat
import time
import os
import random

# local import
from board import Board

# inits
pygame.font.init()
WIN_WIDTH = 1000
WIN_HEIGHT = 900


def drawWindow(win, board):
    # board
    board.drawBoard(win)
    board.drawHands(win)

    # update
    pygame.display.update()


def main():
    # inits
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    board = Board()

    board.genDeck()
    board.dealCards()
    # P2 Random Turn Call
    board.isP2Random = True

    # clock
    clock = pygame.time.Clock()

    # game loop
    run = True
    while run:
        # FPS
        clock.tick(30)

        # quit logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and not board.win_state:
                board.handleCardSelect(event.key)

        # P2 Random Turn Call
        board.p2Random()

        drawWindow(win, board)


main()

# def run(config_path):
#     config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                                 neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

#     p = neat.Population(config)

#     p.add_reporter(neat.StdOutReporter(True))
#     p.add_reporter(neat.StatisticsReporter())

#     winner = p.run(main, 50)


# if __name__ == "__main__":
#     local_dir = os.path.dirname(__file__)
#     config_path = os.path.join(local_dir, "neat-config.txt")
#     run(config_path)
