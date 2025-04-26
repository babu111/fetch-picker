#!/usr/bin/env python3

import rospy
import copy
import tf.transformations as tft
from visualization_msgs.msg import InteractiveMarker, InteractiveMarkerControl, Marker, MenuEntry
from interactive_markers.interactive_marker_server import InteractiveMarkerServer
from geometry_msgs.msg import PoseStamped, Quaternion
from interactive_markers.menu_handler import MenuHandler
import moveit_commander
import moveit_msgs.msg
import numpy as np

import robot_api  # Assuming you have your arm and gripper wrapper classes from previous labs

GRIPPER_MESH = 'package://fetch_description/meshes/gripper_link.dae'
L_FINGER_MESH = 'package://fetch_description/meshes/l_gripper_finger_link.STL'
R_FINGER_MESH = 'package://fetch_description/meshes/r_gripper_finger_link.STL'


def make_6dof_controls():
    controls = []
    axis = ['x', 'y', 'z']
    for ax in axis:
        control_move = InteractiveMarkerControl()
        control_move.name = f"move_{ax}"
        control_move.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
        control_move.orientation = axis_to_quaternion(ax)
        control_move.always_visible = True
        controls.append(control_move)

        control_rotate = InteractiveMarkerControl()
        control_rotate.name = f"rotate_{ax}"
        control_rotate.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
        control_rotate.orientation = axis_to_quaternion(ax)
        control_rotate.always_visible = True
        controls.append(control_rotate)
    return controls

def axis_to_quaternion(axis):
    if axis == 'x':
        q = tft.quaternion_about_axis(np.pi/2, (1, 0, 0))
    elif axis == 'y':
        q = tft.quaternion_about_axis(np.pi/2, (0, 1, 0))
    elif axis == 'z':
        q = tft.quaternion_about_axis(np.pi/2, (0, 0, 1))
    else:
        q = [0, 0, 0, 1]
    quat = Quaternion()
    quat.x, quat.y, quat.z, quat.w = q
    return quat

def make_gripper_visualization():
    markers = []

    offset_x = 0.166

    gripper_marker = Marker()
    gripper_marker.type = Marker.MESH_RESOURCE
    gripper_marker.mesh_resource = GRIPPER_MESH
    gripper_marker.scale.x = gripper_marker.scale.y = gripper_marker.scale.z = 1.0
    gripper_marker.color.r = 0.0
    gripper_marker.color.g = 1.0
    gripper_marker.color.b = 0.0
    gripper_marker.color.a = 1.0
    gripper_marker.pose.position.x = offset_x
    markers.append(gripper_marker)

    left_finger = Marker()
    left_finger.type = Marker.MESH_RESOURCE
    left_finger.mesh_resource = L_FINGER_MESH
    left_finger.scale.x = left_finger.scale.y = left_finger.scale.z = 1.0
    left_finger.color.r = 0.0
    left_finger.color.g = 1.0
    left_finger.color.b = 0.0
    left_finger.color.a = 1.0
    left_finger.pose.position.x = offset_x
    left_finger.pose.position.y = -0.06  # small offset
    markers.append(left_finger)

    right_finger = Marker()
    right_finger.type = Marker.MESH_RESOURCE
    right_finger.mesh_resource = R_FINGER_MESH
    right_finger.scale.x = right_finger.scale.y = right_finger.scale.z = 1.0
    right_finger.color.r = 0.0
    right_finger.color.g = 1.0
    right_finger.color.b = 0.0
    right_finger.color.a = 1.0
    right_finger.pose.position.x = offset_x
    right_finger.pose.position.y = 0.06  # small offset
    markers.append(right_finger)

    return markers


class GripperTeleop(object):
    def __init__(self, arm, gripper, im_server):
        self._arm = arm
        self._gripper = gripper
        self._im_server = im_server
        self._menu_handler = MenuHandler()
        self._current_marker_name = 'gripper_marker'

    def start(self):
        gripper_marker = self.make_gripper_marker()
        self._im_server.insert(gripper_marker, feedback_cb=self.handle_feedback)
        # Add menu entries
        self._menu_handler.insert('Go to Pose', callback=self.handle_feedback)
        self._menu_handler.insert('Open Gripper', callback=self.handle_feedback)
        self._menu_handler.insert('Close Gripper', callback=self.handle_feedback)
        self._menu_handler.apply(self._im_server, self._current_marker_name)
        self._im_server.applyChanges()

    def make_gripper_marker(self):
        im = InteractiveMarker()
        im.header.frame_id = 'base_link'
        im.name = self._current_marker_name
        im.description = "Gripper Teleop"
        im.scale = 0.25

        # Initial pose
        im.pose.position.x = -0.166
        im.pose.position.y = 0
        im.pose.position.z = 0
        im.pose.orientation.w = 1

        # Add gripper visual mesh
        control = InteractiveMarkerControl()
        control.always_visible = True
        control.interaction_mode = InteractiveMarkerControl.MENU
        control.markers.extend(make_gripper_visualization())

        im.controls.append(control)

        # visual_control = InteractiveMarkerControl()
        # visual_control.always_visible = True
        # visual_control.interaction_mode = InteractiveMarkerControl.NONE
        # visual_control.markers.extend(make_gripper_visualization())
        # im.controls.append(visual_control)

        # Add 6DOF controls
        controls = make_6dof_controls()
        im.controls.extend(controls)
 
        return im

    def handle_feedback(self, feedback):
        # print(feedback)
        if feedback.event_type == feedback.MENU_SELECT:
            if feedback.menu_entry_id == 1:
                rospy.loginfo("Go to pose requested.")
                marker = self._im_server.get(self._current_marker_name)
                current_pose = marker.pose
                # rospy.loginfo("Moving to pose:", current_pose)
                pose = PoseStamped()
                pose.header.frame_id = 'base_link'
                pose.pose = current_pose
                self._arm.move_to_pose(pose)
            elif feedback.menu_entry_id == 2:
                rospy.loginfo("Open gripper requested.")
                self._gripper.open()
            elif feedback.menu_entry_id == 3:
                rospy.loginfo("Close gripper requested.")
                self._gripper.close()

        elif feedback.event_type == feedback.POSE_UPDATE:
            rospy.loginfo("Pose updated, checking IK...")
            pose = PoseStamped()
            pose.header.frame_id = 'base_link'
            pose.pose = feedback.pose
            reachable = self._arm.check_pose(pose)
            print("Pose reachable:", reachable)
            self.update_color(reachable)

    def update_color(self, reachable):
        gripper_marker = self.make_gripper_marker()
        for m in gripper_marker.controls[0].markers:
            if reachable:
                m.color.r, m.color.g, m.color.b = 0.0, 1.0, 0.0  # green
            else:
                m.color.r, m.color.g, m.color.b = 1.0, 0.0, 0.0  # red
            m.color.a = 1.0
        self._im_server.insert(gripper_marker, feedback_cb=self.handle_feedback)
        self._im_server.applyChanges()

class AutoPickTeleop(object):
    def __init__(self, arm, gripper, im_server):
        self._arm = arm
        self._gripper = gripper
        self._im_server = im_server
        self._current_marker_name = 'target_marker'

    def start(self):
        obj_marker = self.make_target_marker()
        self._im_server.insert(obj_marker, feedback_cb=self.handle_feedback)
        self._im_server.applyChanges()

    def make_target_marker(self):
        im = InteractiveMarker()
        im.header.frame_id = 'base_link'
        im.name = self._current_marker_name
        im.description = "Target Teleop"
        im.scale = 0.25
        im.pose.position.x = 0.7
        im.pose.position.z = 0.75
        im.pose.orientation.w = 1

        # Simple object marker
        control = InteractiveMarkerControl()
        control.always_visible = True
        box = Marker()
        box.type = Marker.CUBE
        box.scale.x = 0.05
        box.scale.y = 0.05
        box.scale.z = 0.05
        box.color.r = 0.0
        box.color.g = 0.0
        box.color.b = 1.0
        box.color.a = 1.0
        control.markers.append(box)
        control.markers.extend(make_gripper_visualization())

        im.controls.append(control)

        # Add 6DOF controls
        controls = make_6dof_controls()
        im.controls.extend(controls)

        return im

    def handle_feedback(self, feedback):
        if feedback.event_type == feedback.POSE_UPDATE:
            rospy.loginfo("Object moved! Update pre-grasp, grasp, lift poses here.")

def main():
    rospy.init_node('lab26_teleop')

    arm = robot_api.Arm()
    gripper = robot_api.Gripper()

    im_server = InteractiveMarkerServer('gripper_im_server', q_size=2)
    auto_pick_im_server = InteractiveMarkerServer('auto_pick_im_server', q_size=2)

    teleop = GripperTeleop(arm, gripper, im_server)
    auto_pick = AutoPickTeleop(arm, gripper, auto_pick_im_server)

    teleop.start()
    auto_pick.start()

    rospy.spin()

if __name__ == '__main__':
    main()
