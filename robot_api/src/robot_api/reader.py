#!/usr/bin/env python                                                                                  



# this is for filing purposes only, the real file is in ~/catkin_ws/src/cse481c/joint_state_reader/src/joint_state_reader/reader.py

import rospy
from sensor_msgs.msg import JointState
from threading import Lock                                                                                    
                                                                                                       
class JointStateReader(object):                                                                        
    """Listens to /joint_states and provides the latest joint angles.                                  
                                                                                                       
    Usage:                                                                                             
        joint_reader = JointStateReader()                                                              
        rospy.sleep(0.1)                                                                               
        joint_reader.get_joint('shoulder_pan_joint')                                                   
        joint_reader.get_joints(['shoulder_pan_joint', 'shoulder_lift_joint'])                         
    """                                                                                                
    def __init__(self):                                                                                
        self._lock = Lock()
        self._joint_states = {}
        self._sub = rospy.Subscriber('/joint_states', JointState, self._callback)

    def _callback(self, msg):
        with self._lock:
            for name, position in zip(msg.name, msg.position):
                self._joint_states[name] = position                                                                            
                                                                                                       
    def get_joint(self, name):                                                                         
        """Gets the latest joint value.                                                                
                                                                                                       
        Args:                                                                                          
            name: string, the name of the joint whose value we want to read.                           
                                                                                                       
        Returns: the joint value, or None if we do not have a value yet.                               
        """                                                                                            

        with self._lock:
            if name in self._joint_states:
                return self._joint_states[name]
            else:
                rospy.logerr('Joint {} not found'.format(name))
                return None


    def get_joints(self, names):                                                                       
        """Gets the latest values for a list of joint names.                    
                                                                                
        Args:                                                                   
            name: list of strings, the names of the joints whose values we want 
                to read.                                                        
                                                                                
        Returns: A list of the joint values. Values may be None if we do not    
            have a value for that joint yet.                                    
        """                                                                     
        return [self.get_joint(name) for name in names]