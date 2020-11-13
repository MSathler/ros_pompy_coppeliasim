# ros_pompy_coppeliasim

This is a package that adapts the pompy library to the ROS (kinetic) and Coppeliasim (4.1.0) simulator, including a Python script that simulates the gas sensor in Coppeliasim.

## Install Dependencies

- Pompy

        $ pip install pompy
 
- Numpy

        $ pip install numpy
        

        

## Ros_Pompy_CoppeliaSim

To run the Ros_Pompy_CoppeliaSim simulation, first, clone this repository and other packages needed in your workspace:

        $ git clone https://github.com/MSathler/coppelia_remote_pc.git
        $ git clone https://github.com/MSathler/ros_pompy_coppeliasim.git
        
- Coppelia_Remote_PC: To visualizate Point Clount into Coppeliasim install the following package and read the instructions in ```https://github.com/MSathler/coppelia_remote_pc.git``` : 


## How to run

      $ roscore
      $ coppelia

In Coppelia, open the sensor_scene.ttt and start the simulation.

Then:

      $ roslaunch ros_pompy_coppeliasim ros_pompy.launch
      $ rosrun coppeliasim_remote_pc pc_coppelia.py
      
      
![pompy](https://user-images.githubusercontent.com/51409770/99056417-0a5bf000-2579-11eb-9a98-98a2aac2451d.jpeg)
![rviz](https://user-images.githubusercontent.com/51409770/99056416-09c35980-2579-11eb-8083-e73a60de5a8e.jpeg)
![coppeliasim](https://user-images.githubusercontent.com/51409770/99056413-08922c80-2579-11eb-8e2b-b7fa872212be.jpeg)

### Sensor Reads

![simulated_sensor2](https://user-images.githubusercontent.com/51409770/99055027-36c33c80-2578-11eb-9c80-d96bbe043400.png)

