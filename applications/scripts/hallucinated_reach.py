#!/usr/bin/env python

import rospy
from visualization_msgs.msg import MarkerArray
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import PoseStamped
import tf.transformations as tft
import robot_api


def wait_for_time():
    """Wait for simulated time to begin."""
    while rospy.Time().now().to_sec() == 0:
        pass


class ArTagReader(object):
    def __init__(self):
        self.markers = []
        self.sub = rospy.Subscriber('/ar_pose_marker', AlvarMarkers, self.callback)

    def callback(self, msg):
        self.markers = msg.markers


def make_pose_stamped(marker, z_offset=0.1):
    """Convert AR marker pose into a PoseStamped for wrist_roll_link."""
    pose = PoseStamped()
    pose.header = marker.header
    pose.header.stamp = rospy.Time.now()
    pose.pose.position.x = marker.pose.pose.position.x
    pose.pose.position.y = marker.pose.pose.position.y
    pose.pose.position.z = marker.pose.pose.position.z + z_offset  # raise above marker

    # Use identity orientation (no rotation)
    quat = tft.quaternion_from_euler(0, 0, 0)
    pose.pose.orientation.x = quat[0]
    pose.pose.orientation.y = quat[1]
    pose.pose.orientation.z = quat[2]
    pose.pose.orientation.w = quat[3]

    return pose


def main():
    rospy.init_node('hallucinated_reach')
    wait_for_time()

    torso = robot_api.Torso()
    torso.set_height(0.4)  # Fully raised
    rospy.sleep(1.0)

    arm = robot_api.Arm()

    reader = ArTagReader()
    rospy.loginfo("Waiting for AR tag markers...")
    while len(reader.markers) == 0 and not rospy.is_shutdown():
        rospy.sleep(0.1)

    rospy.loginfo("Found {} markers.".format(len(reader.markers)))

    for marker in reader.markers:
        target_pose = make_pose_stamped(marker)

        rospy.loginfo("Trying to move to marker ID: {}".format(marker.id))
        error = arm.move_to_pose(target_pose)
        if error is None:
            rospy.loginfo("✅ Successfully moved to marker ID {}".format(marker.id))
            return
        else:
            rospy.logwarn("❌ Failed to move to marker ID {}".format(marker.id))

    rospy.logerr("⚠️ Failed to move to any markers!")


if __name__ == '__main__':
    main()
