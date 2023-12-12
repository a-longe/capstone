import os,sys
import pygame as pg 

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

SQUARE_SIZE = 50

BOARD_SIZE = 4

BG_COLOR = (50, 50, 50)

a8, a7, a6, a5, a4, a3, a2, a1 = (100, 100), (100, 150), (100, 200), (100, 250), (100, 300), (100, 350), (100, 400), (100, 450)
b8, b7, b6, b5, b4, b3, b2, b1 = (150, 100), (150, 150), (150, 200), (150, 250), (150, 300), (150, 350), (150, 400), (150, 450)
c8, c7, c6, c5, c4, c3, c2, c1 = (200, 100), (200, 150), (200, 200), (200, 250), (200, 300), (200, 350), (200, 400), (200, 450)
d8, d7, d6, d5, d4, d3, d2, d1 = (250, 100), (250, 150), (250, 200), (250, 250), (250, 300), (250, 350), (250, 400), (250, 450)
e8, e7, e6, e5, e4, e3, e2, e1 = (300, 100), (300, 150), (300, 200), (300, 250), (300, 300), (300, 350), (300, 400), (300, 450)
f8, f7, f6, f5, f4, f3, f2, f1 = (350, 100), (350, 150), (350, 200), (350, 250), (350, 300), (350, 350), (350, 400), (350, 450)
g8, g7, g6, g5, g4, g3, g2, g1 = (400, 100), (400, 150), (400, 200), (400, 250), (400, 300), (400, 350), (400, 400), (400, 450)
h8, h7, h6, h5, h4, h3, h2, h1 = (450, 100), (450, 150), (450, 200), (450, 250), (450, 300), (450, 350), (450, 400), (450, 450)

BOARD_RECT = (
    (a8, b8, c8, d8, e8, f8, g8, h8),
    (a7, b7, c7, d7, e7, f7, g7, h7),
    (a6, b6, c6, d6, e6, f6, g6, h6),
    (a5, b5, c5, d5, e5, f5, g5, h5),
    (a4, b4, c4, d4, e4, f4, g4, h4),
    (a3, b3, c3, d3, e3, f3, g3, h3),
    (a2, b2, c2, d2, e2, f2, g2, h2),
    (a1, b1, c1, d1, e1, f1, g1, h1)
)


IMAGE_DIR = path.join(path.dirname(path.abspath(__file__)), 'images')

w_tile_img = pg.image.load(os.path.join(IMAGE_DIR, 'wtile.png'))
b_tile_img = pg.image.load(os.path.join(IMAGE_DIR, 'btile.png'))

def is_odd(num:int) -> bool:
    return num % 2 != 0

def create_checkerboard() -> pg.Surface:
    checkerboard = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    checkerboard.fill(BG_COLOR)
    for i in range(1, BOARD_SIZE + 1):
        for j in range(1, BOARD_SIZE + 1):
            if is_odd(i):
                if is_odd(j):
                    checkerboard.blit(w_tile_img, BOARD_RECT[i - 1][j - 1])
                else:
                    checkerboard.blit(b_tile_img, BOARD_RECT[i - 1][j - 1])
            elif not is_odd(i):
                if is_odd(j):
                    checkerboard.blit(b_tile_img, BOARD_RECT[i - 1][j - 1])
                else:
                    checkerboard.blit(w_tile_img, BOARD_RECT[i - 1][j - 1]) 
    return checkerboard

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
        self.image.fill((255,0,0))
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
        self.board.surface.blit(self.image,self.rect)
            
class Board:
    # Each position corresponds to the arguments needed to instantiate
    # the PyGame.Rect class: (x, y, width, height) corresponding to a player

    # The Board class updates itself by asking the players to paint themselves.
    
    # It has a number of methods that exist so other parts of the program can
    # inquire about the current state of the board
    def __init__(self, positions):
        self.surface = pg.display.set_mode((1000, 600))
        self.players = []
        for pos in positions:
            self.players.append(Player(self, pos))
    def clear_surface(self):
        self.surface.fill(150)
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
    def update_board(self):
        self.clear_surface()
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
                player.click = False
        elif event.type == pg.QUIT:
            pg.quit(); sys.exit()

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
