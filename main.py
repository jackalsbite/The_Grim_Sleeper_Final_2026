import pykraken as kn
from states.fsm import FSM
from states.daystate import DayState
from states.nightstate import NightState
from states.menu import MenuState

class Root:
    def __init__(self) -> None:
        kn.init(debug=True)
        kn.window.create("The Grim Sleeper", 800, 600)

        FSM.register_state("daystate", lambda: DayState())
        FSM.register_state("nightstate", lambda: NightState())
        FSM.register_state("menu", MenuState)

        FSM.enter_state("menu")

        kn.renderer.set_virtual_resolution(400, 250)

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