"""
CS 149: Parallel Computing, Assigment 4 Part 1

This script benchmarks various vector addition kernels using different optimization strategies.
It supports profiling and saving results in .neff and .ntff formats.

For Part 1, your task is to run this script, benchmarking the kernels, and reason about the results.
"""

import argparse
from argparse import RawTextHelpFormatter
import numpy as np
from kernels import (
    vector_add_naive,
    vector_add_tiled,
    vector_add_stream,
    matrix_transpose,
)
import subprocess
import neuronxcc.nki as nki

def benchmark_kernel(kernel, *args, profile_name=None):
    """
    Benchmark a vector addition kernel function and verify its correctness.

    This function runs a specified vector addition kernel on input arrays `a` and `b`, 
    measures its performance, and optionally saves profiling data. It compares the 
    kernel's output with the expected result from a standard NumPy operation to ensure 
    correctness.

    Parameters:
    -----------
    kernel : function
        The kernel function that performs vector addition.
    *args : list
        The arguments to be passed to the kernel.
    profile_name : str
        Name used to save .NEFF and .NTFF files.

    Returns:
    --------
    None
        This function prints the benchmark results and correctness validation to stdout.

    Raises:
    -------
    AssertionError
        If the kernel output does not match the expected NumPy result.
    """
    # run without benchmarking to verify correctness
    out = nki.baremetal(kernel)(*args)
    # expected result by numpy
    if kernel == matrix_transpose:
        out_np = args[0].T
    else:
        out_np = args[0] + args[1]
    print(f"\nCorrectness passed? {np.allclose(out, out_np)}")
    assert np.allclose(out, out_np)

    print("\nBenchmarking performance.........")
    if profile_name:
        bench_func = nki.benchmark(kernel, warmup=1, iters=10,
                                   save_neff_name="file.neff",
                                   save_trace_name=profile_name + ".ntff",
                                   additional_compile_opt="--disable-dge")
        bench_func(*args)
        subprocess.run(["mv", "file.neff", profile_name + ".neff"], check=True)
    else:
        bench_func = nki.benchmark(kernel, warmup=1, iters=10)
        bench_func(*args)

    p99_us = bench_func.benchmark_result.nc_latency.get_latency_percentile(99)
    print(f"\nExecution Time: {p99_us} μs")

def main():
    name_to_kernel = {
        "naive": vector_add_naive,
        "tiled": vector_add_tiled,
        "stream": vector_add_stream,
        "transpose": matrix_transpose,
    }
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("--kernel", type=str, choices=name_to_kernel.keys(), required=True)
    parser.add_argument("-n", type=int, required=True, help="Width of vector/matrix.")
    parser.add_argument("-m", type=int, help="Height of matrix. If not specified, defaults to n.")
    parser.add_argument("--profile_name", type=str, help="Name used to save .NEFF and .NTFF files for profiling.")
    args = parser.parse_args()

    # Generate random input arrays
    kernel = name_to_kernel[args.kernel]
    if kernel == matrix_transpose:
        mat = np.random.rand(args.m or args.n, args.n).astype(np.float32)
        kernel_args = [mat]
        print(f"\nRunning {kernel.__name__} with shape {mat.shape}")
    else:
        a = np.random.rand(args.n).astype(np.float32)
        b = np.random.rand(args.n).astype(np.float32)
        kernel_args = [a, b]
        print(f"\nRunning {kernel.__name__} with shape {a.shape}")
    
    # Run the specified kernel
    benchmark_kernel(kernel, *kernel_args, profile_name=args.profile_name)
    

if __name__ == "__main__":
    main()