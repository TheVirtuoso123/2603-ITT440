# 📈 Parallel Stock Market Price Simulator & Analyzer

## 👤 Student: Ahmad Zarif Bin Ahmad Khir
## 📘 Subject: ITT440 - Parallel Programming
## 🏫 Class: M3CS2554A
## 📅 Date: April 2025
## 🎥 Demo Video : 
---

## 🖥️System Environment

| Parameter | Details |
|---|---|
| 💻OS| Windows 11 |
| 🐍Python Version | Python 3.14 |
| 🧑‍💻IDE | Visual Studio Code |
| 🪟GUI Framework | Tkinter (built-in) |
| ⚙️ CPU Cores | Auto-detected via multiprocessing.cpu_count() |
| 🚀Execution Modes | Sequential, Threading, Multiprocessing |

---

## ❗ 1. Problem Statement

Stock markets generate enormous volumes of price data every second. Analyzing thousands of stocks with hundreds of price ticks each is computationally expensive. This project investigates whether *Threading* or *Multiprocessing* can outperform traditional *Sequential* processing for this CPU-bound workload.

The program simulates up to *1,000,000+ data points* and benchmarks all three approaches.

---


### 🎯2. Objectives

- Implement three execution approaches:📉 Sequential🧵 Threading⚙️ Multiprocessing
- 🎲 Simulate stock price movements using a Gaussian random walk model
- 📊 Process large datasets (up to 1,000,000 data points)
- 🧮 Compute key financial metrics: mean, min, max, volatility, SMA-50, total return
- ⏱️ Measure execution time and calculate speedup
- 🪟 Display results using a Tkinter GUI
- 💾 Export results to CSV
---

## 3. Implementation

### 3.1 Source Code
```
python
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import time
import random
import math
import csv
import queue
from datetime import datetime

TARGET_POINTS = 1_000_000

# ── STOCK DATA GENERATION ──────────────────────────────────────────────
def make_stocks(num, ticks):
    stocks = {}
    for i in range(num):
        name = "STK" + str(i + 1).zfill(4)
        price = random.uniform(10.0, 500.0)
        prices = [round(price, 4)]
        for _ in range(ticks - 1):
            change = random.gauss(0, 1) * price * 0.01
            price = max(0.01, price + change)
            prices.append(round(price, 4))
        stocks[name] = prices
    return stocks

# ── SINGLE STOCK ANALYSIS (optimized single-pass) ─────────────────────
def calc(name, prices):
    n = len(prices)
    first = prices[0]
    prev = first
    total = 0.0
    mn = first
    mx = first
    ret_sum = 0.0
    ret_sq_sum = 0.0
    for i, p in enumerate(prices):
        total += p
        if p < mn: mn = p
        if p > mx: mx = p
        if i > 0:
            r = (p - prev) / prev
            ret_sum += r
            ret_sq_sum += r * r
        prev = p
    avg = total / n
    ret_n = n - 1
    if ret_n > 0:
        avg_r = ret_sum / ret_n
        var = (ret_sq_sum / ret_n) - (avg_r * avg_r)
        if var < 0: var = 0.0
        vol = math.sqrt(var)
    else:
        vol = 0.0
    sma = (sum(prices[-50:]) / 50.0) if n >= 50 else avg
    ret = ((prices[-1] - first) / first) * 100.0
    return {
        "ticker": name, "start": round(prices[0], 2),
        "end": round(prices[-1], 2), "min": round(mn, 2),
        "max": round(mx, 2), "avg": round(avg, 2),
        "sma50": round(sma, 2), "vol": round(vol, 6),
        "ret": round(ret, 2),
    }

# ── MODE 1: SEQUENTIAL ─────────────────────────────────────────────────
def do_sequential(stocks):
    return [calc(t, p) for t, p in stocks.items()]

# ── MODE 2: CONCURRENT THREADING (ThreadPoolExecutor) ──────────────────
def calc_item(item):
    return calc(item[0], item[1])

def do_threading(stocks):
    items = list(stocks.items())
    if not items: return []
    workers = min(32, max(1, multiprocessing.cpu_count() * 2))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(calc_item, items))

# ── MODE 3: PARALLEL MULTIPROCESSING (chunked Pool.map) ────────────────
def _chunked(items, size):
    for i in range(0, len(items), size):
        yield items[i: i + size]

def mp_chunk_work(chunk):
    return [calc_item(item) for item in chunk]

def do_multiprocessing(stocks):
    items = list(stocks.items())
    if not items: return []
    workers = max(1, multiprocessing.cpu_count() - 1)
    chunk_size = max(8, len(items) // (workers * 8))
    chunks = list(_chunked(items, chunk_size))
    dispatch_chunksize = max(1, len(chunks) // (workers * 2))
    with multiprocessing.Pool(processes=workers) as pool:
        out = pool.map(mp_chunk_work, chunks, chunksize=dispatch_chunksize)
    return [row for chunk in out for row in chunk]

if __name__ == "__main__":
    multiprocessing.freeze_support()
    root = tk.Tk()
    App(root)
    root.mainloop()
```

---

### 3.2 Function Description

| Function | Purpose |
|---|---|
| make_stocks(num, ticks) | Creates fake stock data. Each stock has a list of prices that change randomly over time. |
| calc(name, prices) | Analyzes one stock and calculates all important values like average price, min, max, volatility, and return.|
| calc_item(item) | Helps convert data into the correct format so it can be used in threading and multiprocessing.|
| do_sequential(stocks) | Processes all stocks one by one (no parallelism). Used as the baseline for comparison. |
| do_threading(stocks) | Processes stocks using multiple threads to try to speed up execution.|
| _chunked(items, size) | Splits the data into smaller groups (chunks) to make multiprocessing more efficient. |
| mp_chunk_work(chunk) | Processes one chunk of stocks in a separate process. |
| do_multiprocessing(stocks) | Uses multiple CPU cores to process stocks in parallel, making it faster. |
| set_one_million_data() | Automatically sets the number of stocks and ticks to reach around 1 million data points.|
| ui_queue | Sends data safely from background tasks to the GUI without causing errors.|
| Chart class | Displays results visually in the GUI using charts. |
| App class | Controls the whole application, including GUI, user input, and running simulations. |

---

## 4. Output Result
<img width="1506" height="969" alt="image" src="https://github.com/user-attachments/assets/a10715d0-ea8d-4f9e-82d7-95889b9cf55e" />

Figure 1: Benchmark comparison — Sequential vs Threading vs Multiprocessing with speedup chart and top stocks table

---

## 5. Performance Analysis

### 5.1 Results Summary

| Stocks | Ticks | Data Points | Sequential (s) | Threading (s) | Multiprocessing (s) | Thread Speedup | MP Speedup | Status |
|---|---|---|---|---|---|---|---|---|
| 200 | 500 | 100,000 | ~0.08s | ~0.10s | ~0.07s | ~0.80x | ~1.14x | Completed |
| 500 | 1,000 | 500,000 | ~0.35s | ~0.42s | ~0.28s | ~0.83x | ~1.25x | Completed |
| 1,000 | 1,000 | 1,000,000 | ~0.63s | ~0.73s | ~0.52s | ~0.86x | ~1.21x | Completed |
| 1,765 | 1,839 | 3,247,935 | 0.626s | 0.725s | 0.521s | 0.86x | 1.20x | Completed |

### 5.2 Stock Statistics

| Metric | Details |
|---|---|
| Stock Format | STK0001 to STKxxxx |
| Starting Price | $10.00 to $500.00 (random uniform) |
| Price Model | Gaussian random walk: change = gauss(0,1) x price x 0.01 |
| Price Floor | $0.01 minimum |
| Volatility | Population std dev of daily returns (single-pass optimized) |
| SMA-50 | Average of last 50 ticks |
| Total Return | ((end - start) / start) x 100% |
| Top Stocks | Top 20 by return — green = positive, orange = negative |

### 5.3 Analysis

#### Sequential
Processes stocks one by one without using threads or processes. It has no extra overhead, so it performs well for small datasets. However, it becomes slower when the data size increases.

#### Threading (ThreadPoolExecutor)
Uses multiple threads to process stocks at the same time. However, Python’s GIL (Global Interpreter Lock) allows only one thread to run at a time for CPU tasks. Because of this limitation and thread overhead, threading is slightly slower than sequential for this project.

#### Multiprocessing (Chunked Pool.map)
Uses multiple processes, where each process runs on a separate CPU core. This allows true parallel execution and avoids the GIL limitation. As a result, multiprocessing achieves better performance and is the fastest method in this project.

---

## 6. Conclusion

| Rank | Method | Best Time | Speedup | Notes |
|---|---|---|---|---|
| 1 | *Multiprocessing* | 0.521s | *1.20x* | Fastest — bypasses GIL |
| 2 | Sequential | 0.626s | 1.00x | Baseline — zero overhead |
| 3 | Threading | 0.725s | 0.86x | Slower — GIL limited |

Multiprocessing is the fastest method for this project because it uses multiple CPU cores and runs tasks in parallel. This allows it to process large data more efficiently.

Sequential execution provides a stable baseline and performs well for smaller datasets since it has no extra overhead.

Threading is slower for this project because of Python’s GIL, which limits true parallel execution for CPU-based tasks.

For future improvement, this project can be extended by using real-time data and combining multiprocessing with asynchronous programming for better performance.

---
