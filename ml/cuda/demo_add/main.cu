#include <chrono>
#include <iostream>
#include <math.h>

#include "utils/XLogger.h"

void cpu_add(int n, float *x, float *y) {
  for (int i = 0; i < n; i++)
    y[i] = x[i] + y[i];
}

void cpu_add_test() {
  int N = 1 << 25; // 30M elements

  float *x = new float[N];
  float *y = new float[N];

  // initialize x and y arrays on the host
  for (int i = 0; i < N; i++) {
    x[i] = 1.0f;
    y[i] = 2.0f;
  }

  std::chrono::high_resolution_clock::time_point start =
      std::chrono::high_resolution_clock::now();

  // Run kernel on 30M elements on the CPU
  cpu_add(N, x, y);

  std::chrono::high_resolution_clock::time_point end =
      std::chrono::high_resolution_clock::now();
  auto duration =
      std::chrono::duration_cast<std::chrono::duration<double>>(end - start);

  XLOG_INFO("add(int, float*, float*) time: {}ms", duration.count() * 1000);

  // Check for errors (all values should be 3.0f)
  float maxError = 0.0f;
  for (int i = 0; i < N; i++)
    maxError = fmax(maxError, fabs(y[i] - 3.0f));
  XLOG_INFO("Max error: {}", maxError);

  // Free memory
  delete[] x;
  delete[] y;
}

__global__ void add(int n, float *x, float *y) {
  int index = blockIdx.x * blockDim.x + threadIdx.x;
  int stride = blockDim.x * gridDim.x;
  for (int i = index; i < n; i += stride)
    y[i] = x[i] + y[i];
}

void gpu_add_slow_version() {
  int N = 1 << 25;
  float *x, *y;

  // Allocate Unified Memory – accessible from CPU or GPU
  // 内存分配，在GPU或者CPU上统一分配内存
  cudaMallocManaged(&x, N * sizeof(float));
  cudaMallocManaged(&y, N * sizeof(float));

  std::chrono::high_resolution_clock::time_point start =
      std::chrono::high_resolution_clock::now();

  // initialize x and y arrays on the host
  for (int i = 0; i < N; i++) {
    x[i] = 1.0f;
    y[i] = 2.0f;
  }

  // Run kernel on 1M elements on the GPU
  // execution configuration, 执行配置。按照层次从大到小可将GPU按照 grid ->
  // block -> thread划分
  // <<<numBlocks, blockSize>>>
  add<<<1, 1>>>(N, x, y);

  // Wait for GPU to finish before accessing on host
  // CPU需要等待cuda上的代码运行完毕，才能对数据进行读取
  cudaDeviceSynchronize();

  std::chrono::high_resolution_clock::time_point end =
      std::chrono::high_resolution_clock::now();
  auto duration =
      std::chrono::duration_cast<std::chrono::duration<double>>(end - start);

  XLOG_INFO("add(int, float*, float*) time: {}ms", duration.count() * 1000);

  // Check for errors (all values should be 3.0f)
  float maxError = 0.0f;
  for (int i = 0; i < N; i++)
    maxError = fmax(maxError, fabs(y[i] - 3.0f));

  XLOG_INFO("Max error: {}", maxError);

  // Free memory
  cudaFree(x);
  cudaFree(y);
}

void gpu_add_normal_version() {
  int N = 1 << 25;
  float *x, *y;

  // Allocate Unified Memory – accessible from CPU or GPU
  // 内存分配，在GPU或者CPU上统一分配内存
  cudaMallocManaged(&x, N * sizeof(float));
  cudaMallocManaged(&y, N * sizeof(float));

  std::chrono::high_resolution_clock::time_point start =
      std::chrono::high_resolution_clock::now();

  // initialize x and y arrays on the host
  for (int i = 0; i < N; i++) {
    x[i] = 1.0f;
    y[i] = 2.0f;
  }

  // Run kernel on 1M elements on the GPU
  // execution configuration, 执行配置。按照层次从大到小可将GPU按照 grid ->
  // block -> thread划分
  // <<<numBlocks, blockSize>>>
  add<<<32, 256>>>(N, x, y);

  // Wait for GPU to finish before accessing on host
  // CPU需要等待cuda上的代码运行完毕，才能对数据进行读取
  cudaDeviceSynchronize();

  std::chrono::high_resolution_clock::time_point end =
      std::chrono::high_resolution_clock::now();
  auto duration =
      std::chrono::duration_cast<std::chrono::duration<double>>(end - start);

  XLOG_INFO("add(int, float*, float*) time: {}ms", duration.count() * 1000);

  // Check for errors (all values should be 3.0f)
  float maxError = 0.0f;
  for (int i = 0; i < N; i++)
    maxError = fmax(maxError, fabs(y[i] - 3.0f));

  XLOG_INFO("Max error: {}", maxError);

  // Free memory
  cudaFree(x);
  cudaFree(y);
}

int main(void) {
  //  cpu_add_test();
  //  gpu_add_slow_version();
  gpu_add_normal_version();

  return 0;
}