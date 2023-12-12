import os,sys
import pygame as pg 

def inside_bounds(mouse):
    # clean up the hard-coded numbers and move inside Board
    x, y = mouse.get_pos()
    return (x > 51 and x < 949 and y > 51 and y < 549)

class Character:
    def __init__(self, Board, rect):
        self.board = Board
        self.rect = pg.Rect(rect)
        self.previous_center = self.rect.center
        self.click = False
        self.image = pg.Surface(self.rect.size).convert()
        self.image.fill((255,0,0))
    def collisions(self):
        rects = [player.rect for player in self.board.players]
        target_rects = [rect for rect in rects if rect != self.rect]
        return self.rect.collidelistall(target_rects)
    def update(self):
        if (self.click and inside_bounds(pg.mouse) and
            not self.collisions()):
            self.previous_center = self.rect.center
            self.rect.center = pg.mouse.get_pos()
            if self.collisions():
                self.rect.center = self.previous_center
        self.board.surface.blit(self.image,self.rect)

class Board:
    def __init__(self, positions):
        self.surface = pg.display.set_mode((1000, 600))
        self.players = []
        for pos in positions:
            self.players.append(Character(self, pos))
    def clear_surface(self):
        self.surface.fill(0)
    def add_player(self, player):
        self.players.append(player)
    def get_players(self):
        return self.players
    def update_board(self):
        self.clear_surface()
        for player in self.get_players():
            player.update()

def main(Board):
    game_event_loop(Board)
    Board.update_board()

def game_event_loop(Board):
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            for num, player in enumerate(Board.get_players()):
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