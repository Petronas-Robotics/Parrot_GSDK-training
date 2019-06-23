# PETRONAS Technology Challange 6
# Written by: Tareq ALqutami (tareqazizhasan.al-q@petronas.com),  June 2019
# This code is provided as is and we are not liable for any consequential damages from using it.
# Use this code at your own risk.

# This code shows how to pilot the drone using PCMD
# If you are testing this with physcial drone, please ensure you have big enough free space.

import olympe
import olympe_deps as od
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged, PositionChanged, SpeedChanged
from olympe.messages.skyctrl.CoPiloting import setPilotingSource
import time


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

print("Taking off")
drone(
    TakeOff()
    >> FlyingStateChanged(state="hovering", _timeout=5)
).wait()


print("Start piloting")
status = drone.start_piloting()
if not status.OK:
    print("not successful")

# roll by 10 degrees for 5 seconds
drone.piloting_pcmd(10, 0, 0, 0, 5) # (roll, pitch, yaw, gaz, piloting_time)
time.sleep(5)
# pitch by 20 degrees for 5 seconds
drone.piloting_pcmd(0, 20, 0, 0, 5) # (roll, pitch, yaw, gaz, piloting_time)
time.sleep(5)
# yaw by 40 degrees and gaz by 20 for 5 seconds
for i in range(30):
  drone.piloting_pcmd(0, 0, 40, 20, 0.0) # (roll, pitch, yaw, gaz, piloting_time)
  time.sleep(0.1)

# reset all to zero
drone.piloting_pcmd(0, 0, 0, 0, 0.0) # (roll, pitch, yaw, gaz, piloting_time)
time.sleep(1)

print("Landing")
drone(
    Landing()
    >> FlyingStateChanged(state="landing", _timeout=5)
).wait()

drone.disconnection() # disconnect from the drone
