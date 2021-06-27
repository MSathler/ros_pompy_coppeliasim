#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Point32, Pose,Twist
from std_msgs.msg import Float32


class controller():
    def __init__(self):
        rospy.init_node("control")
        self.pub = rospy.Publisher("/cmd_vel",Twist,queue_size= 100)
        self.prev_read = 0.0
        self.__Found = 0
        self.cmd_vel_msg = Twist()
        self.ros()
    
    def ros(self):
        self.sub = rospy.Subscriber("/sensor_read",Float32, self.callback_command)
        rospy.spin()

    def callback_command(self, read):
        
        
        self._gradient = float(read.data) - self.prev_read
        print(self._gradient)

        if self._gradient > 0:
            self.cmd_vel_msg.linear.x = 0.5
            self.cmd_vel_msg.linear.y = 0.0
            self.cmd_vel_msg.linear.z = 0.0
            self.cmd_vel_msg.angular.x = 0.0
            self.cmd_vel_msg.angular.y = 0.0
            self.cmd_vel_msg.angular.z = 0.0

        #elif (self._gradient > 60000) or (self.__Found == 1):

        #    self.cmd_vel_msg.linear.x = 0.0
        #    self.cmd_vel_msg.linear.y = 0.0
        #    self.cmd_vel_msg.linear.z = 0.0
        #    self.cmd_vel_msg.angular.x = 0.0
        #    self.cmd_vel_msg.angular.y = 0.0
        #    self.cmd_vel_msg.angular.z = 0.0
        #    self.__Found = 1
        #    rospy.loginfo("Chegou a Fonte!")
	    
	    
        else:
            self.cmd_vel_msg.linear.x = 0.0
            self.cmd_vel_msg.linear.y = 0.0
            self.cmd_vel_msg.linear.z = 0.0
            self.cmd_vel_msg.angular.x = 0.0
            self.cmd_vel_msg.angular.y = 0.0
            self.cmd_vel_msg.angular.z = 0.3
        self.prev_read = float(read.data)
        self.pub.publish(self.cmd_vel_msg)

if __name__ == "__main__":
    try:
        c_obj = controller()
    except rospy.ROSInterruptException:
        pass
