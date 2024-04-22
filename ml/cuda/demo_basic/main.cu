#include "utils/XLogger.h"
#include <cstdio>
#include <iostream>

// Kernel function to add the elements of two arrays
// __global__ 变量声明符，作用是将add函数变成可以在GPU上运行的函数
// __global__ 函数被称为kernel，
// 在 GPU 上运行的代码通常称为设备代码（device code），而在 CPU 上运行的代码是主机代码（host code）。
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