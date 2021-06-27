#!/usr/bin/env python
import math
import numpy as np
import rospy
from sensor_msgs.msg import PointCloud,ChannelFloat32
import geometry_msgs
import std_msgs
import tf
from cython_pc import t_pc,cython_pub,points,teste
from geometry_msgs.msg import Point32, Pose

__author__ = 'Mauricio Sathler'
__license__ = 'MIT'
_sensor_x_pose = 0
_sensor_y_pose = 0
def pose_callback(pose):
        global _sensor_x_pose,_sensor_y_pose
        _sensor_x_pose = pose.position.x
        _sensor_y_pose = pose.position.y


def circumference(radius,tamanho):
    global _sensor_x_pose,_sensor_y_pose
    rospy.Subscriber("/dummy/pose", Pose, pose_callback)
    rospy.wait_for_message('/dummy/pose',Pose)
    #rospy.sleep(1)
    rospy.loginfo("-------------")
    x= []
    y =[]
    z = []
    inten = []
    #x,y,z,inten = t_pc(radius,tamanho,_sensor_x_pose,_sensor_y_pose,720)
    
    for i in range(tamanho):
        for angle in range(0,360):
            x.append((((i*0.033)+radius)*np.cos(np.deg2rad(angle))+_sensor_x_pose))
            y.append((((i*0.033)+radius)*np.sin(np.deg2rad(angle))+_sensor_y_pose))
            z.append(0.05)
            inten.append((tamanho * 2) - (i*2))

    return x,y,z,inten

def test():
    pc_msg = PointCloud()
    
    pc_publisher = rospy.Publisher("point_pompy",PointCloud, queue_size= None)
    rospy.init_node("no")
    
    tf_listener = tf.TransformListener()
    pc_msg.header.stamp = rospy.Time.now()
    pc_msg.header.frame_id = 'world'
    x,y,z,inten = circumference(0,200)

    pc_msg.points = points(x,y,z) #[Point32(x, y, z) for x, y, z in zip(x, y, z)]
    channel = ChannelFloat32()
    channel.name = 'intensity'
    channel.values = inten
    pc_msg.channels.append(channel)
    
    
    teste(pc_publisher,pc_msg)
    # while not rospy.is_shutdown():
    #         #time = rospy.get_rostime().to_sec()
    #         #cython_pub(pc_publisher,pc_msg)
    #         pc_publisher.publish(pc_msg)
    #         #print(rospy.get_rostime().to_sec() - time)
    #         #rospy.spin()
    #         rate.sleep()


if __name__ == '__main__':

    try:
        test()

    except rospy.ROSInterruptException:
        pass
