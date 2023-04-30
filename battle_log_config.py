from path_correction import get_game_pos_size


def two_log_region():
    pos_size = get_game_pos_size()
    return pos_size["game_xpos"], pos_size["game_ypos"] + int(pos_size["game_height"] * 8/9), \
        int(pos_size["game_width"] * 1/3), int(pos_size["game_height"] * 1/9)
