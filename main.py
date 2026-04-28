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

    def run(self) -> None:

        while kn.window.is_open():
            state = FSM.get_current_state()

        for e in kn.event.poll():
            state.handle_event(e)
        
        state.update()
        kn.renderer.present()

if __name__ == '__main__':
    kn.init(debug=True)
    Root().run()
    kn.quit