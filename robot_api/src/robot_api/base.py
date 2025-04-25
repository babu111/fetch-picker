#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import tf.transformations as tft
import copy
import math

class Base(object):
    """Base controls the mobile base portion of the Fetch robot.

    Sample usage:
        base = robot_api.Base()
        while CONDITION:
            base.move(0.2, 0)
        base.stop()
    """

    def __init__(self):
        # Create publisher
        self._pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self._odom_sub = rospy.Subscriber('odom', Odometry, callback=self._odom_callback)
        self._latest_odom = None

    def _odom_callback(self, msg):
        self._latest_odom = msg

    def get_yaw(self, odom_msg):
        orientation = odom_msg.pose.pose.orientation
        quat = [orientation.x, orientation.y, orientation.z, orientation.w]
        mat = tft.quaternion_matrix(quat)
        x_axis = mat[0, 0]
        y_axis = mat[1, 0]
        return math.atan2(y_axis, x_axis)

    def move(self, linear_speed, angular_speed):
        """Moves the base instantaneously at given linear and angular speeds.

        "Instantaneously" means that this method must be called continuously in
        a loop for the robot to move.

        Args:
            linear_speed: The forward/backward speed, in meters/second. A
                positive value means the robot should move forward.
            angular_speed: The rotation speed, in radians/second. A positive
                value means the robot should rotate clockwise.
        """
        # Create Twist msg
        # Fill out msg
        # Publish msg
        msg = Twist()
        msg.linear.x = linear_speed
        msg.angular.z = angular_speed
        self._pub.publish(msg)  

    def stop(self):
        """Stops the mobile base from moving.
        """
        # Publish 0 velocity
        msg = Twist()  # All fields are zero by default
        self._pub.publish(msg)


    def go_forward(self, distance, speed=0.1):
        while self._latest_odom is None:
            rospy.sleep(0.1)

        start = copy.deepcopy(self._latest_odom)
        start_pos = start.pose.pose.position

        def compute_distance():
            current = self._latest_odom.pose.pose.position
            dx = current.x - start_pos.x
            dy = current.y - start_pos.y
            return math.sqrt(dx ** 2 + dy ** 2)

        direction = -1 if distance < 0 else 1
        while compute_distance() < abs(distance):
            linear_speed = max(0.05, min(0.5, compute_distance()))
            self.move(direction * linear_speed, 0)

        self.move(0, 0)

    # distance given in degrees
    def turn(self, angular_distance, speed=0.5):
        while self._latest_odom is None:
            rospy.sleep(0.1)

        start_yaw = self.get_yaw(self._latest_odom)
        direction = -1 if angular_distance < 0 else 1
        angular_distance = abs(angular_distance) % (2 * math.pi)

        def compute_turned():
            current_yaw = self.get_yaw(self._latest_odom)
            delta = (current_yaw - start_yaw) % (2 * math.pi)
            return delta if direction > 0 else (start_yaw - current_yaw) % (2 * math.pi)

        while compute_turned() < angular_distance:
            angular_speed = max(0.25, min(1, angular_distance - compute_turned()))
            self.move(0, direction * angular_speed)

        self.move(0, 0)

