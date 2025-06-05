#include "perception/segmentation.h"

#include <pcl/common/common.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/segmentation/extract_clusters.h>
#include <pcl_conversions/pcl_conversions.h>
#include <visualization_msgs/Marker.h>

namespace perception {

void SegmentBinObjects(PointCloudC::Ptr cloud, std::vector<pcl::PointIndices>* indices) {
  // Remove NaNs from the input cloud
  std::vector<int> index;
  pcl::removeNaNFromPointCloud(*cloud, *cloud, index);

  
  double cluster_tolerance;
  int min_cluster_size, max_cluster_size;
  ros::param::param("ec_cluster_tolerance", cluster_tolerance, 0.01);
  ros::param::param("ec_min_cluster_size", min_cluster_size, 10);
  ros::param::param("ec_max_cluster_size", max_cluster_size, 10000);

  pcl::EuclideanClusterExtraction<PointC> euclid;
  euclid.setInputCloud(cloud);
  euclid.setClusterTolerance(cluster_tolerance);
  euclid.setMinClusterSize(min_cluster_size);
  euclid.setMaxClusterSize(max_cluster_size);
  euclid.extract(*indices);

  size_t min_size = std::numeric_limits<size_t>::max();
  size_t max_size = std::numeric_limits<size_t>::min();
  for (const auto& cluster : *indices) {
    size_t size = cluster.indices.size();
    min_size = std::min(min_size, size);
    max_size = std::max(max_size, size);
  }

  ROS_INFO("Found %lu objects, min size: %lu, max size: %lu",
           indices->size(), min_size, max_size);
}

void GetAxisAlignedBoundingBox(PointCloudC::Ptr cloud,
                               geometry_msgs::Pose* pose,
                               geometry_msgs::Vector3* dimensions) {
  PointC min_pt, max_pt;
  pcl::getMinMax3D(*cloud, min_pt, max_pt);
  pose->position.x = (min_pt.x + max_pt.x) / 2.0;
  pose->position.y = (min_pt.y + max_pt.y) / 2.0;
  pose->position.z = (min_pt.z + max_pt.z) / 2.0;

  dimensions->x = max_pt.x - min_pt.x;
  dimensions->y = max_pt.y - min_pt.y;
  dimensions->z = max_pt.z - min_pt.z;
}

Segmenter::Segmenter(const ros::Publisher& points_pub, const ros::Publisher& marker_pub)
    : points_pub_(points_pub), marker_pub_(marker_pub) {}

void Segmenter::Callback(const sensor_msgs::PointCloud2& msg) {
  PointCloudC::Ptr cloud(new PointCloudC());
  pcl::fromROSMsg(msg, *cloud);

  std::vector<pcl::PointIndices> object_indices;
  SegmentBinObjects(cloud, &object_indices);

  for (size_t i = 0; i < object_indices.size(); ++i) {
    pcl::PointIndices::Ptr indices(new pcl::PointIndices);
    *indices = object_indices[i];

    PointCloudC::Ptr object_cloud(new PointCloudC());
    pcl::ExtractIndices<PointC> extract;
    extract.setInputCloud(cloud);
    extract.setIndices(indices);
    extract.filter(*object_cloud);

    visualization_msgs::Marker marker;
    marker.ns = "objects";
    marker.id = i;
    marker.header.frame_id = "base_link";
    marker.header.stamp = ros::Time::now();
    marker.type = visualization_msgs::Marker::CUBE;
    marker.action = visualization_msgs::Marker::ADD;

    GetAxisAlignedBoundingBox(object_cloud, &marker.pose, &marker.scale);

    marker.color.r = 0.0;
    marker.color.g = 1.0;
    marker.color.b = 0.0;
    marker.color.a = 0.3;
    marker.lifetime = ros::Duration(1.0);
    marker_pub_.publish(marker);
  }

  sensor_msgs::PointCloud2 output_msg;
  pcl::toROSMsg(*cloud, output_msg);
  output_msg.header.frame_id = "base_link";
  points_pub_.publish(output_msg);
}
}  // namespace perception
