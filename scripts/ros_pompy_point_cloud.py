import rospy
from sensor_msgs.msg import PointCloud,ChannelFloat32
from pompy import models, processors
import geometry_msgs
import std_msgs
from geometry_msgs.msg import Point32, Pose


class pompy_point_cloud(object):
    
    
    def __init__(self,  wind_model, 
			plume_model,
			conc_array,
			array_gen,
			use_pose_coppelia = True,
			node_name = 'plume_simulator_server', 
			dt = 0.01,
			topic_publisher = 'point_pompy',
			topic_subscriber = '/dummy/pose',
			frame = 'world'):
        
        self._topic_publisher = topic_publisher
        self._topic_subscriber = topic_subscriber
        self._frame = frame
        self._conc_array = conc_array
        self._wind_model = wind_model
        self.dt = dt
        self._node_name = node_name
        self._array_gen = array_gen
        self._plume_model = plume_model
        self._use_pose_coppelia = use_pose_coppelia

        self.ros()


    def ros(self):

        rospy.init_node(str(self._node_name))
        self._pc_publisher = rospy.Publisher(str(self._topic_publisher),PointCloud, queue_size= 100)

        if (self._use_pose_coppelia == True):
            self._pose_subscriber = rospy.Subscriber(str(self._topic_subscriber),Pose,self.pose_callback)
            rospy.loginfo("Utilized dummy position with Coppelia Pose")
        else:
            rospy.loginfo("Without using the pose with Coppelia")
            while not rospy.is_shutdown():
                self.without_coppelia() 

        rospy.spin()

    def pose_callback(self, pose):

        for i in range(10):

            self._wind_model.update(self.dt)
            self._plume_model.update(self.dt)

        self._conc_array = self._array_gen.generate_single_array(self._plume_model.puff_array)
        
        # Initiation of variables temporary variables
        x =[]
        y = []
        z = []
        inten = []

        # Creation of Point Cloud object
        self.pc_msg = PointCloud()
        self.pc_msg.header.stamp = rospy.Time.now()
        self.pc_msg.header.frame_id = 'world'
        

        for i in range(self._conc_array.T.shape[0]):

            for j in range(self._conc_array.T.shape[1]):

                if (self._conc_array.T[i][j] != 0):

                    x.append((i*0.01) + pose.position.x)
                    y.append((j*0.01) + pose.position.y)
                    z.append(pose.position.z)
                    inten.append(self._conc_array.T[i][j]*0.001)


                    
        self.pc_msg.points = [Point32(x, y, z) for x, y, z in zip(x, y, z)]
        self.channel = ChannelFloat32()
        self.channel.name = 'intensity'
        self.channel.values = inten
        self.pc_msg.channels.append(self.channel)
        
        # Publshing the Point Cloud
        self._pc_publisher.publish(self.pc_msg)

        # Reset Variables
        x = []
        y = []
        z = []
        inten = []

    def without_coppelia(self):
        for i in range(10):

            self._wind_model.update(self.dt)
            self._plume_model.update(self.dt)

        self._conc_array = self._array_gen.generate_single_array(self._plume_model.puff_array)
        
        # Initiation of variables temporary variables
        x =[]
        y = []
        z = []
        inten = []
        # Creation of Point Cloud object
        self.pc_msg = PointCloud()
        self.pc_msg.header.stamp = rospy.Time.now()
        self.pc_msg.header.frame_id = 'world'

        for i in range(self._conc_array.T.shape[0]):

            for j in range(self._conc_array.T.shape[1]):

                if (self._conc_array.T[i][j] != 0):

                    x.append(i*0.01)
                    y.append(j*0.01)
                    z.append(0.0)
                    inten.append(self._conc_array.T[i][j]*0.001)

        self.pc_msg.points = [Point32(x, y, z) for x, y, z in zip(x, y, z)]
        self.channel = ChannelFloat32()
        self.channel.name = 'intensity'
        self.channel.values = inten
        self.pc_msg.channels.append(self.channel)
        
        # Publshing the Point Cloud
        self._pc_publisher.publish(self.pc_msg)

        # Reset Variables
        x = []
        y = []
        z = []
        inten = []
