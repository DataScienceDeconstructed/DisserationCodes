#!/bin/bash
#SBATCH --cpus-per-task=8
#SBATCH --time=7-00:00:00
#SBATCH --mem-per-cpu=100M
# The above options will allocate a job with 
# 8 CPU-cores and 800 megabytes of memory for 7 days.

# The 'liposome.cpp' code should be compiled before submitting this script!
# liposome testLipo $RANDOM 80000 3.45

# The 'MD.cpp' code should be compiled before submitting this script!
# MD test
