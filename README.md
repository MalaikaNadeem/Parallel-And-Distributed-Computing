# Parallel-And-Distributed-Computing
# Performance Comparison: Sequential, Parallel, and Distributed Processing

## Execution Time

| Method      | Configuration  | Execution Time (s) |
|--------------|----------------|--------------------|
| Sequential   | Single Process | 0.18               |
| Parallel     | 1 Worker       | 0.19               |
| Parallel     | 2 Workers      | 0.11               |
| Parallel     | 4 Workers      | 0.07               |
| Parallel     | 8 Workers      | 0.06               |
| Distributed  | 2 Nodes        | 0.67               |

## Best Number of Workers

The best number of workers was **8**, giving the fastest processing time of **0.06 seconds**.  
With 8 workers, more images were processed simultaneously, which reduced the total time.  
This worked well because image reading and saving are mostly **I/O-based tasks**, so using multiple threads helped **overlap operations** and improved overall performance.

## How Parallelism Improved Performance and What Bottlenecks Still Exist

Parallel processing made the program faster by handling several images at once instead of processing them one by one.  
This reduced the total execution time, especially when more workers were used.  
The speedup mainly came from **overlapping file reading, resizing, and saving operations**.  

However, some **bottlenecks** still remain — such as **slow disk I/O** and **limited CPU cores**.  
Since most of the work involves reading and writing images, the hard drive speed can restrict performance.  
Additionally, the **Global Interpreter Lock (GIL)** in Python and the **overhead of managing multiple threads or processes** can prevent perfect scaling.
