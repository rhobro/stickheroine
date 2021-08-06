import numpy as np
import scrcpy
from adbutils import AdbClient

# connect to adbd
adb_d = AdbClient(host="127.0.0.1", port=5037)
device = adb_d.device_list()[0]

# connect to device via scrcpy
scr = scrcpy.Client(device)


# custom listener
def listen(frame: np.ndarray):
    if frame is not None:
        print(frame.mean())

    else:
        # no change in screen
        pass


# start stream and bot
scr.add_listener(scrcpy.EVENT_FRAME, listen)
scr.start(threaded=True)
