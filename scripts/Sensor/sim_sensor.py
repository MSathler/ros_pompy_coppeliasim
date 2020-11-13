import rospy
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Pose
from std_msgs.msg import Float32

class simSensor():
    def __init__(self, 
		 sensor_dimention = 0.1,
		 node_name = "simSensor",
		 pose_subscriber = "/gas_sensor/pose",
		 pointcloud_subscriber = "/point_pompy",
		 sensorRead_publisher = "/sensor_read"
		 ):

        rospy.init_node(node_name)
        self._points = []
        self._pos_reads = []
        self._xy_reads = []
        self._intensity = []
        self._sum_reads = 0
        self._read = 0
        self._sensor_x = 0
        self._sensor_y = 0
        self._sensor_dimention = sensor_dimention # default 10cm
	self.pose_subscriber = pose_subscriber
	self.pointcloud_subscriber = pointcloud_subscriber
	self.sensorRead_publisher = sensorRead_publisher

        self.ros()
        

    def ros(self):

        self.sub = rospy.Subscriber(self.pose_subscriber, Pose, self.pose_callback)
        self.pc_sub = rospy.Subscriber(self.pointcloud_subscriber, PointCloud,self.pc_callback)
        self.pub = rospy.Publisher(self.sensorRead_publisher,Float32, queue_size = 10)
        rospy.spin()


    def read_sensor(self):

        for i in range(len(self._intensity)):

            if (self._sensor_x >= self._points[i].x - self._sensor_dimention and self._sensor_x <= self._points[i].x + self._sensor_dimention):
                
                for j in range(len(self._intensity)): 

                    if (self._sensor_y >= self._points[j].y - self._sensor_dimention and self._sensor_y <= self._points[j].y + self._sensor_dimention):
                        
                        self._xy_reads.append(self._intensity[i])
                        self._pos_reads.append(i)
                        self._sum_reads += self._intensity[i]          
                        #print(self._sum_reads)              
                        return self._sum_reads
                    
        return 0.0
        

    def pc_callback(self,pc):
        self._points = pc.points
        self._intensity = pc.channels[0].values
        self._read = self.read_sensor()
        self.pub.publish(self._read)
        self.clean_variables()
        

    def pose_callback(self,pose):
        self._sensor_x = pose.position.x
        self._sensor_y = pose.position.y


    def clean_variables(self):
        self._xy_reads = []
        self._intensity = []
        self._sum_reads = 0
        self._points = []
        self._pos_reads = []
    
