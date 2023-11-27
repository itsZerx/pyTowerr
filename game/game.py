import threading

import pygame as pg
import json

from enemies.enemy import Zombie, Warrior
from game.world import World
from game.button import Button
from algorithms.genetic_algorithm import GeneticAlgorithm

import settings


class Game:
    screen = None
    clock = None
    game_over = False
    game_outcome = 0  # -1 the user loses & 1 the user wins
    level_started = False
    last_enemy_spawn = pg.time.get_ticks()
    tower_spritesheets = []
    world = None
    world_data = None
    map_image = None

    def __init__(self, clock, screen):
        # game variables
        self.towers = []  # List of tower objects
        self.restart_button = None
        self.fast_forward_button = None
        self.enemy_group = None
        self.begin_button = None
        self.clock = clock
        self.screen = screen
        # load images
        self.map_image = pg.image.load('levels/level.png').convert_alpha()
        # enemies
        self.enemy_images = {
            "zombie": pg.image.load('assets/images/enemies/zombie.png').convert_alpha(),
            "warrior": pg.image.load('assets/images/enemies/warrior.png').convert_alpha(),
        }
        # buttons
        self.buy_tower_image = pg.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
        self.cancel_image = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()
        self.upgrade_turret_image = pg.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()
        self.begin_image = pg.image.load('assets/images/buttons/begin.png').convert_alpha()
        self.restart_image = pg.image.load('assets/images/buttons/restart.png').convert_alpha()
        self.fast_forward_image = pg.image.load('assets/images/buttons/fast_forward.png').convert_alpha()
        # gui
        self.heart_image = pg.image.load("assets/images/gui/heart.png").convert_alpha()
        self.coin_image = pg.image.load("assets/images/gui/coin.png").convert_alpha()
        self.logo_image = pg.image.load("assets/images/gui/logo.png").convert_alpha()

        # load json data for level
        with open('levels/level.tmj') as file:
            self.world_data = json.load(file)

        # load fonts for displaying text on the screen
        self.text_font = pg.font.SysFont("Consolas", 24, bold=True)
        self.large_font = pg.font.SysFont("Consolas", 36)

        # create world
        self.world = World(self.world_data, self.map_image)
        self.world.process_data()
        self.world.process_enemies()

        # create groups
        self.enemy_group = pg.sprite.Group()

        # create buttons
        self.tower_button = Button(settings.SCREEN_WIDTH + 30, 120, self.buy_tower_image, True)
        self.cancel_button = Button(settings.SCREEN_WIDTH + 50, 180, self.cancel_image, True)
        self.upgrade_button = Button(settings.SCREEN_WIDTH + 5, 180, self.upgrade_turret_image, True)
        self.begin_button = Button(settings.SCREEN_WIDTH + 60, 300, self.begin_image, True)
        self.restart_button = Button(310, 300, self.restart_image, True)
        self.fast_forward_button = Button(settings.SCREEN_WIDTH + 50, 300, self.fast_forward_image, False)

        # GA variables
        self.ga_thread = None
        self.ga_running = False
        self.best_solution = None

    # function for outputting text onto the screen
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def display_data(self):
        # draw panel
        pg.draw.rect(self.screen, "maroon", (settings.SCREEN_WIDTH, 0, settings.SIDE_PANEL, settings.SCREEN_HEIGHT))
        pg.draw.rect(self.screen, "grey0", (settings.SCREEN_WIDTH, 0, settings.SIDE_PANEL, 400), 2)
        self.screen.blit(self.logo_image, (settings.SCREEN_WIDTH, 400))
        # display data
        self.draw_text("LEVEL: " + str(self.world.level), self.text_font, "grey100", settings.SCREEN_WIDTH + 10, 10)
        self.screen.blit(self.heart_image, (settings.SCREEN_WIDTH + 10, 35))
        self.draw_text(str(self.world.health), self.text_font, "grey100", settings.SCREEN_WIDTH + 50, 40)
        self.screen.blit(self.coin_image, (settings.SCREEN_WIDTH + 10, 65))

    def run_ga_in_thread(self):
        if self.ga_thread and self.ga_thread.is_alive():
            return  # GA is already running

        self.ga_running = True
        self.ga_thread = threading.Thread(target=self.run_ga)
        self.ga_thread.start()

    def run_ga(self):
        ga = GeneticAlgorithm()
        ga.run()
        self.best_solution, _ = ga.get_best_solution()
        self.ga_running = False

    def update_tower_strategies(self, solution):
        for tower in self.towers:
            tower.update_strategy(solution)
        self.best_solution = None

    def run(self):
        run = True
        while run:
            self.clock.tick(settings.FPS)
            if not self.game_over:
                # check if player has lost
                if self.world.health <= 0:
                    self.game_over = True
                    self.game_outcome = -1  # loss
                # check if player has won
                if self.world.level > settings.TOTAL_WAVES:
                    self.game_over = True
                    self.game_outcome = 1  # win

                # update groups
                self.enemy_group.update(self.world)
                self.world.tower_group.update(self.enemy_group, self.world)

            # draw level
            self.world.draw(self.screen)

            # draw groups
            self.enemy_group.draw(self.screen)
            for tower in self.world.tower_group:
                tower.draw(self.screen)

            # Update towers with the latest GA solution if available
            if self.best_solution:
                self.update_tower_strategies(self.best_solution)

            # display info
            self.display_data()

            if not self.game_over:
                # check if the level has been started or not
                if not self.level_started:
                    if self.begin_button.draw(self.screen):
                        self.level_started = True
                        # Run GA in a separate thread
                        if not self.ga_running:
                            self.run_ga_in_thread()
                else:
                    # fast-forward option
                    self.world.game_speed = 1
                    if self.fast_forward_button.draw(self.screen):
                        self.world.game_speed = 2
                    # spawn enemies
                    if pg.time.get_ticks() - self.last_enemy_spawn > settings.SPAWN_COOLDOWN:
                        if self.world.spawned_enemies < len(self.world.enemy_list):
                            enemy_type = self.world.enemy_list[self.world.spawned_enemies]
                            if enemy_type == "zombie":
                                enemy = Zombie(self.world.waypoints, self.enemy_images)
                            elif enemy_type == "warrior":
                                enemy = Warrior(self.world.waypoints, self.enemy_images)
                            self.enemy_group.add(enemy)
                            self.world.spawned_enemies += 1
                            self.last_enemy_spawn = pg.time.get_ticks()

                # check if the wave is finished
                if self.world.check_level_complete():
                    self.world.level += 1
                    self.level_started = False
                    self.last_enemy_spawn = pg.time.get_ticks()
                    self.world.reset_level()
                    self.world.process_enemies()

            else:
                pg.draw.rect(self.screen, "dodgerblue", (200, 200, 400, 200), border_radius=30)
                if self.game_outcome == -1:
                    self.draw_text("GAME OVER", self.large_font, "grey0", 310, 230)
                elif self.game_outcome == 1:
                    self.draw_text("YOU WIN!", self.large_font, "grey0", 315, 230)
                # restart level
                if self.restart_button.draw(self.screen):
                    self.game_over = False
                    self.level_started = False
                    self.last_enemy_spawn = pg.time.get_ticks()
                    self.world = World(self.world_data, self.map_image)
                    self.world.process_data()
                    self.world.process_enemies()
                    # empty groups
                    self.enemy_group.empty()
                    self.world.tower_group.empty()

            # event handler
            for event in pg.event.get():
                # quit program
                if event.type == pg.QUIT:
                    run = False
            # update display
            pg.display.flip()

        pg.quit()
