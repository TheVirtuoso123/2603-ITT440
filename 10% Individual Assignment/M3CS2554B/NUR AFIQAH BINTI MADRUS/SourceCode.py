import random
import time
import csv
import threading
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from dataclasses import dataclass
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import numpy as np
import os

# =============================================================================
# CONFIGURATION
# =============================================================================

CONFIG = {
    "total_numbers": 10_000_000,      # Total numbers to process
    "min_value": 1,                    # Minimum random value
    "max_value": 1_000_000,            # Maximum random value
    "num_workers": 8,                  # Number of threads/processes
    "output_csv": "results_output.csv",
    "comparison_csv": "performance_comparison.csv",
    "graph_filename": "performance_graph.png"
}


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class Statistics:
    """
    Data class to hold 8 output metrics for each processing approach.
    """
    total_even: int = 0
    total_odd: int = 0
    sum_even: int = 0
    sum_odd: int = 0
    min_even: int = float('inf')
    max_even: int = 0
    min_odd: int = float('inf')
    max_odd: int = 0
    
    def to_dict(self) -> Dict:
        """Convert statistics to dictionary for CSV export."""
        return {
            "Total Even Numbers": self.total_even,
            "Total Odd Numbers": self.total_odd,
            "Sum of Even Numbers": self.sum_even,
            "Sum of Odd Numbers": self.sum_odd,
            "Minimum Even Number": self.min_even if self.min_even != float('inf') else "N/A",
            "Maximum Even Number": self.max_even,
            "Minimum Odd Number": self.min_odd if self.min_odd != float('inf') else "N/A",
            "Maximum Odd Number": self.max_odd
        }


# =============================================================================
# DATA GENERATION
# =============================================================================

def generate_numbers(count: int, min_val: int, max_val: int) -> List[int]:
    """
    Generate a list of random integers.
    
    Args:
        count: Number of integers to generate
        min_val: Minimum value (inclusive)
        max_val: Maximum value (inclusive)
    
    Returns:
        List of random integers
    """
    print(f"Generating {count:,} random numbers...")
    numbers = [random.randint(min_val, max_val) for _ in range(count)]
    print(f"Generation complete.")
    return numbers


def save_numbers_to_csv(numbers: List[int], filename: str = "generated_numbers.csv"):
    """
    Save generated numbers to CSV file for verification.
    
    Args:
        numbers: List of integers to save
        filename: Output CSV filename
    """
    print(f"Saving numbers to {filename}...")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Index", "Number", "Type"])
        for i, num in enumerate(numbers[:10000]):  # Save first 10,000 for verification
            writer.writerow([i + 1, num, "Even" if num % 2 == 0 else "Odd"])
    print(f"Sample of {min(10000, len(numbers)):,} numbers saved to {filename}")


# =============================================================================
# PROCESSING FUNCTIONS
# =============================================================================

def process_chunk(numbers: List[int]) -> Statistics:
    """
    Process a chunk of numbers and compute statistics.
    This function is used by all approaches (sequential, concurrent, parallel).
    
    Args:
        numbers: List of integers to process
    
    Returns:
        Statistics object with 8 computed metrics
    """
    stats = Statistics()
    
    for num in numbers:
        if num % 2 == 0:
            # Even number processing
            stats.total_even += 1
            stats.sum_even += num
            if num < stats.min_even:
                stats.min_even = num
            if num > stats.max_even:
                stats.max_even = num
        else:
            # Odd number processing
            stats.total_odd += 1
            stats.sum_odd += num
            if num < stats.min_odd:
                stats.min_odd = num
            if num > stats.max_odd:
                stats.max_odd = num
    
    return stats


def merge_statistics(stats_list: List[Statistics]) -> Statistics:
    """
    Merge multiple Statistics objects into one.
    
    Args:
        stats_list: List of Statistics objects to merge
    
    Returns:
        Merged Statistics object
    """
    merged = Statistics()
    
    for stats in stats_list:
        merged.total_even += stats.total_even
        merged.total_odd += stats.total_odd
        merged.sum_even += stats.sum_even
        merged.sum_odd += stats.sum_odd
        
        if stats.min_even < merged.min_even:
            merged.min_even = stats.min_even
        if stats.max_even > merged.max_even:
            merged.max_even = stats.max_even
        if stats.min_odd < merged.min_odd:
            merged.min_odd = stats.min_odd
        if stats.max_odd > merged.max_odd:
            merged.max_odd = stats.max_odd
    
    return merged


def split_data(data: List[int], num_chunks: int) -> List[List[int]]:
    """
    Split data into equal chunks for parallel processing.
    
    Args:
        data: List of integers to split
        num_chunks: Number of chunks to create
    
    Returns:
        List of data chunks
    """
    chunk_size = len(data) // num_chunks
    chunks = []
    
    for i in range(num_chunks):
        start = i * chunk_size
        # Last chunk takes remaining elements
        end = start + chunk_size if i < num_chunks - 1 else len(data)
        chunks.append(data[start:end])
    
    return chunks


# =============================================================================
# APPROACH 1: SEQUENTIAL PROCESSING
# =============================================================================

def sequential_processing(numbers: List[int]) -> Tuple[Statistics, float]:
    """
    Process numbers sequentially (baseline approach).
    
    Args:
        numbers: List of integers to process
    
    Returns:
        Tuple of (Statistics, execution_time)
    """
    print("\n" + "="*60)
    print("SEQUENTIAL PROCESSING")
    print("="*60)
    
    start_time = time.perf_counter()
    stats = process_chunk(numbers)
    end_time = time.perf_counter()
    
    execution_time = end_time - start_time
    print(f"Sequential processing completed in {execution_time:.4f} seconds")
    
    return stats, execution_time


# =============================================================================
# APPROACH 2: CONCURRENT PROCESSING (THREADING)
# =============================================================================

def concurrent_processing(numbers: List[int], num_threads: int) -> Tuple[Statistics, float]:
    """
    Process numbers using threading (concurrent approach).
    
    Threading is suitable for I/O-bound tasks. While this task is CPU-bound,
    we demonstrate threading for educational purposes and comparison.
    
    Args:
        numbers: List of integers to process
        num_threads: Number of threads to use
    
    Returns:
        Tuple of (Statistics, execution_time)
    """
    print("\n" + "="*60)
    print(f"CONCURRENT PROCESSING (Threading - {num_threads} threads)")
    print("="*60)
    
    # Split data into chunks
    chunks = split_data(numbers, num_threads)
    results = []
    lock = threading.Lock()
    
    def thread_worker(chunk: List[int], thread_id: int):
        """Worker function for each thread."""
        thread_stats = process_chunk(chunk)
        with lock:
            results.append(thread_stats)
        print(f"  Thread {thread_id + 1} completed: {len(chunk):,} numbers processed")
    
    start_time = time.perf_counter()
    
    # Create and start threads
    threads = []
    for i, chunk in enumerate(chunks):
        t = threading.Thread(target=thread_worker, args=(chunk, i))
        threads.append(t)
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    # Merge results
    final_stats = merge_statistics(results)
    
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    print(f"Concurrent processing completed in {execution_time:.4f} seconds")
    
    return final_stats, execution_time


# =============================================================================
# APPROACH 3: PARALLEL PROCESSING (MULTIPROCESSING)
# =============================================================================

def parallel_processing(numbers: List[int], num_processes: int) -> Tuple[Statistics, float]:
    """
    Process numbers using multiprocessing (parallel approach).
    
    Multiprocessing bypasses the GIL and is ideal for CPU-bound tasks.
    Each process runs on a separate CPU core.
    
    Args:
        numbers: List of integers to process
        num_processes: Number of processes to use
    
    Returns:
        Tuple of (Statistics, execution_time)
    """
    print("\n" + "="*60)
    print(f"PARALLEL PROCESSING (Multiprocessing - {num_processes} processes)")
    print("="*60)
    
    # Split data into chunks
    chunks = split_data(numbers, num_processes)
    
    start_time = time.perf_counter()
    
    # Use ProcessPoolExecutor for parallel execution
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        # Map process_chunk function to each chunk
        results = list(executor.map(process_chunk, chunks))
        
        for i, stats in enumerate(results):
            print(f"  Process {i + 1} completed: Even={stats.total_even:,}, Odd={stats.total_odd:,}")
    
    # Merge results
    final_stats = merge_statistics(results)
    
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    print(f"Parallel processing completed in {execution_time:.4f} seconds")
    
    return final_stats, execution_time


# =============================================================================
# OUTPUT AND VISUALIZATION
# =============================================================================

def print_statistics(stats: Statistics, approach_name: str):
    """
    Print the 8 output metrics for a given approach.
    
    Args:
        stats: Statistics object to print
        approach_name: Name of the processing approach
    """
    print(f"\n{'─'*50}")
    print(f"  8 OUTPUT METRICS - {approach_name.upper()}")
    print(f"{'─'*50}")
    print(f"  1. Total Even Numbers    : {stats.total_even:,}")
    print(f"  2. Total Odd Numbers     : {stats.total_odd:,}")
    print(f"  3. Sum of Even Numbers   : {stats.sum_even:,}")
    print(f"  4. Sum of Odd Numbers    : {stats.sum_odd:,}")
    print(f"  5. Minimum Even Number   : {stats.min_even:,}")
    print(f"  6. Maximum Even Number   : {stats.max_even:,}")
    print(f"  7. Minimum Odd Number    : {stats.min_odd:,}")
    print(f"  8. Maximum Odd Number    : {stats.max_odd:,}")
    print(f"{'─'*50}")


def save_results_to_csv(results: Dict, filename: str):
    """
    Save all results to CSV file.
    
    Args:
        results: Dictionary containing all approach results
        filename: Output CSV filename
    """
    print(f"\nSaving results to {filename}...")
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow(["Metric", "Sequential", "Concurrent (Threading)", "Parallel (Multiprocessing)"])
        
        # 8 output metrics for each approach
        metrics = [
            "Total Even Numbers",
            "Total Odd Numbers", 
            "Sum of Even Numbers",
            "Sum of Odd Numbers",
            "Minimum Even Number",
            "Maximum Even Number",
            "Minimum Odd Number",
            "Maximum Odd Number"
        ]
        
        for metric in metrics:
            row = [metric]
            for approach in ["Sequential", "Concurrent", "Parallel"]:
                row.append(results[approach]["stats"].to_dict()[metric])
            writer.writerow(row)
        
        # Execution times
        writer.writerow([])
        writer.writerow(["Execution Time (seconds)", 
                        f"{results['Sequential']['time']:.4f}",
                        f"{results['Concurrent']['time']:.4f}",
                        f"{results['Parallel']['time']:.4f}"])
    
    print(f"Results saved to {filename}")


def save_performance_comparison_csv(results: Dict, filename: str):
    """
    Save performance comparison to CSV.
    
    Args:
        results: Dictionary containing all approach results
        filename: Output CSV filename
    """
    print(f"Saving performance comparison to {filename}...")
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Approach", "Execution Time (s)", "Speedup Factor"])
        
        baseline = results["Sequential"]["time"]
        
        for approach in ["Sequential", "Concurrent", "Parallel"]:
            exec_time = results[approach]["time"]
            speedup = baseline / exec_time if exec_time > 0 else 0
            writer.writerow([approach, f"{exec_time:.4f}", f"{speedup:.2f}x"])
    
    print(f"Performance comparison saved to {filename}")


def generate_performance_graph(results: Dict, filename: str):
    """
    Generate performance comparison bar graph.
    
    Args:
        results: Dictionary containing all approach results
        filename: Output image filename
    """
    print(f"\nGenerating performance graph...")
    
    # Data for plotting
    approaches = ["Sequential", "Concurrent\n(Threading)", "Parallel\n(Multiprocessing)"]
    times = [
        results["Sequential"]["time"],
        results["Concurrent"]["time"],
        results["Parallel"]["time"]
    ]
    
    # Calculate speedup factors
    baseline = results["Sequential"]["time"]
    speedups = [baseline / t if t > 0 else 0 for t in times]
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Color scheme
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    # Subplot 1: Execution Time Comparison
    bars1 = ax1.bar(approaches, times, color=colors, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
    ax1.set_title('Execution Time Comparison', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, max(times) * 1.2)
    
    # Add value labels on bars
    for bar, time_val in zip(bars1, times):
        height = bar.get_height()
        ax1.annotate(f'{time_val:.3f}s',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=11, fontweight='bold')
    
    # Subplot 2: Speedup Factor
    bars2 = ax2.bar(approaches, speedups, color=colors, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Speedup Factor (x)', fontsize=12, fontweight='bold')
    ax2.set_title('Speedup Factor Comparison', fontsize=14, fontweight='bold')
    ax2.axhline(y=1, color='red', linestyle='--', linewidth=1, label='Baseline (1x)')
    ax2.set_ylim(0, max(speedups) * 1.2)
    ax2.legend()
    
    # Add value labels on bars
    for bar, speedup in zip(bars2, speedups):
        height = bar.get_height()
        ax2.annotate(f'{speedup:.2f}x',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=11, fontweight='bold')
    
    # Overall title
    fig.suptitle('Performance Analysis: Even & Odd Number Counter\n(Processing 10,000,000 Numbers)',
                 fontsize=16, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Performance graph saved to {filename}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Main function to orchestrate the entire program execution.
    """
    print("="*70)
    print("  PARALLEL EVEN & ODD NUMBER COUNTER")
    print("  Comparing Sequential, Concurrent, and Parallel Approaches")
    print("="*70)
    print(f"\nConfiguration:")
    print(f"  • Total numbers to process: {CONFIG['total_numbers']:,}")
    print(f"  • Number range: {CONFIG['min_value']:,} - {CONFIG['max_value']:,}")
    print(f"  • Number of workers: {CONFIG['num_workers']}")
    print(f"  • CPU cores available: {mp.cpu_count()}")
    
    # Step 1: Generate data
    print("\n" + "─"*70)
    numbers = generate_numbers(
        CONFIG["total_numbers"],
        CONFIG["min_value"],
        CONFIG["max_value"]
    )
    
    # Save sample of generated numbers to CSV
    save_numbers_to_csv(numbers, "generated_numbers.csv")
    
    # Dictionary to store all results
    results = {}
    
    # Step 2: Sequential Processing
    seq_stats, seq_time = sequential_processing(numbers)
    print_statistics(seq_stats, "Sequential")
    results["Sequential"] = {"stats": seq_stats, "time": seq_time}
    
    # Step 3: Concurrent Processing (Threading)
    conc_stats, conc_time = concurrent_processing(numbers, CONFIG["num_workers"])
    print_statistics(conc_stats, "Concurrent (Threading)")
    results["Concurrent"] = {"stats": conc_stats, "time": conc_time}
    
    # Step 4: Parallel Processing (Multiprocessing)
    para_stats, para_time = parallel_processing(numbers, CONFIG["num_workers"])
    print_statistics(para_stats, "Parallel (Multiprocessing)")
    results["Parallel"] = {"stats": para_stats, "time": para_time}
    
    # Step 5: Performance Summary
    print("\n" + "="*70)
    print("  PERFORMANCE SUMMARY")
    print("="*70)
    print(f"\n  {'Approach':<35} {'Time (s)':<15} {'Speedup':<10}")
    print(f"  {'─'*60}")
    
    baseline = results["Sequential"]["time"]
    for approach in ["Sequential", "Concurrent", "Parallel"]:
        exec_time = results[approach]["time"]
        speedup = baseline / exec_time if exec_time > 0 else 0
        print(f"  {approach:<35} {exec_time:<15.4f} {speedup:.2f}x")
    
    # Step 6: Verify results consistency
    print("\n" + "─"*70)
    print("  VERIFICATION: Checking if all approaches produce same results...")
    
    all_match = True
    for metric in ["total_even", "total_odd", "sum_even", "sum_odd"]:
        values = [getattr(results[a]["stats"], metric) for a in ["Sequential", "Concurrent", "Parallel"]]
        if len(set(values)) != 1:
            print(f"  ✗ Mismatch in {metric}: {values}")
            all_match = False
    
    if all_match:
        print("  ✓ All approaches produced identical results!")
    
    # Step 7: Save results to CSV files
    print("\n" + "─"*70)
    save_results_to_csv(results, CONFIG["output_csv"])
    save_performance_comparison_csv(results, CONFIG["comparison_csv"])
    
    # Step 8: Generate performance graph
    generate_performance_graph(results, CONFIG["graph_filename"])
    
    # Final summary
    print("\n" + "="*70)
    print("  EXECUTION COMPLETE")
    print("="*70)
    print(f"\n  Output files generated:")
    print(f"    • generated_numbers.csv     - Sample of input data")
    print(f"    • {CONFIG['output_csv']:<25} - Detailed results")
    print(f"    • {CONFIG['comparison_csv']:<25} - Performance comparison")
    print(f"    • {CONFIG['graph_filename']:<25} - Performance graph")
    print("\n" + "="*70)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Required for Windows multiprocessing support
    mp.freeze_support()
    main()
