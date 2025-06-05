#pragma once

#include "pcl/PointIndices.h"
#include "pcl/point_cloud.h"
#include "pcl/point_types.h"
#include "ros/ros.h"
#include "sensor_msgs/PointCloud2.h"
#include "geometry_msgs/Pose.h"
#include "geometry_msgs/Vector3.h"

namespace perception {

typedef pcl::PointXYZRGB PointC;
typedef pcl::PointCloud<pcl::PointXYZRGB> PointCloudC;

void SegmentBinObjects(PointCloudC::Ptr cloud,
                       std::vector<pcl::PointIndices>* indices);

void GetAxisAlignedBoundingBox(PointCloudC::Ptr cloud,
                               geometry_msgs::Pose* pose,
                               geometry_msgs::Vector3* dimensions);

class Segmenter {
 public:
  Segmenter(const ros::Publisher& points_pub, const ros::Publisher& marker_pub);
  void Callback(const sensor_msgs::PointCloud2& msg);

 private:
  ros::Publisher points_pub_;
  ros::Publisher marker_pub_;
};
}  // namespace perception
