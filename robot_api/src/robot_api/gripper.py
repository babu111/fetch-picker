#! /usr/bin/env python

# import ?????????
# import ???????_msgs.msg
import rospy
import control_msgs.msg
import actionlib
from control_msgs.msg import GripperCommandAction, GripperCommandGoal

ACTION_NAME = '/gripper_controller/gripper_action'
CLOSED_POS = 0.0  # The position for a fully-closed gripper (meters).
OPENED_POS = 0.10  # The position for a fully-open gripper (meters).


class Gripper(object):
    """Gripper controls the robot's gripper.
    """
    MIN_EFFORT = 35  # Min grasp force, in Newtons
    MAX_EFFORT = 100  # Max grasp force, in Newtons

    def __init__(self):
        # Create actionlib client
        # Wait for server
        self._client = actionlib.SimpleActionClient(ACTION_NAME, GripperCommandAction)
        rospy.loginfo("Waiting for gripper action server...")
        self._client.wait_for_server()
        rospy.loginfo("Gripper action server available.")

    def open(self):
        """Opens the gripper.
        """
        # Create goal
        # Send goal
        # Wait for result
        goal = GripperCommandGoal()
        goal.command.position = OPENED_POS
        goal.command.max_effort = self.MAX_EFFORT  # Can still apply effort to stay open
        self._client.send_goal(goal)
        self._client.wait_for_result()

    def close(self, max_effort=MAX_EFFORT):
        """Closes the gripper.

        Args:
            max_effort: The maximum effort, in Newtons, to use. Note that this
                should not be less than 35N, or else the gripper may not close.
        """
        # Create goal
        # Send goal
        # Wait for result
        goal = GripperCommandGoal()
        goal.command.position = CLOSED_POS
        goal.command.max_effort = max_effort
        self._client.send_goal(goal)
        self._client.wait_for_result()