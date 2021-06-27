#!/usr/bin/env python
import rospy
from nav_msgs.msg import Path
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Pose,PoseStamped,Point
import matplotlib.pyplot as plt

x = []
y = []
i = 0.0
plt.show()
def callback(pose):
    global i
    #plt.hold(True)
    i = i + 1
    x.append(pose.x)
    y.append(pose.y)
    plt.plot(x,y)
    if i%10 == 0:
        plt.show()

    

def path():
    rospy.init_node('path_node')
    print("1")
    
    rospy.Subscriber("roboPosicao",Point, callback)
    rospy.spin()

if __name__ == '__main__':
    
    path()