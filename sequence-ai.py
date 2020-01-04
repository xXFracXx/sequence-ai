# pylint: disable=no-member
# imports
import pygame
import pygame.transform as transform
import pygame.image as image
import neat
import time
import os
import random


# inits
pygame.font.init()

WIN_WIDTH = 1000
WIN_HEIGHT = 900

CARD_WIDTH = round(140 / 2.5)
CARD_HEIGHT = round(190 / 2.5)
CARD_SPACE = round(15 / 2.5)


class Board:
    chip_matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    card_matrix = [["MC", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "MC"], ["C6", "C5", "C4", "C3", "C2", "HA", "HK", "HQ", "H1", "S1"], ["C7", "SA", "D2", "D3", "D4", "D5", "D6", "D7", "H9", "SQ"], ["C8", "SK", "C6", "C5", "C4", "C3", "C2", "D8", "H8", "SK"], ["C9", "SQ", "C7", "H6", "H5", "H4", "HA", "D9", "H7", "SA"], [
        "C1", "S1", "C8", "H7", "H2", "H3", "HK", "D1", "H6", "D2"], ["CQ", "S9", "C9", "H8", "H9", "H1", "HQ", "DQ", "H5", "D3"], ["CK", "S8", "C1", "CQ", "CK", "CA", "DA", "DK", "H4", "D4"], ["CA", "S7", "S6", "S5", "S4", "S3", "S2", "H2", "H3", "D5"], ["MC", "DA", "DK", "DQ", "D1", "D9", "D8", "D7", "D6", "MC"]]

    card_codes = ["MC", "SA", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S1", "SK", "SQ", "CA", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C1",
                  "CK", "CQ", "HA", "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H1", "HK", "HQ", "DA", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D1", "DK", "DQ"]

    def __init__(self):
        # self.mc = transform.scale(image.load(
        #     os.path.join("imgs", "cards", "cardMiscC.png")), (CARD_WIDTH, CARD_HEIGHT))

        for c in self.card_codes:
            # card type logic
            card_type = ""
            if c[0] == "M":
                card_type = "Misc"
            elif c[0] == "S":
                card_type = "Spades"
            elif c[0] == "C":
                card_type = "Clubs"
            elif c[0] == "H":
                card_type = "Hearts"
            elif c[0] == "D":
                card_type = "Diamonds"

            if not c[1] == "1":
                card_name = "card" + card_type + c[1] + ".png"
            else:
                card_name = "card" + card_type + "10.png"

            img = transform.scale(image.load(
                os.path.join("imgs", "cards", card_name)), (CARD_WIDTH, CARD_HEIGHT))

            setattr(self, c.lower(), img)
            # self[c.lower()] = img

    def draw(self, win):
        for y, r in enumerate(self.card_matrix):
            for x, c in enumerate(r):
                win_x = CARD_SPACE + (x * (CARD_WIDTH + CARD_SPACE))
                win_y = CARD_SPACE + (y * (CARD_HEIGHT + CARD_SPACE))
                win.blit(getattr(self, c.lower()), (win_x, win_y))


def draw_window(win, board):
    # backgroud
    # win.fill((255, 255, 255))

    # board
    board.draw(win)

    # update
    pygame.display.update()


def main():
    # inits
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    board = Board()

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

        draw_window(win, board)

        # if score > 50:
        #     break


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
