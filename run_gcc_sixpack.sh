#!/bin/bash

# Traces to test
traces=("gcc" "sixpack")
algorithms=("rand" "lru" "clock")

# Loop through traces
for trace in "${traces[@]}"; do
  # Loop through algorithms
  for algo in "${algorithms[@]}"; do

    # --- Shortage region: 2–20 (step = 1) ---
    for i in {2..20}; do
      python memsim.py ${trace}.trace $i $algo quiet >> ${trace}_${algo}_shortage.txt
    done

    # --- Working set region: 20–200 (step = 10) ---
    for i in {20..200..10}; do
      python memsim.py ${trace}.trace $i $algo quiet >> ${trace}_${algo}_workingset.txt
    done

    # --- Excess region: 200–500 (step = 50) ---
    for i in {200..500..50}; do
      python memsim.py ${trace}.trace $i $algo quiet >> ${trace}_${algo}_excess.txt
    done

  done
done
