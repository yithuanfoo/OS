README

## Project Number/Title 

* Authors: Aidan Matkovic (a1886573), Yit Huan Foo (a1886507), Owen Muchini (a1877011)

## Overview

This project implements a multi threaded version of the merge sort algorithm using the pthread library.
The program sorts a randomly generated array using parallel merge sort, which divides the work across
multiple threeads. Compared to regular sequential merge sort that processes each step one by one, this
parallel approach significantly increases performance due to its ability to concurrently sort and merge.

## Manifest

- mergesort.h: Header file for function declarations and defining data structures
- mergesort.c: Implementation of the merge sort functions for both sequential and parallel sorting
- test-mergesort.c: Testing program for benchmarking sorting performance
- Makefile: Build configuration for compiling the program
- README.md: Contains all project documentation

## Building the project

To build the project, run the command: make
Running this command will compile all source files and create the test-mergesort executable
To clean the build after compilation, run the command: make clean

## Features and usage

The main features of this program are:
- Sequential merge sort: Performs traditional merge sorting using a single thread to provide 
baseline performance for comparison
- Parallel merge sort: Multi threaded implementation of merge sort
- Configurable threading levels: The user can specify the number of levels of thread creation (cutoff)

Once the project has been built, this command can be ran to test the program: 
./test-mergesort <array_size> <cutoff_level> <random_seed>
- array_size: Number of elements to sort
- cutoff_level: Number of threading levels
- random_seed: Seed for random number generation

For a quick test to verify merge sorting works:
./test-mergesort 1000 1 1234

To get the baseline performance of merge sorting with a single thread:
./test-mergesort 100000000 0 1234

To get parallel sorting with 2 levels of threading:
./test-mergesort 100000000 2 1234


## Testing

The program was tested for correctness and performance to make sure it ran as intended.

To test for correctness:
- The sorting accuracy was verified using small input sizes such as 100 or 1000 elements
- A fixed random seed was used to produce consistent and reproducible results
- All runs were completed sucessfully with no "sorting failed" messages

To test for performance:
- Tested with 100,000,000 elements as specified in the assignment
- Cutoff levels ranging from 0 - 8 were tested to measure the improvement in performance
- Verified that parallel merge sort achieves at least a 2 times speedup over sequential
merge sort

Level 0 (Sequential merge sort): 12.53 seconds (baseline)
Level 1 (Parallel merge sort): 6.54 seconds (1.92x speedup)
Level 2 (Parallel merge sort): 3.72 seconds (3.37x speedup)
Level 3 (Parallel merge sort): 2.06 seconds (6.08x speedup)
Level 4 (Parallel merge sort): 1.48 seconds (8.47x speedup)
Level 5 (Parallel merge sort): 1.51 seconds (8.30x speedup)
Level 6 (Parallel merge sort): 1.50 seconds (8.35x speedup)
Level 7 (Parallel merge sort): 1.49 seconds (8.41x speedup)
Level 8 (Parallel merge sort): 1.52 seconds (8.24x speedup)

As seen, at the level 2 cutoff, the program achieved a speedup of 3.37x, which is above the 2x
requirement as specified in the assignment.
It can also be seen that the performance plateaus at level 5.

## Known Bugs

There were no known bugs encountered during testing. The program performed as expected
and all tested configurations produced the intended results.

## Reflection and Self Assessment

We initially struggled with understanding the pthread APIs, especially with the pthread_create
and pthread_join functions. We did not really understand how the void pointer casting worked
and why we needed a separate buildArgs function for parallel mergesort. However, while working
on parallel mergesort, we were confused on how we were going to pass the three parameters needed
for parallel mergesort (left, right, level) into pthread_create as it only accepts a single argument
of type void* to pass to the new thread. After reviewing the textbook sections on threads and thread APIs,
we learned that this limitation is why we needed to have the separate buildArgs function. to combine all
three arguments into a single structure so that it can be passed through the void* pointer.

We also struggled with the understanding of recursion using threads as that was a foreign concept to us.
Unlike a normal recursive function that calls itself directly, parallel mergesort relies on pthread_create
to create new threads that each run another instance of the same function. Understanding that however helped
us better understand how parallelism is implemented in mergesort.

We did not encounter any major errors during implementation. However, there were minor issues such as pointer handling
when working with the pthread APIs but were quickly resolved during initial testing.

Seeing how pthread_join prevents race conditions by making sure that both child threads complete before merging really
helped reinforce our understanding of concurrency.

The development and testing process went very smoothly for us. We first tested the program with small arrays to make
sure that the program ran as expected. After verification, we scaled the testing up to 100 million elements to truly
evaluate the performance of the program. The program performed as intended, where it managed to achieve a 
speedup of up to 8.4x, confirming that the parallel mergesort implementation was effective.

## Sources Used

https://www.khanacademy.org/computing/computer-science/algorithms/merge-sort/a/overview-of-merge-sort, referenced in the construction of my_mergesort and merge functions, just for an overview of the actual merge sorting process

