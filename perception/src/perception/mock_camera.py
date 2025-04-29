import rosbag
import rospy
from sensor_msgs.msg import PointCloud2
import os

class MockCamera(object):
    """A MockCamera reads saved point clouds."""

    def __init__(self):
        pass

    def read_cloud(self, path):
        """Returns the sensor_msgs/PointCloud2 in the given bag file.

        Args:
            path: string, the path to a bag file with a single
            sensor_msgs/PointCloud2 in it.

        Returns:
            A sensor_msgs/PointCloud2 message, or None if there were no
            PointCloud2 messages in the bag file.
        """
        # Expand ~ to home directory if needed
        path = os.path.expanduser(path)

        try:
            bag = rosbag.Bag(path, 'r')
            for topic, msg, t in bag.read_messages():
                if isinstance(msg, PointCloud2):
                    bag.close()
                    return msg
            bag.close()
        except Exception as e:
            rospy.logerr(f"Failed to read bag file {path}: {e}")

        return None

if __name__ == '__main__':
    rospy.init_node('mock_camera_test')
    camera = MockCamera()
    cloud = camera.read_cloud('~/data/shelf.bag')
    if cloud is not None:
        rospy.loginfo("Successfully read point cloud from bag.")
    else:
        rospy.logwarn("No point cloud found in bag.")