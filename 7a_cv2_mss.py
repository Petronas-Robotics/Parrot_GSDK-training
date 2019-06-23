# PETRONAS Technology Challange 6
# Written by: M Arif Abd Rahman,  June 2019
# This code is provided as is and we are not liable for any consequential damages from using it.
# Use this code at your own risk.

# Since we cannot get Anafi's video feed directly into Olympe yet,
# we are going to use this little hack;
# 1) Use PDrAW to stream the video feed from Anafi. This stream will appear in one window.
# 2) Use mss (https://pypi.org/project/mss) to screen shot PDrAW's window
# 3) Feed the screenshot into OpenCV and process it accordingly

import time
import cv2
import mss
import numpy as np

with mss.mss() as sct:
    # Set which part of the screen to capture. Make sure your PDrAW window is always here.
    monitor = {"top": 60, "left": 60, "width": 960, "height": 540}

    while 1:
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        frame = np.array(sct.grab(monitor))

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

        # Display the image
        cv2.imshow("Captured frame", gray)

        print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
