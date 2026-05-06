import random

from interactables.dirtygrave import DirtyGrave


class Interactables:
    def __init__(self):
        self.grave_cleaning_coordinates = []
        self.grave_flower_coordinates = []
        self.chime_coordinates = []

        self.current_tasks = []
        self.active_objects = []

        self.total_tasks = 0
        self.current_tasks_counter = 0

    def assign_tasks(
        self,
        possible_grave_cleaning_coordinates,
        possible_grave_flower_coordinates,
        possible_chime_coordinates
    ):
        self.grave_cleaning_coordinates = []
        self.grave_flower_coordinates = []
        self.chime_coordinates = []

        for coordinate in possible_grave_cleaning_coordinates:
            if random.random() <= 0.15:
                self.grave_cleaning_coordinates.append(coordinate)

            if len(self.grave_cleaning_coordinates) >= 15:
                break

        # Safety fallback: prevents the day from spawning with zero visible
        # grave-cleaning tasks just because random was a little gremlin.
        if len(self.grave_cleaning_coordinates) == 0 and len(possible_grave_cleaning_coordinates) > 0:
            self.grave_cleaning_coordinates.append(possible_grave_cleaning_coordinates[0])

        for coordinate in possible_grave_flower_coordinates:
            if random.random() <= 0.10:
                self.grave_flower_coordinates.append(coordinate)

            if len(self.grave_flower_coordinates) >= 5:
                break

        for coordinate in possible_chime_coordinates:
            if random.random() <= 0.10:
                self.chime_coordinates.append(coordinate)

            if len(self.chime_coordinates) >= 3:
                break

    def spawn_tasks(self):
        self.current_tasks = []
        self.active_objects = []

        for coordinate in self.grave_cleaning_coordinates:
            task = self.create_task("grave_cleaning", coordinate)
            self.current_tasks.append(task)
            self.active_objects.append(DirtyGrave(coordinate, self, task))

        for coordinate in self.grave_flower_coordinates:
            task = self.create_task("grave_flowers", coordinate)
            self.current_tasks.append(task)

            # Add a GraveFlowers class here later, then append it to active_objects.
            # Example:
            # self.active_objects.append(GraveFlowers(coordinate, self, task))

        for coordinate in self.chime_coordinates:
            task = self.create_task("chime", coordinate)
            self.current_tasks.append(task)

            # Add a Chime class here later, then append it to active_objects.
            # Example:
            # self.active_objects.append(Chime(coordinate, self, task))

        self.task_counter()

    def create_task(self, task_type, coordinate):
        return {
            "type": task_type,
            "coordinate": coordinate,
            "finished": False
        }

    def update(self):
        self.remove_inactive_objects()
        self.task_counter()

    def rects_overlap(self, a, b):
        return (
            a.x < b.x + b.w
            and a.x + a.w > b.x
            and a.y < b.y + b.h
            and a.y + a.h > b.y
        )

    def draw(self, tile_size):
        for obj in self.active_objects:
            obj.draw(tile_size)

    def interact_with_box(self, interact_box, tile_size):
        for obj in self.active_objects:
            if obj.active == False:
                continue

            obj_rect = obj.get_interaction_rect(tile_size)

            if self.rects_overlap(interact_box, obj_rect):
                obj.interact()
                return True

        return False

    def task_counter(self):
        self.total_tasks = len(self.current_tasks)

        unfinished_tasks = 0

        for task in self.current_tasks:
            if task["finished"] == False:
                unfinished_tasks += 1

        self.current_tasks_counter = unfinished_tasks

    def complete_task(self, task):
        if task in self.current_tasks and task["finished"] == False:
            task["finished"] = True
            self.task_counter()

    def complete_task_by_coordinate(self, task_type, coordinate):
        for task in self.current_tasks:
            if (
                task["type"] == task_type
                and task["coordinate"] == coordinate
                and task["finished"] == False
            ):
                self.complete_task(task)
                return True

        return False

    def remove_inactive_objects(self):
        active_objects = []

        for obj in self.active_objects:
            if obj.active:
                active_objects.append(obj)

        self.active_objects = active_objects

    def all_tasks_finished(self):
        self.task_counter()
        return self.total_tasks > 0 and self.current_tasks_counter == 0