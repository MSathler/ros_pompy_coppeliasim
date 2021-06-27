#include <ros/ros.h>
// PCL specific includes
#include <sensor_msgs/PointCloud.h>
#include <geometry_msgs/Pose.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>

ros::Publisher pub;

void 
cloud_cb (const geometry_msgs::Pose::ConstPtr& input)
{
  // Create a container for the data.
  geometry_msgs::Pose out;
  //sensor_msgs::PointCloud2 output;

  // Do data processing here...
  out = *input;
  ROS_INFO("%s" , out.c_str());
  // Publish the data.
  //pub.publish (output);
}

int
main (int argc, char** argv)
{
  // Initialize ROS
  ros::init (argc, argv, "pc_radial_node");
  ros::NodeHandle nh;

  // Create a ROS subscriber for the input point cloud
  ros::Subscriber sub = nh.subscribe("/dummy/pose", 1, cloud_cb);

  // Create a ROS publisher for the output point cloud
  //pub = nh.advertise<sensor_msgs::PointCloud> ("output", 1);

  // Spin
  ros::spin ();
}