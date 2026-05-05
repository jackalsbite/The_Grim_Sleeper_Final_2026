import pykraken as kn
from player import Player
from states.fsm import FSM, StateType
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

        self.day_length = 300.0
        self.time_left = self.day_length

        self.player = Player()
        self.interactables = Interactables()

        self.possible_grave_cleaning_coordinates = [
            kn.Vec2(80, 80),
            kn.Vec2(120, 80),
            kn.Vec2(160, 80),
            kn.Vec2(200, 80),
            kn.Vec2(80, 120),
            kn.Vec2(120, 120),
            kn.Vec2(160, 120),
            kn.Vec2(200, 120),
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

        self.time_left -= dt

        if self.time_left <= 0:
            self.go_to_nightstate()
            return

        self.player.move()
        self.interactables.update()
        self.snap_camera_to_player()

        self.draw_world()
        self.draw_ui()

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
            # Draw lower/floor layers first.
            if len(tile_layers) > 0:
                tile_layers[0].draw()

            if len(tile_layers) > 1:
                tile_layers[1].draw()

            # Draw world objects after lower layers.
            self.interactables.draw()
            self.player.draw()

            # Draw upper layers above the player.
            for i in range(2, len(tile_layers)):
                tile_layers[i].draw()

        self.camera.unset()

    def draw_ui(self):
        seconds = max(0, int(self.time_left))
        self.timer_text.text = f"Time Left: {seconds}"
        self.timer_text.draw(kn.Vec2(20, 20), kn.Anchor.TOP_LEFT)

    def go_to_nightstate(self):
        self.camera.unset()
        FSM.exit_state()
        FSM.enter_state("nightstate")