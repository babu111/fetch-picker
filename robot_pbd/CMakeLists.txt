cmake_minimum_required(VERSION 3.0.2)
project(robot_pbd)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  geometry_msgs
  moveit_commander
  tf2_ros
  tf2_geometry_msgs
  actionlib
  robot_controllers_msgs
)

catkin_package()

catkin_install_python(PROGRAMS
  scripts/pbd_interface.py
  scripts/pbd_executor.py
  scripts/controller_manager.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch config
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(DIRECTORY src/robot_pbd
  DESTINATION ${CATKIN_PACKAGE_PYTHON_DESTINATION}
)

catkin_python_setup()