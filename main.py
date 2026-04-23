import pykraken as kn
from states.fsm import FSM
from states.level import LevelState
from states.menu import MenuState

class Root:
    def __init__(self) -> None:
        kn.init()
        kn.window.create("The Grim Sleeper", 1200, 900)

        FSM.register_state("level", lambda: LevelState),
        FSM.register_state("menu", lambda: MenuState)

        FSM.enter_state("menu")

while kn.window.is_open():
    kn.event.poll()

    kn.renderer.clear()
    kn.renderer.present()

kn.quit