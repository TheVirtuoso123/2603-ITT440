import pandas as pd
import numpy as np
import time
import threading
import multiprocessing
import matplotlib.pyplot as plt
import os

# 1. GENERATE DATASET (5 Million Records distributed into 8 Departments)
def generate_dataset(filename="payroll_data.csv"):
    if not os.path.exists(filename):
        print("Generating 5 million records for 8 departments... please wait.")
        num_records = 5000000
        departments = [f'Dept_{i+1}' for i in range(8)]
        
        data = {
            'Employee_ID': np.arange(1, num_records + 1),
            'Department': np.random.choice(departments, num_records),
            'Base_Salary': np.random.randint(3000, 10000, size=num_records),
            'Overtime_Hours': np.random.randint(0, 20, size=num_records)
        }
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Dataset saved as {filename}")
    else:
        print("Dataset found. Loading existing file...")

# Payroll Calculation Logic (CPU Intensive Task)
def calculate_payroll_chunk(data_chunk):
    # Simulate complex tax and allowance calculations
    results = []
    for salary in data_chunk:
        tax = salary * 0.11
        epf = salary * 0.09
        net = salary - tax - epf
        results.append(net)
    return results

# 2. SEQUENTIAL EXECUTION (Single Thread)
def run_sequential(data):
    start_time = time.time()
    _ = calculate_payroll_chunk(data)
    return time.time() - start_time

# 3. CONCURRENT EXECUTION (Threading - 4 Threads)
def run_threading(data):
    start_time = time.time()
    chunks = np.array_split(data, 4)
    threads = []
    for chunk in chunks:
        t = threading.Thread(target=calculate_payroll_chunk, args=(chunk,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return time.time() - start_time

# 4. PARALLEL EXECUTION (Multiprocessing - 8 Processes for 8 Departments)
def run_multiprocessing(data):
    start_time = time.time()
    # Splitting data into 8 parts to represent 8 departments
    chunks = np.array_split(data, 8)
    with multiprocessing.Pool(processes=8) as pool:
        pool.map(calculate_payroll_chunk, chunks)
    return time.time() - start_time

# 5. VISUALIZATION
def plot_results(s, t, p):
    methods = ['Sequential', 'Concurrent (Threading)', 'Parallel (Multiprocessing)']
    times = [s, t, p]
    
    plt.figure(figsize=(12, 7))
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    bars = plt.bar(methods, times, color=colors, edgecolor='black')
    
    plt.ylabel('Execution Time (Seconds)', fontsize=12)
    plt.title('Performance Comparison: Processing 5 Million Records (8 Depts)', fontsize=14)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                 f'{height:.4f}s', ha='center', va='bottom', fontweight='bold')
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

if __name__ == "__main__":
    # Ensure dataset is ready
    generate_dataset()
    df = pd.read_csv("payroll_data.csv")
    salaries = df['Base_Salary'].values
    
    print(f"\n--- Starting Payroll Engine Processing ---")
    print(f"Total Records: {len(salaries)}")
    print(f"Departments: 8")
    
    # Run and Measure
    print("\n[1/3] Running Sequential...")
    time_seq = run_sequential(salaries)
    
    print("[2/3] Running Concurrent (Threading)...")
    time_thread = run_threading(salaries)
    
    print("[3/3] Running Parallel (8 Processes)...")
    time_para = run_multiprocessing(salaries)
    
    # Console Output
    print("-" * 40)
    print(f"Sequential Time  : {time_seq:.4f}s")
    print(f"Concurrent Time  : {time_thread:.4f}s")
    print(f"Parallel Time    : {time_para:.4f}s")
    print("-" * 40)
    
    # Show Visual Comparison
    plot_results(time_seq, time_thread, time_para)