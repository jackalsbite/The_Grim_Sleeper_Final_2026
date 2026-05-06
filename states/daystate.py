import pykraken as kn
from player import Player
from states.fsm import FSM, StateType
from states.nightstate import NightState
from interactables.interactables import Interactables


class DayState(StateType):
    def __init__(self):
        super().__init__()

        self.tilemap = kn.tilemap.Map()
        self.tilemap.load("tilemap/map.tmx")

        self.camera = kn.Camera(True)
        self.camera_zoom = 2.0

        self.font = kn.Font("font/leander.ttf", 20)
        self.timer_text = kn.Text(self.font, "")
        self.task_counter_text = kn.Text(self.font, "")

        self.day_length = 60
        self.time_left = self.day_length

        self.player = Player()
        self.interactables = Interactables()

        # Shed interaction tile coordinate.
        # Tile coordinate, not pixel coordinate.
        self.shed_coordinate = kn.Vec2(61, 54)

        self.possible_grave_cleaning_coordinates = [
            kn.Vec2(68, 25),
            kn.Vec2(71, 25),
            kn.Vec2(72, 25),

            kn.Vec2(24, 26),
            kn.Vec2(26, 26),
            kn.Vec2(29, 26),
            kn.Vec2(30, 26),
            kn.Vec2(33, 26),
            kn.Vec2(36, 26),
            kn.Vec2(38, 26),
            kn.Vec2(42, 26),
            kn.Vec2(45, 26),
            kn.Vec2(47, 26),
            kn.Vec2(58, 26),
            kn.Vec2(60, 26),
            kn.Vec2(62, 26),

            kn.Vec2(68, 29),
            kn.Vec2(74, 29),

            kn.Vec2(35, 30),
            kn.Vec2(38, 30),
            kn.Vec2(44, 30),
            kn.Vec2(46, 30),
            kn.Vec2(49, 30),
            kn.Vec2(58, 30),
            kn.Vec2(61, 30),

            kn.Vec2(69, 33),
            kn.Vec2(71, 33),
            kn.Vec2(76, 33),

            kn.Vec2(45, 34),
            kn.Vec2(48, 34),
            kn.Vec2(50, 34),
            kn.Vec2(59, 34),
            kn.Vec2(62, 34),

            kn.Vec2(23, 36),
            kn.Vec2(25, 36),
            kn.Vec2(27, 36),
            kn.Vec2(32, 36),
            kn.Vec2(33, 36),
            kn.Vec2(36, 36),
            kn.Vec2(38, 36),

            kn.Vec2(68, 37),
            kn.Vec2(71, 37),
            kn.Vec2(74, 37),

            kn.Vec2(44, 38),
            kn.Vec2(48, 38),
            kn.Vec2(59, 38),
            kn.Vec2(61, 38),

            kn.Vec2(25, 40),
            kn.Vec2(28, 40),
            kn.Vec2(30, 40),
            kn.Vec2(34, 40),
            kn.Vec2(35, 40),
            kn.Vec2(38, 40),

            kn.Vec2(69, 41),
            kn.Vec2(72, 41),
            kn.Vec2(76, 41),
            kn.Vec2(77, 41),
            kn.Vec2(79, 41),

            kn.Vec2(44, 47),
            kn.Vec2(45, 47),
            kn.Vec2(47, 47),
            kn.Vec2(48, 47),
            kn.Vec2(49, 47),

            kn.Vec2(24, 49),
            kn.Vec2(29, 49),
            kn.Vec2(31, 49),
            kn.Vec2(35, 49),

            kn.Vec2(44, 51),
            kn.Vec2(46, 51),
            kn.Vec2(49, 51),

            kn.Vec2(24, 55),
            kn.Vec2(28, 55),
            kn.Vec2(29, 55),

            kn.Vec2(23, 59),

            kn.Vec2(29, 63),

            kn.Vec2(24, 67),
            kn.Vec2(28, 67),
            kn.Vec2(30, 67),
        ]

        self.possible_grave_flower_coordinates = []
        self.possible_chime_coordinates = []

    def startup(self):
        self.time_left = self.day_length

        self.interactables.assign_tasks(
            self.possible_grave_cleaning_coordinates,
            self.possible_grave_flower_coordinates,
            self.possible_chime_coordinates
        )

        self.interactables.spawn_tasks()

        self.snap_camera_to_player()

    def handle_event(self, event):
        pass

    def update(self):
        dt = kn.time.get_delta()

        if self.interactables.all_tasks_finished() == False:
            self.time_left -= dt

            if self.time_left <= 0:
                self.go_to_nightstate()
                return

        self.player.move(self.get_collision_layer())

        if kn.input.is_just_pressed("Interact"):
            if self.try_shed_interaction() == False:
                self.interactables.interact_with_box(
                    self.player.interact_box,
                    self.get_tile_size()
                )

        self.interactables.update()
        self.snap_camera_to_player()

        self.draw_world()
        self.draw_ui()

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

    def rects_overlap(self, a, b):
        return (
            a.x < b.x + b.w
            and a.x + a.w > b.x
            and a.y < b.y + b.h
            and a.y + a.h > b.y
        )

    def try_shed_interaction(self):
        if self.interactables.all_tasks_finished() == False:
            return False

        shed_rect = self.get_tile_rect(self.shed_coordinate)

        if self.rects_overlap(self.player.interact_box, shed_rect):
            self.go_to_nightstate()
            return True

        return False

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
            # Layer 2 is the collision layer, but it is still visible.
            for i in range(len(tile_layers)):
                if i <= 2:
                    tile_layers[i].draw()

            # Draw objects and player above lower layers.
            self.interactables.draw(self.get_tile_size())
            self.player.draw()

            # Draw upper layers over the player.
            for i in range(len(tile_layers)):
                if i > 2:
                    tile_layers[i].draw()

        self.camera.unset()

    def draw_ui(self):
        seconds = max(0, int(self.time_left))
        self.timer_text.text = f"Time Left: {seconds}"
        self.timer_text.draw(kn.Vec2(20, 20), kn.Anchor.TOP_LEFT)

        completed_tasks = self.interactables.total_tasks - self.interactables.current_tasks_counter
        total_tasks = self.interactables.total_tasks

        if self.interactables.all_tasks_finished():
            self.task_counter_text.text = "Go to the shed..."
        else:
            self.task_counter_text.text = f"{completed_tasks}/{total_tasks}"

        self.task_counter_text.draw(kn.Vec2(20, 50), kn.Anchor.TOP_LEFT)

    def go_to_nightstate(self):
        unfinished_tasks = []

        for task in self.interactables.current_tasks:
            if task["finished"] == False:
                unfinished_tasks.append(task)

        NightState.receive_day_results(
            unfinished_tasks,
            self.player.position
        )

        self.camera.unset()
        FSM.exit_state()
        FSM.enter_state("nightstate")