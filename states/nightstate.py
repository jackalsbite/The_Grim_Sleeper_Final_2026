import pykraken as kn
import game_audio
from player import Player
from states.fsm import FSM, StateType
from deadpeople import Deadperson


class NightState(StateType):
    unfinished_tasks_from_day = []
    player_position_from_day = None

    # Exit tile coordinates.
    # These are tile coordinates, not pixel coordinates.
    EXIT_NORTH = kn.Vec2(65, 20)
    EXIT_EAST = kn.Vec2(84, 44)
    EXIT_SOUTH = kn.Vec2(54, 72)
    EXIT_WEST = kn.Vec2(20, 33)

    EXIT_COORDINATES = {
        "north": EXIT_NORTH,
        "east": EXIT_EAST,
        "south": EXIT_SOUTH,
        "west": EXIT_WEST
    }

    @staticmethod
    def receive_day_results(unfinished_tasks, player_position):
        NightState.unfinished_tasks_from_day = unfinished_tasks
        NightState.player_position_from_day = player_position

    def __init__(self):
        super().__init__()

        self.tilemap = kn.tilemap.Map()
        self.tilemap.load("tilemap/map.tmx")

        self.camera = kn.Camera(True)
        self.camera_zoom = 2.0

        self.font = kn.Font("font/leander.ttf", 20)
        self.night_text = kn.Text(self.font, "")
        self.dead_counter_text = kn.Text(self.font, "")
        self.willow_text = kn.Text(self.font, "")
        self.end_message_text = kn.Text(self.font, "")

        self.player = Player()

        self.unfinished_tasks = []
        self.dead_people = []
        self.path_tiles = set()

        self.show_exit_debug_boxes = False

        # Willow interaction tile coordinate.
        # Tile coordinate, not pixel coordinate.
        self.willow_coordinate = kn.Vec2(54, 41)
        self.willow_mode = False

        self.night_ending = False
        self.end_message = ""
        self.end_timer = 0.0
        self.end_delay = 5

        # Big fake post-processing rectangle.
        # Drawn after the world, before UI, so ONLY the night world gets tinted.
        self.night_overlay_rect = kn.Rect(
            -5000,
            -5000,
            10000,
            10000
        )

        # Tweak this color/alpha if you want it lighter or darker.
        # R, G, B, A
        self.night_overlay_color = kn.Color(8, 18, 50, 135)

    def startup(self):
        game_audio.play_night_background()

        self.unfinished_tasks = []

        for task in NightState.unfinished_tasks_from_day:
            self.unfinished_tasks.append(task)

        self.dead_people = []

        self.willow_mode = len(self.unfinished_tasks) == 0

        self.night_ending = False
        self.end_message = ""
        self.end_timer = 0.0

        if NightState.player_position_from_day is not None:
            self.player.position = kn.Vec2(
                NightState.player_position_from_day.x,
                NightState.player_position_from_day.y
            )

            self.player.transform.pos = kn.Vec2(
                round(self.player.position.x),
                round(self.player.position.y)
            )

            self.player.update_boxes()

        self.build_path_tiles()

        if self.willow_mode == False:
            self.spawn_dead_people_from_unfinished_tasks()

        self.snap_camera_to_player()

    def handle_event(self, event):
        pass

    def update(self):
        if self.night_ending:
            self.update_ending()
            return

        skeleton_colliders = self.get_active_deadperson_colliders()

        # Player cares about the map AND skeleton bodies.
        self.player.move(self.get_collision_layer(), skeleton_colliders)

        if kn.input.is_just_pressed("Interact"):
            if self.willow_mode:
                self.try_willow_interaction()
            else:
                self.interact_with_dead_people()

        # Skeletons only care about the player's body.
        if self.willow_mode == False:
            for dead_person in self.dead_people:
                dead_person.update(self.player.collider, self.player.position)

            self.check_night_end_conditions()

        self.snap_camera_to_player()

        self.draw_world()
        self.draw_night_overlay()
        self.draw_ui()

    def update_ending(self):
        dt = kn.time.get_delta()
        self.end_timer += dt

        self.snap_camera_to_player()

        self.draw_world()
        self.draw_night_overlay()
        self.draw_end_message()

        if self.end_timer >= self.end_delay:
            self.go_to_menu()

    def check_night_end_conditions(self):
        total_dead_people = len(self.dead_people)
        escaped_dead_people = 0
        returned_dead_people = 0

        for dead_person in self.dead_people:
            if dead_person.escaped:
                escaped_dead_people += 1

            if dead_person.returned:
                returned_dead_people += 1

        if escaped_dead_people > 0:
            self.start_ending("You let one escape... D:")
            return

        if total_dead_people > 0 and returned_dead_people >= total_dead_people:
            self.start_ending("You put them all back to sleep :D")
            return

    def start_ending(self, message):
        self.night_ending = True
        self.end_message = message
        self.end_timer = 0.0

    def go_to_menu(self):
        game_audio.stop_background()
        self.camera.unset()
        FSM.exit_state()
        FSM.enter_state("menu")

    def rects_overlap(self, a, b):
        return (
            a.x < b.x + b.w
            and a.x + a.w > b.x
            and a.y < b.y + b.h
            and a.y + a.h > b.y
        )

    def get_active_deadperson_colliders(self):
        colliders = []

        for dead_person in self.dead_people:
            if dead_person.active:
                colliders.append(dead_person.collider)

        return colliders

    def try_willow_interaction(self):
        willow_rect = self.get_tile_rect(self.willow_coordinate)

        if self.rects_overlap(self.player.interact_box, willow_rect):
            game_audio.play_interact()
            self.start_ending("Good job being responsible :D")
            return True

        return False

    def interact_with_dead_people(self):
        for dead_person in self.dead_people:
            if dead_person.active == False:
                continue

            dead_rect = dead_person.get_interaction_rect()

            if self.rects_overlap(self.player.interact_box, dead_rect):
                game_audio.play_interact()
                dead_person.interact()
                return True

        return False

    def get_path_layer(self):
        tile_layers = self.tilemap.tile_layers

        # Tile Layer 2 is index 1.
        if len(tile_layers) > 1:
            return tile_layers[1]

        return None

    def build_path_tiles(self):
        self.path_tiles = set()

        path_layer = self.get_path_layer()

        if path_layer is None:
            return

        tile_size = self.get_tile_size()

        # Current map size is 105 by 93 tiles.
        # If the map changes size later, update these two numbers.
        map_width = 105
        map_height = 93

        for y in range(map_height):
            for x in range(map_width):
                tile_rect = kn.Rect(
                    x * tile_size.x,
                    y * tile_size.y,
                    tile_size.x,
                    tile_size.y
                )

                touched_tiles = path_layer.get_from_area(tile_rect)

                for result in touched_tiles:
                    if result.tile is not None and result.tile.id != 0:
                        self.path_tiles.add((x, y))
                        break

    def spawn_dead_people_from_unfinished_tasks(self):
        tile_size = self.get_tile_size()

        for task in self.unfinished_tasks:
            dead_person = Deadperson(
                task["coordinate"],
                tile_size,
                self.path_tiles,
                NightState.EXIT_COORDINATES
            )

            self.dead_people.append(dead_person)

    def get_collision_layer(self):
        tile_layers = self.tilemap.tile_layers

        if len(tile_layers) > 2:
            return tile_layers[2]

        return None

    def get_tile_size(self):
        tile_size = self.tilemap.tile_size

        return kn.Vec2(
            int(tile_size.x),
            int(tile_size.y)
        )

    def get_tile_rect(self, tile_coordinate):
        tile_size = self.get_tile_size()

        return kn.Rect(
            tile_coordinate.x * tile_size.x,
            tile_coordinate.y * tile_size.y,
            tile_size.x,
            tile_size.y
        )

    def snap_camera_to_player(self):
        self.camera.transform.pos = kn.Vec2(
            round(self.player.position.x),
            round(self.player.position.y)
        )

        self.camera.transform.scale = kn.Vec2(
            self.camera_zoom,
            self.camera_zoom
        )

    def draw_world(self):
        self.camera.set()

        tile_layers = self.tilemap.tile_layers

        if len(tile_layers) == 0:
            self.tilemap.draw()
        else:
            # Draw layers 0, 1, and 2 first.
            # Layer 1 is the path layer.
            # Layer 2 is the collision layer.
            for i in range(len(tile_layers)):
                if i <= 2:
                    tile_layers[i].draw()

            for dead_person in self.dead_people:
                dead_person.draw()

            self.player.draw()

            # Draw upper layers over the player and dead people.
            for i in range(len(tile_layers)):
                if i > 2:
                    tile_layers[i].draw()

            if self.show_exit_debug_boxes:
                self.draw_exit_debug_boxes()

        self.camera.unset()

    def draw_night_overlay(self):
        kn.draw.rect(
            self.night_overlay_rect,
            self.night_overlay_color
        )

    def draw_exit_debug_boxes(self):
        tile_size = self.get_tile_size()

        for exit_name in NightState.EXIT_COORDINATES:
            exit_coordinate = NightState.EXIT_COORDINATES[exit_name]

            exit_rect = kn.Rect(
                exit_coordinate.x * tile_size.x - 16,
                exit_coordinate.y * tile_size.y - 16,
                tile_size.x * 3,
                tile_size.y * 3
            )

            kn.draw.rect(
                exit_rect,
                kn.Color(255, 0, 255, 255)
            )

    def draw_ui(self):
        self.night_text.text = "Night"
        self.night_text.draw(kn.Vec2(20, 20), kn.Anchor.TOP_LEFT)

        if self.willow_mode:
            self.willow_text.text = "Go to the willow tree..."
            self.willow_text.draw(kn.Vec2(20, 50), kn.Anchor.TOP_LEFT)
            return

        total_dead_people = len(self.dead_people)
        returned_dead_people = 0

        for dead_person in self.dead_people:
            if dead_person.returned:
                returned_dead_people += 1

        self.dead_counter_text.text = f"Returned: {returned_dead_people}/{total_dead_people}"
        self.dead_counter_text.draw(kn.Vec2(20, 50), kn.Anchor.TOP_LEFT)

    def draw_end_message(self):
        self.end_message_text.text = self.end_message
        self.end_message_text.draw(kn.Vec2(200, 125), kn.Anchor.CENTER)