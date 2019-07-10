# Parrot_GSDK-training
Training material and code for Parrot Ground SDK (Olympe). This is part of PETRONAS technology challenge 6.

Read the Powerpoint slides for general understaing of the SDK and basics of Olympe.
You can run the code examples either in simulation (Sphinx) or with physical drone.
These codes are provided as is and we are not liable for any consequential damages from using it. Use the code at your own risk.

The codes have been tested using Simulated and actual Anafi 4K drone with GSDK version 1.0.



## How to load the obstacle course models into your Sphinx / Gazebo:

 1. Copy all the **contents** of folder `sim_models`.
 2. Find and go into the folder `.gazebo` in your Home folder.  
	 a. This is a hidden folder, so if you cannot see it, go to your Home folder, and press `Ctrl + H`.  
	 b. If there is no such folder, just create one (right click > New Folder)  
 3. Go into the models folder; `/home/user/.gazebo/models`   
 4. Paste the folders copied from Step 1.   
 
 

## How to load obstacle course world:

 1. The basic command to load a custom world together with a drone is  
	 > $ sphinx <path/to/my.world> <path/to/my.drone>
 2. So if you are using the default drone configuration;
	 > $ sphinx sim_world/tc6.world /opt/parrot-sphinx/usr/share/sphinx/drones/anafi4k.drone::stolen_interface=::simple_front_cam=true



	 
