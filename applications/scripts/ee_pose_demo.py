#!/usr/bin/env python

import rospy
import tf

def main():
    rospy.init_node('ee_pose_demo')
    
    listener = tf.TransformListener()
    rospy.sleep(0.5)  # Sleep to allow the listener to fill its buffer

    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        try:
            # Get the latest transform from base_link to gripper_link
            (trans, rot) = listener.lookupTransform('base_link', 'gripper_link', rospy.Time(0))
            rospy.loginfo("Position: %s", trans)
            rospy.loginfo("Orientation (quaternion): %s", rot)

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
            rospy.logwarn(e)

        rate.sleep()

if __name__ == '__main__':
    main()
