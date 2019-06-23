# PETRONAS Technology Challange 6
# Written by: Tareq ALqutami (tareqazizhasan.al-q@petronas.com),  June 2019
# This code is provided as is and we are not liable for any consequential damages from using it.
# Use this code at your own risk.

# This code shows how to use moveBy command to move the drone relative to its current position and change heading angle.
# the code also shows how to cascade commands using >> operator and use FlyingStateChanged.

import olympe
import olympe_deps as od
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.skyctrl.CoPiloting import setPilotingSource

SIMULATION = True # choose wether to use simulated drone or physical one
file_object  = open('drone_log.txt', 'w', encoding='UTF-8') # create a file to store logs


if SIMULATION:
   # connect to simulated drone in SPHINX and redirect drone logs into the file to keep terminal clean
   drone = olympe.Drone("10.202.0.1", logfile=file_object) # create Drone instance
else:
   # connect to physical drone through the Sky Controller
   # you can also connect to drone using Wifi using ip address 192.168.42.1
   drone = olympe.Drone("192.168.53.1", logfile=file_object, mpp=True, drone_type=od.ARSDK_DEVICE_TYPE_ANAFI4K)

# connect to the drone and check if connection was established
response = drone.connection()
if not response.OK: # if connection failed, exit
   print("Connection was not successful")
   exit()

# set piloting source to controller, only when connecting through the Sky Controller
if not SIMULATION:
   drone(setPilotingSource(source="Controller")).wait()

# send takeoff command then wait for flyingState to change to hovering. Waiting timeout is 5 seconds.
# this is a more efficient way to wait for takeoff to finish.
print("TakingOff")
drone(
    TakeOff()
    >> FlyingStateChanged(state="hovering", _timeout=5)
).wait()

# Move the drone by 01m in x direction then 1m in y-direction then change heading angle by 90 degree
# We use FlyingStateChanged to wait for drone to hover after each moveBy command
# the command has the following signature: moveBy(dX, dY, dZ, dPsi,..). dX,Dy and dZ are displacements in meter. dPsi is heading in radian.
print("Moving in x-direction by 1m")
drone(
    moveBy(1, 0, 0, 0)
    >> FlyingStateChanged(state="hovering", _timeout=5)
).wait()

print("Moving in y-direction by 1m")
drone(
    moveBy(0, 1, 0, 0)
    >> FlyingStateChanged(state="hovering", _timeout=5)
).wait()

print("Rotate heading by 90 degrees (1.571 radian)")
drone(
    moveBy(0, 0, 0, 1.571)
    >> FlyingStateChanged(state="hovering", _timeout=5)
).wait()

print("Landing")
drone(
    Landing()
    >> FlyingStateChanged(state="landing", _timeout=5)
).wait()

drone.disconnection() # disconnect from the drone
