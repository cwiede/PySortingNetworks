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

If the image is fully valid, a median selection network might be better suited (this is not part of this project)

## Results

### 3x3 median filtering network

(see https://github.com/cwiede/PySortingNetworks/blob/master/PySortingNetworks/median_filter_3x3.py for the code)

      0: ─┊┬─┬──────┊────┬────┊────┬──
      1: ─┊┼┬┴──────┊──┬─┼────┊┬───┼┬─
      2: ─┊┴┴───────┊┬─┼─┼─┬─┬┊┼──┬┼┼┬
      3: ─┊───┬─┬───┊┼─┼─┼┬┼─┼┊┼──┼┴┴┴
      4: ─┊───┼┬┴───┊┼─┼┬┼┼┼─┼┊┴┬─┴───
      5: ─┊───┴┴────┊┼┬┼┼┼┼┴┬┼┊─┼┬────
      6: ─┊──────┬─┬┊┼┼┼┼┴┴─┼┴┊─┴┴────
      7: ─┊──────┼┬┴┊┼┼┴┴───┴─┊───────
      8: ─┊──────┴┴─┊┴┴───────┊───────

This network has **25 swap operations** for a complete sort (which is an optimal sorter for 9 elements) and sorting only the upper half 
of the pixels in a median filtering iteration need 25 - 6 - 3 = **16 swap operations**.

### 5x5 median filtering network

(see https://github.com/cwiede/PySortingNetworks/blob/master/PySortingNetworks/median_filter_5x5.py for the code)

      0: ─┊┬──┬──┬─┬────────────────────────────────────┊────────┬───────────┬┬──────────────────────────────────────────────────────────────────────┬────────────
      1: ─┊┼─┬┼─┬┼─┴────────────────────────────────────┊──────┬─┼───────────┼┼──┬┬───────────────────────────────────────────────────────────────┬──┼────────┬──┬
      2: ─┊┼┬┼┴─┴┼┬─────────────────────────────────────┊────┬─┼─┼───────────┼┼──┼┼──┬┬───────────────────────────┬───────────────────────────────┼──┼┬───────┼──┴
      3: ─┊┼┼┴─┬─┴┴─────────────────────────────────────┊──┬─┼─┼─┼───────────┼┼──┼┼──┼┼──┬┬────────────────────┬──┼────┬──────────────────────────┼┬─┼┼──────┬┴┬──
      4: ─┊┴┴──┴────────────────────────────────────────┊┬─┼─┼─┼─┼───────────┼┼──┼┼──┼┼──┼┼──┬┬──────┬───────┬─┼──┼────┼──────────────────────────┼┼─┼┼┬─────┴─┴┬─
      5: ─┊─────────┬──┬──┬─┬───────────────────────────┊┼─┼─┼─┼─┼─┬─────────┼┼┬─┼┼──┼┼──┼┼──┼┼──────┼───────┼─┼──┼────┼──────────────────────────┼┼─┴┴┴┬───────┴─
      6: ─┊─────────┼─┬┼─┬┼─┴───────────────────────────┊┼─┼─┼─┼─┼─┼─┬───────┼┼┼─┼┼┬─┼┼──┼┼──┼┼──────┼───────┼─┼──┼────┼──────────────────────────┴┴┬───┴┬────────
      7: ─┊─────────┼┬┼┴─┴┼┬────────────────────────────┊┼─┼─┼─┼─┼─┼─┼─┬─────┼┼┼─┼┼┼─┼┼┬─┼┼──┼┼──────┼───────┼─┼──┴┬───┼────────────────────────┬───┴────┴┬───────
      8: ─┊─────────┼┼┴─┬─┴┴────────────────────────────┊┼─┼─┼─┼─┼─┼─┼─┼─┬───┼┼┼─┼┼┼─┼┼┼─┼┼┬─┼┼──────┼───────┼─┴┬──┼───┼─────────────────────┬──┴┬────────┴┬──────
      9: ─┊─────────┴┴──┴───────────────────────────────┊┼─┼─┼─┼─┼─┼─┼─┼─┼─┬─┼┼┼─┼┼┼─┼┼┼─┼┼┼─┼┼┬─────┴┬──────┼──┼──┼───┴┬────────────────────┴┬──┴─────────┴┬─────
     10: ─┊──────────────────┬──┬──┬─┬──────────────────┊┼─┼─┼─┼─┼┬┼─┼─┼─┼─┼─┴┼┴┬┼┼┼─┼┼┼─┼┼┼─┼┼┼──────┼──────┴┬─┼──┴┬───┼─────────────────┬───┴┬────────────┴─────
     11: ─┊──────────────────┼─┬┼─┬┼─┴──────────────────┊┼─┼─┼─┼┬┼┼┼─┼─┼─┼─┼──┼─┼┴┼┴┬┼┼┼─┼┼┼─┼┼┼──────┼───────┼─┴┬──┼───┴┬────────────────┴┬───┴──────────────────
     12: ─┊──────────────────┼┬┼┴─┴┼┬───────────────────┊┼─┼─┼┬┼┼┼┼┼─┼─┼─┼─┼──┼─┼─┼─┼┴┼┴┬┼┼┼─┼┼┼──────┼───────┼──┼──┴┬───┴┬────────────┬───┴┬─────────────────────
     13: ─┊──────────────────┼┼┴─┬─┴┴───────────────────┊┼─┼┬┼┼┼┼┼┼┼─┼─┼─┼─┼──┼─┼─┼─┼─┼─┼┴┼┴┬┼┼┼────┬─┼───────┼──┴───┼────┴┬──────┬────┴┬───┴─────────────────────
     14: ─┊──────────────────┴┴──┴──────────────────────┊┼┬┼┼┼┼┼┼┼┼┼─┼─┼─┼─┼──┼─┼─┼─┼─┼─┼─┼─┼┴┼┴┬──┬┼─┼───────┴──────┴┬────┼──────┴┬────┴┬────────────────────────
     15: ─┊───────────────────────────┬──┬──┬─┬─────────┊┼┼┼┼┼┼┼┼┼┼┴┬┼─┼─┼─┼──┴─┴─┼─┼─┼─┼─┼─┼─┼─┼──┼┼─┴┬──────────────┼────┴┬──────┴┬─┬──┴────────────────────────
     16: ─┊───────────────────────────┼─┬┼─┬┼─┴─────────┊┼┼┼┼┼┼┼┼┼┼─┼┴┬┼─┼─┼──────┴─┴─┼─┼─┼─┼─┼─┼──┼┴──┼──────────────┼─────┴┬──────┴┬┴───────────────────────────
     17: ─┊───────────────────────────┼┬┼┴─┴┼┬──────────┊┼┼┼┼┼┼┼┼┼┼─┼─┼┴┬┼─┼──────────┴─┴─┼─┼─┼─┼──┼───┼──────────────┴──────┴┬──┬───┴────────────────────────────
     18: ─┊───────────────────────────┼┼┴─┬─┴┴──────────┊┼┼┼┼┼┼┼┼┼┼─┼─┼─┼┴┬┼──────────────┴─┴─┼─┼──┼───┼┬─────────────────────┴┬─┴────────────────────────────────
     19: ─┊───────────────────────────┴┴──┴─────────────┊┼┼┼┼┼┼┼┼┼┼─┼─┼─┼─┼┴┬─────────────────┴─┴┬─┼───┼┼┬─────────────────────┴┬─────────────────────────────────
     20: ─┊────────────────────────────────────┬──┬──┬─┬┊┼┼┼┼┼┼┼┼┴┴─┴─┼─┼─┼─┼────────────────────┼─┴───┼┼┴┬─┬───────────────────┴─────────────────────────────────
     21: ─┊────────────────────────────────────┼─┬┼─┬┼─┴┊┼┼┼┼┼┼┴┴─────┴─┼─┼─┼────────────────────┼─────┴┴─┴┬┴─────────────────────────────────────────────────────
     22: ─┊────────────────────────────────────┼┬┼┴─┴┼┬─┊┼┼┼┼┴┴─────────┴─┼─┼────────────────────┴┬────────┴──────────────────────────────────────────────────────
     23: ─┊────────────────────────────────────┼┼┴─┬─┴┴─┊┼┼┴┴─────────────┴─┼─────────────────────┴───────────────────────────────────────────────────────────────
     24: ─┊────────────────────────────────────┴┴──┴────┊┴┴─────────────────┴─────────────────────────────────────────────────────────────────────────────────────

This network has **150 swap operations** for a complete sort, which is not an optimal network for 25 elements. However, 
sorting only the upper half of the pixels in a median filtering iteration need 150 - 4*9 - 21 = **93 swap operations**.

This network was found using a greedy strategy for all comparisons following the initial sorting of the rows/columns.

## 7x7 median filtering network

(see https://github.com/cwiede/PySortingNetworks/blob/master/PySortingNetworks/median_filter_7x7.py for the code)

      0: ─┊──┬──┬──────┬──┬────────────────────────────────────────────────────────────────────────────────────────────────┊───────────────────────────────────────────────────────────────────────────────────────────────────┬────────────────────────────────────┬┬───────────────────────────────────────────────────┬┬──────────┬───────────────────────────────────────────────────────────────────────────────────────────
      1: ─┊─┬┼──┼─┬──┬─┼──┴────────────────────────────────────────────────────────────────────────────────────────────────┊─────────────────────────────────────────────────────────────────────────────────────────┬─────────┼───────────┬────────────────────────┴┼───┬─────────────────────────┬─────────────────────┼┼──────────┼┬──────────────────────┬─────────────────────────────────────────────────────────────┬────┬
      2: ─┊┬┼┼──┴┬┼──┴┬┼─┬─────────────────────────────────────────────────────────────────────────────────────────────────┊─────────────────────────────────────────────────────────────────────────────────────────┼──┬──────┼─────────┬─┼┬┬─────────────────────┬─┼───┼─────────────────────────┼─────────────────────┴┼──────────┼┴┬─────────────────────┼───────────────────────────────────────────────────────┬─────┼──┬─┴
      3: ─┊┼┼┼─┬─┼┴─┬─┼┴─┴─────────────────────────────────────────────────────────────────────────────────────────────────┊────────────────────────────────────────────────────────────────────────────────────────┬┼──┼──────┼────┬────┼─┴┴┼─────────┬───────────┼─┼───┼────────────────────┬────┴┬─────────────────────┼──────────┼─┼─────────────────────┼───┬───────────────────────────────────────────────────┼─┬───┼┬─┼┬─
      4: ─┊┼┼┴┬┼─┴──┴─┼─┬──────────────────────────────────────────────────────────────────────────────────────────────────┊───────────────────────────────────────────────────────────────────────────────────────┬┼┼──┼──────┼┬───┼────┴┬──┼──┬──────┼───────────┼─┼───┼────────────┬───────┼──┬──┴┬──────────────────┬─┼──────────┴─┼─────────────────────┼───┼───────────────────────────────────────────────────┼─┼───┼┼─┴┴─
      5: ─┊┼┴─┼┴───┬──┴─┴──────────────────────────────────────────────────────────────────────────────────────────────────┊──────────────────────────────────────────────────────────────────────────────────────┬┼┼┼┬─┼──────┼┼───┼┬────┴──┼──┼──────┼──┬────────┼─┼───┼────────────┼─┬─────┼┬─┼┬──┼──────────────────┼─┼────────────┼────┬────────────────┼───┼─────────────────────────────────────────────┬─────┼─┼───┴┴┬───
      6: ─┊┴──┴────┴───────────────────────────────────────────────────────────────────────────────────────────────────────┊──────────────────────────────────────────────────────────────────────────────────────┼┼┼┼┼─┼┬─────┼┼┬──┼┼┬┬┬────┼──┼──────┼──┼────────┴─┼───┼────────────┼─┼─────┼┼─┴┴──┼───────┬──────────┼─┼────────┬───┼────┼────────────────┼───┼─────────────────────────────────────────────┼─────┴┬┼─────┴───
      7: ─┊──────────────────┬──┬──────┬──┬────────────────────────────────────────────────────────────────────────────────┊──────────────────────────────────────────────────────────────────────────────────────┼┼┼┼┼─┼┼─────┼┼┼──┴┴┴┼┼────┼──┼────┬─┼──┼──────────┼───┼─────┬──────┼─┼─────┴┴┬────┼───────┼──────────┼─┼────────┼───┼────┼─────┬──────────┼───┼────────────────────────────────────────┬────┼──────┼┴┬─┬──────
      8: ─┊─────────────────┬┼──┼─┬──┬─┼──┴────────────────────────────────────────────────────────────────────────────────┊──────────────────────────────────────────────────────────────────────────────────────┼┼┼┼┼─┼┼─────┴┴┴┬┬───┼┼────┼──┼────┼─┼──┼──────────┼┬──┼─────┼──────┴┬┼───────┴────┼──┬────┼──────────┼─┼──────┬─┼┬──┼────┼─────┼──────────┼───┼────────────────────────────────────────┼────┼──────┴─┼─┴──────
      9: ─┊────────────────┬┼┼──┴┬┼──┴┬┼─┬─────────────────────────────────────────────────────────────────────────────────┊──────────────────────────────────────────────────────────────────────────────────────┼┼┼┴┴┬┼┼────────┴┼───┼┼────┼──┼───┬┼─┼──┼──────────┼┼──┼┬────┼───────┼┴┬───┬───────┼──┼────┼──────────┼─┼──────┼─┼┼──┼────┼──┬──┼──────────┼───┼────────────────────────────┬───────────┼────┼┬───────┴┬───────
     10: ─┊────────────────┼┼┼─┬─┼┴─┬─┼┴─┴─────────────────────────────────────────────────────────────────────────────────┊──────────────────────────────────────────────────────────────────────────────────────┼┼┼──┼┴┴┬─┬─┬────┼───┼┼────┼┬─┼───┼┼─┼──┼───────┬──┼┼──┼┼────┼───────┴─┼───┴───────┼──┼────┼──┬───────┼─┼──────┼─┼┼──┼────┼──┼──┼──────────┼───┼────────────────────────┬───┼─────────┬─┼────┼┼──┬─────┴───────
     11: ─┊────────────────┼┼┴┬┼─┴──┴─┼─┬──────────────────────────────────────────────────────────────────────────────────┊──────────────────────────────────────────────────────────────────────────────────────┼┼┴──┴──┼─┴┬┼────┼───┼┼────┼┼─┼───┼┼─┼┬─┼───────┼──┼┼──┼┼────┼┬────────┴┬──────────┼──┼────┼──┼───────┼─┼──────┼─┼┼──┼────┼──┼──┼──┬───────┼───┼────────────────────────┼───┼─┬───────┼─┼┬───┼┼┬─┼┬────────────
     12: ─┊────────────────┼┴─┼┴───┬──┴─┴──────────────────────────────────────────────────────────────────────────────────┊──────────────────────────────────────────────────────────────────────────────────────┼┴──────┴┬─┼┼────┼───┼┼────┼┼─┼┬──┼┼─┼┼─┼───────┼──┼┼┬─┼┼────┼┼───┬─────┴┬┬────────┼──┼────┼──┼───────┴─┼──────┼─┼┴──┼────┼──┼──┼──┼───────┼───┼────────────────────────┼───┼─┼───────┼─┼┼───┼┼┼─┴┴────────────
     13: ─┊────────────────┴──┴────┴───────────────────────────────────────────────────────────────────────────────────────┊──────────────────────────────────────────────────────────────────────────────────────┴────────┴─┼┼────┼───┼┼────┼┼─┼┼──┼┼─┼┼─┼┬──────┼──┼┼┼─┼┼┬───┼┼┬──┼┬─────┼┼────────┼──┼────┼──┼────┬────┼──────┼─┼───┼────┼──┼──┼──┼───────┼───┼─────────────────┬──────┼───┼─┼───────┼─┼┼───┴┴┴┬──────────────
     14: ─┊──────────────────────────────────┬──┬──────┬──┬────────────────────────────────────────────────────────────────┊──────────────────────────────────────────────────────────────────────────┬──────────┬───────────┼┼────┼───┼┴────┼┼─┼┼──┼┼─┼┼─┼┼──────┴──┼┼┼─┼┼┼───┼┼┼──┴┴─────┼┼────────┼──┼──┬─┼──┼────┼────┼───┬──┼─┴───┼────┼──┼──┼──┼───────┼───┼─────────────────┼──────┼───┼─┼───────┴┬┼┼──────┴──────────────
     15: ─┊─────────────────────────────────┬┼──┼─┬──┬─┼──┴────────────────────────────────────────────────────────────────┊──────────────────────────────────────────────────────────────────┬───────┼────────┬─┴───────────┼┼────┼───┼─────┼┼─┼┼──┼┼─┼┼─┼┼─────────┼┼┼─┼┼┼───┴┴┴┬────────┼┼────────┼──┼──┼─┼──┼───┬┼────┼───┼──┼─────┼────┼──┼──┼──┼───────┼───┼───────────┬─────┼──────┼───┼─┼────────┼┴┴┬─┬──────────────────
     16: ─┊────────────────────────────────┬┼┼──┴┬┼──┴┬┼─┬─────────────────────────────────────────────────────────────────┊──────────────────────────────────────────────────────────────────┼──┬────┼──────┬─┼┬────────────┼┼────┼───┼─────┼┼─┼┼──┼┼─┼┼─┼┼─────────┴┴┴┬┼┼┼──────┴┬───────┼┼────────┼──┼──┼─┼──┼───┼┼────┼┬──┼──┴┬────┼────┼──┼──┼──┼───────┼───┼───────────┼─────┼──────┼───┼─┼────────┴──┼─┴──────────────────
     17: ─┊────────────────────────────────┼┼┼─┬─┼┴─┬─┼┴─┴─────────────────────────────────────────────────────────────────┊─────────────────────────────────────────────────────────────────┬┼──┼────┼───┬──┼─┴┴────────────┼┼────┼───┼─────┼┼─┼┼──┼┼─┼┼─┼┼────────────┼┴┴┴┬─┬────┼───────┼┼────────┼──┼──┼─┼──┼───┼┼────┼┼──┼───┼────┼────┼──┼──┼──┼───────┼┬──┼───────────┼─────┼──────┼───┴┬┼───────────┴┬───────────────────
     18: ─┊────────────────────────────────┼┼┴┬┼─┴──┴─┼─┬──────────────────────────────────────────────────────────────────┊────────────────────────────────────────────────────────────────┬┼┼──┼────┼┬──┼──┴┬──────────────┼┼────┼───┼─────┴┴┬┼┼──┼┼─┼┼─┼┼────────────┴───┼─┴────┼───────┼┼────────┼──┼──┼─┼──┼───┼┼────┼┼──┼───┼────┼┬───┼──┼──┼──┼───────┼┼──┼───────────┼─────┼──────┴┬─┬─┼┼────────────┴───────────────────
     19: ─┊────────────────────────────────┼┴─┼┴───┬──┴─┴──────────────────────────────────────────────────────────────────┊───────────────────────────────────────────────────────────────┬┼┼┼┬─┼────┼┼──┼┬──┴──────────────┼┼────┼───┼───────┼┼┼──┼┼─┴┴┬┼┼────────────────┴┬─────┼───────┼┼────────┼──┼──┼─┼──┼───┼┼────┼┼──┼───┼────┼┼───┼──┼──┼──┼───────┼┼──┼┬──────────┼─────┼───────┼─┼─┼┴┬───┬─┬─────────────────────────
     20: ─┊────────────────────────────────┴──┴────┴───────────────────────────────────────────────────────────────────────┊───────────────────────────────────────────────────────────────┼┼┼┼┼─┼┬───┼┼┬─┼┼┬────────────────┼┼────┼───┼───────┼┴┴┬─┼┼┬──┼┼┼─────────────────┴─────┼───────┼┼────────┼┬─┼──┼─┼──┼───┼┼─┬──┼┼──┼───┴────┼┼───┼──┼──┼──┼───────┼┼──┼┼──────────┼─────┼───────┼─┴─┼─┼───┼─┴─────────────────────────
     21: ─┊──────────────────────────────────────────────────┬──┬──────┬──┬────────────────────────────────────────────────┊───────────────────────────────────────────────────────────────┼┼┼┼┼─┼┼───┼┼┼─┴┴┴────────────────┼┼────┼───┼───────┼──┼─┼┼┼──┼┴┴┬──┬─┬─────────────────┼───────┼┼────────┼┼─┼──┼─┼──┼───┼┼─┼──┼┼──┼────────┼┼───┼┬─┼──┼──┼───────┼┼──┼┼──────────┼─────┼┬──────┼───┴─┼───┴┬──────────────────────────
     22: ─┊─────────────────────────────────────────────────┬┼──┼─┬──┬─┼──┴────────────────────────────────────────────────┊───────────────────────────────────────────────────────────────┼┼┼┼┼─┼┼───┴┴┴┬───────────────────┼┼────┼───┴───────┴──┼─┼┼┴──┼──┼──┼─┴─────────────────┼───────┼┼────────┼┼─┼──┼─┼┬─┼───┼┼─┼──┼┼──┼┬───────┼┼───┼┼─┼──┼──┼───────┼┼──┼┼──────────┼─────┼┼──────┴┬────┼────┴──────────────────────────
     23: ─┊────────────────────────────────────────────────┬┼┼──┴┬┼──┴┬┼─┬─────────────────────────────────────────────────┊───────────────────────────────────────────────────────────────┼┼┼┴┴┬┼┼──────┴───────────────────┼┼────┼──────────────┼─┼┴───┴──┼──┴┬──────────────────┼───────┼┼────────┼┼─┼──┼─┼┼─┼───┼┼─┼──┼┼──┼┼───────┼┼───┼┼─┼──┼┬─┼───────┼┼──┼┼──────────┼┬────┼┼───────┼────┴┬─┬────────────────────────────
     24: ─┊────────────────────────────────────────────────┼┼┼─┬─┼┴─┬─┼┴─┴─────────────────────────────────────────────────┊───────────────────────────────────────────────────────────────┼┼┼──┼┴┴┬─┬───────────────────────┼┼────┴──────────────┴┬┼───────┼───┴──────────────────┼───────┼┼────────┼┼─┼┬─┼─┼┼─┼───┼┼─┼──┼┼┬─┼┼┬──────┼┼───┼┼─┼──┼┼─┼───────┼┼──┼┼──────────┼┼────┼┼───────┴─────┼─┴────────────────────────────
     25: ─┊────────────────────────────────────────────────┼┼┴┬┼─┴──┴─┼─┬──────────────────────────────────────────────────┊───────────────────────────────────────────────────────────────┼┼┴──┴──┼─┴───────────────────────┼┼────────────────────┼┴───────┴┬┬────────────────────┼───────┼┼────────┼┼─┼┼─┼─┼┼─┼───┼┼─┼──┼┼┼─┼┼┼──────┼┼───┼┼─┼┬─┼┼─┼───────┼┼┬─┼┼──────────┼┼────┼┼┬────────────┴┬─────────────────────────────
     26: ─┊────────────────────────────────────────────────┼┴─┼┴───┬──┴─┴──────────────────────────────────────────────────┊───────────────────────────────────────────────────────────────┼┴──────┴┬────────────────────────┼┴────────────────────┴─────────┼┴────────────────────┼───────┼┼────────┼┼─┼┼─┼─┼┼─┼┬──┼┼─┼──┼┼┼─┼┼┼──────┼┼┬──┼┼─┼┼─┼┼─┼───────┼┼┼─┼┼────────┬─┼┼────┼┼┼──┬──────────┴─────────────────────────────
     27: ─┊────────────────────────────────────────────────┴──┴────┴───────────────────────────────────────────────────────┊───────────────────────────────────────────────────────────────┴────────┴────────────────────────┴───────────────────────────────┴─────────────────────┼───────┼┼────────┼┼─┼┼─┼─┼┼─┼┼──┼┼─┼──┼┼┼─┼┼┼──────┼┼┼──┼┼─┼┼─┼┼─┼┬──────┼┼┼─┼┼┬───────┼─┼┼┬───┼┼┼┬─┼┬───────────────────────────────────────
     28: ─┊──────────────────────────────────────────────────────────────────┬──┬──────┬──┬────────────────────────────────┊───────────┬───────────────────┬┬────────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────────┼───────┼┴────────┼┼─┼┼─┼─┼┼─┼┼──┼┼─┴──┼┼┼─┼┼┴──────┼┼┼──┼┼─┼┼─┼┼─┼┼──────┼┼┼─┼┼┼───────┼─┼┼┼───┼┼┼┼─┴┴───────────────────────────────────────
     29: ─┊─────────────────────────────────────────────────────────────────┬┼──┼─┬──┬─┼──┴────────────────────────────────┊───┬───────┼───────────┬───────┴┼───┬──────────────────────┬─┼┬────────────────────────────────────────────────────────────────────────────────────────┼───────┼─────────┼┼─┼┼─┼─┼┼─┼┼──┼┼────┼┼┼─┼┼───────┼┼┼──┼┼─┼┼─┼┼─┼┼──────┼┼┼─┼┼┼───────┼─┼┼┼───┴┴┴┴┬─────────────────────────────────────────
     30: ─┊────────────────────────────────────────────────────────────────┬┼┼──┴┬┼──┴┬┼─┬─────────────────────────────────┊───┼──┬────┼───────┬───┼┬──┬──┬─┼───┼──────────────────────┼─┴┴────────────────────────────────────────────────────────────────────────────────────────┼───────┼─────────┼┼─┼┼─┼─┼┼─┼┼──┼┼────┼┼┼─┴┴───────┼┼┼──┼┼─┼┼─┼┼─┼┼──────┼┼┼─┼┼┼───────┴┬┼┼┼───────┴─────────────────────────────────────────
     31: ─┊────────────────────────────────────────────────────────────────┼┼┼─┬─┼┴─┬─┼┴─┴─────────────────────────────────┊──┬┼──┼────┼───┬───┼───┴┴┬─┼──┼─┼───┼─────────────────┬────┴┬──────────────────────────────────────────────────────────────────────────────────────────┼───────┼─────────┼┼─┼┼─┼─┼┼─┼┼──┼┼────┼┼┼──────────┼┼┼──┼┼─┼┼─┼┼─┼┼──────┼┼┼─┼┼┼────────┼┴┴┴┬─┬──────────────────────────────────────────────
     32: ─┊────────────────────────────────────────────────────────────────┼┼┴┬┼─┴──┴─┼─┬──────────────────────────────────┊─┬┼┼──┼────┼┬──┼───┴┬┬───┼─┼──┼─┼───┼───────────┬─────┼──┬──┴──────────────────────────────────────────────────────────────────────────────────────────┼───────┼─────────┼┼─┼┼─┼─┼┼─┼┼──┼┼────┴┴┴┬─────────┼┼┼──┼┼─┼┼─┼┼─┼┼──────┼┼┼─┼┼┼────────┴───┼─┴──────────────────────────────────────────────
     33: ─┊────────────────────────────────────────────────────────────────┼┴─┼┴───┬──┴─┴──────────────────────────────────┊┬┼┼┼┬─┼────┼┼──┼┬───┴┼───┼─┼──┼─┼───┼───────────┼─┬───┼┬─┼┬────────────────────────────────────────────────────────────────────────────────────────────┼───────┼─────────┼┼─┼┼─┼─┼┼─┼┼──┼┼───────┼─────────┼┼┼──┼┼─┼┼─┼┼─┼┼──────┴┴┴┬┼┼┼────────────┴┬───────────────────────────────────────────────
     34: ─┊────────────────────────────────────────────────────────────────┴──┴────┴───────────────────────────────────────┊┼┼┼┼┼─┼┬───┼┼┬─┼┼┬┬──┼───┼─┼──┴─┼───┼───────────┼─┼───┼┼─┴┴────────────────────────────────────────────────────────────────────────────────────────────┼───────┼─────────┼┼─┼┼─┼─┼┼─┼┼──┼┼───────┼─────────┴┴┴┬─┼┼─┼┼─┼┼─┼┼─────┬───┼┼┼┼─────────────┴───────────────────────────────────────────────
     35: ─┊──────────────────────────────────────────────────────────────────────────────────┬──┬──────┬──┬────────────────┊┼┼┼┼┼─┼┼───┼┼┼─┴┴┴┼──┼───┼─┼────┼───┼─────┬─────┼─┼───┴┴┬──────────────────────────────────────────────────────────────────────────────────────────────┼───────┼─────────┼┼─┼┼─┼─┼┼─┼┼──┼┼───────┼────────────┼─┼┼─┼┼─┼┼─┼┼─────┼───┼┴┴┴┬───┬─┬──────────────────────────────────────────────────────
     36: ─┊─────────────────────────────────────────────────────────────────────────────────┬┼──┼─┬──┬─┼──┴────────────────┊┼┼┼┼┼─┼┼───┴┴┴┬───┼──┼───┼─┼────┼┬──┼─────┼─────┴┬┼─────┴──────────────────────────────────────────────────────────────────────────────────────────────┼───────┼─────────┴┴┬┼┼─┼─┼┼─┼┼──┼┼───────┴────────────┼─┼┼─┼┼─┼┼─┼┼─────┴───┼───┼───┼─┴──────────────────────────────────────────────────────
     37: ─┊────────────────────────────────────────────────────────────────────────────────┬┼┼──┴┬┼──┴┬┼─┬─────────────────┊┼┼┼┴┴┬┼┼──────┴───┼──┼───┼─┼────┼┼──┼┬────┼──────┼┴┬─┬─────────────────────────────────────────────────────────────────────────────────────────────────┼───────┼───────────┼┼┼─┼─┼┼─┼┼──┼┼────────────────────┼─┴┴┬┼┼─┼┼─┼┼─────────┴───┼───┴┬───────────────────────────────────────────────────────
     38: ─┊────────────────────────────────────────────────────────────────────────────────┼┼┼─┬─┼┴─┬─┼┴─┴─────────────────┊┼┼┼──┼┴┴┬─┬───────┼──┼───┼─┼┬┬──┼┼──┼┼────┼──────┴─┼─┴─────────────────────────────────────────────────────────────────────────────────────────────────┼───────┼───────────┼┼┼─┼─┴┴┬┼┼──┼┼────────────────────┴┬──┼┼┼─┼┼─┼┼─────────────┼────┴───────────────────────────────────────────────────────
     39: ─┊────────────────────────────────────────────────────────────────────────────────┼┼┴┬┼─┴──┴─┼─┬──────────────────┊┼┼┴──┴──┼─┴───────┼──┼───┼┬┼┼┼──┼┼──┼┼────┼┬───────┴┬──────────────────────────────────────────────────────────────────────────────────────────────────┼───────┼───────────┼┼┼─┼───┼┼┼──┼┼─────────────────────┼──┼┼┼─┴┴┬┼┼─────────────┴┬─┬─────────────────────────────────────────────────────────
     40: ─┊────────────────────────────────────────────────────────────────────────────────┼┴─┼┴───┬──┴─┴──────────────────┊┼┴──────┴┬────────┼──┼┬──┼┼┼┼┼──┼┼┬─┼┼────┼┼──┬─────┴──────────────────────────────────────────────────────────────────────────────────────────────────┼───────┼───────────┼┴┴┬┼┬──┼┼┼──┼┼─────────────────────┴──┼┼┼───┼┼┼──────────────┼─┴─────────────────────────────────────────────────────────
     41: ─┊────────────────────────────────────────────────────────────────────────────────┴──┴────┴───────────────────────┊┴────────┴────────┼──┼┼──┼┼┼┼┼──┼┼┼─┼┼┬───┼┼┬─┼┬───────────────────────────────────────────────────────────────────────────────────────────────────────┼───────┼───────────┼──┼┼┼──┼┼┼──┼┼────────────────────────┼┴┴┬──┼┼┼──────────────┴┬──────────────────────────────────────────────────────────
     42: ─┊──────────────────────────────────────────────────────────────────────────────────────────────────┬──┬──────┬──┬┊──────────────────┴──┼┼──┼┼┼┼┴──┼┼┼─┼┼┼───┼┼┼─┴┴───────────────────────────────────────────────────────────────────────────────────────────────────────┼───────┼───────────┼──┼┼┼──┼┴┴┬─┼┼┬───────────────────────┼──┼──┼┼┼───────────────┴──────────────────────────────────────────────────────────
     43: ─┊─────────────────────────────────────────────────────────────────────────────────────────────────┬┼──┼─┬──┬─┼──┴┊─────────────────────┼┼──┼┼┼┼───┼┼┼─┼┼┼───┴┴┴┬─────────────────────────────────────────────────────────────────────────────────────────────────────────┼───────┼───────────┼──┼┼┼──┼──┼─┼┼┼───────────────────────┼──┼──┼┴┴┬─┬─┬─────────────────────────────────────────────────────────────────────
     44: ─┊────────────────────────────────────────────────────────────────────────────────────────────────┬┼┼──┴┬┼──┴┬┼─┬─┊─────────────────────┼┼──┼┼┼┼───┴┴┴┬┼┼┼──────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────┼───────┴───────────┴──┼┼┴──┼──┼─┼┼┴───────────────────────┼──┼──┼──┼─┼─┴─────────────────────────────────────────────────────────────────────
     45: ─┊────────────────────────────────────────────────────────────────────────────────────────────────┼┼┼─┬─┼┴─┬─┼┴─┴─┊─────────────────────┼┼──┼┼┼┼──────┼┴┴┴┬─┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────────┼┼───┼──┼─┼┴────────────────────────┴──┴──┼──┼─┴┬──────────────────────────────────────────────────────────────────────
     46: ─┊────────────────────────────────────────────────────────────────────────────────────────────────┼┼┴┬┼─┴──┴─┼─┬──┊─────────────────────┼┼──┼┼┴┴──────┴───┼─┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────────┼┴───┴──┴┬┼───────────────────────────────┼──┼──┴──────────────────────────────────────────────────────────────────────
     47: ─┊────────────────────────────────────────────────────────────────────────────────────────────────┼┴─┼┴───┬──┴─┴──┊─────────────────────┼┼──┴┴────────────┴┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────────┼────────┼┴───────────────────────────────┴──┴┬────────────────────────────────────────────────────────────────────────
     48: ─┊────────────────────────────────────────────────────────────────────────────────────────────────┴──┴────┴───────┊─────────────────────┴┴─────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────┴──────────────────────┴────────┴────────────────────────────────────┴────────────────────────────────────────────────────────────────────────

This network has **405 swap operations** for a complete sort, which is not an optimal network for 49 elements. However, 
sorting only the upper half of the pixels in a median filtering iteration need 405 - 6*16 - 28 = **281 swap operations**.

This network was found by consecutively applying batcher merges to the pre-sorted values. 
