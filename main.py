import numpy as np
import scrcpy
from adbutils import AdbClient

# consts and coords
TAP_COORDS = (2400, 720)
RED_Y = 2225
CHERRY_Y = 2290
LEVEL_Y = 2218


def main():
    # connect to adbd
    adb_d = AdbClient(host="127.0.0.1", port=5037)
    device = adb_d.device_list()[0]

    # connect to device via scrcpy
    scr = scrcpy.Client(device)

    # start stream and bot
    scr.add_listener(scrcpy.EVENT_FRAME, listen)
    scr.start()


# custom listener
def listen(frame: np.ndarray):
    """Frame has dimensions (2960, 1440, 3)"""

    if frame is not None:
        growth_x = stick_growth_x(frame)

    else:
        # no change in screen
        pass


BLACK_MAX = 5


def stick_growth_x(frame: np.ndarray) -> int:
    frame = frame.mean(axis=2)
    entered_black = False

    for x in range(frame.shape[1]):
        point = frame[TAP_COORDS[0], x]

        if entered_black:
            # look for next non-black
            if point > BLACK_MAX:
                return x

        else:
            # has entered black platform?
            if point <= BLACK_MAX:
                entered_black = True


if __name__ == "__main__":
    main()
