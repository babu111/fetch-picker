#!/usr/bin/env python

import rospy
import json
import tf2_ros
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander, RobotCommander, roscpp_initialize
from robot_pbd.action_format import PoseStep
from robot_pbd.tf_utils import transform_pose

class PbDRecorder:
    def __init__(self):
        roscpp_initialize([])
        self.arm = MoveGroupCommander("arm")
        self.poses = []
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

    def record_pose(self, relative_to="base_link", gripper_open=True):
        pose = self.arm.get_current_pose()
        transformed = transform_pose(pose, self.tf_buffer, relative_to)
        step = PoseStep(transformed, relative_to, gripper_open)
        self.poses.append(step)
        print(f"✅ Recorded pose relative to {relative_to}, gripper: {'open' if gripper_open else 'closed'}")

    def save_program(self, filename):
        action = [step.to_dict() for step in self.poses]
        with open(filename, 'w') as f:
            json.dump(action, f, indent=2)
        print(f"💾 Saved program to {filename}")

if __name__ == '__main__':
    rospy.init_node("pbd_interface")
    recorder = PbDRecorder()

    # Demo loop
    while not rospy.is_shutdown():
        cmd = input("Command (save_pose/save_program): ")
        if cmd.startswith("save_pose"):
            _, frame, gripper = cmd.split()
            recorder.record_pose(relative_to=frame, gripper_open=(gripper == "open"))
        elif cmd.startswith("save_program"):
            _, name = cmd.split()
            recorder.save_program(f"src/fetch-picker/robot_pbd/config/actions/{name}.json")


# save_pose ar_marker_1 open
# save_pose ar_marker_1 close
# save_pose base_link open
# save_program pick_place
