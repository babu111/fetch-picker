import rospy
import tf2_geometry_msgs
from tf2_ros import Buffer

def transform_pose(pose, tf_buffer: Buffer, target_frame: str):
    pose.header.stamp = rospy.Time(0)
    pose.header.frame_id = pose.header.frame_id or "base_link"
    try:
        transformed = tf_buffer.transform(pose, target_frame, rospy.Duration(1.0))
        return transformed
    except Exception as e:
        rospy.logerr(f"Failed to transform pose: {e}")
        return None
