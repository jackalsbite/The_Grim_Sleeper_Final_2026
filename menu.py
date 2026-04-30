import pykraken as kn
from states.fsm import FSM, StateType

kn.input.bind("start", actions=[
    kn.InputAction(kn.S_RETURN)
])

class MenuState(StateType):
    def __init__(self) -> None:
        super().__init__()
        self.font = kn.Font("font/leander.ttf", 48)
        self.title = kn.Text(self.font, "The Grim Sleeper")
        self.prompt = kn.Text(self.font, "Press Enter")

        self.background = kn.Texture("assets/Grim_Sleeper_Menu.png")
        self.background_xf = kn.Transform(pos=kn.Vec2(200, 125))

    def handle_event(self, event: kn.Event):
        if event.type == kn.K_RETURN:

            FSM.enter_state("level")

    def update(self):
        kn.renderer.clear()
        self.title.draw(kn.Vec2(600, 360), kn.Anchor.CENTER)
        self.prompt.draw(kn.Vec2(600, 440), kn.Anchor.CENTER)
    

        kn.renderer.draw(
        self.background,
        self.background_xf,
        kn.Anchor.CENTER
        )

        if kn.input.is_just_pressed("start"):
            FSM.enter_state("level")