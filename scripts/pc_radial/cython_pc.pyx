import numpy as np
import rospy
from geometry_msgs.msg import Point32
def t_pc(radius,tamanho,_sensor_x_pose,_sensor_y_pose,qt):
    x = []
    y = []
    z = []
    inten = []
    for i in range(tamanho):
            for angle in range(qt):
                if angle <45:
                   x.append((((i*0.033)+radius)*round(np.cos(np.deg2rad(angle)),6)+_sensor_x_pose))
                   y.append((((i*0.033)+radius)*round(np.sin(np.deg2rad(angle)),6)+_sensor_y_pose))
                   z.append(0.3)
                   inten.append((tamanho * 2) - (i*2))
    return x,y,z,inten


def cython_pub(pc_publisher,pc_msg):
    pc_publisher.publish(pc_msg)

def points(x,y,z):
    return [Point32(x, y, z) for x, y, z in zip(x, y, z)]

def teste(pc_publisher,pc_msg):
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
            #time = rospy.get_rostime().to_sec()
            #cython_pub(pc_publisher,pc_msg)
            pc_publisher.publish(pc_msg)
            #print(rospy.get_rostime().to_sec() - time)
            #rospy.spin()
            rate.sleep()
