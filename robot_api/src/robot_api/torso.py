#!/usr/bin/env python

import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectoryPoint

ACTION_NAME = '/torso_controller/follow_joint_trajectory'
JOINT_NAME = 'torso_lift_joint'
TIME_FROM_START = 5  # How many seconds it should take to set the torso height.


class Torso(object):
    """Torso controls the robot's torso height.
    """
    MIN_HEIGHT = 0.0
    MAX_HEIGHT = 0.4

    def __init__(self):
        # Create actionlib client
        # Wait for server
        self.client = actionlib.SimpleActionClient(ACTION_NAME, FollowJointTrajectoryAction)
        rospy.loginfo("Waiting for torso action server...")
        self.client.wait_for_server()
        rospy.loginfo("Connected to torso action server.")

    def set_height(self, height):
        """Sets the torso height.

        This will always take ~5 seconds to execute.

        Args:
            height: The height, in meters, to set the torso to. Values range
                from Torso.MIN_HEIGHT (0.0) to Torso.MAX_HEIGHT(0.4).
        """
        # Check that the height is between MIN_HEIGHT and MAX_HEIGHT.
        # Create a trajectory point
        # Set position of trajectory point
        # Set time of trajectory point

        # Create goal
        # Add joint name to list
        # Add the trajectory point created above to trajectory

        # Send goal
        # Wait for result
        if not (self.MIN_HEIGHT <= height <= self.MAX_HEIGHT):
            rospy.logwarn("Requested height %.2f out of range [%.2f, %.2f]" %
                          (height, self.MIN_HEIGHT, self.MAX_HEIGHT))
            return

        # Create trajectory point
        point = JointTrajectoryPoint()
        point.positions = [height]
        point.time_from_start = rospy.Duration(TIME_FROM_START)

        # Create goal
        goal = FollowJointTrajectoryGoal()
        goal.trajectory.joint_names = [JOINT_NAME]
        goal.trajectory.points = [point]

        # Send goal
        self.client.send_goal(goal)
        self.client.wait_for_result()
