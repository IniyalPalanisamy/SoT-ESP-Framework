@Author https://github.com/DougTheDruid
@Source https://github.com/DougTheDruid/SoT-ESP-Framework
For community support, please contact me on Discord: DougTheDruid#2784

from base64 import b64decode
import pyglet
from pyglet.text import Label
from pyglet.gl import Config
from helpers import SOT_WINDOW, SOT_WINDOW_H, SOT_WINDOW_W, main_batch, version, logger, initialize_window
from sot_hack import SoTMemoryReader

# Constants
FPS_TARGET = 60
DEBUG = False
UPDATE_INTERVAL = 5  # seconds for generating all actors
PROCESS_CHECK_INTERVAL = 3  # seconds for checking process activity

# Pyglet clock used to track time via FPS
clock = pyglet.clock.Clock()

def generate_all(_):
    """Triggers a read_actors call to refresh display objects."""
    smr.read_actors()

def update_graphics(_):
    """Updates the graphics for all relevant display objects."""
    smr.update_my_coords()
    to_remove = []

    for actor in smr.display_objects:
        actor.update(smr.my_coords)
        if actor.to_delete:
            to_remove.append(actor)

    for removable in to_remove:
        smr.display_objects.remove(removable)

if __name__ == '__main__':
    logger.info(b64decode("RG91Z1RoZURydWlkJ3MgRVNQIEZzcmF3ZW1hbGx5IEZyYW1ld29yayBTdGFydGluZw==").decode("utf-8"))
    logger.info(f"Hack Version: {version}")

    # Initialize our SoT Hack object
    smr = SoTMemoryReader()

    if DEBUG:
        while True:
            smr.read_actors()

    config = Config(double_buffer=True, depth_size=24, alpha_size=8)
    window = pyglet.window.Window(SOT_WINDOW_W, SOT_WINDOW_H, vsync=False, style='overlay', config=config,
                                  caption="DougTheDruid's ESP Framework")
    window.set_location(SOT_WINDOW[0], SOT_WINDOW[1])

    @window.event
    def on_draw():
        """Draws the current state of the window."""
        window.clear()
        if smr.crew_data:
            player_count.text = f"Player Count: {smr.crew_data.total_players}"
        main_batch.draw()
        fps_display.draw()

    # Initialize the window
    init = initialize_window()

    pyglet.clock.schedule_interval(generate_all, UPDATE_INTERVAL)
    pyglet.clock.schedule_interval(smr.rm.check_process_is_active, PROCESS_CHECK_INTERVAL)
    pyglet.clock.schedule(update_graphics)

    # FPS counter
    fps_display = pyglet.window.FPSDisplay(window)

    # Player count label
    player_count = Label("...Initializing Framework...",
                         x=SOT_WINDOW_W * 0.85,
                         y=SOT_WINDOW_H * 0.9, batch=main_batch)

    pyglet.app.run(interval=1 / FPS_TARGET)
