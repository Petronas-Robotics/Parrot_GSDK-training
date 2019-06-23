# PETRONAS Technology Challange 6
# Written by: M Arif Abd Rahman,  June 2019
# This code is provided as is and we are not liable for any consequential damages from using it.
# Use this code at your own risk.

# This code shows how to detect apriltags from video stream of Anafi
# (temperary using mss screenshot until olympe video streaming API is fixed by Parrot)
# and based on detected tag, the drone will takeoff or land.

import olympe
import olympe_deps as od
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing
from olympe.messages.skyctrl.CoPiloting import setPilotingSource
import time
import cv2
import mss
import numpy as np
import apriltag

# Create the apriltag detector
detector = apriltag.Detector()

# If using real drone with Skycontroller 3:
drone = olympe.Drone("192.168.53.1", mpp=True, drone_type=od.ARSDK_DEVICE_TYPE_ANAFI4K)
# If using simulation:
# drone = olympe.Drone("10.202.0.1")

# Connect to the drone
drone.connection()
drone(setPilotingSource(source="Controller")).wait()

# Flag for takeoff state
takeoff_flag = False

# Here we use mss to capture the screen output from PDrAW
with mss.mss() as sct:
    # Set which part of the screen to capture. Make sure your PDrAW window is always here.
    monitor = {"top": 60, "left": 60, "width": 960, "height": 540}

    while 1:
        # Get raw pixels from the screen, save it to a Numpy array
        frame = np.array(sct.grab(monitor))

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

        # Detect the tag
        result = detector.detect(gray)
        # Example result:
        ### [Detection(tag_family=b'tag36h11', tag_id=1, hamming=0, goodness=0.0, decision_margin=68.70601654052734, homography=array([[-6.54479552e-01, -1.57007978e-01, -4.53781537e+00],
        ### [ 1.16328645e-01, -7.23913268e-01, -1.29534166e+00],
        ### [ 6.58239283e-05, -1.05436347e-04, -7.62466203e-03]]), center=array([595.14970657, 169.88840335]), corners=array([[491.27270508,  90.67271423],
        ### [675.56896973,  61.0593338 ],
        ### [697.95294189, 248.2852478 ],
        ### [518.26373291, 273.93597412]]))]

        # Now we loop through each detected tag
        for i in range(len(result)):
            # Draw bounding boxes
            pts = np.array(result[i].corners, np.int32)
            pts = pts.reshape((-1,1,2))
            frame = cv2.polylines(frame,[pts],True,(0,255,255),10)
            # Print the tag ID
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,str(result[i].tag_id), tuple(np.array(result[i].center, np.int32)), font, 3,(255,255,255),5,cv2.LINE_AA)

            # Control the drone
            # If tag ID 0 detected, and the drone has not taken off, then take off
            if(result[i].tag_id==0 and not takeoff_flag):
                # Take off!
                drone(TakeOff()).wait()
                # Just to display on the terminal
                for p in range(10):
                    print("I'm taking off!!!!!!!!")
                # Set the flag
                takeoff_flag = True
            # If tag ID 1 detected, and the drone has already taken off, then land
            elif(result[i].tag_id==1 and takeoff_flag):
                # Landing!
                drone(Landing()).wait()
                # Just to display on the terminal
                for p in range(10):
                    print("I'm landing!!!!!!!!")
                # Unset the flag
                takeoff_flag = False

        # Display the image
        cv2.imshow("Anafi apriltag", frame)

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

# Disconnect from the drone
drone.disconnection()
