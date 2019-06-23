# PETRONAS Technology Challange 6
# Written by: Tareq ALqutami (tareqazizhasan.al-q@petronas.com),  June 2019
# This code is provided as is and we are not liable for any consequential damages from using it.
# Use this code at your own risk.

# This code shows how to connect to a Simulated/actual Parrot Anafi drone, then takeoff and land after a few seconds.

import olympe
import olympe_deps as od
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
from olympe.messages.skyctrl.CoPiloting import setPilotingSource
import time

SIMULATION = True # choose wether to use simulated drone or physical one


if SIMULATION:
   # connect to simulated drone in SPHINX.
   drone = olympe.Drone("10.202.0.1") # create Drone instance
else:
   # connect to physical drone through the Sky Controller
   # you can also connect to drone using Wifi using ip address 192.168.42.1
   drone = olympe.Drone("192.168.53.1", mpp=True, drone_type=od.ARSDK_DEVICE_TYPE_ANAFI4K)

# connect to the drone and check if connection was established
response = drone.connection()
if not response.OK: # if connection failed, exit
   print("Connection was not successful")
   exit()

# set piloting source to controller, only when connecting through the Sky Controller
if not SIMULATION:
   drone(setPilotingSource(source="Controller")).wait()

print("TakingOff")
response = drone(TakeOff()).wait() # send takeoff command and wait for response or timeout
if not response.success(): # if takeoff command was not successful, exit
   print("Takeoff was not successful")
   exit()

time.sleep(5) # wait until drone is hovering (we will see how to use the SDK to do this more efficiently later)

print("Landing")
response = drone(Landing()).wait() # send landing command and wait for response or timeout
if not response.success(): # if landing command was not successful, exit
   print("Landing was not successful")
   exit()

# disconnect from the drone
drone.disconnection()
