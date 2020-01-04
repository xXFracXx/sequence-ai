# pylint: disable=no-member
# imports
import pygame
import pygame.transform as transform
import pygame.image as image
import pygame.draw as draw
import neat
import time
import os
import random

# local imports
from card import Card

# inits
BOARD_SIZE_X = 10
BOARD_SIZE_Y = 10
CARD_WIDTH = round(140 / 2.5)
CARD_HEIGHT = round(190 / 2.5)
CARD_SPACE = round(15 / 2.5)
HAND_SPACE = 650
CARDS_TO_DEAL = 5
INIT_CHIP_MATRIX = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
INIT_CARD_MATRIX = [["MC", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "MC"], ["C6", "C5", "C4", "C3", "C2", "HA", "HK", "HQ", "H1", "S1"], ["C7", "SA", "D2", "D3", "D4", "D5", "D6", "D7", "H9", "SQ"], ["C8", "SK", "C6", "C5", "C4", "C3", "C2", "D8", "H8", "SK"], ["C9", "SQ", "C7", "H6", "H5", "H4", "HA", "D9", "H7", "SA"], [
    "C1", "S1", "C8", "H7", "H2", "H3", "HK", "D1", "H6", "D2"], ["CQ", "S9", "C9", "H8", "H9", "H1", "HQ", "DQ", "H5", "D3"], ["CK", "S8", "C1", "CQ", "CK", "CA", "DA", "DK", "H4", "D4"], ["CA", "S7", "S6", "S5", "S4", "S3", "S2", "H2", "H3", "D5"], ["MC", "DA", "DK", "DQ", "D1", "D9", "D8", "D7", "D6", "MC"]]


class Board:
    # card_codes = ["MC", "SA", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S1", "SJ", "SQ", "SK", "CA", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C1",
    #               "CJ", "CQ", "CK", "HA", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H1", "HJ", "HQ", "HK", "DA", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D1", "DJ", "DQ", "DK"]
    card_codes = ["MC", "SA", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S1", "SQ", "SK", "CA", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C1",
                  "CQ", "CK", "HA", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H1", "HQ", "HK", "DA", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D1", "DQ", "DK"]

    addi_cards = ["SJ", "CJ", "HJ", "DJ"]

    def __init__(self):
        self.p1_cards = []
        self.p2_cards = []
        self.current_turn = 1
        self.turn_state = 1
        self.card_selected = ""

        # board cards
        col = []
        for i in range(BOARD_SIZE_X):
            row = []
            for j in range(BOARD_SIZE_Y):
                row.append(
                    Card(INIT_CHIP_MATRIX[i][j], INIT_CARD_MATRIX[i][j]))
            col.append(row)
        self.card_matrix = col

        # load chips
        self.rc = transform.scale(image.load(
            os.path.join("imgs", "red", "chip.png")), (CARD_WIDTH, CARD_HEIGHT))
        self.bc = transform.scale(image.load(
            os.path.join("imgs", "blue", "chip.png")), (CARD_WIDTH, CARD_HEIGHT))
        self.gc = transform.scale(image.load(
            os.path.join("imgs", "green", "chip.png")), (CARD_WIDTH, CARD_HEIGHT))

        # load option cards
        self.o1 = transform.scale(image.load(
            os.path.join("imgs", "cards", "option1.png")), (CARD_WIDTH, CARD_HEIGHT))
        self.o2 = transform.scale(image.load(
            os.path.join("imgs", "cards", "option2.png")), (CARD_WIDTH, CARD_HEIGHT))

        # load cards
        self.cb = transform.scale(image.load(
            os.path.join("imgs", "cards", "cardBack.png")), (CARD_WIDTH, CARD_HEIGHT))
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

    def genDeck(self):
        temp_deck = self.card_codes
        temp_deck.remove("MC")
        # temp_deck += self.addi_cards
        random.shuffle(temp_deck)
        self.card_deck = temp_deck

        # os.write(1, str(self.card_deck).encode())

    def dealCards(self):
        for x in range(CARDS_TO_DEAL):
            self.p1_cards.append(self.card_deck.pop(0))
            self.p2_cards.append(self.card_deck.pop(0))

        # os.write(1, str(self.p1_cards).encode())
        # os.write(1, str(self.p2_cards).encode())

    def drawBoard(self, win):
        # draw cards
        for card_y, card_r in enumerate(self.card_matrix):
            for card_x, card_c in enumerate(card_r):
                win_x = CARD_SPACE + (card_x * (CARD_WIDTH + CARD_SPACE))
                win_y = CARD_SPACE + (card_y * (CARD_HEIGHT + CARD_SPACE))
                win.blit(getattr(self, card_c.cType.lower()), (win_x, win_y))

        # draw chip
        for chip_y, chip_r in enumerate(self.card_matrix):
            for chip_x, chip_c in enumerate(chip_r):
                if not chip_c.chip == 0:
                    win_x = CARD_SPACE + (chip_x * (CARD_WIDTH + CARD_SPACE))
                    win_y = CARD_SPACE + (chip_y * (CARD_HEIGHT + CARD_SPACE))
                    if chip_c.chip == 1:
                        chip_img = self.rc
                    elif chip_c.chip == 2:
                        chip_img = self.bc
                    elif chip_c.chip == 3:
                        chip_img = self.gc
                    win.blit(chip_img, (win_x, win_y))

        # draw double card selection
        if self.turn_state == 2:
            draw_count = 0
            for card_y, card_r in enumerate(self.card_matrix):
                for card_x, card_c in enumerate(card_r):
                    if card_c.cType == self.card_selected:
                        win_x = CARD_SPACE + \
                            (card_x * (CARD_WIDTH + CARD_SPACE))
                        win_y = CARD_SPACE + \
                            (card_y * (CARD_HEIGHT + CARD_SPACE))
                        if draw_count == 0:
                            win.blit(self.o1, (win_x, win_y))
                            draw_count = 1
                        elif draw_count == 1:
                            win.blit(self.o2, (win_x, win_y))

    def drawHands(self, win):
        if self.current_turn == 1:
            for x, card in enumerate(self.p1_cards):
                win_x = HAND_SPACE + (x * (CARD_WIDTH + CARD_SPACE))
                win_y = CARD_SPACE
                win.blit(getattr(self, card.lower()), (win_x, win_y))
        else:
            for x in range(5):
                win_x = HAND_SPACE + (x * (CARD_WIDTH + CARD_SPACE))
                win_y = CARD_SPACE
                win.blit(self.cb, (win_x, win_y))

        if self.current_turn == 2:
            for x, card in enumerate(self.p2_cards):
                win_x = HAND_SPACE + (x * (CARD_WIDTH + CARD_SPACE))
                win_y = CARD_SPACE + CARD_HEIGHT + CARD_SPACE
                win.blit(getattr(self, card.lower()), (win_x, win_y))
        else:
            for x in range(5):
                win_x = HAND_SPACE + (x * (CARD_WIDTH + CARD_SPACE))
                win_y = CARD_SPACE + CARD_HEIGHT + CARD_SPACE
                win.blit(self.cb, (win_x, win_y))

    def handleCardSelect(self, key):
        # os.write(1, str(key).encode())

        # normal turn
        if self.turn_state == 1:
            card_selected_n = 0
            if key == pygame.K_1:
                card_selected_n = 0
            elif key == pygame.K_2:
                card_selected_n = 1
            elif key == pygame.K_3:
                card_selected_n = 2
            elif key == pygame.K_4:
                card_selected_n = 3
            elif key == pygame.K_5:
                card_selected_n = 4

            # card_selected = self.p1_cards[card_selected_n]
            player_cards = getattr(
                self, "p" + str(self.current_turn) + "_cards")
            card_selected = player_cards[card_selected_n]

            self.card_selected_n = card_selected_n
            self.card_selected = card_selected

            open_count = 0
            for x, row in enumerate(self.card_matrix):
                for y, col in enumerate(row):
                    if col.cType == card_selected and col.chip == 0:
                        open_count += 1

            if open_count == 2:
                self.turn_state = 2
                return

            if open_count == 0:
                self.turn_state = 3
                return

            if open_count == 1:
                self.playCard(1)
                self.nextTurn()
                self.turn_state = 1
                return
            return

        # double card turn
        if self.turn_state == 2:
            opt_selected_n = 1
            if key == pygame.K_1:
                opt_selected_n = 1
            elif key == pygame.K_2:
                opt_selected_n = 2

            self.playCard(opt_selected_n)
            self.nextTurn()
            self.turn_state = 1
            return

        # dead card turn
        if self.turn_state == 3:
            pass

    def nextTurn(self):
        if self.current_turn == 1:
            played_card = self.p1_cards.pop(self.card_selected_n)
            new_card = self.card_deck.pop(
                random.randrange(len(self.card_deck)))
            self.p1_cards.append(new_card)
            self.card_deck.insert(random.randrange(
                len(self.card_deck) + 1), played_card)
            self.current_turn = 2
        elif self.current_turn == 2:
            played_card = self.p2_cards.pop(self.card_selected_n)
            new_card = self.card_deck.pop(
                random.randrange(len(self.card_deck)))
            self.p2_cards.append(new_card)
            self.card_deck.insert(random.randrange(
                len(self.card_deck) + 1), played_card)
            self.current_turn = 1

    def playCard(self, matrix_card_inst):
        opt_count = 1
        for card_y, card_r in enumerate(self.card_matrix):
            for card_x, card_c in enumerate(card_r):
                if card_c.cType == self.card_selected:
                    if opt_count == matrix_card_inst:
                        self.card_matrix[card_y][card_x].chip = self.current_turn
                        opt_count += 1
