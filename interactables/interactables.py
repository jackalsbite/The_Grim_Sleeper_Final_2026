import random
import pykraken as kn


class Interactables:
    def __init__(self):
        self.grave_cleaning_coordinates = []
        self.grave_flower_coordinates = []
        self.chime_coordinates = []

        self.current_tasks = []
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
            if random.random() <= 0.10:
                self.grave_cleaning_coordinates.append(coordinate)

            if len(self.grave_cleaning_coordinates) >= 10:
                break

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

        for coordinate in self.grave_cleaning_coordinates:
            task = {
                "type": "grave_cleaning",
                "coordinate": coordinate,
                "finished": False
            }

            self.current_tasks.append(task)

            # Replace this with your actual pykraken spawn code.
            # Example:
            # kn.spawn("dirty_grave", coordinate)

        for coordinate in self.grave_flower_coordinates:
            task = {
                "type": "grave_flowers",
                "coordinate": coordinate,
                "finished": False
            }

            self.current_tasks.append(task)

            # Replace this with your actual pykraken spawn code.
            # Example:
            # kn.spawn("grave_needs_flowers", coordinate)

        for coordinate in self.chime_coordinates:
            task = {
                "type": "chime",
                "coordinate": coordinate,
                "finished": False
            }

            self.current_tasks.append(task)

            # Replace this with your actual pykraken spawn code.
            # Example:
            # kn.spawn("chime_marker", coordinate)

        self.task_counter()

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