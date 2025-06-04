#!/usr/bin/env python

import rospy
import json
import tf2_ros
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander, RobotCommander, roscpp_initialize
from robot_api.gripper import Gripper
from robot_pbd.action_format import PoseStep
from robot_pbd.tf_utils import transform_pose

class PbDExecutor:
    def __init__(self):
        roscpp_initialize([])
        self.arm = MoveGroupCommander("arm")
        self.gripper = Gripper()
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

    def execute_program(self, filename):

        print("Replaying actions...")
        with open(filename) as f:
            steps = json.load(f)

        for step_dict in steps:
            step = PoseStep.from_dict(step_dict)
            transformed = transform_pose(step.pose, self.tf_buffer, "base_link")
            self.arm.set_pose_target(transformed)
            self.arm.go(wait=True)

            if step.gripper_open:
                self.gripper.open()
            else:
                self.gripper.close()
            rospy.sleep(1.0)

if __name__ == '__main__':
    rospy.init_node("pbd_executor")
    executor = PbDExecutor()
    executor.execute_program("src/fetch-picker/robot_pbd/config/actions/pick_place.json")
