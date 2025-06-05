#ifndef _PERCEPTION_FEATURE_EXTRACTION_H_
#define _PERCEPTION_FEATURE_EXTRACTION_H_

#include "perception/object.h"
#include "perception_msgs/ObjectFeatures.h"

namespace perception {
void ExtractSizeFeatures(const Object& object,
                         perception_msgs::ObjectFeatures* features);

void ExtractColorFeatures(const Object& object,
                          perception_msgs::ObjectFeatures* features);

void ExtractFeatures(const Object& object,
                     perception_msgs::ObjectFeatures* features);
}
#endif
