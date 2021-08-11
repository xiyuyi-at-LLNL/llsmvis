#include <cfloat>
#include <vector>
#include <iostream>

class Index
{
 public:
  int id[3];
};

class Position
{
 public:
  float x[3];
  Position(){}
  Position(float a, float b, float c)
    {
      x[0]=a;x[1]=b;x[2]=c;
    }
};

std::vector<Index> voxel_traversal(Position ray_start, Position ray_end) {
  double _bin_size = 1;
  std::vector<Index> visited_voxels;
  Index current_voxel;
  current_voxel.id[0] = (int) std::floor(ray_start.x[0]/_bin_size);
  current_voxel.id[1] = (int) std::floor(ray_start.x[1]/_bin_size);
  current_voxel.id[2] = (int) std::floor(ray_start.x[2]/_bin_size);
  Index last_voxel;
  last_voxel.id[0]=std::floor(ray_end.x[0]/_bin_size);
  last_voxel.id[1]=std::floor(ray_end.x[1]/_bin_size);
  last_voxel.id[2]=std::floor(ray_end.x[2]/_bin_size);
  Position ray;
  ray.x[0] = ray_end.x[0]-ray_start.x[0];
  ray.x[1] = ray_end.x[1]-ray_start.x[1];
  ray.x[2] = ray_end.x[2]-ray_start.x[2];
  double stepX = (ray.x[0] >= 0) ? 1:-1; 
  double stepY = (ray.x[1] >= 0) ? 1:-1; 
  double stepZ = (ray.x[2] >= 0) ? 1:-1; 
  double next_voxel_boundary_x = (current_voxel.id[0]+stepX)*_bin_size;
  double next_voxel_boundary_y = (current_voxel.id[1]+stepY)*_bin_size;
  double next_voxel_boundary_z = (current_voxel.id[2]+stepZ)*_bin_size;
  double tMaxX = (ray.x[0]!=0) ? (next_voxel_boundary_x - ray_start.x[0])/ray.x[0] : DBL_MAX; 
  double tMaxY = (ray.x[1]!=0) ? (next_voxel_boundary_y - ray_start.x[1])/ray.x[1] : DBL_MAX; 
  double tMaxZ = (ray.x[2]!=0) ? (next_voxel_boundary_z - ray_start.x[2])/ray.x[2] : DBL_MAX; 
  double tDeltaX = (ray.x[0]!=0) ? _bin_size/ray.x[0]*stepX : DBL_MAX;
  double tDeltaY = (ray.x[1]!=0) ? _bin_size/ray.x[1]*stepY : DBL_MAX;
  double tDeltaZ = (ray.x[2]!=0) ? _bin_size/ray.x[2]*stepZ : DBL_MAX;
  Index diff;
  diff.id[0]=0;
  diff.id[1]=0;
  diff.id[2]=0;
  bool neg_ray=false;
  if (current_voxel.id[0]!=last_voxel.id[0] && ray.x[0]<0) { diff.id[0]--; neg_ray=true; }
  if (current_voxel.id[1]!=last_voxel.id[1] && ray.x[1]<0) { diff.id[1]--; neg_ray=true; }
  if (current_voxel.id[2]!=last_voxel.id[2] && ray.x[2]<0) { diff.id[2]--; neg_ray=true; }
  visited_voxels.push_back(current_voxel);
  if (neg_ray) {
    current_voxel.id[0]+=diff.id[0];
    current_voxel.id[1]+=diff.id[1];
    current_voxel.id[2]+=diff.id[2];
    visited_voxels.push_back(current_voxel);
  }
  while(last_voxel.id[0] != current_voxel.id[0] || last_voxel.id[1] != current_voxel.id[1] || last_voxel.id[2] != current_voxel.id[2]) {
    if (tMaxX < tMaxY) {
      if (tMaxX < tMaxZ) {
        current_voxel.id[0] += stepX;
        tMaxX += tDeltaX;
      } else {
        current_voxel.id[2] += stepZ;
        tMaxZ += tDeltaZ;
      }
    } else {
      if (tMaxY < tMaxZ) {
        current_voxel.id[1] += stepY;
        tMaxY += tDeltaY;
      } else {
        current_voxel.id[2] += stepZ;
        tMaxZ += tDeltaZ;
      }
    }
    visited_voxels.push_back(current_voxel);
  }
  return visited_voxels;
}
