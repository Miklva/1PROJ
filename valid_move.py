# Fonction qui permet de vérifier si un mouvement est valide
def is_valid_move(game_interface, from_pos, to_pos):
    from_screen_x, from_screen_y, from_tag = from_pos
    to_screen_x, to_screen_y = to_pos

    from_hex = game_interface.coords.get((from_screen_x, from_screen_y))
    to_hex = game_interface.coords.get((to_screen_x, to_screen_y))
    
    from_x, from_y = from_hex
    to_x, to_y = to_hex

    # Vérifier si la position cible est vide
    all_positions = game_interface.place_circle_blue + game_interface.place_circle_red
    for px, py, _ in all_positions:
        if (to_screen_x, to_screen_y) == (px, py):
            return False

    # Vérifier le mouvement vertical
    if from_x == to_x:
        step = 1 if to_y > from_y else -1
        current_y = from_y + step

        while current_y != to_y:
            for px, py, _ in all_positions:
                if from_x == px and current_y == py:
                    print("Une case intermédiaire est occupée.")
                    return False
            current_y += step

        return True

    # Vérifier les mouvements diagonaux
    dx = to_x - from_x
    dy = to_y - from_y

    if abs(dx) == abs(dy):  # Mouvement diagonal classique
        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1
        current_x = from_x + step_x
        current_y = from_y + step_y

        while (current_x, current_y) != (to_x, to_y):
            for px, py, _ in all_positions:
                if current_x == px and current_y == py:
                    print("Une case intermédiaire est occupée.")
                    return False
            current_x += step_x
            current_y += step_y

        return True

    # Vérifier les mouvements diagonaux NW ou SE
    if from_y == to_y:  # Mouvement NW ou SE
        step_x = 1 if dx > 0 else -1
        current_x = from_x + step_x

        while current_x != to_x:
            for px, py, _ in all_positions:
                if current_x == px and from_y == py:
                    print("Une case intermédiaire est occupée.")
                    return False
            current_x += step_x

        return True

    return False  # Mouvement non valide si ce n'est ni vertical ni diagonal
