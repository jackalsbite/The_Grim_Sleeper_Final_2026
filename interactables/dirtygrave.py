import pykraken as kn


class DirtyGrave:
    def __init__(self, coordinate, interactables):
        self.texture = kn.Texture("Dirtygrave.png")
        self.coordinate = coordinate
        self.interactables = interactables
        self.active = True

    def interact(self):
        if self.active:
            self.active = False

            # Tell the Interactables class this task is finished.
            self.interactables.complete_task_by_coordinate(
                "grave_cleaning",
                self.coordinate
            )

    def draw(self):
        if self.active:
            # Replace this with the actual pykraken draw function if different.
            kn.draw(self.texture, self.coordinate)