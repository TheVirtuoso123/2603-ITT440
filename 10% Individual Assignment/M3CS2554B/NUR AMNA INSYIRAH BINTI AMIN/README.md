# NUR AMNA INSYIRAH BINTI AMIN
# ITT440-INDIVIDUAL ASSIGNMENT 
# CLASSIFICATION OF LARGE-SCALE NUMERIC DATASET 

# INTRODUCTION 
This project focuses on the implementation and performance evaluation of parallel programming techniques using Python. The task involves classifying a massive dataset of **5,000,000 numeric records** into three distinct categories (Category A, B, and C) based on CPU-bound mathematical logic. This project demonstrates how hardware resources can be optimized to reduce execution time in data-heavy environments. 

Three distinct categories:

**Category A:** 

**Category B:**

**Category C:** 

# PROBLEM STATEMENT 
In traditional sequential programming, tasks are processed one after another using only a single CPU core. When dealing with millions of data points, this creates a significant performance bottleneck, leaving modern multi-core processors underutilized. This project addresses the inefficiency of single-threaded execution by implementing **Multiprocessing** allowing the workload to be distributed across all available logical processors. 

# SYSTEM SPECIFICATIONS 
The analysis was conducted on a high-performance laptop with the following specifications:

-**Processor:** AMD Ryzen 5 7535HS 

-**Architecture:** 6 Physical Cores, 12 Logical Processors

-**Base Speed:** 3.30 GHz

-**Memory (RAM):** 8.0 GB 

-**Operating System:** Windows 11

# METHODOLOGY 
The classification logic involves complex mathematical operations to simulate a heavy CPU-bound workload. Three approaches were compared:

1. **Sequential:** Using a standard 'for' loop (Single core).
2. **Threading:** Using 'ThreadPoolExecutor' (Concurrency).
3. **Multiprocessing:** Using 'ProcessPoolExecutor' (True Parallelism).

# IMPLEMENTATION 

     import time
     import numpy as np
     import os
    # Importing concurrent.futures for both Threading and Multiprocessing
    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
    # --- 1. CLASSIFICATION LOGIC FUNCTION (CPU-BOUND) ---
    def classify_data(data_chunk):
    """
    This function performs heavy mathematical calculations to 
    classify numeric data into Category A, B, or C.
    """
    results = []
    for val in data_chunk:
        # Simulate heavy CPU workload using square roots and trigonometry
        calc = np.sqrt(val**2 + np.log1p(val)) * np.sin(val)
        
        if calc > 500:
            results.append("Category A")
        elif calc > 200:
            results.append("Category B")
        else:
            results.append("Category C")
            
    return len(results)
    
      def main():
    # --- 2. GENERATING LARGE VOLUME DATA ---
    print("="*60)
    print("PROJECT: CLASSIFICATION OF LARGE-SCALE NUMERIC DATASET")
    print("="*60)
    
     # Using 5 million rows to ensure the performance difference is visible
    data_size = 5_000_000  
    print(f"Status: Generating {data_size:,} random numeric data points...")
    data = np.random.uniform(1, 1000, data_size)
    
    # Split data into chunks based on the number of available CPU cores
    cpu_cores = os.cpu_count()
    data_chunks = np.array_split(data, cpu_cores)
    print(f"System Info: Detected {cpu_cores} CPU cores.\n")

    # --- 3. SEQUENTIAL EXECUTION (BASELINE) ---
    print("--- Running Sequential Approach ---")
    # Processing the entire dataset in a single thread/process
    start_time = time.perf_counter()
    classify_data(data)
    sequential_duration = time.perf_counter() - start_time
    print(f"Sequential Execution Time: {sequential_duration:.4f} seconds\n")

    # --- 4. CONCURRENT EXECUTION (THREADING) ---
    print("--- Running Concurrent Approach (Threading) ---")
    # Using ThreadPoolExecutor to demonstrate concurrency
    start_time = time.perf_counter()
    with ThreadPoolExecutor(max_workers=cpu_cores) as executor:
        list(executor.map(classify_data, data_chunks))
    threading_duration = time.perf_counter() - start_time
    print(f"Threading Execution Time: {threading_duration:.4f} seconds")
    print("Note: Threading may be slow for math due to the Global Interpreter Lock (GIL).\n")

    # --- 5. PARALLEL EXECUTION (MULTIPROCESSING) ---
    print("--- Running Parallel Approach (Multiprocessing) ---")
    # Using ProcessPoolExecutor to demonstrate true parallelism
    start_time = time.perf_counter()
    with ProcessPoolExecutor(max_workers=cpu_cores) as executor:
        list(executor.map(classify_data, data_chunks))
    multiprocessing_duration = time.perf_counter() - start_time
    print(f"Multiprocessing Execution Time: {multiprocessing_duration:.4f} seconds")
    print("Note: This bypasses the GIL and utilizes all CPU cores.\n")

    # --- 6. PERFORMANCE SUMMARY ---
    print("="*60)
    speedup_ratio = sequential_duration / multiprocessing_duration
    print(f"RESULTS: Parallelism is {speedup_ratio:.2f}x faster than Sequential!")
    print("="*60)

    if __name__ == "__main__":
    main()


# PERFORMANCE RESULT & OBSERVATION 
<img width="605" height="666" alt="image" src="https://github.com/user-attachments/assets/e462a030-3368-465b-b0ee-acc973701eaa" />
<img width="745" height="231" alt="image" src="https://github.com/user-attachments/assets/4a33f7ec-b331-4710-9fad-3f8e84d08b08" />
<img width="617" height="83" alt="image" src="https://github.com/user-attachments/assets/1d575abb-3e8f-4b8f-811f-5935b428de91" />

| Approach | Execution Time ( Second ) |
| :--- | :--- |
| **Sequential** | 8.4396s |
| **Threading** | 7.6682s |
| **Multiprocessing** | 3.0576s | 

# CONCLUSION 

# VIDEO DEMONSTATION 
