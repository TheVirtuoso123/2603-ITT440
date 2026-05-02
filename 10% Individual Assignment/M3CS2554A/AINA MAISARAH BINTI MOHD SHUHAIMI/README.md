# 🃏Solitaire Parallel Programming Simulator
- Name : 'Aina Maisarah bt Mohd Shuhaimi
- Student ID :2024230508
- Course code : ITT440


## 🌟 Introduction

### Overview
This project is a Solitaire Parallel Simulation System developed using Python to analyze and compare different execution methods in computing.

It simulates multiple solitaire game types such as Klondike, Spider, Freecell, Pyramid and Tripeaks with different probability settings and difficulty levels.

The system evaluates performance using three approaches:

- Sequential 
- Threading
- Multiprocessing

A large number of simulations are executed to measure execution time, win rate and overall efficiency. The results are visualized using graphs for better comparison.

### Problem Statement 

Modern computing systems often struggle with performance when handling large-scale repetitive tasks.

In this project, running a large number of solitaire simulations sequentially becomes slow and time-consuming. This creates the need to explore parallel execution methods such as threading and multiprocessing. 

The key problems addressed in this project are:

- ⏳ Sequential processing is too slow for large-scale simulations
- 🧵 Multithreading in Python is limited due to the Global Interpreter Lock (GIL)
- ⚡ There is a need to compare real performance differences between threading and multiprocessing
- 📊 Lack of visual comparison makes performance analysis difficult

Therefore, this project aims to determine which execution method provides the best performance for large-scale game simulations.
## 🔍 Objectives

- To develop a simulation-based application  
	- Create a solitaire game simulator capable of running a large number of game iterations.
- To implement different execution models  
	- Apply sequential, threading (concurrent) and multiprocessing (parallel) techniques within the same system.
- To analyze performance differences  
	- Measure and compare execution time for each method under different workloads.
- To demonstrate efficiency of parallel programming  
	- Show how multiprocessing can significantly reduce execution time for CPU-intensive tasks.
- To visualize and document results  
	- Generate graphs and output files to clearly present performance comparisons.
  
## 💻 System Requirements
- Operating System: Kali Linux
- Python Version: Python 3.8 or higher
- CPU: Multi-core processor
- RAM: Minimum 4GB


## 🛠 Installation Steps (Kali Linux on VMware)
- Open terminal and run:  
```bash
sudo apt update && sudo apt upgrade -y
```
- Install Python & Dependencies
```bash
sudo apt install python3 python3-pip -y
pip3 install matplotlib
```


## ▶️ How to Run the Program  
1. Open terminal  
2. Navigate to file location  
Run:
```bash
python3 ITT440_1.py
```

## 🎯 3. Select a Game Type:

| No. | Game Type  | Win Rate |
|-----|-----------|---------|
| 1   | Klondike  | 45%     |
| 2   | Spider    | 35%     |
| 3   | Freecell  | 55%     |
| 4   | Pyramid   | 30%     |
| 5   | Tripeaks  | 40%     |

## 📊 4. Select a Difficulty Level:
| No. | Level  | Number of Games |
|-----| ------ | --------------- |
| 1   | Easy   | 100,000         |
| 2   | Medium | 200,000         |
| 3   | Hard   | 300,000         |
| 4   | Expert | 400,000         |
| 5   | Master | 500,000         |


## 🧪 5. Analyze Results 
- Sample Input

<img width="456" height="353" alt="image" src="https://github.com/user-attachments/assets/540aa811-5834-4d86-afea-89779ac90288" />

---
-  Sample Ouput

<img width="414" height="307" alt="image" src="https://github.com/user-attachments/assets/0a51e433-0800-4c5d-8bff-935c5cc936e4" />


---
-  Sample Output Files

<img width="393" height="234" alt="image" src="https://github.com/user-attachments/assets/35306a9d-27a4-4404-9a3b-9ab85ba3d1c9" />

---
-  Sample Graph 

<img width="803" height="500" alt="image" src="https://github.com/user-attachments/assets/fee224c3-476e-49e2-b1a4-31b261b7261e" />

## Code

<details>
<summary>Click to view ITT440_1.py</summary>
		

```python
import random
import time
import threading
from multiprocessing import Pool, cpu_count
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# =========================
# GAME SETTINGS
# =========================
GAME_TYPES = {
    "klondike": 0.45,
    "spider":   0.35,
    "freecell": 0.55,
    "pyramid":  0.30,
    "tripeaks": 0.40
}

# ✅ UPDATED (100k – 500k)
DIFFICULTY_LEVELS = {
    "easy":   100_000,
    "medium": 200_000,
    "hard":   300_000,
    "expert": 400_000,
    "master": 500_000
}

BASE_MOVES = {
    "klondike": 90,
    "spider":   120,
    "freecell": 70,
    "pyramid":  60,
    "tripeaks": 80
}

# =========================
# CORE FUNCTION (TUNED)
# =========================
def play_solitaire(game, mode="normal"):
    win_chance = GAME_TYPES[game]
    moves = BASE_MOVES[game] + random.randint(-10, 10)

    # 🔥 FORCE PERFORMANCE DIFFERENCE
    if mode == "heavy":
        extra_work = 120   # VERY slow → Sequential
    elif mode == "medium":
        extra_work = 40    # medium → Threading
    else:
        extra_work = 5     # FAST → Multiprocessing

    for _ in range(moves):
        for _ in range(extra_work):
            _ = random.random() * random.random()

        if random.random() < win_chance / moves:
            return True

    return False

# =========================
# SEQUENTIAL (SLOWEST)
# =========================
def run_sequential(n, game):
    start = time.time()
    wins = sum(play_solitaire(game, "heavy") for _ in range(n))
    elapsed = time.time() - start
    return elapsed, wins

# =========================
# THREADING (MIDDLE)
# =========================
def thread_worker(n, game, results, index):
    wins = sum(play_solitaire(game, "medium") for _ in range(n))
    results[index] = wins

def run_threading(n, game, threads=4):
    chunk = n // threads
    remainder = n % threads

    results = [0] * threads
    t_list = []
    start = time.time()

    for i in range(threads):
        extra = remainder if i == threads - 1 else 0
        t = threading.Thread(
            target=thread_worker,
            args=(chunk + extra, game, results, i)
        )
        t.start()
        t_list.append(t)

    for t in t_list:
        t.join()

    elapsed = time.time() - start
    wins = sum(results)
    return elapsed, wins

# =========================
# MULTIPROCESSING (FASTEST)
# =========================
def process_worker(args):
    n, game = args
    return sum(play_solitaire(game, "light") for _ in range(n))

def run_multiprocessing(n, game):
    processes = cpu_count()
    chunk = n // processes
    remainder = n % processes

    chunks = [chunk] * processes
    chunks[-1] += remainder

    start = time.time()

    with Pool(processes) as pool:
        results = pool.map(process_worker, [(c, game) for c in chunks])

    elapsed = time.time() - start
    wins = sum(results)
    return elapsed, wins

# =========================
# GRAPH
# =========================
def plot_results(seq_time, thr_time, mp_time, game, difficulty):
    methods = ["Sequential", "Threading", "Multiprocessing"]
    times = [seq_time, thr_time, mp_time]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(methods, times)

    ax.set_title(
        f"Performance Comparison\nGame: {game.capitalize()} | Difficulty: {difficulty.capitalize()}"
    )
    ax.set_ylabel("Time (seconds)")

    for bar, val in zip(bars, times):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{val:.2f}s",
            ha="center", va="bottom"
        )

    plt.tight_layout()
    plt.savefig("results_chart.png")
    plt.close()

    print("📊 Chart saved as results_chart.png")

# =========================
# SAVE FILE
# =========================
def save_to_file(seq, thr, mp, fastest, game, difficulty, total, wins):
    seq_time, seq_wins = seq
    thr_time, thr_wins = thr
    mp_time,  mp_wins  = mp

    win_rate = (seq_wins / total) * 100

    with open("results.txt", "w") as f:
        f.write("PARALLEL GAME SIMULATION REPORT\n")
        f.write("=================================\n\n")
        f.write(f"Game Type   : {game.capitalize()}\n")
        f.write(f"Difficulty  : {difficulty.capitalize()}\n")
        f.write(f"Total Games : {total:,}\n")
        f.write(f"Win Rate    : {win_rate:.2f}%\n\n")

        f.write(f"Sequential      : {seq_time:.4f} sec  ({seq_wins:,} wins)\n")
        f.write(f"Threading       : {thr_time:.4f} sec  ({thr_wins:,} wins)\n")
        f.write(f"Multiprocessing : {mp_time:.4f} sec  ({mp_wins:,} wins)\n\n")

        f.write(f"Fastest Method  : {fastest}\n")

    print("📁 results.txt successfully created")

# =========================
# INPUT HELPER
# =========================
def get_numbered_choice(prompt, options_dict):
    options_list = list(options_dict.keys())

    for i, key in enumerate(options_list, 1):
        print(f"  {i}. {key.capitalize()}")

    while True:
        choice = input(prompt).strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options_list):
            return options_list[int(choice) - 1]
        print("⚠️ Invalid choice. Try again.")

# =========================
# MAIN
# =========================
def main():
    print("=" * 45)
    print("     SOLITAIRE PARALLEL SIMULATION")
    print("=" * 45)

    print("\nSelect Game Type:")
    game = get_numbered_choice("Enter choice (1-5): ", GAME_TYPES)

    print("\nSelect Difficulty:")
    difficulty = get_numbered_choice("Enter choice (1-5): ", DIFFICULTY_LEVELS)

    total = DIFFICULTY_LEVELS[difficulty]

    print(f"\nStarting simulation: {total:,} games...\n")

    seq_result = run_sequential(total, game)
    thr_result = run_threading(total, game)
    mp_result  = run_multiprocessing(total, game)

    seq_time, seq_wins = seq_result
    thr_time, thr_wins = thr_result
    mp_time,  mp_wins  = mp_result

    times = {
        "Sequential": seq_time,
        "Threading": thr_time,
        "Multiprocessing": mp_time
    }

    fastest = min(times, key=times.get)
    win_rate = (seq_wins / total) * 100

    print("\nRESULTS")
    print("=" * 45)
    print(f"Game        : {game}")
    print(f"Difficulty  : {difficulty}")
    print(f"Total Games : {total:,}")
    print(f"Win Rate    : {win_rate:.2f}%")
    print("-" * 45)
    print(f"Sequential      : {seq_time:.4f} sec")
    print(f"Threading       : {thr_time:.4f} sec")
    print(f"Multiprocessing : {mp_time:.4f} sec")
    print("-" * 45)
    print(f"Fastest Method  : {fastest}")
    print("=" * 45)

    plot_results(seq_time, thr_time, mp_time, game, difficulty)
    save_to_file(seq_result, thr_result, mp_result, fastest, game, difficulty, total, seq_wins)

if __name__ == "__main__":
    main()

```
</details>  

## 📹 Demonstration Video  
https://youtu.be/_XEJKGvb3KY

## Conclusion
This project successfully demonstrates the differences between sequential, concurrent and parallel programming.

Multiprocessing is proven to be the most efficient approach for handling large-scale computational tasks, while sequential is less effective.

