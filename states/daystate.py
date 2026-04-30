import pykraken as kn
from player import Player
from states.fsm import FSM, StateType

class DayState(StateType):
    def __init__(self):
        super().__init__()

        self.tilemap = kn.tilemap.Map()
        self.tilemap.load("tilemap/map.tmx")

    def startup(self):
        pass
        
        #   start timer
        #   Interactables, assign tasks, and then spawn tasks

    def update(self):
        dt = kn.time.get_delta()

        # if timer expires before all tasks are completed, go to nightstate
        # if all tasks are completed before timer expires, player can interact with shed to skip to nightstate