# Fetch Picker

This repositiory involves starter code and samples for two classes at the University of Washington, Spring 2022, that aim to program the Fetch mobile manipulator to pick requested items from densely packed shelves.

* [CSE 481 C: Robotics Capstone](https://sites.google.com/cs.washington.edu/cse481csp22/home)
* [TECHIN 517: Robotics Lab II](https://sites.google.com/cs.washington.edu/techin517sp22/home)

Labs and other documentation are on the **[wiki](https://github.com/robotic-picker-sp22/fetch-picker/wiki)**.


### Lab 25
The commands for configuring lab 25 environment is in

```
lab25.sh
```


### lab 26
Lab 26 may be a bit difficult to implement. The code is in

```
applications/scripts/lab26_teleop.py
```
After configuring the correct environment for IKFast, applications, etc, you will be able to run the teleop code with the following command. Start each command in a new terminal.
```
roscore
```
```
roslaunch fetch_gazebo playground.launch
```
```
roslaunch robot_api move_group.launch
```
```
rosrun rviz rviz -d rviz_config/lab26.rviz
```
```
rosrun applications lab26_teleop.py
```
