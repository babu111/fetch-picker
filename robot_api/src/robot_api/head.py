import actionlib
import math
import rospy
import control_msgs.msg
import trajectory_msgs.msg
from geometry_msgs.msg import PointStamped
from control_msgs.msg import PointHeadAction, PointHeadGoal


LOOK_AT_ACTION_NAME = '/head_controller/point_head'
PAN_TILT_ACTION_NAME = '/head_controller/follow_joint_trajectory'
PAN_JOINT = 'head_pan_joint'
TILT_JOINT = 'head_tilt_joint'
PAN_TILT_TIME = 2.5  # seconds

class Head(object):
    MIN_PAN = -1.57  # -90 degrees
    MAX_PAN = 1.57   # +90 degrees
    MIN_TILT = -0.76
    MAX_TILT = 1.45

    def __init__(self):
        self._pan_tilt_client = actionlib.SimpleActionClient(PAN_TILT_ACTION_NAME,
                                                              control_msgs.msg.FollowJointTrajectoryAction)
        self._look_at_client = actionlib.SimpleActionClient(LOOK_AT_ACTION_NAME,
                                                             PointHeadAction)

        rospy.loginfo("Waiting for head action servers...")
        self._pan_tilt_client.wait_for_server()
        self._look_at_client.wait_for_server()
        rospy.loginfo("Head action servers ready!")

    def look_at(self, frame_id, x, y, z):
        goal = PointHeadGoal()
        goal.target = PointStamped()
        goal.target.header.stamp = rospy.Time.now()
        goal.target.header.frame_id = frame_id
        goal.target.point.x = x
        goal.target.point.y = y
        goal.target.point.z = z
        goal.min_duration = rospy.Duration(1.0)

        self._look_at_client.send_goal(goal)
        self._look_at_client.wait_for_result()

    def pan_tilt(self, pan, tilt):
        if not (self.MIN_PAN <= pan <= self.MAX_PAN):
            rospy.logerr("Pan angle out of bounds")
            return
        if not (self.MIN_TILT <= tilt <= self.MAX_TILT):
            rospy.logerr("Tilt angle out of bounds")
            return

        goal = control_msgs.msg.FollowJointTrajectoryGoal()
        goal.trajectory.joint_names = [PAN_JOINT, TILT_JOINT]

        point = trajectory_msgs.msg.JointTrajectoryPoint()
        point.positions = [pan, tilt]
        point.time_from_start = rospy.Duration(PAN_TILT_TIME)

        goal.trajectory.points.append(point)
        goal.trajectory.header.stamp = rospy.Time.now()

        self._pan_tilt_client.send_goal(goal)
        self._pan_tilt_client.wait_for_result()
