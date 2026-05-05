import pykraken as kn


class DirtyGrave:
    def __init__(self, coordinate, interactables, task=None):
        self.texture = kn.Texture("placeholder.png")
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

    def draw(self):
        if self.active == False:
            return

        # Keep all drawing in one tiny spot so it is easy to adjust if your
        # pykraken version uses a different texture draw call.
        if hasattr(kn, "draw"):
            kn.draw(self.texture, self.coordinate)
        elif hasattr(self.texture, "draw"):
            self.texture.draw(self.coordinate)
