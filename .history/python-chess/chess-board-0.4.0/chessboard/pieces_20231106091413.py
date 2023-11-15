import os
import pygame
import utils

from chessboard.constants import IMAGE_DIR

class PieceColor:
    BLACK = 'BLACK'
    WHITE = 'WHITE'


class PieceType:
    BISHOP = 'BISHOP'
    KING = 'KING'
    KNIGHT = 'KNIGHT'
    PAWN = 'PAWN'
    QUEEN = 'QUEEN'
    ROOK = 'ROOK'


class Piece:
    b_bishop = pygame.image.load(os.path.join(IMAGE_DIR, 'bB.png'))
    b_king = pygame.image.load(os.path.join(IMAGE_DIR, 'bK.png'))
    b_knight = pygame.image.load(os.path.join(IMAGE_DIR, 'bN.png'))
    b_pawn = pygame.image.load(os.path.join(IMAGE_DIR, 'bP.png'))
    b_queen = pygame.image.load(os.path.join(IMAGE_DIR, 'bQ.png'))
    b_rook = pygame.image.load(os.path.join(IMAGE_DIR, 'bR.png'))

    w_bishop = pygame.image.load(os.path.join(IMAGE_DIR, 'wB.png'))
    w_king = pygame.image.load(os.path.join(IMAGE_DIR, 'wK.png'))
    w_knight = pygame.image.load(os.path.join(IMAGE_DIR, 'wN.png'))
    w_pawn = pygame.image.load(os.path.join(IMAGE_DIR, 'wP.png'))
    w_queen = pygame.image.load(os.path.join(IMAGE_DIR, 'wQ.png'))
    w_rook = pygame.image.load(os.path.join(IMAGE_DIR, 'wR.png'))

    def __init__(self, color, piece, display_surf):
        self.position = None
        self.sprite = None
        self.rect = None
        self.display_surf = display_surf

        self.color = color
        self.piece = piece

        self.set_sprite()

    def set_position(self, position):
        self.position = position

    def set_sprite(self):
        if self.color == PieceColor.WHITE:
            match self.piece:
                case PieceType.BISHOP: self.sprite, self.rect = utils.load_image("wB.png", -1)
                case PieceType.KING: self.sprite, self.rect = utils.load_image("wK.png", -1)
                case PieceType.KNIGHT: self.sprite, self.rect = utils.load_image("wN.png", -1)
                case PieceType.PAWN: self.sprite, self.rect = utils.load_image("wP.png", -1)
                case PieceType.QUEEN: self.sprite, self.rect = utils.load_image("wQ.png", -1)
                case PieceType.ROOK: self.sprite, self.rect = utils.load_image("wR.png", -1)
        elif self.color == PieceColor.BLACK:
            match self.piece:
                case PieceType.BISHOP: self.sprite, self.rect = utils.load_image("bB.png", -1)
                case PieceType.KING: self.sprite, self.rect = utils.load_image("bK.png", -1)
                case PieceType.KNIGHT: self.sprite, self.rect = utils.load_image("bN.png", -1)
                case PieceType.PAWN: self.sprite, self.rect = utils.load_image("bP.png", -1)
                case PieceType.QUEEN: self.sprite, self.rect = utils.load_image("bQ.png", -1)
                case PieceType.ROOK: self.sprite, self.rect = utils.load_image("bR.png", -1)
        
    def display_piece(self):
        self.display_surf.blit(self.sprite, self.position)
