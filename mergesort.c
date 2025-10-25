/**
 * This file implements parallel mergesort.
 */

#include <stdio.h>
#include <string.h> /* for memcpy */
#include <stdlib.h> /* for malloc */
#include "mergesort.h"

/* this function will be called by mergesort() and also by parallel_mergesort(). */
void merge(int leftstart, int leftend, int rightstart, int rightend){

	int l = leftstart;
	int r = rightstart;
	int i  = leftstart;

	while (l <= leftend && r <= rightend) {

		if(A[l] <= A[r]){
			B[i] = A[l];
			l++;
		} else {
			B[i] = A[r];
			r++;
		}
		i++;
	}

	while(l <= leftend){
		B[i++] = A[l++];
		}

	while(r <= rightend){
		B[i++] = A[r++];
		}

	memcpy(&A[leftstart], &B[leftstart], (rightend - leftstart + 1) * sizeof(int));


}

/* this function will be called by parallel_mergesort() as its base case. */
void my_mergesort(int left, int right){
	// base case, when each partition has 1 element
	if(left >= right) {
		return;
	}
    
	// find the midpoint to the divide the array
	int midpoint = (left+right)/2;
    
	// then can sort both halves recursively
	my_mergesort(left, midpoint);
	my_mergesort(midpoint+1, right);
    
    //combine the two results and call the actual merge sort function
	merge(left, midpoint, midpoint + 1, right);
}

/* this function will be called by the testing program. */
void * parallel_mergesort(void *arg){
		return NULL;
}

/* we build the argument for the parallel_mergesort function. */
struct argument * buildArgs(int left, int right, int level){
		return NULL;
}

