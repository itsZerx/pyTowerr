import random
import settings
import pygame as pg
from towers.tower import Tower


class World:
    def __init__(self, data, map_image):
        self.wave_number = 0
        self.game_speed = 1
        self.towers = []
        self.tower_group = pg.sprite.Group()
        self.tile_map = []
        self.health = 5
        self.waypoints = []
        self.level_data = data
        self.image = map_image
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0
        self.tower_spritesheets = []
        for x in range(1, settings.TOWER_LEVELS + 1):
            tower_sheet = pg.image.load(f'assets/images/towers/cannon{x}.png').convert_alpha()
            self.tower_spritesheets.append(tower_sheet)

    def process_data(self):
        # look through data to extract relevant info
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data)

        # Process initial towers
        for tower_data in settings.TOWER_POSITIONS:
            # Extract tower data
            tower_id = tower_data["id"]
            tower_type = tower_data["type"]
            tile_x = tower_data["x"]
            tile_y = tower_data["y"]
            angle = tower_data["angle"]
            # Create tower instances
            self.create_towers(tower_id, tower_type, tile_x, tile_y, angle)

    def create_towers(self, tower_id, tower_type, tile_x, tile_y, angle):
        new_tower = Tower(tower_id, tower_type, self.tower_spritesheets, tile_x, tile_y, angle)
        self.towers.append(new_tower)
        self.tower_group.add(new_tower)  # Add to a group or list of towers

    def process_waypoints(self, data):
        # iterate through waypoints to extract individual sets of x and y coordinates
        for point in data:
            temp_x = point.get("x")
            temp_y = point.get("y")
            self.waypoints.append((temp_x, temp_y))

    def process_enemies(self):
        enemies = settings.ENEMY_SPAWN_DATA[self.wave_number]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
        # now randomize the list to shuffle the enemies
        random.shuffle(self.enemy_list)

    def check_level_complete(self):
        if (self.killed_enemies + self.missed_enemies) == len(self.enemy_list):
            return True

    def reset_level(self):
        # reset enemy list
        self.enemy_list = []

    def draw(self, surface):
        surface.blit(self.image, (0, 0))
