import rospy
from nav_msgs.msg import Path
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Pose,PoseStamped
import tf
from std_msgs.msg import Float32
import cython_for

__author__ = 'Mauricio Sathler'
__license__ = 'MIT'

class simSensorRos():

    
    def __init__(self, 
		 sensor_dimention = 0.04,
		 node_name = "simSensor",
		 pose_subscriber = "/gas_sensor/pose",
		 pointcloud_subscriber = "/point_pompy",
		 sensorRead_publisher = "/sensor_read",
         use_tf = True
		 ):

        rospy.init_node(node_name)


        self._use_tf = use_tf
        self._points = []
        self._path_msg = Path()
        self._pose_msg = PoseStamped()
        self.pub_path = rospy.Publisher("/robot_path",Path,queue_size=None)
        self._pos_reads = []
        self._xy_reads = []
        self._intensity = []
        self.i = 0
        self._sum_reads = 0
        self._read = 0
        self._mean = 0
        self._sensor_x = 0
        self._sensor_y = 0
        self.tf_listener = tf.TransformListener()
        self._sensor_dimention = sensor_dimention
        self.pose_subscriber = pose_subscriber
        self.pointcloud_subscriber = pointcloud_subscriber
        self.sensorRead_publisher = sensorRead_publisher
        self.r = rospy.Rate(1)
        
        self.ros()
        

    def ros(self):
        #if (self._use_tf == True):
        #    self.echo_tf()
        #else:
	
        self.sub = rospy.Subscriber(self.pose_subscriber, Pose, self.pose_callback)

        self.pc_sub = rospy.Subscriber(self.pointcloud_subscriber, PointCloud,self.pc_callback)
        self.pub = rospy.Publisher(self.sensorRead_publisher,Float32, queue_size = 100)
	
        rospy.spin()


    def read_sensor(self):

        return cython_for.read_sensor(self._points,self._intensity,self._sensor_x_pose,self._sensor_y_pose,self._sensor_dimention,self._sum_reads)
        #return cython_for.cython_distance(self._points,self._intensity,self._sensor_x_pose,self._sensor_y_pose,self._sensor_dimention,self._sum_reads)

    def pc_callback(self,pc):
	
        self._points = pc.points
        self._intensity = pc.channels[0].values
	#t = rospy.get_rostime().to_sec()
        self._mean = self.read_sensor()
	#print(rospy.get_rostime().to_sec() - t)
	 
        self.pub.publish(self._mean)
        self.clean_variables()
	#print(rospy.get_rostime().to_sec() - self.t)
        
    def pose_callback(self,pose):
	self.t = rospy.get_rostime().to_sec()
        self._sensor_x_pose = pose.position.x
        self._sensor_y_pose = pose.position.y
        self._pose_msg.header.frame_id = 'world'
        self._pose_msg.header.stamp = rospy.get_rostime()
        self._pose_msg.pose = pose 
        self._path_msg.poses.append(self._pose_msg)

        self._path_msg.header.stamp = rospy.get_rostime()
        self._path_msg.header.frame_id = 'world'
        self.pub_path.publish(self._path_msg)
        #self.echo_tf()

    def echo_tf(self):

        (trans,rot) = self.tf_listener.lookupTransform('world','gas_sensor',rospy.Time(0))
        self._sensor_x_tf = trans[0]
        self._sensor_y_tf = trans[1]
        
    def clean_variables(self):
        self._mean = 0
        self._xy_reads = []
        self._intensity = []
        self._sum_reads = 0
        self._points = []
        self._pos_reads = []


    
