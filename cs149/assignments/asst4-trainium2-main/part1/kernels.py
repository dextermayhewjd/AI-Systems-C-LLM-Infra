"""
CS 149: Parallel Computing, Assigment 4 Part 1

This file contains the kernel implementations for the vector addition benchmark.

For Step 1 & 2, you should look at these kernels:
    - vector_add_naive
    - vector_add_tiled
    - vector_add_stream
For Step 3, you should look at this kernel:
    - matrix_transpose

It's highly recommended to carefully read the code of each kernel and understand how
they work. For NKI functions, you can refer to the NKI documentation at:
https://awsdocs-neuron-staging.readthedocs-hosted.com/en/nki_docs_2.21_beta_class/
"""

import numpy as np
import math

import neuronxcc.nki as nki
import neuronxcc.nki.language as nl
import neuronxcc.nki.isa as nisa


"""
This is the naive implementation of a vector add kernel. 
Due to the 128 partition size limit, this kernel only works for vector sizes <=128.
"""
@nki.compiler.skip_middle_end_transformations
@nki.jit
def vector_add_naive(a_vec, b_vec):
    
    # Allocate space for the output vector in HBM
    out = nl.ndarray(shape=a_vec.shape, dtype=a_vec.dtype, buffer=nl.hbm)

    # Allocate space for the input vectors in SBUF and copy them from HBM
    a_sbuf = nl.ndarray(shape=(a_vec.shape[0], 1), dtype=a_vec.dtype, buffer=nl.sbuf)
    b_sbuf = nl.ndarray(shape=(b_vec.shape[0], 1), dtype=b_vec.dtype, buffer=nl.sbuf)
    
    nisa.dma_copy(src=a_vec, dst=a_sbuf)
    nisa.dma_copy(src=b_vec, dst=b_sbuf)

    # Add the input vectors
    res = nisa.tensor_scalar(a_sbuf, nl.add, b_sbuf)

    # Store the result into HBM
    nisa.dma_copy(src=res, dst=out)

    return out

"""
This is the tiled implementation of a vector add kernel.
We load the input vectors in chunks, add them, and then store the result
chunk into HBM. Therefore, this kernel works for any vector that is a
multiple of 128.
"""
@nki.compiler.skip_middle_end_transformations
@nki.jit
def vector_add_tiled(a_vec, b_vec):
    
    # Allocate space for the output vector in HBM
    out = nl.ndarray(shape=a_vec.shape, dtype=a_vec.dtype, buffer=nl.hbm)

    # Get the total number of vector rows
    M = a_vec.shape[0]
    
    # TODO: You should modify this variable for Step 1
    ROW_CHUNK = 1

    # Loop over the total number of chunks, we can use affine_range
    # because there are no loop-carried dependencies
    for m in nl.affine_range(M // ROW_CHUNK):

        # Allocate row-chunk sized tiles for the input vectors
        a_tile = nl.ndarray((ROW_CHUNK, 1), dtype=a_vec.dtype, buffer=nl.sbuf)
        b_tile = nl.ndarray((ROW_CHUNK, 1), dtype=b_vec.dtype, buffer=nl.sbuf)
        
        # Load a chunk of rows
        nisa.dma_copy(src=a_vec[m * ROW_CHUNK : (m + 1) * ROW_CHUNK], dst=a_tile)
        nisa.dma_copy(src=b_vec[m * ROW_CHUNK : (m + 1) * ROW_CHUNK], dst=b_tile)

        # Add the row chunks together
        res = nisa.tensor_scalar(a_tile, nl.add, b_tile)

        # Store the result chunk into HBM
        nisa.dma_copy(src=res, dst=out[m * ROW_CHUNK : (m + 1) * ROW_CHUNK])
    
    return out

"""
This is an extension of the vector_add_tiled kernel. Instead of loading tiles
of size (ROW_CHUNK, 1), we reshape the vectors into (PARTITION_DIM, FREE_DIM)
tiles. This allows us to amortize DMA transfer overhead and load many more
elements per DMA transfer.
"""
@nki.compiler.skip_middle_end_transformations
@nki.jit
def vector_add_stream(a_vec, b_vec):

    # Get the total number of vector rows
    M = a_vec.shape[0]

    # TODO: You should modify this variable for Step 2a
    FREE_DIM = 2

    # The maximum size of our Partition Dimension
    PARTITION_DIM = 128

    a_vec_re = a_vec.reshape((PARTITION_DIM, M // PARTITION_DIM))
    b_vec_re = b_vec.reshape((PARTITION_DIM, M // PARTITION_DIM))
    out = nl.ndarray(shape=a_vec_re.shape, dtype=a_vec_re.dtype, buffer=nl.hbm)

    # Loop over the total number of tiles
    for m in nl.affine_range(M // (PARTITION_DIM * FREE_DIM)):

        # Allocate space for a reshaped tile
        a_tile = nl.ndarray((PARTITION_DIM, FREE_DIM), dtype=a_vec.dtype, buffer=nl.sbuf)
        b_tile = nl.ndarray((PARTITION_DIM, FREE_DIM), dtype=b_vec.dtype, buffer=nl.sbuf)

        # Load the input tiles
        nisa.dma_copy(src=a_vec_re[:, m * FREE_DIM : (m + 1) * FREE_DIM], dst=a_tile)
        nisa.dma_copy(src=b_vec_re[:, m * FREE_DIM : (m + 1) * FREE_DIM], dst=b_tile)

        # Add the tiles together. Note that we must switch to tensor_tensor instead of tensor_scalar
        res = nisa.tensor_tensor(a_tile, b_tile, op=nl.add)

        # Store the result tile into HBM
        nisa.dma_copy(src=res, dst=out[:, m * FREE_DIM : (m + 1) * FREE_DIM])

    # Reshape the output vector into its original shape
    out = out.reshape(a_vec.shape)

    return out

"""
This kernel implements a simple 2D matrix transpose.
It uses a tile-based approach along with NKI's built-in transpose kernel,
which only works on tiles of size <= 128x128.
"""
@nki.compiler.skip_middle_end_transformations
@nki.jit
def matrix_transpose(a_tensor):
    M, N = a_tensor.shape
    out = nl.ndarray((N, M), dtype=a_tensor.dtype, buffer=nl.hbm)
    tile_dim = nl.tile_size.pmax  # this should be 128

    assert M % tile_dim == N % tile_dim == 0, "Matrix dimensions not divisible by tile dimension!"

    # TODO: Your implementation here. The only compute instruction you should use is `nisa.nc_transpose`.

    return out
