#ifndef _PERCEPTION_OBJECT_H_
#define _PERCEPTION_OBJECT_H_

#include <string>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include "geometry_msgs/Pose.h"
#include "geometry_msgs/Vector3.h"

namespace perception {
struct Object {
  std::string name;
  double confidence;
  pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud;
  geometry_msgs::Pose pose;
  geometry_msgs::Vector3 dimensions;
};
}
#endif
