import random

import pygame as pg
import math
import settings


class Tower(pg.sprite.Sprite):
    def __init__(self, tower_type, sprite_sheets, tile_x, tile_y, angle, strategy_params=None):
        pg.sprite.Sprite.__init__(self)
        self.tower_type = tower_type
        self.upgrade_level = 1
        self.range = settings.TOWER_TYPES[tower_type].get("range")
        self.cooldown = settings.TOWER_TYPES[tower_type].get("cooldown")
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None

        # position variables
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.angle = angle
        # calculate center coordinates
        self.x = (self.tile_x + 0.5) * settings.TILE_SIZE
        self.y = (self.tile_y + 0.5) * settings.TILE_SIZE
        # shot sound effect
        self.shot_fx = pg.mixer.Sound('assets/audio/shot.wav')
        self.shot_fx.set_volume(0.5)

        # animation variables
        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        # update image
        self.angle = angle
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # create transparent circle showing range
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

        # Genetic Algorithm
        self.strategy_params = strategy_params or {"target_selection_range": 1.0, "accuracy": 0.5}

    def load_images(self, sprite_sheet):
        # extract images from spritesheet
        size = sprite_sheet.get_height()
        animation_list = []
        for x in range(settings.ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self, enemy_group, world):
        # if target picked, play firing animation
        if self.target:
            self.play_animation()
        else:
            # search for new target once turret has cooled down
            if pg.time.get_ticks() - self.last_shot > (self.cooldown / world.game_speed):
                self.pick_target(enemy_group, world)

    def pick_target(self, enemy_group, world):
        # check distance to each enemy to see if it is in range
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)

                # Use the target_selection_range from GA
                if dist < self.range * self.strategy_params["target_selection_range"]:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))

                    # Check for accuracy before hitting the enemy
                    if self.is_hit_successful():
                        self.attack_enemy()
                    break

    def attack_enemy(self):
        # damage enemy
        self.target.health -= settings.TOWER_TYPES.get(self.tower_type).get("damage")
        # play sound effect
        self.shot_fx.play()

    def is_hit_successful(self):
        # Determine if the shot hits based on the accuracy parameter
        accuracy = self.strategy_params["accuracy"]
        hit_chance = random.random()
        return hit_chance <= accuracy

    def update_strategy(self, strategy_params):
        # Update tower's strategy based on GA results
        self.strategy_params = strategy_params

    def play_animation(self):
        # update image
        self.original_image = self.animation_list[self.frame_index]
        # check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > settings.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            # check if the animation has finished and reset to idle
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                # record completed time and clear target so cooldown can begin
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def upgrade(self):
        self.upgrade_level += 1
        self.range = settings.TOWER_TYPES[f'cannon{self.upgrade_level}'].get("range")
        self.cooldown = settings.TOWER_TYPES[f'cannon{self.upgrade_level}'].get("cooldown")
        # upgrade turret image
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_list[self.frame_index]

        # upgrade range circle
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
