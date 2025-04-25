#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Pose, Point, Quaternion, PoseStamped
import robot_api

def main():
    rospy.init_node('cart_arm_demo')

    arm = robot_api.Arm()

    def shutdown():
        rospy.loginfo("Shutting down: canceling all goals...")
        arm.cancel_all_goals()

    rospy.on_shutdown(shutdown)

    # Define two gripper poses
    pose1 = Pose(
        position=Point(0.042, 0.384, 1.826),
        orientation=Quaternion(0.173, -0.693, -0.242, 0.657)
    )
    pose2 = Pose(
        position=Point(0.047, 0.545, 1.822),
        orientation=Quaternion(-0.274, -0.701, 0.173, 0.635)
    )

    ps1 = PoseStamped()
    ps1.header.frame_id = 'base_link'
    ps1.pose = pose1

    ps2 = PoseStamped()
    ps2.header.frame_id = 'base_link'
    ps2.pose = pose2

    gripper_poses = [ps1, ps2]

    # Give torso time to lift before starting if needed
    rospy.sleep(2.0)

    idx = 0
    while not rospy.is_shutdown():
        pose = gripper_poses[idx]
        rospy.loginfo(f"Moving to pose {idx + 1}")

        error = arm.move_to_pose(pose)
        if error is not None:
            rospy.logerr(f"Failed to move to pose {idx + 1}: {error}")

        # Alternate between pose1 and pose2
        idx = (idx + 1) % len(gripper_poses)

        # Sleep to allow the robot to settle before next move
        rospy.sleep(1.0)

if __name__ == '__main__':
    main()
