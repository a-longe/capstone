import pygame

def print_mouse_pos()->None:
    pos = pygame.mouse.get_pos()
    print(f"X:{pos[0]} Y:{pos[1]}")