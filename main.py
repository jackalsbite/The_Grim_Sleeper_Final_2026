import pykraken as kn
from states.fsm import FSM
from states.level import LevelState
from states.menu import MenuState

class Root:
    def __init__(self) -> None:
        kn.init(debug=True)
        kn.window.create("The Grim Sleeper", 1200, 900)

        FSM.register_state("level", LevelState)
        FSM.register_state("menu", MenuState)

        FSM.enter_state("menu")

        kn.renderer.set_virtual_resolution(200, 125)

    def run(self) -> None:

        while kn.window.is_open():
            state = FSM.get_current_state()

            for e in kn.event.poll():
                state.handle_event(e)

            state.update()
            kn.renderer.present()

if __name__ == '__main__':
    Root().run()
    kn.quit()