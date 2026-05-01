# MUHAMMAD AFI SYAZRIQ BIN ANUAR
# A Concurrent and Parallel Architecture for Massive Data Hashing

# ITT440: Individual Assignment Report
**Course:** ITT440 - Network Programming  
**Group:** M3CS2554B  
**Name:** Muhammad Afi Syazriq Bin Anuar  
**Student ID:** 2024249492  
**Lecturer:** Sir Shahadan Bin Saad  
**Video Link:** https://youtu.be/GoumoxCvVyI

## 1.0 Project Title
**A Concurrent and Parallel Architecture for Massive Data Hashing**

## 2.0 Problem Statement
Analyzing and securing massive datasets often exposes critical hardware bottlenecks in standard sequential programming. When processing a large volume of data (e.g., millions of plain-text passwords), a single-threaded application suffers from two distinct latency issues:
1.  **CPU Bottleneck (Mathematical Processing):** Cryptographic hashing (SHA-256) is highly CPU-intensive. Standard execution overloads a single core while leaving multi-core system resources unutilized.
2.  **I/O Bottleneck (Data Export):** Writing millions of processed records to disk sequentially forces the CPU to idle while waiting for the slower physical storage drive to complete the write operations.

This project investigates these bottlenecks by developing a Python application that hashes 10,000,000 strings. It isolates and benchmarks the performance differences between pure sequential processing, CPU-parallelism via `multiprocessing`, and I/O-concurrency via `threading`.

## 3.0 Development Environment
* **Integrated Development Environment (IDE):** Microsoft Visual Studio 
* **Language:** Python 3.x
* **Key Libraries:** `multiprocessing`, `threading`, `hashlib`, `time`, `matplotlib` (for data visualization)
* **Hardware Specifications:** 16-Core CPU Environment 

## 4.0 Methodology
The benchmark was conducted using a single, pre-generated dataset of 10,000,000 randomized 8-character strings to ensure an accurate, controlled testing environment. The dataset was passed through three distinct architectural tests:

### 4.1 Test A: Pure Sequential (Control Group)
* **Architecture:** 1 CPU Core, 1 Thread, 1 Output File.
* **Process:** The program iterates through the dataset one by one, hashing the string and then writing the entire processed array sequentially to a single `.txt` file.

### 4.2 Test B: Parallel Processing (CPU Optimization)
* **Architecture:** 16 CPU Cores, 1 Thread, 1 Output File.
* **Process:** The `multiprocessing.Pool` module is utilized to bypass the Python Global Interpreter Lock (GIL). The 10-million string array is distributed evenly across all 16 physical cores, allowing the mathematical SHA-256 hashing to occur simultaneously. The writing phase remains sequential.

### 4.3 Test C: Concurrent Processing (I/O Optimization)
* **Architecture:** 1 CPU Core, 5 Threads, 5 Output Files.
* **Process:** The hashing remains sequential. However, the data export utilizes the `threading` module. The processed array is divided into 5 chunks, and 5 separate threads stream the data concurrently into 5 distinct `.txt` log files, masking disk latency.

## 5.0 Results and Performance Analysis

### 5.1 Terminal Output Validation
<p align="center">
  <img src="terminal.png" alt="Output for the program" />
  <br>
  <b>Figure 1.0:</b> Console output of the final performance report.
</p>

### 5.2 Visual Data Comparison
<p align="center">
  <img src="graph.png" alt="Performance Comparison Chart" />
  <br>
  <b>Figure 2.0:</b> Auto-generated Matplotlib chart comparing execution times.
</p>

### 5.3 Technical Analysis
Based on the execution times logged by the benchmarking tool, we can observe the following architectural impacts:

1.  **Parallel Math Acceleration:** Test B (15.89 seconds) outperformed Test A (19.00 seconds) by approximately 3.11 seconds. This confirms that cryptographic hashing is strictly a CPU-bound task. Distributing the workload across 16 cores successfully mitigated the mathematical bottleneck.
2.  **I/O Concurrency Impact:** Test C (18.63 seconds) yielded a time nearly identical to the sequential baseline. Because the test environment features a highly capable solid-state drive, the disk writing latency was already minimal. Therefore, threading the file logging did not result in a massive time reduction for this specific hardware, further proving that threading does *not* accelerate CPU-bound mathematical operations.

## 6.0 System Output and Data Generation Analysis

This section presents the actual system outputs generated during the password hashing performance benchmark, providing direct evidence of the application’s functionality and raw data generation.

### 6.1 Console Performance Report
The following screenshot captures the primary console output summarizing the final results of the performance benchmark for processing 10,000,000 raw passwords.

<p align="center">
  <img src="terminal.png" alt="Output for the program" />
  <br>
  <b>Figure 3.0:</b> Console output of the final performance report.
</p>

This screen details three distinct tests, providing exact configurations and execution times:
* **TEST A (Pure Sequential):** 1 Core, 1 File – Completed in 19.00 seconds.
* **TEST B (Parallel Only):** 16 Cores, 1 File – Completed in 15.89 seconds. This represents the fastest performance, showcasing the significant advantage of multi-core parallel processing for this cryptographic task.
* **TEST C (Concurrent Only):** 1 Core, 5 Files – Completed in 18.63 seconds. The results show that while concurrent writing was fast, it did not significantly reduce overall time, as the mathematical hashing was still performed sequentially on a single core.

### 6.2 Sample of Generated Hashing Log
This screenshot provides a crucial look at the actual raw data generated by the tests. It confirms that the system successfully generated a structured log file containing the hashed records.

<p align="center">
  <img src="Output.png" alt="Output for the program" />
  <br>
  <b>Figure 4.0:</b> Generated data that has been hashed.
</p>

### 6.3 Automated Graph Generation
As part of the final execution step, the benchmarking application utilizes the Matplotlib library to automatically generate a visual representation of the data. This chart provides an immediate, clear comparison of how the hardware managed the specific bottlenecks.

<p align="center">
  <img src="graph.png" alt="Performance Comparison Chart" />
  <br>
  <b>Figure 5.0:</b> Auto-generated Matplotlib chart comparing execution times.
</p>

The graph directly corroborates the terminal output, visually emphasizing the speedup achieved by multi-core parallelism (Test B) against the single-core sequential baseline (Test A). Generating this graph dynamically proves that the system is capable of not only processing massive datasets but also visualizing the results for high-level technical analysis.

This view confirms that each line is accurately formatted with an alphanumeric string (the original raw password) followed by a colon and its corresponding SHA-256 hexadecimal hash. This direct view provides essential verification that the raw output matches the expected cryptographic structure.

## 7.0 Conclusion
The development and execution of this project successfully demonstrate the structural differences between parallel and concurrent programming in Python. 

Parallelism (`multiprocessing`) is required to distribute heavy computational workloads across a system's hardware, while Concurrency (`threading`) is utilized strictly for workflow management during latency-heavy I/O tasks. By benchmarking 10,000,000 records, this application proves that standard sequential programming is inefficient for large-scale data processing and must be optimized according to the specific nature (CPU-bound vs. I/O-bound) of the task.

---

## 8.0 User Manual (GitHub README)

### 8.1 System Requirements
* **Operating System:** Windows 10/11, macOS, or Linux.
* **Processor:** Multi-core CPU (4+ cores recommended to observe distinct parallel performance gains).
* **RAM:** Minimum 8GB RAM (16GB recommended due to the in-memory generation of 10,000,000 records).
* **Software:** Python 3.8 or newer.
* **Dependencies:** `matplotlib` (for generating the performance graph).

### 8.2 Installation Steps
1. Clone or download the repository to your local machine.
2. Open your preferred IDE (e.g., Microsoft Visual Studio or VS Code) or terminal.
3. Ensure Python is installed by running: `python --version`.
4. Install the required visualization library by running the following command in your terminal:
   ```bash
   pip install matplotlib
   ```

### 8.3 How to Run the Program
1. Navigate to the project directory containing the source code.
2. Execute the main script via the terminal:
   ```bash
   python main.py
   ```
3. Wait for the data generation to complete. The terminal will provide real-time status updates as it executes Test A, Test B, and Test C sequentially. 
4. Upon completion, review the terminal dashboard for the execution times and check the project directory for the generated log files and performance graph.

### 8.4 Sample Input/Output
* **Sample Input:** The program automatically generates an in-memory list of 10,000,000 random 8-character strings. Example string: `x7B9mV2q`
* **Sample Output (Terminal):**
  ```text
  FINAL PERFORMANCE REPORT (10 Million Records)
  ==================================================
  Test A (Pure Sequential):  19.00s
  Test B (Parallel Only):    15.89s
  Test C (Concurrent Only):  18.63s
  ==================================================
  Generating performance graph...
  Graph successfully saved as 'performance_comparison_chart.png'!
  ```
* **Sample Output (Log File Entry):**
  `x7B9mV2q:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08`

### 8.5 Screenshots
<p align="center">
  <img src="terminal.png" alt="Output for the program" />
  <br>

<p align="center">
  <img src="Output.png" alt="Output for the program" />
  <br>

  <p align="center">
  <img src="graph.png" alt="Performance Comparison Chart" />
  <br>

### 8.6 Source Code
Below is the complete `main.py` source code utilized for this benchmark.

```python
import multiprocessing
import threading
import hashlib
import time
import random
import string
import gc
import matplotlib.pyplot as plt

# --- 1. DATA GENERATION ---
def generate_passwords(amount):
    print(f"Generating {amount:,} raw passwords... (Please wait)")
    chars = string.ascii_letters + string.digits
    return [''.join(random.choices(chars, k=8)) for _ in range(amount)]

# --- 2. CPU-BOUND TASK: CRYPTOGRAPHIC HASHING ---
def hash_password(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return f"{password}:{hashed}\n"

# --- 3. I/O-BOUND TASK: FILE LOGGING ---
def write_to_file(filename, data_chunk):
    with open(filename, 'w') as f:
        f.writelines(data_chunk)

# ==========================================
# MAIN EXECUTION AND COMPARISON
# ==========================================
if __name__ == '__main__':
    NUM_PASSWORDS = 10000000  
    NUM_FILES = 5           
    NUM_CORES = multiprocessing.cpu_count()

    start_gen = time.time()
    passwords = generate_passwords(NUM_PASSWORDS)
    print(f"Data generation complete in {time.time() - start_gen:.2f} seconds.\n")

    # --- TEST A: PURE SEQUENTIAL ---
    print("==================================================")
    print("TEST A: Pure Sequential (1 Core, 1 File)")
    start_a = time.time()
    hashes_a = [hash_password(p) for p in passwords]
    write_to_file("log_A_sequential.txt", hashes_a)
    time_a = time.time() - start_a
    print(f"[TEST A COMPLETE] Time: {time_a:.2f} seconds\n")
    del hashes_a
    gc.collect()

    # --- TEST B: PARALLEL ONLY ---
    print("==================================================")
    print(f"TEST B: Parallel Only ({NUM_CORES} Cores, 1 File)")
    start_b = time.time()
    with multiprocessing.Pool(processes=NUM_CORES) as pool:
        hashes_b = pool.map(hash_password, passwords)
    write_to_file("log_B_parallel_only.txt", hashes_b)
    time_b = time.time() - start_b
    print(f"[TEST B COMPLETE] Time: {time_b:.2f} seconds\n")
    del hashes_b
    gc.collect()

    # --- TEST C: CONCURRENT ONLY ---
    print("==================================================")
    print(f"TEST C: Concurrent Only (1 Core, {NUM_FILES} Files)")
    start_c = time.time()
    hashes_c = [hash_password(p) for p in passwords]
    chunk_size = len(hashes_c) // NUM_FILES
    threads = []
    for i in range(NUM_FILES):
        start_idx = i * chunk_size
        end_idx = None if i == NUM_FILES - 1 else (i + 1) * chunk_size
        chunk = hashes_c[start_idx:end_idx]
        thread = threading.Thread(target=write_to_file, args=(f"log_C_concurrent_{i+1}.txt", chunk))
        threads.append(thread)
        thread.start() 
    for thread in threads:
        thread.join()
    time_c = time.time() - start_c
    print(f"[TEST C COMPLETE] Time: {time_c:.2f} seconds\n")
    del hashes_c
    gc.collect()

    # --- FINAL DASHBOARD & GRAPH ---
    print("==================================================")
    print("FINAL PERFORMANCE REPORT (10 Million Records)")
    print("==================================================")
    print(f"Test A (Pure Sequential):  {time_a:.2f}s")
    print(f"Test B (Parallel Only):    {time_b:.2f}s")
    print(f"Test C (Concurrent Only):  {time_c:.2f}s")
    print("==================================================")

    print("Generating performance graph...")
    test_names = ['Test A\n(Sequential)', 'Test B\n(Parallel)', 'Test C\n(Concurrent)']
    execution_times = [time_a, time_b, time_c]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1'] 

    plt.bar(test_names, execution_times, color=colors, edgecolor='black')
    plt.title('Performance Comparison: 10 Million Hashes', fontsize=14, fontweight='bold')
    plt.ylabel('Execution Time (Seconds)', fontsize=12)
    plt.xlabel('Processing Method', fontsize=12)

    for index, value in enumerate(execution_times):
        plt.text(index, value + (max(execution_times)*0.02), f'{value:.2f}s', ha='center', fontweight='bold')

    image_filename = 'performance_comparison_chart.png'
    plt.savefig(image_filename, bbox_inches='tight', dpi=300)
    print(f"Graph successfully saved as '{image_filename}'!")
```
