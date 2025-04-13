import actionlib
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
import rospy

from .arm_joints import ArmJoints


class Arm(object):
    """Arm controls the robot's arm.

    Joint space control:
        joints = ArmJoints()
        # Fill out joint states
        arm = robot_api.Arm()
        arm.move_to_joints(joints)
    """

    def __init__(self):
        # Create actionlib client
        # Wait for server
        self.client = actionlib.SimpleActionClient(
            '/arm_controller/follow_joint_trajectory',
            FollowJointTrajectoryAction
        )
        rospy.loginfo('Waiting for arm controller...')
        self.client.wait_for_server()
        rospy.loginfo('...connected to arm controller!')


    def move_to_joints(self, arm_joints):
        """Moves the robot's arm to the given joints.

        Args:
            arm_joints: An ArmJoints object that specifies the joint values for
                the arm.
        """
        # Create a trajectory point
        # Set position of trajectory point
        # Set time of trajectory point

        # Create goal
        # Add joint name to list
        # Add the trajectory point created above to trajectory

        # Send goal
        # Wait for result
        point = JointTrajectoryPoint()
        point.positions = arm_joints.values()
        point.time_from_start = rospy.Duration(5.0)  # 5 seconds

        # Create goal
        goal = FollowJointTrajectoryGoal()
        goal.trajectory.joint_names = ArmJoints.names()
        goal.trajectory.points.append(point)

        # Required header stamp
        goal.trajectory.header.stamp = rospy.Time.now() + rospy.Duration(0.1)

        # Send goal
        self.client.send_goal(goal)
        self.client.wait_for_result()
