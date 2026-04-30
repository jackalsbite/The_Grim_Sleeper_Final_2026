import pykraken as kn
from player import Player
from states.fsm import FSM, StateType

class NightState(StateType):
    def __init__(self):
        super().__init__()

        self.tilemap = kn.tilemap.Map()
        self.tilemap.load("tilemap/map.tmx")

        self.player = Player()

    def startup(self):
        pass
        
        #   start timer
        #   Interactables, assign tasks, and then spawn tasks

    def update(self):
        dt = kn.time.get_delta()

        # for tasks remaining in current tasks, spawn dead person
        # if dead person reaches exit gate, lose
        # if all dead people are interacted with, win