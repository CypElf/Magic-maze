from upemtk import donne_evenement, type_evenement, clic_x, clic_y, ferme_fenetre, touche, mise_a_jour, attente_clic, efface_tout
from display import display_controls
import keys as k

def handle_pause_menu_interaction(pause_rectangle_coords, zones_coords, pause_key):
    """
    Handles the pause menu interactions, such as clicking on save or quit.
    """
    unpaused = False
    while not unpaused:

        event = donne_evenement()
        type_ev = type_evenement(event)

        if type_ev == "ClicGauche":
            click_x = clic_x(event)
            click_y = clic_y(event)

            for i, (x1, y1, x2, y2, txt) in enumerate(zones_coords):
                if click_x >= x1 and click_x <= x2 and click_y >= y1 and click_y <= y2:
                    if txt == "quitter":
                        ferme_fenetre()
                        exit(0)
                    else:
                        # TODO : save the game state in a file
                        pass
                elif not (click_x >= pause_rectangle_coords[0] and click_x <= pause_rectangle_coords[2] and click_y >= pause_rectangle_coords[1] and click_y <= pause_rectangle_coords[3]):
                    unpaused = True
        elif type_ev == "Touche":
            if touche(event).lower() == pause_key:
                unpaused = True
        mise_a_jour()

def handle_main_menu_interaction(zones_coords, window_width, window_height):
    """
    Handles the main menu interactions, such as loading a save or choosing the players count.
    """
    keys = dict()
    nothing_selected = True

    while nothing_selected:
        click_x, click_y, _ = attente_clic()
        for i, (x1, y1, x2, y2) in enumerate(zones_coords):
            if click_x >= x1 and click_x <= x2 and click_y >= y1 and click_y <= y2:
                efface_tout()

                players_count = i + 1
                keys = k.get_keys(players_count)

                display_controls(window_width, window_height, players_count, keys)
                attente_clic()
                nothing_selected = False
                return keys