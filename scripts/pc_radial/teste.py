import math
import rospy
from sensor_msgs.msg import PointCloud,ChannelFloat32
import geometry_msgs
import std_msgs
from geometry_msgs.msg import Point32, Pose




class pompy_point_cloud(object):
    
    
    def __init__(self,
			use_pose_coppelia = True,
			node_name = 'plume_simulator_server', 
			topic_publisher = 'point_pompy',
			topic_subscriber = '/dummy/pose',
			frame = 'world'):
        
        self._topic_publisher = topic_publisher
        self._topic_subscriber = topic_subscriber
        self._frame = frame
        
        self._node_name = node_name

        self._use_pose_coppelia = use_pose_coppelia
        
        


        self.ros()


    def ros(self):

        rospy.init_node(str(self._node_name))
        self._pc_publisher = rospy.Publisher(str(self._topic_publisher),PointCloud, queue_size= 100)
        self._pose_subscriber = rospy.Subscriber(str(self._topic_subscriber),Pose,self.pose_callback)
        
        self.rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            self._pc_publisher.publish(self.pc_msg)
            self.rate.sleep()
            
            #rospy.spin()

    def pose_callback(self, pose):
        
        self.pc_msg = PointCloud()
        self.pc_msg.header.stamp = rospy.Time.now()
        self.pc_msg.header.frame_id = 'world'
        x = []
        y = []
        z = []
        inten = []
        self.inten = []
        for i in range(10):
            x,y,z,inten = self.circumference(i*0.01,100-i)

        #print("a")
        self.pc_msg.points = [Point32(x, y, z) for x, y, z in zip(x, y, z)]
        self.channel = ChannelFloat32()
        self.channel.name = 'intensity'
        self.channel.values = inten
        self.pc_msg.channels.append(self.channel)

        # Creation of Point Cloud object
        print("a")
        
        # Publshing the Point Cloud
        
        # Reset Variables
        x = []
        y = []
        z = []
        inten = []
        self.pc_msg = PointCloud()


    def circumference(self,radius,intensidade):
        x = []
        y = []
        z = []
        inten = []
        for angle in range(360):
            x.append(radius*math.cos(angle))
            y.append(radius*math.sin(angle))
            z.append(0.3)
            inten = intensidade
        return x,y,z,inten


