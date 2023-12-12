import os
import sys
import pygame as pg
import math

Cord = tuple[int, int]
TOP_LEFT = 0
BOTTOM_RIGHT = 800
SQUARE_SIZE = 100
BOARD_SIZE = 800


def is_even(n):
    return 0 == n % 2


def is_odd(n):
    return 1 == n % 2


def black_square(surface, image, rect):
    image.fill((210, 180, 140))
    surface.blit(image, rect)


def white_square(surface, image, rect):
    image.fill((255, 255, 255))
    surface.blit(image, rect)

def get_snap_cords(x, y) -> Cord:
    return (math.floor(x / 100) * 100, math.floor(y / 100) * 100)



square_coords = [[i, j] for i in range(TOP_LEFT, BOTTOM_RIGHT, SQUARE_SIZE) \
                for j in range(TOP_LEFT, BOTTOM_RIGHT, SQUARE_SIZE)]


class Player:
    # A Player object needs to know about the Board because its behaviour
    # depends on the location of other Player objects--only the Board knows
    # about them--that's why Board is an argument. It also needs to know its
    # dimensions, so we pass them in rect
    def __init__(self, Board, rect):
        self.board = Board
        self.rect = pg.Rect(rect)
        self.previous_center = self.rect.center
        # a Player object has a click attribute that is true if the
        # left mouse button is down and on top of the Player
        self.click = False
        self.image = pg.Surface(self.rect.size).convert()
        self.image.fill((255, 0, 0))

    # Check that the player has been selected and that the mouse will
    # not cause the player to bleed out of bounds.

    # To deal with collisions, save current position, and then move
    # the player to the mouse position. If there is a collision, then
    # move the rectangle back to the previous position.

    # Regardless, draw the player
    def update(self):
        if (self.click and self.board.mouse_inside_bounds()):
            self.previous_center = self.rect.center
            self.rect.center = pg.mouse.get_pos()
            # Ask the board if self (the player) will collide
            if self.board.collisions(self):
                self.rect.center = self.previous_center
        self.board.surface.blit(self.image, self.rect)


class Board:
    # Each position corresponds to the arguments needed to instantiate
    # the PyGame.Rect class: (x, y, width, height) corresponding to a player

    # The Board class updates itself by asking the players to paint themselves.

    # It has a number of methods that exist so other parts of the program can
    # inquire about the current state of the board
    def __init__(self, positions):
        self.surface = pg.display.set_mode((BOARD_SIZE, BOARD_SIZE))
        self.players = []
        for pos in positions:
            self.players.append(Player(self, pos))

    def clear_surface(self):
        self.surface.fill(0)

    def get_players(self):
        return self.players

    def mouse_inside_bounds(self):
        # hard-coded numbers should be fixed
        x, y = pg.mouse.get_pos()
        return (x > 51 and x < 949 and y > 51 and y < 549)

    def collisions(self, a_player):
        rects = [player.rect for player in self.get_players()]
        target_rects = [rect for rect in rects if rect != a_player.rect]
        return a_player.rect.collidelistall(target_rects)

    def display_grid(self):
        # print("I should be displaying...")
        for x, y in square_coords:
            row = x / 100
            column = y / 100
            rect = pg.Rect([x, y, 100, 100])
            image = pg.Surface(rect.size).convert()
            if is_odd(row) and is_odd(column):
                black_square(self.surface, image, rect)
            elif is_odd(row) and is_even(column):
                white_square(self.surface, image, rect)
            elif is_even(row) and is_even(column):
                black_square(self.surface, image, rect)
            else:
                white_square(self.surface, image, rect)

    def update_board(self):
        self.clear_surface()
        self.display_grid()
        for player in self.get_players():
            player.update()


def main(Board):
    # listen for events and update board in response to them
    game_event_loop(Board)
    Board.update_board()


# Notice that the event loop has been given its own function. This makes
# the program easier to understand.
def game_event_loop(Board):
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            for player in Board.get_players():
                # The event positions is the mouse coordinates
                if player.rect.collidepoint(event.pos):
                    player.click = True
        elif event.type == pg.MOUSEBUTTONUP:
            for player in Board.get_players():
                if player.click:
                    player_cords = (player.rect.center[0], player.rect.center[1])
                    player.rect.center = (get_snap_cords(*player_cords) + (BOARD_SIZE / 2, BOARD_SIZE / 2)), SQUARE_SIZE, SQUARE_SIZE
                player.click = False
        elif event.type == pg.QUIT:
            pg.quit()
            sys.exit()


if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    MyBoard = Board([(50, 50, 100, 100),
                     (200, 200, 100, 100)])
    MyClock = pg.time.Clock()
    while True:
        main(MyBoard)
        pg.display.update()
        MyClock.tick(60)
