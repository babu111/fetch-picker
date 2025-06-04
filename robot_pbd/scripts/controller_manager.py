#!/usr/bin/env python

import rospy
import actionlib
from robot_controllers_msgs.msg import QueryControllerStatesAction, QueryControllerStatesGoal, ControllerState

class ControllerManager:
    def __init__(self):
        self.client = actionlib.SimpleActionClient("/query_controller_states", QueryControllerStatesAction)
        self.client.wait_for_server()

    def set_state(self, state):
        goal = QueryControllerStatesGoal()
        arm_state = ControllerState()
        arm_state.name = "arm_controller/follow_joint_trajectory"
        arm_state.state = state
        goal.updates.append(arm_state)
        self.client.send_goal(goal)
        self.client.wait_for_result()
