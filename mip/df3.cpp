#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include "voxel_travelsal.h"

static const int nx = 800, ny = 512, nz = 1308;

// Assuming the file is having z fastest changing index (for x for y for z)
void readPositionObj(std::string file, int NX, int NY, int NZ, float ***v1,
                     float ***v2, float ***v3) {
  std::ifstream fs;
  fs.open(file);

  std::string line;
  float x, y, z;

  std::vector<float> x_array;
  std::vector<float> y_array;
  std::vector<float> z_array;
  int count = 0;
  while (std::getline(fs, line)) {
    count++;
    for (int zz = 10; zz <= 100; zz += 10)
      if (count == NX * NY * NZ / 100 * zz)
        std::cout << zz << "% done" << std::endl;
    std::stringstream ss(line);
    if (line[0] == 'v' && line[1] == ' ') {
      ss.ignore();
      ss >> x;
      ss >> y;
      ss >> z;
      x_array.emplace_back(x);
      y_array.emplace_back(y);
      z_array.emplace_back(z);
    }
  }

  int id = 0;
  for (int i = 0; i < NX; ++i) {
    for (int j = 0; j < NY; ++j) {
      for (int k = 0; k < NZ; ++k) {
        v1[i][j][k] = x_array[id];
        v2[i][j][k] = y_array[id];
        v3[i][j][k] = z_array[id];
        id++;
      }
    }
  }

  fs.close();
}

#define SWAP_2(x) ((((x)&0xff) << 8) | ((unsigned short)(x) >> 8))
#define SWAP_4(x)                                                              \
  (((x) << 24) | (((x) << 8) & 0x00ff0000) | (((x) >> 8) & 0x0000ff00) |       \
   ((x) >> 24))
#define FIX_SHORT(x) (*(unsigned short *)&(x) = SWAP_2(*(unsigned short *)&(x)))
#define FIX_INT(x) (*(unsigned int *)&(x) = SWAP_4(*(unsigned int *)&(x)))

int main(int argc, char *argv[]) {

  {
    // Write PGM picture
    FILE *pgmimg;
    std::string filename = "black.pgm";
    pgmimg = fopen(filename.c_str(), "wb");
    fprintf(pgmimg, "P2\n");
    fprintf(pgmimg, "%d %d\n", nz, ny);
    fprintf(pgmimg, "255\n");
    int count = 0;
    for (int j = 0; j < ny; j++) {
      for (int k = 0; k < nz; k++) {
	int color = int(0);
	fprintf(pgmimg, "%d ", color);
      }
      fprintf(pgmimg, "\n");
    }
    fclose(pgmimg);
  }
  
  
  int i, j, k;
  float v;
  float themin_x = 1e32, themax_x = -1e32;
  float themin_y = 1e32, themax_y = -1e32;
  float themin_z = 1e32, themax_z = -1e32;
  float ***df3x;
  float ***df3y;
  float ***df3z;
  FILE *fptr;

  /* Malloc the df3 volume - should really check the results of malloc() */
  df3x = (float ***)malloc(nx * sizeof(float **));
  df3y = (float ***)malloc(nx * sizeof(float **));
  df3z = (float ***)malloc(nx * sizeof(float **));

  for (i = 0; i < nx; i++) {
    df3x[i] = (float **)malloc(ny * sizeof(float *));
    df3y[i] = (float **)malloc(ny * sizeof(float *));
    df3z[i] = (float **)malloc(ny * sizeof(float *));
  }
  for (i = 0; i < nx; i++) {
    for (j = 0; j < ny; j++) {
      df3x[i][j] = (float *)malloc(nz * sizeof(float));
      df3y[i][j] = (float *)malloc(nz * sizeof(float));
      df3z[i][j] = (float *)malloc(nz * sizeof(float));
    }
  }

  /* Zero the grid */
  for (i = 0; i < nx; i++) {
    for (j = 0; j < ny; j++) {
      for (k = 0; k < nz; k++) {
        df3x[i][j][k] = 0;
        df3y[i][j][k] = 0;
        df3z[i][j][k] = 0;
      }
    }
  }
  std::cout << "reading..." << std::endl;
  readPositionObj("input.obj", nx, ny, nz, df3x, df3y, df3z);

  /* Calculate the bounds */
  for (i = 0; i < nx; i++) {
    for (j = 0; j < ny; j++) {
      for (k = 0; k < nz; k++) {
        themax_x = std::max(themax_x, df3x[i][j][k]);
        themin_x = std::min(themin_x, df3x[i][j][k]);
        themax_y = std::max(themax_y, df3y[i][j][k]);
        themin_y = std::min(themin_y, df3y[i][j][k]);
        themax_z = std::max(themax_z, df3z[i][j][k]);
        themin_z = std::min(themin_z, df3z[i][j][k]);
      }
    }
  }
  if (themin_x >= themax_x) { /* There is no variation */
    themax_x = themin_x + 1;
    themin_x -= 1;
  }
  if (themin_y >= themax_y) { /* There is no variation */
    themax_y = themin_y + 1;
    themin_y -= 1;
  }
  if (themin_z >= themax_z) { /* There is no variation */
    themax_z = themin_z + 1;
    themin_z -= 1;
  }

  std::cout << "write image for first channel..." << std::endl;
  // the image plane is y-z plane (orthographics)
  // the object as a hex mesh has [nx,ny,nz] cells with h=1, as a box, min corner is at (0,0,0)
  Position object_center;
  object_center.x[0] = (float)nx/2.0f;
  object_center.x[1] = (float)ny/2.0f;
  object_center.x[2] = (float)nz/2.0f;


  for(int theta_int = 49; theta_int<360; theta_int+=1){
    std::cout << "write image for first channel..." << std::endl;
    float img1[ny][nz];
    float img2[ny][nz];
    float img3[ny][nz];
    for (j = 0; j < ny; j++) for (k = 0; k < nz; k++) img1[j][k] = 0;
    for (j = 0; j < ny; j++) for (k = 0; k < nz; k++) img2[j][k] = 0;
    for (j = 0; j < ny; j++) for (k = 0; k < nz; k++) img3[j][k] = 0;
    int count = 0;
    for (j = 0; j < ny; j++) {
      for (k = 0; k < nz; k++) {
      
	for (int zz = 10; zz <= 100; zz += 10)
	  if (count == ny * nz / 100 * zz)
	    std::cout << zz << "% done" << std::endl;
	count++;

	Position ray_start, ray_end;
	ray_start.x[0] = 0-500; 
	ray_start.x[1] = 0.5+j;
	ray_start.x[2] = 0.5+k;
	ray_end.x[0] = nx+500; 
	ray_end.x[1] = 0.5+j;
	ray_end.x[2] = 0.5+k;

	// rotate ray
	Position u(0,1,0);
	float theta=theta_int*3.141592653/180.0;
	for(int q=0;q<3;q++){
	  ray_start.x[q]-=object_center.x[q];
	  ray_end.x[q]-=object_center.x[q];
	}
	using namespace std;
	float ux = u.x[0], uy=u.x[1], uz=u.x[2];
	float R00 = cos(theta)+ux*ux*(1-cos(theta));
	float R01 = ux*uy*(1-cos(theta))-uz*sin(theta);
	float R02 = ux*uz*(1-cos(theta))+uy*sin(theta);
	float R10 = uy*ux*(1-cos(theta))+uz*sin(theta);
	float R11 = cos(theta)+uy*uy*(1-cos(theta));
	float R12 = uy*uz*(1-cos(theta))-ux*sin(theta);
	float R20 = uz*ux*(1-cos(theta))-uy*sin(theta);
	float R21 = uz*uy*(1-cos(theta))+ux*sin(theta);
	float R22 = cos(theta)+uz*uz*(1-cos(theta));
	Position ray_start_new, ray_end_new;
	ray_start_new.x[0] = R00*ray_start.x[0]+R01*ray_start.x[1]+R02*ray_start.x[2];
	ray_start_new.x[1] = R10*ray_start.x[0]+R11*ray_start.x[1]+R12*ray_start.x[2];
	ray_start_new.x[2] = R20*ray_start.x[0]+R21*ray_start.x[1]+R22*ray_start.x[2];
	ray_end_new.x[0] = R00*ray_end.x[0]+R01*ray_end.x[1]+R02*ray_end.x[2];
	ray_end_new.x[1] = R10*ray_end.x[0]+R11*ray_end.x[1]+R12*ray_end.x[2];
	ray_end_new.x[2] = R20*ray_end.x[0]+R21*ray_end.x[1]+R22*ray_end.x[2];
	for(int q=0;q<3;q++){
	  ray_start.x[q]=ray_start_new.x[q]+object_center.x[q];
	  ray_end.x[q]=ray_end_new.x[q]+object_center.x[q];
	}
      
	img1[j][k] = 0;	img2[j][k] = 0;	img3[j][k] = 0;
	std::vector<Index> voxels = voxel_traversal(ray_start, ray_end);
	for(auto& voxel:voxels)
	  if(voxel.id[0] >=0 && voxel.id[0]< nx)
	    if(voxel.id[1] >=0 && voxel.id[1]< ny)
	      if(voxel.id[2] >=0 && voxel.id[2]< nz){
		img1[j][k] = std::max(img1[j][k], df3x[voxel.id[0]][voxel.id[1]][voxel.id[2]]);
		img2[j][k] = std::max(img2[j][k], df3y[voxel.id[0]][voxel.id[1]][voxel.id[2]]);
		img3[j][k] = std::max(img3[j][k], df3z[voxel.id[0]][voxel.id[1]][voxel.id[2]]);}
      }
    }

    /*
      for (j = 0; j < ny; j++) {
      for (k = 0; k < nz; k++) {
      for (i = 0; i < nx; i++) {
      img[j][k] = std::max(df3x[i][j][k], img[j][k]);
      }
      }
      }
    */
    float pmax1 = 0, pmax2=0, pmax3=0;
    float pmin1 = 999999999,pmin2 = 999999999,pmin3=999999999;
    for (j = 0; j < ny; j++) {
      for (k = 0; k < nz; k++) {
	pmax1 = std::max(pmax1, img1[j][k]);
	pmin1 = std::min(pmin1, img1[j][k]);
	pmax2 = std::max(pmax2, img2[j][k]);
	pmin2 = std::min(pmin2, img2[j][k]);
	pmax3 = std::max(pmax3, img3[j][k]);
	pmin3 = std::min(pmin3, img3[j][k]);
      }
    }
    for (j = 0; j < ny; j++) {
      for (k = 0; k < nz; k++) {
	img1[j][k] = (img1[j][k] - pmin1) / (pmax1 - pmin1) * 10;
	if (img1[j][k] > 1) img1[j][k] = 1;
	img2[j][k] = (img2[j][k] - pmin2) / (pmax2 - pmin2) * 10;
	if (img2[j][k] > 1) img2[j][k] = 1;
	img3[j][k] = (img3[j][k] - pmin3) / (pmax3 - pmin3) * 1; // channel 3 does not need dynamic range
	if (img3[j][k] > 1) img3[j][k] = 1;
      }
    }

    for(int zz=1;zz<=3;zz++)
    {
      
      FILE *pgmimg;
      std::string filename;
      if(zz==1) filename = "channel1_" + std::to_string(theta_int) + ".pgm";
      if(zz==2) filename = "channel2_" + std::to_string(theta_int) + ".pgm";
      if(zz==3) filename = "channel3_" + std::to_string(theta_int) + ".pgm";
      pgmimg = fopen(filename.c_str(), "wb");
      fprintf(pgmimg, "P2\n");
      fprintf(pgmimg, "%d %d\n", nz, ny);
      fprintf(pgmimg, "255\n");
      count = 0;
      for (j = 0; j < ny; j++) {
	for (k = 0; k < nz; k++) {
	  float temp;
	  if(zz==1) temp = img1[j][k];
	  if(zz==2) temp = img2[j][k];
	  if(zz==3) temp = img3[j][k];
	  temp *= 255;
	  int color = int(temp);
	  if (color < 0)
	    color = 0;
	  if (color > 255)
	    color = 255;
	  fprintf(pgmimg, "%d ", color);
	}
	fprintf(pgmimg, "\n");
      }
      fclose(pgmimg);
    }

    
  }
  return 0;

  // Write df3 volume
  std::cout << "writing1..." << std::endl;
  if ((fptr = fopen("channel1.df3", "w")) == NULL)
    return false;
  fputc(nx >> 8, fptr);
  fputc(nx & 0xff, fptr);
  fputc(ny >> 8, fptr);
  fputc(ny & 0xff, fptr);
  fputc(nz >> 8, fptr);
  fputc(nz & 0xff, fptr);
  int count = 0;
  for (k = 0; k < nz; k++) {
    for (j = 0; j < ny; j++) {
      for (i = 0; i < nx; i++) {
        count++;
        for (int zz = 10; zz <= 100; zz += 10)
          if (count == nx * ny * nz / 100 * zz)
            std::cout << zz << "% done" << std::endl;
        v = 65535 * (df3x[i][j][k] - themin_x) / (themax_x - themin_x);
        if (v < 0)
          v = 0;
        if (v > 65535)
          v = 65535;
        FIX_SHORT(v);
        fwrite(&v, 2, 1, fptr);
      }
    }
  }
  fclose(fptr);

  std::cout << "writing2..." << std::endl;
  if ((fptr = fopen("channel2.df3", "w")) == NULL)
    return false;
  fputc(nx >> 8, fptr);
  fputc(nx & 0xff, fptr);
  fputc(ny >> 8, fptr);
  fputc(ny & 0xff, fptr);
  fputc(nz >> 8, fptr);
  fputc(nz & 0xff, fptr);
  count = 0;
  for (k = 0; k < nz; k++) {
    for (j = 0; j < ny; j++) {
      for (i = 0; i < nx; i++) {
        count++;
        for (int zz = 10; zz <= 100; zz += 10)
          if (count == nx * ny * nz / 100 * zz)
            std::cout << zz << "% done" << std::endl;

        v = 65535 * (df3y[i][j][k] - themin_y) / (themax_y - themin_y);
        if (v < 0)
          v = 0;
        if (v > 65535)
          v = 65535;
        FIX_SHORT(v);
        fwrite(&v, 2, 1, fptr);
      }
    }
  }
  fclose(fptr);

  std::cout << "writing3..." << std::endl;
  if ((fptr = fopen("channel3.df3", "w")) == NULL)
    return false;
  fputc(nx >> 8, fptr);
  fputc(nx & 0xff, fptr);
  fputc(ny >> 8, fptr);
  fputc(ny & 0xff, fptr);
  fputc(nz >> 8, fptr);
  fputc(nz & 0xff, fptr);
  count = 0;
  for (k = 0; k < nz; k++) {
    for (j = 0; j < ny; j++) {
      for (i = 0; i < nx; i++) {
        count++;
        for (int zz = 10; zz <= 100; zz += 10)
          if (count == nx * ny * nz / 100 * zz)
            std::cout << zz << "% done" << std::endl;

        v = 65535 * (df3z[i][j][k] - themin_z) / (themax_z - themin_z);
        if (v < 0)
          v = 0;
        if (v > 65535)
          v = 65535;
        FIX_SHORT(v);
        fwrite(&v, 2, 1, fptr);
      }
    }
  }
  fclose(fptr);
}

/*

 for (k=0;k<nz;k++) {
    for (j=0;j<ny;j++) {
       for (i=0;i<nx;i++) {
          v = 255 * (df3[i][j][k]-themin)/(themax-themin);
          if(v<0) v=0;
          if(v>255) v=255;
          fputc((int)v,fptr);
       }
    }
 }
*/
