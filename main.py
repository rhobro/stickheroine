import io

import numpy as np
from PIL import Image
from ppadb.client import Client as Adb

ESTIMATE_Y = 2600
REPLAY_COORD = (1150, 2130)
STICK_GEN_SPEED = 1
STICK_GEN_COEFF = 0.75

adb = Adb()
device = adb.device("192.168.0.10:5555")


def main():
    while True:
        p_row = screen()[ESTIMATE_Y].sum(axis=1)

        # find x-coord for gap start
        gap_start = 0
        pillar_start = 0
        pillar_end = 0
        for i, p in enumerate(p_row):
            if i == 0:
                continue

            if gap_start == 0:
                # find gap start
                if p_row[i - 1] == 0 and p != 0:
                    gap_start = i

            elif pillar_start == 0:
                # find gap end
                if p_row[i - 1] != 0 and p == 0:
                    pillar_start = i

            elif pillar_end == 0:
                # find pillar end
                if p_row[i - 1] == 0 and p != 0:
                    pillar_end = i
                    break

        print(pillar_start, pillar_end, gap_start)
        stick_len = (pillar_start + pillar_end) // 2 - gap_start
        device.input_swipe(500, 500, 500, 500, int(STICK_GEN_COEFF * stick_len * STICK_GEN_SPEED))
        wait_until_still()


def wait_until_still():
    while not (screen()[ESTIMATE_Y] == screen()[ESTIMATE_Y]).all():
        continue


def screen():
    return np.array(Image.open(io.BytesIO(device.screencap())))[:, :, :3]


if __name__ == "__main__":
    main()
