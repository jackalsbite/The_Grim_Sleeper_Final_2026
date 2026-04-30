import pykraken as kn


class interactables:
    def __init__(self):
        pass

    #   possible_grave_cleaning_coordinates = list of coordinates
    #   possible_grave_flower_coordinates = list of coordinates
    #   possible_chime_coordinates = list of coordinates

    def assign_tasks(self): # do the lists need to be parameters?
        pass

        #   grave_cleaning_coordinates: empty list
        #   grave_flower_coordinates: empty list
        #   chime_coordinates: empty list

        #   for coordinate in possible_grave_cleaning_coordinates:
        #       10% chance to mark
        #       append marked coordinates to the list
        #       if number of marked = 10
        #           stop marking
        
        #   for coordinate in possible_grave_flower_coordinates:
        #       10% chance to mark
        #       append marked coordinates to the list
        #       if number of marked = 5
        #           stop marking
        

        #   for coordinate in possible_chime_coordinates:
        #       10% chance to mark
        #       append marked coordinates to the list
        #       if number of marked = 3
        #           stop marking
    
    def spawn_tasks(self):
        pass

        # current_tasks = empty list

        #   for coordinate in grave_cleaning_coordinates:
        #       append to current tasks
        #       spawn dirty grave

        #   for coordinate in grave_flower_coordinates:
        #       append to current tasks
        #       spawn grave that needs flowers

        #   for coordinate in chime_coordinates:
        #       append to current tasks
        #       spawn chime markers

    def task_counter(self):
        pass

        #   total_tasks = (int)
        #   current_tasks_counter = (int)

        #   for task in current_tasks:
        #       total_tasks = number of tasks
        #       current_tasks_counter = number of tasks
        #           when one task is marked as finished, decrease current tasks counter