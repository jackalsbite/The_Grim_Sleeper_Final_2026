import pykraken as kn


class DirtyGrave:
    def __init__(self, coordinate, interactables, task=None):
        self.texture = kn.Texture("assets/DirtyGrave.png")
        self.coordinate = coordinate
        self.interactables = interactables
        self.task = task
        self.active = True

    def interact(self):
        if self.active == False:
            return

        self.active = False

        if self.task is not None:
            self.interactables.complete_task(self.task)
        else:
            self.interactables.complete_task_by_coordinate(
                "grave_cleaning",
                self.coordinate
            )

    def get_draw_position(self, tile_size):
        return kn.Vec2(
            self.coordinate.x * tile_size.x,
            self.coordinate.y * tile_size.y
        )
    
    def get_interaction_rect(self, tile_size):
        draw_position = self.get_draw_position(tile_size)

        return kn.Rect(
            draw_position.x,
            draw_position.y,
            tile_size.x,
            tile_size.y
        )

    def draw(self, tile_size):
        if self.active == False:
            return

        transform = kn.Transform()
        transform.pos = self.get_draw_position(tile_size)

        kn.renderer.draw(
            self.texture,
            transform,
            kn.Anchor.TOP_LEFT
        )