# action_format.py

from geometry_msgs.msg import PoseStamped, Pose
import rospy

class PoseStep:
    def __init__(self, pose_stamped, relative_to, gripper_open):
        self.pose = pose_stamped  # geometry_msgs/PoseStamped
        self.relative_to = relative_to  # 'base_link' or 'ar_marker_1'
        self.gripper_open = gripper_open

    def to_dict(self):
        return {
            "pose": {
                "position": {
                    "x": self.pose.pose.position.x,
                    "y": self.pose.pose.position.y,
                    "z": self.pose.pose.position.z
                },
                "orientation": {
                    "x": self.pose.pose.orientation.x,
                    "y": self.pose.pose.orientation.y,
                    "z": self.pose.pose.orientation.z,
                    "w": self.pose.pose.orientation.w
                }
            },
            "frame_id": self.pose.header.frame_id,
            "relative_to": self.relative_to,
            "gripper_open": self.gripper_open
        }

    @staticmethod
    def from_dict(d):
        pose = PoseStamped()
        pose.header.frame_id = d["frame_id"]
        pose.pose.position.x = d["pose"]["position"]["x"]
        pose.pose.position.y = d["pose"]["position"]["y"]
        pose.pose.position.z = d["pose"]["position"]["z"]
        pose.pose.orientation.x = d["pose"]["orientation"]["x"]
        pose.pose.orientation.y = d["pose"]["orientation"]["y"]
        pose.pose.orientation.z = d["pose"]["orientation"]["z"]
        pose.pose.orientation.w = d["pose"]["orientation"]["w"]
        return PoseStep(pose, d["relative_to"], d["gripper_open"])
