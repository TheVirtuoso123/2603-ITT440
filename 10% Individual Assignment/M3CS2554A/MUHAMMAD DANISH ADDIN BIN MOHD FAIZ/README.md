# Parallel CSV Data Cleaner & Formatter
### Course code : ITT440
### Lecturer : Shahadan Bin Saad
### Youtube link :


## 📌 Overview
This project demonstrates the use of **parallel programming in Python** to clean and process large-scale CSV datasets efficiently.

The system compares three execution methods:
- Sequential Processing
- Concurrent Processing (Threading)
- Parallel Processing (Multiprocessing)

---

## ❗ Problem Statement
In modern applications, large datasets often contain incomplete, inconsistent, or invalid data that must be cleaned before use.Despite the availability of concurrency and parallel programming approaches, it is not always evident which approach offers the best performance for big datasets. Specifically, Python adds new difficulties like the Global Interpreter Lock (GIL), which can reduce the efficiency of threading for CPU-bound operations.
In order to find the best way to improve speed, this research compares sequential, concurrent (threading), and parallel (multiprocessing) techniques to the challenge of effectively cleaning huge CSV datasets.

---

## 🎯 Objectives
- Process and clean large datasets (millions of records)
- Apply different programming techniques
- Compare execution performance
- Analyze how data size affects efficiency

---

## ⚙️ Features
- Generate up to **10 million dirty records**
- Clean and validate:
  - Email
  - Age
  - Salary
  - Phone number
  - Name formatting
- Detect invalid data issues
- Performance benchmarking (time + speedup)
- Export cleaned CSV files

---

## 🧠 Techniques Used

###  Sequential
```
1. Loop one by one
2. Clean record
3. Store result
```

###  Threading (Concurrent)
```
1. Split data
2. Use threads
3. Process chunks concurrently
4. Limited by Python GIL
```

###  Multiprocessing (Parallel)
```
1. Split data into chunks
2. Send chunks to multiple CPU cores
3. Each core runs clean_chunk()
4. Combine all results
```

---

## Code Structure

### Parallel cleaner (MULTIPROCESSING)
```
def run_parallel(records: list[dict]):
    print(f"\n[PARALLEL] Multiprocessing Cleaner  ({NUM_WORKERS} cores, chunk={CHUNK_SIZE:,})")
    start = time.time()

    chunks = [records[i:i + CHUNK_SIZE] for i in range(0, len(records), CHUNK_SIZE)]
    print(f"[PARALLEL] {len(chunks)} chunks dispatched across {NUM_WORKERS} processes")

    with multiprocessing.Pool(processes=NUM_WORKERS) as pool:
        chunked_results = pool.map(clean_chunk, chunks)

    # Flatten list-of-lists
    results = [r for batch in chunked_results for r in batch]

    elapsed = time.time() - start
    print(f"[PARALLEL] Completed in {elapsed:.2f}s")
    return results, elapsed
```
### Sequential cleaner
```
def run_sequential(records: list[dict]):
    print("\n[SEQUENTIAL] Cleaning records...")
    start   = time.time()
    results = [clean_record(r) for r in records]
    elapsed = time.time() - start
    print(f"[SEQUENTIAL] Completed in {elapsed:.2f}s")
    return results, elapsed
```
###  Threading cleaner
```
def run_concurrent(records: list[dict]):
    print("\n[CONCURRENT] Threading Cleaner...")
    start   = time.time()
    # Fewer, fatter chunks for threads too — reduces scheduler overhead
    t_chunk = max(100_000, len(records) // NUM_WORKERS)
    chunks  = [records[i:i + t_chunk] for i in range(0, len(records), t_chunk)]
    results = []
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as ex:
        futures = [ex.submit(clean_chunk, c) for c in chunks]
        for f in futures:
            results.extend(f.result())
    elapsed = time.time() - start
    print(f"[CONCURRENT] Completed in {elapsed:.2f}s")
    return results, elapsed
```
---
## Result & Performance Analysis
### Expected Output
```
============================================================
PARALLEL CSV DATA CLEANER & FORMATTER
Records: 10,000,000  |  Workers: 22  |  Chunk: 454,545
============================================================
[GEN] Generating 10,000,000 dirty CSV records...
[GEN] Completed in 93.39s

[PARALLEL] Multiprocessing Cleaner  (22 cores, chunk=454,545)
[PARALLEL] 23 chunks dispatched across 22 processes
[PARALLEL] Completed in 40.07s

[SEQUENTIAL] Cleaning records...
[SEQUENTIAL] Completed in 176.06s

[CONCURRENT] Threading Cleaner...
[CONCURRENT] Completed in 96.97s

============================================================
PERFORMANCE COMPARISON
============================================================

Method                             Time    Speedup
--------------------------------------------------
Sequential                      176.06s     1.00x
Concurrent (Threads)             96.97s     1.82x
Parallel (Processes)             40.07s     4.39x

                                 Winner: Parallel

============================================================
CLEANING SUMMARY
============================================================
  Total records  : 10,000,000
  Valid records  : 156,259 (1.6%)
  Invalid records: 9,843,741 (98.4%)

  Issue Breakdown:
    invalid_email        8,000,891  (80.0%)
    invalid_age          6,093,973  (60.9%)
    invalid_phone        5,999,727  (60.0%)
    invalid_salary       4,998,141  (50.0%)
[OUT] Saved 10,000,000 records → cleaned_output\cleaned_sequential.csv
[OUT] Saved 10,000,000 records → cleaned_output\cleaned_parallel.csv

============================================================
PROGRAM COMPLETE!
============================================================
```


---
## 📊 Performance Comparison (Different Data Sizes)

| Method | 1M Data | 3M Data | 5M Data | 10M Data |
|--------|--------|--------|--------|---------|
| Sequential | 5.45s | 9.66s | 21.89s | 176.06s |
| Threading | 5.94s | 10.22s | 28.24s | 96.97s |
| Parallel | 4.18s | 5.16s | 21.88s | 40.07s |
| Winner | Parallel |Parallel | Parallel | Parallel |

---
## 📈 Key Findings
- Parallel processing consistently achieved the **fastest execution time**
- Sequential processing became slower as dataset size increased
- Threading did not improve performance due to the **Global Interpreter Lock (GIL)**
- Multiprocessing effectively utilized multiple CPU cores
---
## 🧠 Analysis
- For all tested dataset sizes (1M–10M), parallel processing outperformed other methods
- Optimizations such as:
  - Large chunk size
  - Efficient workload distribution
  - Reduced inter-process communication

---
## 📋 Data Cleaning Summary

Example (10M dataset):
- Total records: 10,000,000
- Valid records: 1.6%
- Invalid records: 98.4%

Common issues:
- invalid_email
- invalid_age
- invalid_phone
- invalid_salary

---

## 📚 Conclusion

- Parallel processing is the most efficient method for large-scale data cleaning
- Proper optimization is important to achieve the best performance
- Multiprocessing is recommended for CPU-intensive tasks

---








