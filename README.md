# PySortingNetworks

I started this project to understand sorting networks in the context of median filtering in image processing.

## Problem statement

### Median Filtering Structure

The 2D median filtering has a specific structure that makes it advantageous to pre-sort rows or columns while
sliding the window. When moving the sliding window by one pixel, only one row or column needs to be sorted
while the other ones are already sorted.

However, this pre-condition needs to be taken into account by the sorting function for being able to take 
advantage of it. In traditional sort algorithms, a merge sort works well for the purpose. A merge sort is
not suited for parallel execution though.

Sorting networks are known to be suited for parallel execution.

### Invalid pixels

When the median filter needs to cope with invalid pixels, these pixels are assumed to have a lower value than
all valid pixels. If we want to use the same sorting function independent from the number of valid pixels in 
a sliding window, we have to ensure that the upper half of the pixels have the correct (sorted) values while
the lower half of the pixels do not need to be sorted.

If the image is fully valid, the sorting network needs to only find the median of the elements, while the order
of the lower and the upper half is not relevant. Both cases are adressed here.

## Results

### 3x3 median filtering network

(see https://github.com/cwiede/PySortingNetworks/blob/master/PySortingNetworks/median_filter_3x3.py for the code)

![image](https://user-images.githubusercontent.com/62332054/195197502-d5d9a71a-ad83-4165-b7ae-bf48493a5c53.png)

This network has **25 swap operations** for a complete sort (which is an optimal sorter for 9 elements). Sorting only the upper half 
of the pixels in a median filtering iteration need 25 - 6 - 3 = **16 swap operations**. Finding the median in an
iteration needs 25 - 6 - 5 = **14 swap operations**.

### 5x5 median filtering network

(see https://github.com/cwiede/PySortingNetworks/blob/master/PySortingNetworks/median_filter_5x5.py for the code)

![image](https://user-images.githubusercontent.com/62332054/195198336-ca0fd1c1-d610-487a-a0dc-ff56608723a1.png)

This network has **150 swap operations** for a complete sort, which is not an optimal network for 25 elements. However, 
sorting only the upper half of the pixels in a median filtering iteration need 150 - 4\*9 - 21 = **93 swap operations**.
Finding the median needs 150 - 4\*9 - 21 - 16 = **77 swap operations**.

This network was found using a greedy strategy for all comparisons following the initial sorting of the rows/columns.

## 7x7 median filtering network

(see https://github.com/cwiede/PySortingNetworks/blob/master/PySortingNetworks/median_filter_7x7.py for the code)

![image](https://user-images.githubusercontent.com/62332054/195200924-532532c2-116b-4ef3-b2b3-b9d62833eea8.png)

This network has **405 swap operations** for a complete sort, which is not an optimal network for 49 elements. However, 
sorting only the upper half of the pixels in a median filtering iteration need 405 - 6\*16 - 37 = **272 swap operations**.
Finding the median needs 405 - 5\*16 - 37 - 42 = **230 swap operations**.

This network was found by consecutively applying batcher merges to the pre-sorted values. 

