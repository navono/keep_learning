#include "utils/XLogger.h"
#include <cstdio>
#include <iostream>

__global__ void hi_gpu() { printf("Hello World from GPU!\n"); }

int main(int argc, char **argv) {
  XLOG_DEBUG("Hello World from CPU!");

  hi_gpu<<<1, 10>>>();
  const cudaError_t err_t = cudaDeviceReset();
  const std::string err_s = cudaGetErrorString(err_t);
  if (err_t != cudaSuccess) {
    XLOG_ERROR("CUDA error: code: {}, reason: {}", (int)err_t, err_s.c_str());
    exit(1);
  }
  return 0;
}