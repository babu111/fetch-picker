#!/usr/bin/env python

import rospy
import math
from visualization_msgs.msg import InteractiveMarker, InteractiveMarkerControl, Marker
from interactive_markers.interactive_marker_server import InteractiveMarkerServer
from geometry_msgs.msg import Point
import robot_api


class MarkerController:
    def __init__(self):
        self.server = InteractiveMarkerServer("base_marker_server")
        self.base = robot_api.Base()

        self.create_marker("forward", Point(0.5, 0, 0), self.move_forward, direction="x")
        self.create_marker("backward", Point(-0.5, 0, 0), self.move_backward, direction="x", reverse=True)
        self.create_marker("left", Point(0, 0.5, 0), self.turn_left, direction="y")
        self.create_marker("right", Point(0, -0.5, 0), self.turn_right, direction="y", reverse=True)

        self.server.applyChanges()

    def create_marker(self, name, position, callback, direction="x", reverse=False):
        int_marker = InteractiveMarker()
        int_marker.header.frame_id = "base_link"
        int_marker.name = name
        int_marker.description = name
        int_marker.pose.position = position
        int_marker.scale = 0.3

        # Create a visible arrow marker
        arrow_marker = Marker()
        arrow_marker.type = Marker.ARROW
        arrow_marker.scale.x = 0.3
        arrow_marker.scale.y = 0.05
        arrow_marker.scale.z = 0.05
        arrow_marker.color.r = 0.0
        arrow_marker.color.g = 1.0
        arrow_marker.color.b = 0.0
        arrow_marker.color.a = 1.0

        if direction == "x":
            arrow_marker.points = [Point(0, 0, 0), Point(-0.3 if reverse else 0.3, 0, 0)]
        elif direction == "y":
            arrow_marker.points = [Point(0, 0, 0), Point(0, -0.3 if reverse else 0.3, 0)]

        control = InteractiveMarkerControl()
        control.always_visible = True
        control.interaction_mode = InteractiveMarkerControl.BUTTON
        control.markers.append(arrow_marker)
        int_marker.controls.append(control)

        self.server.insert(int_marker, lambda feedback: callback())

    def move_forward(self):
        rospy.loginfo("Moving forward...")
        self.base.go_forward(0.5)

    def move_backward(self):
        rospy.loginfo("Moving backward...")
        self.base.go_forward(-0.5)

    def turn_left(self):
        rospy.loginfo("Turning left...")
        self.base.turn(math.radians(30))

    def turn_right(self):
        rospy.loginfo("Turning right...")
        self.base.turn(math.radians(-30))


if __name__ == "__main__":
    rospy.init_node("marker_controller")
    MarkerController()
    rospy.spin()
