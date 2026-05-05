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
        self.position = kn.Vec2(200, 125)

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

        self.collider = kn.Rect(0, 0, 20, 20)
        self.interact_box = kn.Rect(0, 0, 22, 22)

        self.texture = kn.Texture(
            "assets/player.png",
            filter=kn.FilterMode.NEAREST
            )
        self.transform = kn.Transform(self.position, 0.0, kn.Vec2(1.0, 1.0))

        self.update_sprite_clip()
        self.update_boxes()

    def move(self):
        dt = kn.time.get_delta()

        input_direction = kn.input.get_direction("up", "right", "down", "left")

        self.is_moving = input_direction.x != 0 or input_direction.y != 0

        if self.is_moving:
            self.position += self.speed * dt * input_direction
            self.update_facing(input_direction)
            self.update_animation(dt)
        else:
            self.frame_index = 0
            self.frame_timer = 0.0
            self.update_sprite_clip()

        # Keep the drawn sprite on whole pixels to reduce shimmer.
        self.transform.pos = kn.Vec2(
            round(self.position.x),
            round(self.position.y)
        )

        self.update_boxes()

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
        self.collider.x = self.position.x - 10
        self.collider.y = self.position.y - 10

        self.interact_box.x = self.position.x - 11
        self.interact_box.y = self.position.y - 11

    def interact(self):
        pass

    def _physics_process(self, delta: float) -> None:
        pass
    
    def draw(self):
        kn.renderer.draw(
            self.texture,
            self.transform,
            kn.Anchor.CENTER
        )