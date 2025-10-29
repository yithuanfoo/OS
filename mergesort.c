/**
 * This file implements parallel mergesort.
 */

#include "mergesort.h"

#include <stdio.h>
#include <stdlib.h> /* for malloc */
#include <string.h> /* for memcpy */

/* this function will be called by mergesort() and also by parallel_mergesort().
 */
void merge(int leftstart, int leftend, int rightstart, int rightend) {
  // indices for subarrays and new b array
  int l = leftstart;
  int r = rightstart;
  int i = leftstart;

  // merge a subarray to new b array
  while (l <= leftend && r <= rightend) {
    if (A[l] <= A[r]) {
      B[i] = A[l];
      l++;
    } else {
      B[i] = A[r];
      r++;
    }
    i++;
  }

  // copy left over elements from left subarray
  while (l <= leftend) {
    B[i++] = A[l++];
  }

  // copy left over elements from right subarray
  while (r <= rightend) {
    B[i++] = A[r++];
  }

  // copy the sorted elements back to the original array
  size_t count = (size_t)((rightend - leftstart + 1) * sizeof(int));
  memcpy(&A[leftstart], &B[leftstart], count);
}

/* this function will be called by parallel_mergesort() as its base case. */
void my_mergesort(int left, int right) {
  // base case, when each partition has 1 element
  if (left >= right) {
    return;
  }

  // find the midpoint to the divide the array
  int midpoint = (left + right) / 2;

  // then can sort both halves recursively
  my_mergesort(left, midpoint);
  my_mergesort(midpoint + 1, right);

  // combine the two results and call the actual merge sort function
  merge(left, midpoint, midpoint + 1, right);
}

/* this function will be called by the testing program. */
void *parallel_mergesort(void *arg) {
  // Cast the void pointer back to struct argument pointer
  struct argument *args = (struct argument *)arg;

  // Extract the values from the argument
  int left = args->left;
  int right = args->right;
  int level = args->level;

  // Free the argument memory now that we've extracted the values
  free(arg);

  // Base case 1: if the subarray has 1 or 0 elements, it's already sorted
  if (left >= right) {
    return NULL;
  }

  // Base case 2: if we've reached the cutoff level, use sequential mergesort
  if (level >= cutoff) {
    my_mergesort(left, right);
    return NULL;
  }

  // Recursive case: create threads for parallel sorting

  // Find the midpoint to divide the array
  int midpoint = (left + right) / 2;

  // Build arguments for the left and right child threads
  // Level is incremented by 1 for the next level of the tree
  struct argument *left_arg = buildArgs(left, midpoint, level + 1);
  struct argument *right_arg = buildArgs(midpoint + 1, right, level + 1);

  // Create two threads to handle each half
  pthread_t left_thread, right_thread;

  // create a thread for the left and right child threads
  int rc1 = pthread_create(&left_thread, NULL, parallel_mergesort, left_arg);
  int rc2 = pthread_create(&right_thread, NULL, parallel_mergesort, right_arg);

  // Check return codes if the threads were created successfully
  if (rc1 != 0) {
    fprintf(stderr, "ERROR: pthread_create failed for left thread\n");
    exit(1);
  }
  if (rc2 != 0) {
    fprintf(stderr, "ERROR: pthread_create failed for right thread\n");
    exit(1);
  }

  // Wait for both threads to finish so both halves are sorted before we merge
  int rc3 = pthread_join(left_thread, NULL);
  int rc4 = pthread_join(right_thread, NULL);

  // Check join return codes if the threads were joined successfully
  if (rc3 != 0) {
    fprintf(stderr, "ERROR: pthread_join failed for left thread\n");
    exit(1);
  }
  if (rc4 != 0) {
    fprintf(stderr, "ERROR: pthread_join failed for right thread\n");
    exit(1);
  }

  // Merge the two halves together
  merge(left, midpoint, midpoint + 1, right);

  return NULL;
}

/* we build the argument for the parallel_mergesort function. */
struct argument *buildArgs(int left, int right, int level) {
  // Allocate memory for the argument structure
  struct argument *arg = (struct argument *)malloc(sizeof(struct argument));

  // Check if malloc succeeded
  if (arg == NULL) {
    fprintf(stderr, "ERROR: malloc failed in buildArgs\n");
    exit(1);
  }

  // Fill in the fields
  arg->left = left;
  arg->right = right;
  arg->level = level;

  return arg;
}
