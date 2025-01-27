import pygame, sys
from pygame.math import Vector2 as vector

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
ANIMATION_SPEED = 6

Z_LAYERS = { # basically allows me to control the way assets are loaded and not via the order they are coded in from
    'bg': 0,
    'clouds': 1,
    'bg tiles': 2,
    'path': 3,
    'bg details': 4,
    'main': 5,
    'water': 6,
    'fg': 7
}