import pykraken as kn
from collections import deque


class Deadperson:
    def __init__(self, spawn_coordinate, tile_size, path_tiles, exit_coordinates):
        self.spawn_coordinate = spawn_coordinate
        self.tile_size = tile_size
        self.path_tiles = path_tiles
        self.exit_coordinates = exit_coordinates

        self.speed = 25

        self.position = self.tile_to_world_center(spawn_coordinate)
        self.transform = kn.Transform(
            self.position,
            0.0,
            kn.Vec2(1.0, 1.0)
        )

        self.frame_width = 32
        self.frame_height = 32
        self.frame_count = 2

        self.frame_index = 0
        self.frame_timer = 0.0
        self.frame_time = 0.25

        self.facing = "down"

        self.animation_rows = {
            "down": 0,
            "right": 2,
            "left": 1,
            "up": 3
        }

        # Skeleton has a real collider box.
        # It only uses this against the player, not the map or other skeletons.
        self.collider_width = 16
        self.collider_height = 16
        self.collider = kn.Rect(0, 0, self.collider_width, self.collider_height)

        self.texture = kn.Texture(
            "assets/deadguy.png",
            filter=kn.FilterMode.NEAREST
        )

        self.update_sprite_clip()

        self.active = True
        self.escaped = False
        self.returned = False
        self.returning_to_grave = False

        self.chosen_exit_name = None
        self.chosen_exit_coordinate = None

        self.path = []
        self.path_index = 0

        self.final_target_coordinate = None

        self.locate_exit()
        self.locate_path_to_exit()
        self.update_collider()

    def tile_to_tuple(self, tile_coordinate):
        return (
            int(tile_coordinate.x),
            int(tile_coordinate.y)
        )

    def tuple_to_tile(self, tile_tuple):
        return kn.Vec2(
            tile_tuple[0],
            tile_tuple[1]
        )

    def tile_to_world_center(self, tile_coordinate):
        return kn.Vec2(
            tile_coordinate.x * self.tile_size.x + self.tile_size.x / 2,
            tile_coordinate.y * self.tile_size.y + self.tile_size.y / 2
        )

    def world_to_tile(self, world_position):
        return kn.Vec2(
            int(world_position.x / self.tile_size.x),
            int(world_position.y / self.tile_size.y)
        )

    def distance_between_tiles(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def locate_exit(self):
        exit_distances = []

        for exit_name in self.exit_coordinates:
            exit_coordinate = self.exit_coordinates[exit_name]
            distance = self.distance_between_tiles(
                self.spawn_coordinate,
                exit_coordinate
            )

            exit_distances.append({
                "name": exit_name,
                "coordinate": exit_coordinate,
                "distance": distance
            })

        exit_distances.sort(key=lambda exit_info: exit_info["distance"])

        if len(exit_distances) >= 2:
            chosen_exit = exit_distances[1]
        elif len(exit_distances) == 1:
            chosen_exit = exit_distances[0]
        else:
            self.chosen_exit_name = None
            self.chosen_exit_coordinate = None
            return

        self.chosen_exit_name = chosen_exit["name"]
        self.chosen_exit_coordinate = chosen_exit["coordinate"]

    def find_nearest_path_tile(self, tile_coordinate):
        closest_tile = None
        closest_distance = None

        for path_tile in self.path_tiles:
            distance = abs(path_tile[0] - tile_coordinate.x) + abs(path_tile[1] - tile_coordinate.y)

            if closest_distance is None or distance < closest_distance:
                closest_distance = distance
                closest_tile = path_tile

        return closest_tile

    def locate_path_to_exit(self):
        start_tile = self.find_nearest_path_tile(self.spawn_coordinate)
        exit_tile = self.find_nearest_path_tile(self.chosen_exit_coordinate)

        if start_tile is None or exit_tile is None:
            self.path = []
            return

        self.path = self.find_path(start_tile, exit_tile)
        self.path_index = 0
        self.final_target_coordinate = self.chosen_exit_coordinate

    def locate_path_to_grave(self):
        current_tile = self.world_to_tile(self.position)

        start_tile = self.find_nearest_path_tile(current_tile)
        grave_path_tile = self.find_nearest_path_tile(self.spawn_coordinate)

        if start_tile is None or grave_path_tile is None:
            self.path = []
            self.path_index = 0
            self.final_target_coordinate = self.spawn_coordinate
            return

        self.path = self.find_path(start_tile, grave_path_tile)
        self.path_index = 0
        self.final_target_coordinate = self.spawn_coordinate

    def find_path(self, start_tile, exit_tile):
        frontier = deque()
        frontier.append(start_tile)

        came_from = {}
        came_from[start_tile] = None

        while len(frontier) > 0:
            current = frontier.popleft()

            if current == exit_tile:
                break

            neighbors = [
                (current[0], current[1] - 1),
                (current[0] + 1, current[1]),
                (current[0], current[1] + 1),
                (current[0] - 1, current[1])
            ]

            for neighbor in neighbors:
                if neighbor not in self.path_tiles:
                    continue

                if neighbor in came_from:
                    continue

                frontier.append(neighbor)
                came_from[neighbor] = current

        if exit_tile not in came_from:
            return []

        path = []
        current = exit_tile

        while current is not None:
            path.append(current)
            current = came_from[current]

        path.reverse()
        return path

    def get_interaction_rect(self):
        return kn.Rect(
            self.position.x - 12,
            self.position.y - 12,
            24,
            24
        )

    def get_collider_at(self, position):
        return kn.Rect(
            position.x - 8,
            position.y,
            self.collider_width,
            self.collider_height
        )

    def update_collider(self):
        self.collider.x = self.position.x - 8
        self.collider.y = self.position.y
        self.collider.w = self.collider_width
        self.collider.h = self.collider_height

    def rects_overlap(self, a, b):
        return (
            a.x < b.x + b.w
            and a.x + a.w > b.x
            and a.y < b.y + b.h
            and a.y + a.h > b.y
        )

    def collides_with_player_at(self, position, player_collider):
        if player_collider is None:
            return False

        test_collider = self.get_collider_at(position)

        return self.rects_overlap(test_collider, player_collider)

    def interact(self):
        if self.active == False:
            return

        if self.escaped:
            return

        if self.returning_to_grave:
            return

        self.returning_to_grave = True
        self.locate_path_to_grave()

    def update_sprite_clip(self):
        row = self.animation_rows[self.facing]

        self.texture.clip_area = kn.Rect(
            self.frame_index * self.frame_width,
            row * self.frame_height,
            self.frame_width,
            self.frame_height
        )

    def update_facing(self, direction):
        if abs(direction.x) > abs(direction.y):
            if direction.x > 0:
                self.facing = "right"
            elif direction.x < 0:
                self.facing = "left"
        else:
            if direction.y > 0:
                self.facing = "down"
            elif direction.y < 0:
                self.facing = "up"

    def update_animation(self, dt):
        self.frame_timer += dt

        if self.frame_timer >= self.frame_time:
            self.frame_timer = 0.0
            self.frame_index += 1

            if self.frame_index >= self.frame_count:
                self.frame_index = 0

            self.update_sprite_clip()

    def update(self, player_collider=None):
        if self.active == False:
            return

        if self.escaped:
            return

        if self.path_index >= len(self.path):
            self.move_to_final_target(player_collider)
        else:
            self.move_along_path(player_collider)

        self.transform.pos = kn.Vec2(
            round(self.position.x),
            round(self.position.y)
        )

        self.update_collider()

    def move_along_path(self, player_collider=None):
        target_tile = self.tuple_to_tile(self.path[self.path_index])
        target_position = self.tile_to_world_center(target_tile)

        reached_target = self.move_toward_position(target_position, player_collider)

        if reached_target:
            self.path_index += 1

    def move_to_final_target(self, player_collider=None):
        if self.final_target_coordinate is None:
            return

        target_position = self.tile_to_world_center(self.final_target_coordinate)

        reached_target = self.move_toward_position(target_position, player_collider)

        if reached_target:
            if self.returning_to_grave:
                self.returned = True
                self.active = False
            else:
                self.escaped = True
                self.active = False

    def move_toward_position(self, target_position, player_collider=None):
        dt = kn.time.get_delta()

        direction = kn.Vec2(
            target_position.x - self.position.x,
            target_position.y - self.position.y
        )

        distance = (direction.x * direction.x + direction.y * direction.y) ** 0.5

        if distance <= 1:
            if self.collides_with_player_at(target_position, player_collider) == False:
                self.position = target_position
                return True

            return False

        self.update_facing(direction)

        movement_amount = self.speed * dt

        if movement_amount >= distance:
            new_position = target_position
        else:
            new_position = kn.Vec2(
                self.position.x + direction.x / distance * movement_amount,
                self.position.y + direction.y / distance * movement_amount
            )

        # This is the skeleton's ONLY collision concern.
        # No tile collision. No other skeleton collision.
        if self.collides_with_player_at(new_position, player_collider):
            return False

        self.position = new_position
        self.update_animation(dt)

        return False

    def draw(self):
        if self.active == False:
            return

        kn.renderer.draw(
            self.texture,
            self.transform,
            kn.Anchor.CENTER
        )