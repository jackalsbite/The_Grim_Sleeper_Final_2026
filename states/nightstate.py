import pykraken as kn
from player import Player
from states.fsm import FSM, StateType
from deadpeople import Deadperson

class NightState(StateType):
    def __init__(self):
        super().__init__()

        self.tilemap = kn.tilemap.Map()
        self.tilemap.load("tilemap/map.tmx")

        self.camera = kn.Camera(True)
        self.camera_zoom = 2.0

        self.night_length = 180
        self.time_left= self.night_length

        self.player = Player()
        self.deadpeople = Deadperson()



    def startup(self):
        self.time_left = self.night_length

        self.deadpeople.spawn()

        self.snap_camera_to_player()
        
        #   start timer
        #   Interactables, assign tasks, and then spawn tasks

    def update(self):
        dt = kn.time.get_delta()


        # for tasks remaining in current tasks, spawn dead person
        # if dead person reaches exit gate, lose
        # if all dead people are interacted with, win