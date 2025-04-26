#! /usr/bin/env python3

from moveit_python import PlanningSceneInterface
import robot_api
import rospy
from moveit_msgs.msg import PlanningScene, ObjectColor
from std_msgs.msg import ColorRGBA



def wait_for_time():
    """Wait for simulated time to begin.
    """
    while rospy.Time().now().to_sec() == 0:
        pass


def print_usage():
    print('Usage: rosrun applications lab26_obstacles.py')
    print('Drive the robot until the PlanningScene lines up with the point cloud.')


def main():
    rospy.init_node('lab26_obstacles')
    wait_for_time()

    planning_scene = PlanningSceneInterface('base_link')
    planning_scene.clear()
    planning_scene.removeCollisionObject('table')
    planning_scene.removeCollisionObject('floor')
    planning_scene.addBox('floor', 2, 2, 0.01, 0, 0, 0.01/2)
    planning_scene.addBox('table', 0.5, 1, 0.72, 1, 0, 0.72/2)

    rospy.sleep(2)

    # Create a publisher to /planning_scene
    scene_pub = rospy.Publisher('/planning_scene', PlanningScene, queue_size=10)

    # Wait for publisher to be ready
    rospy.sleep(1)

    # Define grey color
    grey = ColorRGBA()
    grey.r = 0.5
    grey.g = 0.5
    grey.b = 0.5
    grey.a = 1.0  # fully opaque

    # Create ObjectColor messages
    floor_color = ObjectColor()
    floor_color.id = 'floor'
    floor_color.color = grey

    table_color = ObjectColor()
    table_color.id = 'table'
    table_color.color = grey

    # Create a PlanningScene message to apply colors
    planning_scene_msg = PlanningScene()
    planning_scene_msg.is_diff = True
    planning_scene_msg.object_colors.append(floor_color)
    planning_scene_msg.object_colors.append(table_color)

    # Publish the PlanningScene message
    scene_pub.publish(planning_scene_msg)

    rospy.sleep(1)


if __name__ == '__main__':
    main()