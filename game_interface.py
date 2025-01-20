from tkinter import Tk, Canvas, PhotoImage, Frame, Label, Button, mainloop
from action import handle_ring_placement, handle_marker_placement, handle_ring_removal, handle_ring_movement
from valid_move import is_valid_move
from winning import winning_condition
from update_game import move_ring, convert_marker, convert_markers_along_path, remove_ring
from ai import AI as ai

class GameInterface:
    def __init__(self, master, img_path, coords, mode):
        self.master = master
        self.master.title("Yinsh")
        self.canvas = Canvas(master, width=750, height=750)
        self.img = PhotoImage(file=img_path)
        self.background = self.canvas.create_image(375, 375, image=self.img, tags="background")

        self.canvas.pack()
        self.coords = coords
        self.hovered_circle = None
        self.draw_intersections(coords)
        self.turn = 1
        self.turn_ai = 1
        self.text_color = "blue"

        self.turn_label = Label(master, text="Player 1", font=("Helvetica", 16), fg=self.text_color)
        self.turn_label.pack()

        self.coord_label = Label(master, text="", font=("Helvetica", 12))
        self.coord_label.pack()
        
        self.rings_removed_label = Label(master, text="Rings removed - Player 1: 0, Player 2: 0", font=("Helvetica", 12))
        self.rings_removed_label.pack()

        self.button_frame = Frame(master)
        self.button_frame.pack(side='right')

        self.button_frame = Frame(master)
        self.button_frame.pack(pady=(5, 0))

        self.button_1player = Button(self.button_frame, text="Restart", command=self.restart_game)
        self.button_1player.pack(side='left', padx=5)

        self.canvas.bind('<Motion>', self.mouse_hover)
        self.canvas.bind('<Button-1>', self.mouse_click)

        self.last_circles = [] 
        self.place_circle_blue = []
        self.place_circle_red = []
        self.place_marker_blue = []
        self.place_marker_red = []
        
        self.state = 'PLACING_RINGS'
        
        self.rings_removed  = {1: 0, 2: 0}
        self.max_removed_rings  = 3
        self.max_removed_rings_blitz = 1
        self.rings_placed = {1: 0, 2: 0}
        self.max_rings = 5
        self.mode = mode

        self.selected_ring = None
        self.next_circle_id = 1 
        
        self.circles = {}
        
        if self.mode == "ai":
            self.ai = ai(self)
        else:
            self.ai = None
        
    DIRECTIONS = {
        'N': (0, 1),
        'NE': (1, 1),
        'SE': (1, 0),
        'S': (0, -1),
        'SW': (-1, -1),
        'NW': (-1, 0)
    }

    # Fonction pour afficher le nombre d'anneaux retirés sur l'interface graphique
    def update_rings_removed_label(self):
        self.rings_removed_label.config(text=f"Rings removed - Player 1: {self.rings_removed[1]}, Player 2: {self.rings_removed[2]}")
    
    def prompt_ring_removal(self):
        self.turn_label.config(text=f"Player {self.turn}, remove one of your rings", fg=self.text_color)

    # Fonction pour afficher les points à chaque intersections du plateau
    def draw_intersections(self, coords):
        for coord_x, coord_y in self.coords:
            self.create_clickable_point(coord_x, coord_y)

    # Fonction pour créer un point cliquable
    def create_clickable_point(self, x, y):
        self.canvas.create_oval(x, y, x, y, fill='white', tags=f"point{x}_{y}")
        self.canvas.tag_bind(f"point{x}_{y}", '<Button-1>')

    # Fonction pour dessiner un cercle au survol d'un point
    def draw_hover_circle(self, x, y, color):
        hover_circle_id = self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, outline=color, width=5)
        self.last_circles.append(hover_circle_id)
        return hover_circle_id

    # Fonction pour dessiner un anneau
    def draw_fixed_circle(self, x, y, color):
        tag = f"{color}_ring_{x}_{y}"
        self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, outline=color, width=5, tags=tag)
        return tag

    #Fonction qui permet de savoir si un point est survolé
    def mouse_hover(self, event):
        x, y = event.x, event.y
        hovered_circle_coords = None
        for point_x, point_y in self.coords:
            distance = ((point_x - x) ** 2 + (point_y - y) ** 2) ** 0.5
            if distance < 30:
                for circle_list in [self.place_circle_blue, self.place_circle_red]:
                    for px, py, _ in circle_list:
                        if (point_x, point_y) == (px, py):
                            self.clear_hovered_circle()
                            self.clear_possible_moves()
                            self.coord_label.config(text="")
                            return
                        
                hovered_circle_coords = (point_x, point_y)
                break

        if hovered_circle_coords is not None:
            self.clear_hovered_circle()
            color = 'blue' if self.turn == 1 else 'red'
            self.draw_hover_circle(hovered_circle_coords[0], hovered_circle_coords[1], color)
            self.hovered_circle = hovered_circle_coords
            hex_coords = self.coords[hovered_circle_coords]
            self.coord_label.config(text=f"Hex coordinates: {hex_coords}")
            if self.state == 'MOVING_RINGS':
                self.show_possible_moves(self.selected_ring)
        else:
            self.clear_hovered_circle()
            self.clear_possible_moves()
            self.coord_label.config(text="")

    # Fonction pour afficher les mouvements possibles
    def show_possible_moves(self, ring_pos):
        from_screen_x, from_screen_y, from_tag = ring_pos
        from_hex = self.coords[(from_screen_x, from_screen_y)]
        from_x, from_y = from_hex

        for direction, (dx, dy) in self.DIRECTIONS.items():
            to_x, to_y = from_x, from_y
            while True:
                to_x += dx
                to_y += dy
                screen_pos = self.get_screen_coords((to_x, to_y))
                if not screen_pos or not self.is_valid_move(ring_pos, screen_pos):
                    break
                screen_x, screen_y = screen_pos
                hover_id = self.canvas.create_oval(screen_x - 30, screen_y - 30, screen_x + 30, screen_y + 30, outline="green", width=2)
                self.last_circles.append(hover_id)

    # Fonction pour obtenir les coordonnées "écran" à partir des coordonnées hexagonales
    def get_screen_coords(self, hex_coords):
        for screen_coords, hex in self.coords.items():
            if hex == hex_coords:
                return screen_coords
        return None

    # Fonction pour effacer les mouvements possibles
    def clear_possible_moves(self):
        while self.last_circles:
            last_circle = self.last_circles.pop()
            self.canvas.delete(last_circle)

    # Fonction pour effacer le cercle survolé
    def clear_hovered_circle(self):
        if self.hovered_circle is not None:
            self.canvas.delete(self.hovered_circle)
            self.hovered_circle = None

    # Fonction pour gérer le clic de la souris
    def mouse_click(self, event):
        x, y = event.x, event.y
        if self.turn == 2 and self.mode == "ai":
            self.ai.make_move()
            return
            
        for point_x, point_y in self.coords.keys():
            distance = ((x - point_x) ** 2 + (y - point_y) ** 2) ** 0.5
            if distance < 30:
                if self.state == 'PLACING_RINGS':
                    self.handle_ring_placement(point_x, point_y)
                elif self.state == 'PLACING_MARKERS':
                    self.handle_marker_placement(point_x, point_y)
                elif self.state == 'MOVING_RINGS':
                    self.handle_ring_movement(point_x, point_y)
                elif self.state == 'REMOVING_RING':
                    self.handle_ring_removal(point_x, point_y)
                break
            
#-----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------
            
    # Appel des fonctions de action.py
            
    def handle_ring_placement(self, point_x, point_y):
        handle_ring_placement(self, point_x, point_y)

    def handle_marker_placement(self, point_x, point_y):
        handle_marker_placement(self, point_x, point_y)

    def handle_ring_removal(self, point_x, point_y):
        handle_ring_removal(self, point_x, point_y)

    def handle_ring_movement(self, point_x, point_y):
        handle_ring_movement(self, point_x, point_y)
            
#-----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------

    # Appel des fonctions de valid_move.py
    
    def is_valid_move(self, from_pos, to_pos):
        return is_valid_move(self, from_pos, to_pos)
    
#-----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------

    # Appel des fonctions de winning.py et gestion de la fin de partie

    def winning_condition(self):
        return winning_condition(self)
    
    def end_game(self):
        winner = "Player 1" if self.turn == 1 else "Player 2"
        self.turn_label.config(text=f"{winner} wins!", fg=self.text_color)
        self.canvas.unbind('<Button-1>')

    
#-----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------

    # Appel des fonctions de update_game.py

    def move_ring(self, from_pos, to_pos):
        move_ring(self, from_pos, to_pos)

    def convert_marker(self, position):
        convert_marker(self, position)

    def convert_markers_along_path(self, from_pos, to_pos):
        convert_markers_along_path(self, from_pos, to_pos)

    def remove_ring(self, x, y, color):
        remove_ring(self, x, y, color)
            
#-----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------

    # Fonction pour placer un marker (remplir un anneau avec un marqueur)
    def fill_circle(self, x, y):
        circle_color = 'blue' if self.turn == 1 else 'red'
        tag = f"{circle_color}_marker_{x}_{y}"
        
        hex_coords = self.coords[(x, y)]
        x_hex, y_hex = hex_coords

        if circle_color == 'blue':
            self.place_marker_blue.append((x_hex, y_hex, tag))
        else:
            self.place_marker_red.append((x_hex, y_hex, tag))
            self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill=circle_color, outline='', tags=tag)
            self.remove_ring(x, y, circle_color)
        self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill=circle_color, outline='', tags=tag)
        self.remove_ring(x, y, circle_color)
        self.change_turn()

    # Fonction pour connaître le tour actuel
    def current_player_turn(self):
        if self.turn == 2:
            player = "Player 2"
            text_color = "red"
        elif self.turn == 1:
            player = "Player 1"
            text_color = "blue"
        
        self.turn_label.config(text=f"{player}", fg=text_color)

    # Fonction pour changer de tour
    def change_turn(self):
        self.turn = 2 if self.turn == 1 else 1
        self.current_player_turn()

    def displayBoard(self):
        mainloop()

    # Fonction pour redémarrer le jeu
    def restart_game(self):
        from start_interface import StartInterface  # Importation retardée
        self.master.destroy()  # Ferme la fenêtre actuelle
        start_interface = StartInterface()
        start_interface.run()

# Fonction pour initialiser l'interface graphique du jeu avec son dictionnaire de coordonnées
def initialize_game_interface(mode):
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
    boardImage = 'src/plateau750.png'
    root = Tk()
    return GameInterface(root, boardImage, coords, mode)
