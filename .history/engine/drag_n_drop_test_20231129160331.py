import os,sys
import pygame as pg 

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
