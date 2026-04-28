import pykraken as kn
from states.fsm import FSM
from states.fsm import FSM, StateType

class MenuState(StateType):
    def __init__(self) -> None:
        super().__init__()

    def handle_event(self, event: kn.Event):
        if event.type == kn.KEY_DOWN and kn.K_RETURN:
            FSM.enter_state("level")

    def update(self):
        kn.renderer.clear()