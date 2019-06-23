# PETRONAS Technology Challange 6
# Written by: Tareq ALqutami (tareqazizhasan.al-q@petronas.com),  June 2019
# This code is provided as is and we are not liable for any consequential damages from using it.
# Use this code at your own risk.

# This code shows how to get different drone states

import olympe
import olympe_deps as od
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy
from olympe.messages.common.CommonState import BatteryStateChanged
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged, PositionChanged, SpeedChanged
from olympe.messages.skyctrl.CoPiloting import setPilotingSource
from olympe.enums.ardrone3.PilotingState import FlyingStateChanged_State
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

# check current FlyingState(hovering, takingoff, landed, flying, ..)
cur_fly_state = drone.get_state(FlyingStateChanged)['state']
print("Current flying state is: ",cur_fly_state)
if cur_fly_state != FlyingStateChanged_State.hovering or cur_fly_state != FlyingStateChanged_State.flying:  # if current state is not hovering nor flying, send takeoff command
   print("takeoff required")
   drone(
       TakeOff()
       >> FlyingStateChanged(state="hovering", _timeout=10)
   ).wait()
else:
   print("Drone is already hovering/flying.")

# check flying state again
cur_fly_state = drone.get_state(FlyingStateChanged)['state']
print("Current flying state is: ",cur_fly_state)

# check battery percentage
print("current battery percentage: ", drone.get_state(BatteryStateChanged)['percent'])

print("Moving in x-direction by 1m")
state = drone(moveBy(1, 0, 0, 0)) # don't wait. Send command and proceed
# wait until you get a PositionChanged event from drone
while not drone(PositionChanged()):
   pass

# Keep checking response state from moveBy until it's success.
while not state.success():
   # keep checking Global position (GPS) and speed.
   cur_pos = drone.get_state(PositionChanged)
   cur_speed = drone.get_state(SpeedChanged)
   print("current pos(gps): = ",cur_pos)
   print("current speed: = ",cur_speed)
   time.sleep(0.1)

print("Landing")
drone(
    Landing()
    >> FlyingStateChanged(state="landing", _timeout=5)
).wait()

drone.disconnection() # disconnect from the drone
