import pykraken as kn

kn.input.bind("left", actions=[
    kn.InputAction(kn.S_a)
])

kn.input.bind("right", actions=[
    kn.InputAction(kn.S_d)

])

kn.input.bind("up", actions=[
    kn.InputAction(kn.S_w)
])

kn.input.bind("down", actions=[
    kn.InputAction(kn.S_s)
])

kn.input.bind("Interact", actions=[
    kn.InputAction(kn.S_e)
])

class Player:
    def __init__(self):
        
        self.speed = 50

        self.collider = kn.Rect(0, 0, 20, 20)
        pa = kn.PixelArray("assets/player.png")
        self.texture = kn.Texture(pa)

    def move(self):

        dt = kn.time.get_delta()

        input_direction = kn.input.get_direction("up", "right", "down", "left")
        self.xf.pos += self.speed * dt * input_direction
        

    def draw(self):
        kn.renderer.draw(
            self.texture,
            self.xf,
            kn.Anchor.CENTER
    )