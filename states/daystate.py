import pykraken as kn
from player import Player
from states.fsm import FSM, StateType

class DayState(StateType):
    def __init__(self):
        super().__init__()

        self.tilemap = kn.tilemap.Map()
        self.tilemap.load("tilemap/map.tmx")
        self.font = kn.Font("font/leander.ttf", 20)
        self.timer_text = kn.Text(self.font, "")

        self.day_length = 300.0
        self.time_left = self.day_length

        self.player = Player()

    def startup(self):
        pass
        
        #   start timer
        #   Interactables, assign tasks, and then spawn tasks

    def update(self):
        dt = kn.time.get_delta()

        seconds = max(0, int(self.time_left))
        self.timer_text.text = f"Time Left: {seconds}"
        self.timer_text.draw(kn.Vec2(20, 20), kn.Anchor.TOP_RIGHT)

        self.time_left -= dt

        if self.time_left <= 0:
            FSM.exit_state()
            FSM.enter_state("nightstate")

        # if timer expires before all tasks are completed, go to nightstate
        # if all tasks are completed before timer expires, player can interact with shed to skip to nightstate