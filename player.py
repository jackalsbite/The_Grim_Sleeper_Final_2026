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
        self.speed = 100

        # Moved away from the grave cluster while collision is being tested.
        self.position = kn.Vec2(850, 1100)

        self.frame_width = 32
        self.frame_height = 32
        self.frame_count = 2

        self.frame_index = 0
        self.frame_timer = 0.0
        self.frame_time = 0.18

        self.facing = "down"
        self.is_moving = False

        self.animation_rows = {
            "down": 0,
            "right": 2,
            "left": 1,
            "up": 3
        }

        # Smaller than one tile so it does not snag constantly.
        self.collider_width = 16
        self.collider_height = 16

        self.collider = kn.Rect(0, 0, self.collider_width, self.collider_height)
        self.interact_box = kn.Rect(0, 0, 22, 22)

        self.texture = kn.Texture(
            "assets/player.png",
            filter=kn.FilterMode.NEAREST
        )

        self.transform = kn.Transform(
            self.position,
            0.0,
            kn.Vec2(1.0, 1.0)
        )

        self.update_sprite_clip()
        self.update_boxes()

    def move(self, collision_layer=None, blocking_rects=None):
        dt = kn.time.get_delta()

        if blocking_rects is None:
            blocking_rects = []

        input_direction = kn.input.get_direction("up", "right", "down", "left")

        self.is_moving = input_direction.x != 0 or input_direction.y != 0

        if self.is_moving:
            self.update_facing(input_direction)

            movement = self.speed * dt * input_direction

            # Move X first so the player can slide along walls and skeletons.
            new_position = kn.Vec2(
                self.position.x + movement.x,
                self.position.y
            )

            if self.collides_at(new_position, collision_layer, blocking_rects) == False:
                self.position.x = new_position.x

            # Then move Y.
            new_position = kn.Vec2(
                self.position.x,
                self.position.y + movement.y
            )

            if self.collides_at(new_position, collision_layer, blocking_rects) == False:
                self.position.y = new_position.y

            self.update_animation(dt)
        else:
            self.frame_index = 0
            self.frame_timer = 0.0
            self.update_sprite_clip()

        self.transform.pos = kn.Vec2(
            round(self.position.x),
            round(self.position.y)
        )

        self.update_boxes()

    def get_collider_at(self, position):
        return kn.Rect(
            position.x - 8,
            position.y,
            self.collider_width,
            self.collider_height
        )

    def collides_at(self, position, collision_layer=None, blocking_rects=None):
        if blocking_rects is None:
            blocking_rects = []

        if collision_layer is not None:
            if self.collides_with_layer(position, collision_layer):
                return True

        if self.collides_with_blocking_rects(position, blocking_rects):
            return True

        return False

    def collides_with_layer(self, position, collision_layer):
        test_collider = self.get_collider_at(position)
        touched_tiles = collision_layer.get_from_area(test_collider)

        for result in touched_tiles:
            if result.tile is not None and result.tile.id != 0:
                return True

        return False

    def collides_with_blocking_rects(self, position, blocking_rects):
        test_collider = self.get_collider_at(position)

        for blocking_rect in blocking_rects:
            if self.rects_overlap(test_collider, blocking_rect):
                return True

        return False

    def rects_overlap(self, a, b):
        return (
            a.x < b.x + b.w
            and a.x + a.w > b.x
            and a.y < b.y + b.h
            and a.y + a.h > b.y
        )

    def update_facing(self, direction):
        if abs(direction.x) > abs(direction.y):
            if direction.x > 0:
                self.facing = "right"
            elif direction.x < 0:
                self.facing = "left"
        else:
            if direction.y > 0:
                self.facing = "down"
            elif direction.y < 0:
                self.facing = "up"

    def update_animation(self, dt):
        self.frame_timer += dt

        if self.frame_timer >= self.frame_time:
            self.frame_timer = 0.0
            self.frame_index += 1

            if self.frame_index >= self.frame_count:
                self.frame_index = 0

            self.update_sprite_clip()

    def update_sprite_clip(self):
        row = self.animation_rows[self.facing]

        self.texture.clip_area = kn.Rect(
            self.frame_index * self.frame_width,
            row * self.frame_height,
            self.frame_width,
            self.frame_height
        )

    def update_boxes(self):
        self.collider.x = self.position.x - 8
        self.collider.y = self.position.y
        self.collider.w = self.collider_width
        self.collider.h = self.collider_height

        if self.facing == "up":
            self.interact_box.x = self.position.x - 11
            self.interact_box.y = self.position.y - 32

        elif self.facing == "down":
            self.interact_box.x = self.position.x - 11
            self.interact_box.y = self.position.y + 16

        elif self.facing == "left":
            self.interact_box.x = self.position.x - 32
            self.interact_box.y = self.position.y

        elif self.facing == "right":
            self.interact_box.x = self.position.x + 10
            self.interact_box.y = self.position.y

    def interact(self):
        pass

    def draw(self):
        kn.renderer.draw(
            self.texture,
            self.transform,
            kn.Anchor.CENTER
        )