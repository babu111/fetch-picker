#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from std_msgs.msg import Header, ColorRGBA

import math

class NavPathVisualizer(object):
    def __init__(self):
        self._path = []
        self._last_position = None
        self.publisher = rospy.Publisher('visualization_marker', Marker, queue_size=10)
        rospy.Subscriber('/odom', Odometry, self.callback)

    def distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def callback(self, msg):
        pos = msg.pose.pose.position
        if self._last_position is None or self.distance(pos, self._last_position) > 0.1:
            self._path.append(Point(pos.x, pos.y, pos.z))
            self._last_position = pos
            self.publish_path()

    def publish_path(self):
        marker = Marker()
        marker.header = Header(frame_id='odom')
        marker.type = Marker.LINE_STRIP
        marker.action = Marker.ADD
        marker.pose.orientation.w = 1.0
        marker.scale.x = 0.02
        marker.color = ColorRGBA(0.0, 0.0, 1.0, 1.0)  # Blue
        marker.points = self._path
        marker.id = 1
        marker.lifetime = rospy.Duration(0)  # Infinite
        self.publisher.publish(marker)

def main():
    rospy.init_node('path_marker')
    NavPathVisualizer()
    rospy.spin()

if __name__ == '__main__':
    main()
