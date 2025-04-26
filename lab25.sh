ZEYI_PATH=/fetch_ws/src/fetch-picker

mkdir ~/local
cd ~/local
git clone git@github.com:fetchrobotics/fetch_ros.git
cp -r fetch_ros/fetch_ikfast_plugin /fetch_ws/src/fetch-picker/
cd /fetch_ws/src/fetch-picker/
catkin build fetch_ikfast_plugin


source ~/.bashrc
mkdir $ZEYI_PATH/robot_api/launch
mkdir $ZEYI_PATH/robot_api/config
cd $ZEYI_PATH/robot_api
roscp fetch_moveit_config move_group.launch launch
roscp fetch_moveit_config planning_context.launch launch
roscp fetch_moveit_config kinematics.yaml config



# GIT_SSH_COMMAND='ssh -i ~/.ssh/id_fetch' git push origin
# rosrun rviz rviz -d /path/to/your_config.rviz
