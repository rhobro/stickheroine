import io
from time import time as t, sleep as s

import numpy as np
from PIL import Image
from ppadb.client import Client as Adb

ESTIMATE_Y = 2600
CHERRY_Y = 2290
REPLAY_COORD = (1150, 2130)
STICK_GEN_SPEED = 1
STICK_GEN_COEFF = .7

adb = Adb()
device = adb.devices()[0]


def main():
    while True:
        scr = screen()
        p_row = scr[ESTIMATE_Y].sum(axis=1)

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

        stick_len = (pillar_start + pillar_end) // 2 - gap_start
        move_t = t() * 1000
        device.input_swipe(500, 500, 500, 500, dist2time(stick_len))

        # calculate cherry position
        cherry_row = scr[CHERRY_Y, gap_start: pillar_start]
        cherry_row_s = cherry_row.sum(axis=1)
        cherry_dist = 0
        for i in range(len(cherry_row_s[:-80])):
            if 250 < cherry_row_s[i: i + 80].mean() < 260:
                cherry_dist = i
                break

        # send flip commands
        if cherry_dist != 0:
            delay = dist2time(cherry_dist) - 100
            while t() * 1000 < move_t + delay:
                continue
            print("now")
            device.input_tap(500, 500)
            s(.2)
            device.input_tap(500, 500)

        wait_until_still()
        # failed? restart?
        btn_colours = screen()[REPLAY_COORD[1], REPLAY_COORD[0]]
        if (btn_colours == (104, 104, 104)).all():
            device.input_tap(REPLAY_COORD[0], REPLAY_COORD[1])
            wait_until_still()


def dist2time(pixels) -> int:
    return int(STICK_GEN_COEFF * pixels * STICK_GEN_SPEED)


def wait_until_still():
    while not (screen()[ESTIMATE_Y] == screen()[ESTIMATE_Y]).all():
        continue


def screen() -> np.ndarray:
    return np.array(Image.open(io.BytesIO(device.screencap())))[:, :, :3]


if __name__ == "__main__":
    main()
