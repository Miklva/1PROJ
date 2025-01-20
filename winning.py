# Fonction qui permet de vérifier si un joueur a gagné
def winning_condition(game_interface):
    for i in range(-5, 6):
        consecutive_blue = []
        consecutive_red = []
        for (screen_x, screen_y), (hex_x, hex_y) in sorted(game_interface.coords.items(), key=lambda item: item[1]):
            if hex_x == i:
                marker_status = "No marker"
                for (px, py, tag) in game_interface.place_marker_blue:
                    if (hex_x, hex_y) == (px, py):
                        marker_status = "Blue marker"
                        consecutive_blue.append((px, py, tag))
                        consecutive_red = []
                        if len(consecutive_blue) == 5:
                            for bx, by, btag in consecutive_blue:
                                game_interface.canvas.delete(btag)
                                game_interface.place_marker_blue.remove((bx, by, btag))
                            return True
                        break
                else:
                    consecutive_blue = []

                for (px, py, tag) in game_interface.place_marker_red:
                    if (hex_x, hex_y) == (px, py):
                        marker_status = "Red marker"
                        consecutive_red.append((px, py, tag))
                        consecutive_blue = []
                        if len(consecutive_red) == 5:
                            for rx, ry, rtag in consecutive_red:
                                game_interface.canvas.delete(rtag)
                                game_interface.place_marker_red.remove((rx, ry, rtag))
                            return True
                        break
                else:
                    consecutive_red = []

    for i in range(-5, 6):
        consecutive_blue = []
        consecutive_red = []
        for (screen_x, screen_y), (hex_x, hex_y) in sorted(game_interface.coords.items(), key=lambda item: item[1]):
            if hex_y == i:
                marker_status = "No marker"
                for (px, py, tag) in game_interface.place_marker_blue:
                    if (hex_x, hex_y) == (px, py):
                        marker_status = "Blue marker"
                        consecutive_blue.append((px, py, tag))
                        consecutive_red = []
                        if len(consecutive_blue) == 5:
                            for bx, by, btag in consecutive_blue:
                                game_interface.canvas.delete(btag)
                                game_interface.place_marker_blue.remove((bx, by, btag))
                            return True
                        break
                else:
                    consecutive_blue = []

                for (px, py, tag) in game_interface.place_marker_red:
                    if (hex_x, hex_y) == (px, py):
                        marker_status = "Red marker"
                        consecutive_red.append((px, py, tag))
                        consecutive_blue = []
                        if len(consecutive_red) == 5:
                            for rx, ry, rtag in consecutive_red:
                                game_interface.canvas.delete(rtag)
                                game_interface.place_marker_red.remove((rx, ry, rtag))
                            return True
                        break
                else:
                    consecutive_red = []

    for diff in range(-5, 6):
        consecutive_blue = []
        consecutive_red = []
        for (screen_x, screen_y), (hex_x, hex_y) in sorted(game_interface.coords.items(), key=lambda item: item[1]):
            if hex_x - hex_y == diff:
                marker_status = "No marker"
                for (px, py, tag) in game_interface.place_marker_blue:
                    if (hex_x, hex_y) == (px, py):
                        marker_status = "Blue marker"
                        consecutive_blue.append((px, py, tag))
                        consecutive_red = []
                        if len(consecutive_blue) == 5:
                            for bx, by, btag in consecutive_blue:
                                game_interface.canvas.delete(btag)
                                game_interface.place_marker_blue.remove((bx, by, btag))
                            return True
                        break
                else:
                    consecutive_blue = []

                for (px, py, tag) in game_interface.place_marker_red:
                    if (hex_x, hex_y) == (px, py):
                        marker_status = "Red marker"
                        consecutive_red.append((px, py, tag))
                        consecutive_blue = []
                        if len(consecutive_red) == 5:
                            for rx, ry, rtag in consecutive_red:
                                game_interface.canvas.delete(rtag)
                                game_interface.place_marker_red.remove((rx, ry, rtag))
                            return True
                        break
                else:
                    consecutive_red = []

    return False
