import numpy as np
from ppadb.client import Client as Adb
from PIL import Image
import io

PIXEL_LEVEL = 2300
REPLAY_COORD = (1150, 2130)

adb = Adb()
device = adb.device("192.168.0.10:5555")


while True:
    h=3


def screen():
    return np.array(Image.open(io.BytesIO(device.screencap())))[:, :, :3]
