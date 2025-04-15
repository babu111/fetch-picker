#! /usr/bin/env python                                                                                 
                                                                                                       
import robot_api                                                                                       
from joint_state_reader import JointStateReader
import rospy                  
                              
                       
def wait_for_time():   
    """Wait for simulated time to begin.
    """                
    while rospy.Time().now().to_sec() == 0:                                                            
        pass                                                                                           
                                                                                                       
                                                                                                       
def main():                                                                                            
    rospy.init_node('joint_reader_demo')                                                               
    wait_for_time()                                                                                    
    argv = rospy.myargv()                                                                              
    reader = JointStateReader()
    rospy.sleep(0.5)
    # Fetch Only
    names = robot_api.ArmJoints.names()
    print(names)
    # Kuri: Browse joints and initialize your own names list
    # names = []
    arm_vals = reader.get_joints(names)
    for k, v in zip(names, arm_vals):
        print('{}\t{}'.format(k, v))

    name = 'l_gripper_finger_joint'
    print('{}\t{}'.format(name, reader.get_joint(name)))
    name = 'torso_lift_joint'
    print('{}\t{}'.format(name, reader.get_joint(name)))
                      
if __name__ == '__main__':
    main()