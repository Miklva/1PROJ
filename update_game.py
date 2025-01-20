import socket
import pickle

# Fonction qui permet de déplacer un anneau d'une position à une autre
def move_ring(game_interface, from_pos, to_pos):
    from_x, from_y, from_tag = from_pos
    to_x, to_y = to_pos
    color = 'blue' if game_interface.turn == 1 else 'red'

    game_interface.canvas.delete(from_tag)

    new_tag = f"{color}_ring_{to_x}_{to_y}"
    game_interface.canvas.create_oval(to_x - 30, to_y - 30, to_x + 30, to_y + 30, outline=color, width=5, tags=new_tag)

    player_list = game_interface.place_circle_blue if game_interface.turn == 1 else game_interface.place_circle_red
    player_list.append((to_x, to_y, new_tag))

    convert_markers_along_path(game_interface, (from_x, from_y), (to_x, to_y))

# Fonction qui permet convertir un marker (s'il est bleu, il devient rouge et vice versa)
def convert_marker(game_interface, position):
    x, y = position
    found = False

    screen_coords = None
    for screen_position, hex_position in game_interface.coords.items():
        if hex_position == (x, y):
            screen_coords = screen_position
            break

    if screen_coords is None:
        return

    screen_x, screen_y = screen_coords

    for px, py, tag in game_interface.place_marker_blue:
        if (x, y) == (px, py):
            new_color = 'red'
            new_tag = f"{new_color}_marker_{x}_{y}"
            game_interface.canvas.delete(tag)
            game_interface.canvas.create_oval(screen_x - 25, screen_y - 25, screen_x + 25, screen_y + 25, fill=new_color, outline='', tags=new_tag)
            game_interface.place_marker_blue.remove((px, py, tag))
            game_interface.place_marker_red.append((x, y, new_tag))
            found = True
            break

    if not found:
        for px, py, tag in game_interface.place_marker_red:
            if (x, y) == (px, py):
                new_color = 'blue'
                new_tag = f"{new_color}_marker_{x}_{y}"
                game_interface.canvas.delete(tag)
                game_interface.canvas.create_oval(screen_x - 25, screen_y - 25, screen_x + 25, screen_y + 25, fill=new_color, outline='', tags=new_tag)
                game_interface.place_marker_red.remove((px, py, tag))
                game_interface.place_marker_blue.append((x, y, new_tag))
                found = True
                break

    if not found:
        False

# Fonction qui permet de convertir les markers sur le chemin lors d'un déplacement d'anneau
def convert_markers_along_path(game_interface, from_pos, to_pos):
    from_screen_x, from_screen_y = from_pos
    to_screen_x, to_screen_y = to_pos

    from_hex = game_interface.coords.get((from_screen_x, from_screen_y))
    to_hex = game_interface.coords.get((to_screen_x, to_screen_y))

    if from_hex is None or to_hex is None:
        return

    from_x, from_y = from_hex
    to_x, to_y = to_hex

    if from_x == to_x:
        step = 1 if to_y > from_y else -1
        for y in range(from_y + step, to_y, step):
            screen_coords = None
            for screen_position, hex_position in game_interface.coords.items():
                if hex_position == (from_x, y):
                    screen_coords = screen_position
                    break

            if screen_coords:
                screen_x, screen_y = screen_coords
                convert_marker(game_interface, (from_x, y))
        return

    dx = to_x - from_x
    dy = to_y - from_y

    if abs(dx) == abs(dy):
        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1
        x, y = from_x + step_x, from_y + step_y

        while (x, y) != (to_x, to_y):
            screen_coords = None
            for screen_position, hex_position in game_interface.coords.items():
                if hex_position == (x, y):
                    screen_coords = screen_position
                    break

            if screen_coords:
                screen_x, screen_y = screen_coords
                convert_marker(game_interface, (x, y))
            x += step_x
            y += step_y

    elif from_y == to_y:
        step_x = 1 if dx > 0 else -1
        x = from_x + step_x

        while x != to_x:
            screen_coords = None
            for screen_position, hex_position in game_interface.coords.items():
                if hex_position == (x, from_y):
                    screen_coords = screen_position
                    break

            if screen_coords:
                screen_x, screen_y = screen_coords
                convert_marker(game_interface, (x, from_y))
            x += step_x
    else:
        print("Le mouvement n'est ni vertical ni diagonal.")

# Fonction qui permet de retirer un anneau
def remove_ring(game_interface, x, y, color):
    player_list = game_interface.place_circle_blue if color == 'blue' else game_interface.place_circle_red
    for px, py, tag in player_list.copy():
        if px == x and py == y:
            game_interface.canvas.delete(tag)
            player_list.remove((px, py, tag))
            break
