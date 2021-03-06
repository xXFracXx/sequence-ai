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
pygame.font.init()
BOARD_SIZE_X = 10
BOARD_SIZE_Y = 10
CARD_WIDTH = round(140 / 2.5)
CARD_HEIGHT = round(190 / 2.5)
CARD_SPACE = round(15 / 2.5)
HAND_SPACE = 650
CARDS_TO_DEAL = 5
INIT_CHIP_MATRIX = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
INIT_CARD_MATRIX = [["1MC", "1S2", "1S3", "1S4", "1S5", "1S6", "1S7", "1S8", "1S9", "2MC"], ["1C6", "1C5", "1C4", "1C3", "1C2", "1HA", "1HK", "1HQ", "1H1", "1S1"], ["1C7", "1SA", "1D2", "1D3", "1D4", "1D5", "1D6", "1D7", "1H9", "1SQ"], ["1C8", "1SK", "2C6", "2C5", "2C4", "2C3", "2C2", "1D8", "1H8", "2SK"], ["1C9", "2SQ", "2C7", "1H6", "1H5", "1H4", "2HA", "1D9", "1H7", "2SA"], [
    "1C1", "2S1", "2C8", "2H7", "1H2", "1H3", "2HK", "1D1", "2H6", "2D2"], ["1CQ", "2S9", "2C9", "2H8", "2H9", "2H1", "2HQ", "1DQ", "2H5", "2D3"], ["1CK", "2S8", "2C1", "2CQ", "2CK", "1CA", "1DA", "1DK", "2H4", "2D4"], ["2CA", "2S7", "2S6", "2S5", "2S4", "2S3", "2S2", "2H2", "2H3", "2D5"], ["3MC", "2DA", "2DK", "2DQ", "2D1", "2D9", "2D8", "2D7", "2D6", "4MC"]]
P1_1 = [[1], [1], [1], [1], [1]]
P1_2 = [[1, 1, 1, 1, 1]]
P1_3 = [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [
    0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]]
P1_4 = [[0, 0, 0, 0, 1], [0, 0, 0, 1, 0], [
    0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [1, 0, 0, 0, 0]]
P2_1 = [[2], [2], [2], [2], [2]]
P2_2 = [[2, 2, 2, 2, 2]]
P2_3 = [[2, 0, 0, 0, 0], [0, 2, 0, 0, 0], [
    0, 0, 2, 0, 0], [0, 0, 0, 2, 0], [0, 0, 0, 0, 2]]
P2_4 = [[0, 0, 0, 0, 2], [0, 0, 0, 2, 0], [
    0, 0, 2, 0, 0], [0, 2, 0, 0, 0], [2, 0, 0, 0, 0]]
STAT_FONT = pygame.font.SysFont("consolas", 20)
TEXT_LINE_HEIGHT = STAT_FONT.get_height() + 4
P1_COLOR = (232, 106, 23)
P2_COLOR = (30, 167, 225)


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
        self.p1_win = [P1_1, P1_2, P1_3, P1_4]
        self.p2_win = [P2_1, P2_2, P2_3, P2_4]
        self.winner = 0
        self.win_state = False
        self.isP2Random = False
        self.p1TurnsPlayed = 0
        self.p2TurnsPlayed = 0

        # board cards
        col = []
        for i in range(BOARD_SIZE_X):
            row = []
            for j in range(BOARD_SIZE_Y):
                temp_str = INIT_CARD_MATRIX[i][j]
                row.append(
                    Card(INIT_CHIP_MATRIX[i][j], int(temp_str[0]), temp_str[1:]))
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
        if not self.isP2Random or self.current_turn == 1:
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
                else:
                    return

            if self.turn_state == 2:
                card_selected_n = 1
                if key == pygame.K_1:
                    card_selected_n = 1
                elif key == pygame.K_2:
                    card_selected_n = 2
                else:
                    return

            self.playTurn(card_selected_n)

    def playTurn(self, card_selected_n):
        # os.write(1, str(key).encode())

        # normal turn
        if self.turn_state == 1:
            # card_selected = self.p1_cards[card_selected_n]
            player_cards = getattr(
                self, "p" + str(self.current_turn) + "_cards")
            card_selected = player_cards[card_selected_n]
            self.card_selected = card_selected
            self.card_selected_n = card_selected_n

            open_count = 0
            valid_count = 0
            for x, row in enumerate(self.card_matrix):
                for y, col in enumerate(row):
                    if col.cType == card_selected and col.chip == 0:
                        valid_count = col.count
                        open_count += 1

            if open_count == 2:
                self.turn_state = 2
                return

            if open_count == 0:
                # self.turn_state = 3
                self.nextTurn(True)
                return

            if open_count == 1:
                self.playCard(card_selected, valid_count)
                self.nextTurn(False)
                self.turn_state = 1
                return
            return

        # double card turn
        if self.turn_state == 2:
            self.playCard(self.card_selected, card_selected_n)
            self.nextTurn(False)
            self.turn_state = 1
            return

        # dead card turn
        # if self.turn_state == 3:
        #     pass

    def nextTurn(self, dead):
        if self.current_turn == 1:
            played_card = self.p1_cards.pop(self.card_selected_n)
            new_card = self.card_deck.pop(
                random.randrange(len(self.card_deck)))
            self.p1_cards.append(new_card)
            self.card_deck.insert(random.randrange(
                len(self.card_deck) + 1), played_card)
            self.p1TurnsPlayed += 1
            if not dead:
                self.current_turn = 2
        elif self.current_turn == 2:
            played_card = self.p2_cards.pop(self.card_selected_n)
            new_card = self.card_deck.pop(
                random.randrange(len(self.card_deck)))
            self.p2_cards.append(new_card)
            self.card_deck.insert(random.randrange(
                len(self.card_deck) + 1), played_card)
            self.p2TurnsPlayed += 1
            if not dead:
                self.current_turn = 1
        self.checkWin()

    def playCard(self, card_selected, count):
        for card_y, card_r in enumerate(self.card_matrix):
            for card_x, card_c in enumerate(card_r):
                if card_c.cType == card_selected and card_c.count == count:
                    self.card_matrix[card_y][card_x].chip = self.current_turn

    def checkWinPatternSearch(self, arr, pattern, x, y):
        for i in range(len(pattern)):
            for j in range(len(pattern[0])):
                if arr[x + i][y + j].chip != pattern[i][j]:
                    return False
            if i == len(pattern) - 1:
                return True

    def checkWinPattern(self, arr, pattern):
        check = False
        for x in range(len(arr) - len(pattern) + 1):
            for y in range(len(arr[0]) - len(pattern[0]) + 1):
                if not check:
                    check = self.checkWinPatternSearch(arr, pattern, x, y)
        return check

    def checkWin(self):
        board_arr = self.card_matrix

        # check p1 win
        for p in self.p1_win:
            if self.checkWinPattern(board_arr, p):
                self.winner = 1
                self.win_state = True

        # check p1 win
        for p in self.p2_win:
            if self.checkWinPattern(board_arr, p):
                self.winner = 2
                self.win_state = True

    def p2Random(self):
        if self.isP2Random and self.current_turn == 2:
            if self.turn_state == 1:
                card_selected_n = random.choice([0, 1, 2, 3, 4])

            if self.turn_state == 2:
                card_selected_n = random.choice([1, 2])

            self.playTurn(card_selected_n)

    def drawStats(self, win):
        # Player 1
        p1t_X = HAND_SPACE
        p1t_y = CARD_SPACE + (3 * (CARD_HEIGHT + CARD_SPACE))
        if self.win_state and self.winner == 1:
            wins = " Wins!"
        else:
            wins = ""
        text1_1 = STAT_FONT.render(
            "Player 1" + str(wins), 1, P1_COLOR)
        win.blit(text1_1, (p1t_X, p1t_y))
        text1_2 = STAT_FONT.render(
            "Turns Played: " + str(self.p1TurnsPlayed), 1, P1_COLOR)
        win.blit(text1_2, (p1t_X, p1t_y + (1 * TEXT_LINE_HEIGHT)))

        # Player 2
        p2t_X = HAND_SPACE
        p2t_y = CARD_SPACE + (6 * (CARD_HEIGHT + CARD_SPACE))
        if self.win_state and self.winner == 2:
            wins = " Wins!"
        else:
            wins = ""
        text2_1 = STAT_FONT.render(
            "Player 2" + str(wins), 1, P2_COLOR)
        win.blit(text2_1, (p2t_X, p2t_y))
        text2_2 = STAT_FONT.render(
            "Turns Played: " + str(self.p2TurnsPlayed), 1, P2_COLOR)
        win.blit(text2_2, (p2t_X, p2t_y + (1 * TEXT_LINE_HEIGHT)))

    def drawNNStats(self, win):
        draw.rect(win, (250, 250, 250), (0, CARD_SPACE +
                                         (10 * (CARD_HEIGHT + CARD_SPACE)), 1000, 74))
