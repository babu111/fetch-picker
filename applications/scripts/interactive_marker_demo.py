#!/usr/bin/env python  
import rospy

from interactive_markers.interactive_marker_server import InteractiveMarkerServer
from visualization_msgs.msg import InteractiveMarker, InteractiveMarkerControl, InteractiveMarkerFeedback
from visualization_msgs.msg import Marker


def handle_viz_input(input):
    if input.event_type == InteractiveMarkerFeedback.BUTTON_CLICK:
        rospy.loginfo(f"{input.marker_name} was clicked.")
    else:
        rospy.loginfo("Unhandled event type: %d", input.event_type)


def main():
    rospy.init_node("interactive_marker_demo")

    # Create the server
    server = InteractiveMarkerServer("simple_marker")

    # Create the interactive marker
    int_marker = InteractiveMarker()
    int_marker.header.frame_id = "base_link"
    int_marker.name = "my_marker"
    int_marker.description = "Simple Click Control"
    int_marker.pose.position.x = 1.0
    int_marker.pose.orientation.w = 1.0

    # Create the visual marker (a teal cube)
    box_marker = Marker()
    box_marker.type = Marker.CUBE
    box_marker.pose.orientation.w = 1.0
    box_marker.scale.x = 0.45
    box_marker.scale.y = 0.45
    box_marker.scale.z = 0.45
    box_marker.color.r = 0.0
    box_marker.color.g = 0.5
    box_marker.color.b = 0.5
    box_marker.color.a = 1.0

    # Create an interactive marker control, attach the visual marker to it
    button_control = InteractiveMarkerControl()
    button_control.interaction_mode = InteractiveMarkerControl.BUTTON
    button_control.always_visible = True
    button_control.markers.append(box_marker)

    # Add the control to the interactive marker
    int_marker.controls.append(button_control)

    # Add the marker to the server and register the callback
    server.insert(int_marker, handle_viz_input)
    server.applyChanges()

    rospy.spin()


if __name__ == "__main__":
    main()
