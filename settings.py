# Authors: Antonio Raimundo
# Partial credits to: Brandon Fong and Michael Ou

# Import pygame
import pygame as pg

# Game settings
ROWS = 15
COLS = 15
TILE_SIZE = 48
SCREEN_WIDTH = TILE_SIZE * COLS
SCREEN_HEIGHT = TILE_SIZE * ROWS
SIDE_PANEL = 300
FPS = 60
HEALTH = 100
TOTAL_WAVES = 3
UPGRADE_COST = 100
KILL_REWARD = 1
LEVEL_COMPLETE_REWARD = 100
GAME_MODE = "MANUAL"  # MANUAL, GENETIC_ALGORITHM, QLEARNING

# Enemies
SPAWN_COOLDOWN = 400
ENEMY_TYPES = {
    "zombie": {
        "health": 6,
        "speed": 2,
        "image": pg.image.load('assets/images/enemies/zombie.png'),
    },
    "warrior": {
        "health": 10,
        "speed": 4,
        "image": pg.image.load('assets/images/enemies/warrior.png'),
    },
}
ENEMY_SPAWN_DATA = [
    {
        # Wave 1
        "zombie": 5,
        "warrior": 0,
    },
    {
        # Wave 2
        "zombie": 7,
        "warrior": 3,
    },
    {
        # Wave 3
        "zombie": 15,
        "warrior": 5,
    }
]

# Towers
TOWER_LEVELS = 2
TOWER_TYPES = {
    "cannon1": {
        "range": 90,
        "cooldown": 1500,
        "damage": 2,
        "image": pg.image.load('assets/images/towers/cannon1.png'),
    },
    "cannon2": {
        "range": 120,
        "cooldown": 1200,
        "damage": 5,
        "image": pg.image.load('assets/images/towers/cannon2.png'),
    },
}
TOWER_POSITIONS = [
    {
        "type": "cannon1",
        "x": 5,
        "y": 3,
        "angle": 90
    },
    {
        "type": "cannon2",
        "x": 11,
        "y": 2,
        "angle": -90
    },
    {
        "type": "cannon1",
        "x": 3,
        "y": 8,
        "angle": -90
    },
    {
        "type": "cannon2",
        "x": 6,
        "y": 7,
        "angle": 90
    },
    {
        "type": "cannon1",
        "x": 12,
        "y": 11,
        "angle": -90
    },
    {
        "type": "cannon2",
        "x": 6,
        "y": 11,
        "angle": -90
    },
]

# Animation
ANIMATION_STEPS = 8
ANIMATION_DELAY = 15
