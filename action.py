#Fonction 1: Sert à placer un anneau
def handle_ring_placement(game_interface, point_x, point_y):
    player_list = game_interface.place_circle_blue if game_interface.turn == 1 else game_interface.place_circle_red

    for px, py, tag in player_list:
        if (point_x, point_y) == (px, py):
            print(f"Ring already placed at ({point_x}, {point_y}). No action taken.")
            return

    if game_interface.rings_placed[game_interface.turn] >= game_interface.max_rings:
        print(f"Player {game_interface.turn} has already placed the maximum number of rings.")
        return

    color = 'blue' if game_interface.turn == 1 else 'red'
    tag = game_interface.draw_fixed_circle(point_x, point_y, color)
    player_list.append((point_x, point_y, tag))
    game_interface.rings_placed[game_interface.turn] += 1
    hex_coords = game_interface.coords[(point_x, point_y)]

    if game_interface.rings_placed[1] == game_interface.max_rings and game_interface.rings_placed[2] == game_interface.max_rings:
        game_interface.state = 'PLACING_MARKERS'
        print("All rings placed. Switching to MARKER PLACEMENT phase.")

    game_interface.change_turn()

#Fonction 2: Sert à placer un marqueur
def handle_marker_placement(game_interface, point_x, point_y):
    player_rings = game_interface.place_circle_blue if game_interface.turn == 1 else game_interface.place_circle_red

    marker_placed = False

    for px, py, tag in player_rings:
        if (point_x, point_y) == (px, py):
            game_interface.fill_circle(point_x, point_y)
            win = game_interface.winning_condition()
            if win:
                game_interface.state = 'REMOVING_RING'
                game_interface.selected_alignment = win
                game_interface.prompt_ring_removal()
            else:
                game_interface.state = 'MOVING_RINGS'
            game_interface.selected_ring = (point_x, point_y, tag)
            game_interface.change_turn()
            marker_placed = True
            hex_coords = game_interface.coords[(point_x, point_y)]
            break

    if not marker_placed:
        print("Vous devez placer un marqueur dans un de vos anneaux.")

#Fonction 3: Sert à retirer un anneau
def handle_ring_removal(game_interface, point_x, point_y):
    player_rings = game_interface.place_circle_blue if game_interface.turn == 1 else game_interface.place_circle_red

    for px, py, tag in player_rings:
        if (point_x, point_y) == (px, py):
            game_interface.canvas.delete(tag)
            player_rings.remove((px, py, tag))
            game_interface.rings_removed[game_interface.turn] += 1
            game_interface.update_rings_removed_label()
            if game_interface.mode == "normal":
                if game_interface.rings_removed[game_interface.turn] == game_interface.max_removed_rings:
                    game_interface.end_game()
                else:
                    game_interface.state = 'MOVING_RINGS'
            elif game_interface.mode == "blitz":
                if game_interface.rings_removed[game_interface.turn] == game_interface.max_removed_rings_blitz:
                    game_interface.end_game()
                else:
                    game_interface.state = 'MOVING_RINGS'
            return

    print("Vous devez retirer un de vos anneaux.")

#Fonction 4: Sert à déplacer un anneau
def handle_ring_movement(game_interface, point_x, point_y):
    if game_interface.selected_ring:
        to_pos = (point_x, point_y)
        game_interface.is_valid_move(game_interface.selected_ring, to_pos)
        if game_interface.is_valid_move(game_interface.selected_ring, to_pos):
            game_interface.move_ring(game_interface.selected_ring, to_pos)
            game_interface.selected_ring = None
            game_interface.change_turn()
            game_interface.state = 'PLACING_MARKERS'
        else:
            from_hex = game_interface.coords[(game_interface.selected_ring[0], game_interface.selected_ring[1])]
            to_hex = game_interface.coords[(point_x, point_y)]
            print(f"Mouvement invalide de {from_hex} à {to_hex}.")
    else:
        print("Aucun anneau sélectionné pour le mouvement.")
