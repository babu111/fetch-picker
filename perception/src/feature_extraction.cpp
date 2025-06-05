#include "perception/feature_extraction.h"
#include <algorithm>
#include <ros/ros.h>

namespace perception {

void ExtractSizeFeatures(const Object& object,
                         perception_msgs::ObjectFeatures* features) {
  double weight;
  ros::param::param("size_weight", weight, 2.0);
  features->names.push_back("box_dim_x");
  features->values.push_back(weight * std::min(object.dimensions.x, object.dimensions.y));
  features->names.push_back("box_dim_y");
  features->values.push_back(weight * std::max(object.dimensions.x, object.dimensions.y));
  features->names.push_back("box_dim_z");
  features->values.push_back(weight * object.dimensions.z);
}

void ExtractColorFeatures(const Object& object,
                          perception_msgs::ObjectFeatures* features) {
  std::vector<double> color_features(125, 0.0);
  for (const auto& pt : object.cloud->points) {
    int r = std::min(pt.r / 51, 4);
    int g = std::min(pt.g / 51, 4);
    int b = std::min(pt.b / 51, 4);
    int index = r * 25 + g * 5 + b;
    color_features[index] += 1.0;
  }
  for (double& val : color_features)
    val /= object.cloud->points.size();
  features->values.insert(features->values.end(), color_features.begin(), color_features.end());
}

void ExtractFeatures(const Object& object,
                     perception_msgs::ObjectFeatures* features) {
  ExtractSizeFeatures(object, features);
  ExtractColorFeatures(object, features);
}

}
