import pykraken as kn
from player import Player
from fsm import FSM, StateType

class LevelState(StateType):
    def __init__(self):
        super().__init__()

        self.tilemap = kn.tilemap.Map()
        self.tilemap.load("tilemap/map.tmx")

    def update(self):
        dt = kn.time.get_delta()