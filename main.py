import pygame as pg
from game.game import Game
import settings


def main():
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((settings.SCREEN_WIDTH + settings.SIDE_PANEL, settings.SCREEN_HEIGHT))
    pg.display.set_caption("pyTowerr - A Python Tower Defense 2D game for Genetic Algorithms & Reinforcement Learning")
    game = Game(clock, screen)
    game.run()


if __name__ == "__main__":
    main()
