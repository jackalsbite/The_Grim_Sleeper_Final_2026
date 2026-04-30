import pykraken as kn

class Deadperson:
    def __init__(self):

        self.rect = kn.Rect(0, 0, 20, 20)
        self.interact_box = kn.Rect(0, 0, 22, 22)
        
        self.speed = 5

        pa = kn.PixelArray("assets/deadguy.png")
        self.texture = kn.Texture(pa)

    def locate_exit(self):
        pass

    def locate_path(self):
        pass

    def escape(self):
        pass

        #find nearest exit coordinate, find path, and walk

        # while active and not escaped:
        #   self.locate exit
        #   self.locate path
        #   self.move
