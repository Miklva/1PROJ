import random
from action import handle_marker_placement, handle_ring_placement, handle_ring_removal, handle_ring_movement

class AI:
    def __init__(self, game_interface):
        self.game_interface = game_interface

    # Fonction pour faire un mouvement
    def make_move(self):
        if self.game_interface.state == 'PLACING_RINGS':
            self.place_ring()
        elif self.game_interface.state == 'PLACING_MARKERS':
            self.place_marker()
        elif self.game_interface.state == 'MOVING_RINGS':
            self.move_ring()
        elif self.game_interface.state == 'REMOVING_RING':
            self.remove_ring()

    # Fonction pour placer un anneau
    def place_ring(self):
        available_positions = []
        circle_blue = self.game_interface.place_circle_blue
        for key in coords:
            available_positions.append(key)
            
        available_positions = [element for element in available_positions if element not in circle_blue]

        if available_positions:
            x, y = random.choice(available_positions)
            handle_ring_placement(self.game_interface, x, y)

    # Fonction pour placer un marqueur
    def place_marker(self):
        circle_red = self.game_interface.place_circle_red
        available_positions = []
        for x, y, _ in circle_red:
            available_positions.append((x, y))
        if available_positions:
            x, y = random.choice(available_positions)
            handle_marker_placement(self.game_interface, x, y)  

    # Fonction pour déplacer un anneau
    def move_ring(self):
        available_positions = []
        for key in coords:
            available_positions.append(key)
        if available_positions:
            x, y = random.choice(available_positions)
            handle_ring_movement(self.game_interface, x, y)

    # Fonction pour retirer un anneau
    def remove_ring(self):
        circle_red = self.game_interface.place_circle_red
        available_positions = []
        for x, y, _ in circle_red:
            available_positions.append((x, y))
        if available_positions:
            x, y, _ = random.choice(available_positions)
            handle_ring_removal(self.game_interface, x, y)


# Dictionnaire des points du plateau
coords = {
        (300, 10): (-1, 4), (445, 10): (1, 5),
        (228, 47): (-2, 3), (372, 47): (0, 4), (516, 47): (2, 5),
        (163, 83): (-3, 2), (305, 83): (-1, 3), (445, 83): (1, 4), (588, 83): (3, 5),
        (95, 130): (-4, 1), (230, 130): (-2, 2), (372, 130): (0, 3), (516, 130): (2, 4), (659, 130): (4, 5),
        (163, 170): (-3, 1), (305, 170): (-1, 2), (445, 170): (1, 3), (588, 170): (3, 4),
        (95, 210): (-4, 0), (230, 210): (-2, 1), (372, 210): (0, 2), (516, 210): (2, 3), (659, 210): (4, 4),
        (25, 250): (-5, -1), (163, 250): (-3, 0), (305, 250): (-1, 1), (445, 250): (1, 2), (588, 250): (3, 3), (725, 250): (5, 4),
        (95, 290): (-4, -1), (230, 290): (-2, 0), (372, 290): (0, 1), (516, 290): (2, 2), (659, 290): (4, 3),
        (25, 330): (-5, -2), (163, 330): (-3, -1), (305, 330): (-1, 0), (445, 330): (1, 1), (588, 330): (3, 2), (725, 330): (5, 3),
        (95, 370): (-4, -2), (230, 370): (-2, -1), (372, 370): (0, 0), (516, 370): (2, 1), (659, 370): (4, 2),
        (25, 415): (-5, -3), (163, 415): (-3, -2), (305, 415): (-1, -1), (445, 415): (1, 0), (588, 415): (3, 1), (725, 415): (5, 2),
        (95, 455): (-4, -3), (372, 455): (0, -1), (230, 455): (-2, -2), (516, 455): (2, 0), (659, 455): (4, 1),
        (25, 495): (-5, -4), (163, 495): (-3, -3), (305, 495): (-1, -2), (445, 495): (1, -1), (588, 495): (3, 0), (725, 495): (5, 1),
        (95, 535): (-4, -4), (230, 535): (-2, -3), (372, 535): (0, -2), (516, 535): (2, -1), (659, 535): (4, 0),
        (163, 575): (-3, -4), (305, 575): (-1, -3), (445, 575): (1, -2), (588, 575): (3, -1),
        (95, 615): (-4, -5), (230, 615): (-2, -4), (372, 615): (0, -3), (516, 615): (2, -2), (659, 615): (4, -1),
        (163, 660): (-3, -5), (305, 660): (-1, -4), (445, 660): (1, -3), (588, 660): (3, -2),
        (228, 700): (-2, -5), (372, 700): (0, -4), (516, 700): (2, -3),
        (300, 745): (-1, -5), (445, 745): (1, -4)
    }
