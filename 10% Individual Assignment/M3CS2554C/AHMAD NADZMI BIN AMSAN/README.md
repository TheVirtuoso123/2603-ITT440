# 🔓 Parallel Hash Breaker: Cracking Passwords at the Speed of Parallel Computing

Name: Ahmad Nadzmi Bin Amsan 

Student ID: 2025239524

Course Code: ITT440: Network Programming

Lecturer: Shahadan Bin Saad

Youtube Link : https://www.youtube.com/watch?v=EzCX8cD6PAc&t=6s

# 🎯 Mission Objective
In password security auditing, time is the only barrier between a hash and its plaintext. Traditional brute‑force methods test one password at a time, making complex cracking attempts painfully slow.

The Parallel Hash Breaker is a high‑performance cryptographic cracker that leverages multiprocessing, threading, and sequential models to demonstrate real‑world parallel computing concepts. By distributing password attempts across all available CPU cores, it transforms a standard laptop into a password‑recovery powerhouse, achieving over 3x speedup on intensive workloads while generating professional performance graphs.

# 📁 Project Overview
The Parallel Hash Breaker is a Python‑based tool designed to teach and demonstrate the differences between sequential, threaded, and parallel (multiprocessing) execution for CPU‑bound tasks specifically password hashing. Understanding parallelism is critical for modern cybersecurity and data processing. A security analyst who can parallelise log analysis, hash cracking, or pattern matching gains a decisive speed advantage. This project provides a hands‑on, visual, and quantitative comparison of three execution models, making abstract concepts like the GIL and process‑based parallelism tangible

# 💻 Hardware & Environment
Processor: Quad‑Core / Octa‑Core CPU (e.g., Intel i5‑8250U @ 1.60GHz)

Memory: 8GB RAM minimum

OS: Linux Environment (Ubuntu 22.04+ recommended)

Runtime: Python 3.8+ with matplotlib for analytics and tqdm for real‑time progress bars.

# 🛠️ Install required libraries
The Parallel Hash Breaker uses two optional but highly recommended libraries:

1. matplotlib – Automatic Graph Generation
Purpose: After each benchmark run, the script automatically generates two professional‑grade graph.

2. tqdm – Real‑time Progress Bars
Purpose: Shows a live, updating progress bar during the sequential crack, giving visual feedback on how many passwords have been tested and the estimated time remaining.

# 🔋Run the full benchmark (sequential, threading, parallel) with default SHA256
python parallel_hash_breaker.py --limit 50000000
C. Extra Tasks for Deeper Analysis
The following additional commands allow you to explore different hash algorithms, worker counts, dictionary attacks, and the lightweight difficulty benchmark.

**Task	Command**
1. Switch to MD5 algorithm:	*python parallel_hash_breaker.py --algo md5*
2. Use fewer workers: *python parallel_hash_breaker.py --workers2*
3. Run dictionary attack:	*python3 parallel_hash_breaker.py --dict*
4. Run difficulty benchmark: *python parallel_hash_breaker.py --difficulty*


# 📊 Battlefield Analytics
**A. Single Large Task** (50 Million Hashes) – Default SHA256
When cracking a SHA‑256 hash positioned near the end of a 50‑million number space, the engine produces the following performance breakdown:

Method	Time (seconds)	Speedup vs Sequential
Sequential (1 core)	36.14 s	1.00x (baseline)
Threading (8 threads)	35.92 s	1.01x (GIL limited)
Parallel (8 cores)	11.34 s	3.19x 🚀
Total passwords tested: 50,000,000
Target hash: SHA-256("49999999")
Result found: 49999999

![image alt](https://github.com/NadzmiAmsan/Parallel-Hash-Breaker-with-Performance-Visualizer/blob/5cdefac15cd26d75bee3578d48601a5bb4c47e22/performance_comparison%20normal.png)

    Figure 1: Parallel multiprocessing outperforms threading and sequential models due to true CPU parallelism.



**B. Effect of Hash Algorithm** – MD5 vs SHA256
Hash algorithms have different speeds. MD5 is generally faster than SHA256 because it uses fewer computational rounds. Running the same benchmark with --algo md5 

Algorithm	Sequential Time (s)	Parallel Time (8 cores)	Speedup
SHA256	36.14	11.34	3.19x
MD5	28.50	8.90	3.20x
Observation: MD5 is ~21% faster overall, but the parallel speedup ratio remains similar – proving that parallel gains are independent of hash algorithm.

![image alt](https://github.com/NadzmiAmsan/Parallel-Hash-Breaker-with-Performance-Visualizer/blob/5cdefac15cd26d75bee3578d48601a5bb4c47e22/performance_comparison%20MD5.png)

    Figure 2: Parallel multiprocessing outperforms threading and sequential using MD5, diffenrent hash algorithm.


**C. Scaling with Fewer Workers** – The --workers 2 Test
Not all environments have 8 cores. Running with only 2 workers (--workers 2) shows how speedup scales with fewer resources:

Workers	Time (s)	Speedup vs Sequential
1 (sequential)	36.14	1.00x
2	18.92	1.91x
4	14.10	2.56x
8	11.34	3.19x
Observation: Doubling workers roughly doubles speed until diminishing returns due to overhead. This is a textbook example of near‑linear scaling – perfect for teaching parallel computing concepts.

![image alt](https://github.com/NadzmiAmsan/Parallel-Hash-Breaker-with-Performance-Visualizer/blob/5cdefac15cd26d75bee3578d48601a5bb4c47e22/performance_comparison%202%20cpu.png)

    Figure 3: Parallel multiprocessing outperforms threading and sequential with 2 workers(CPU).



**D. Dictionary Attack** – Fast Wordlist Cracking
The dictionary attack tries common words plus simple mutations (capitalization, appending 123 or !). It is extremely fast because the search space is tiny.

Command: *python parallel_hash_breaker.py --dict*

Dictionary Size	Mutations per Word	Candidates Tested	Result	Time
5 base words	20 total	20	Not found (default)	0.0004 s
Note: The default dictionary (admin, password, 123456, etc.) does not match the numeric target hash (49999999). To see a successful crack, either:

Change Config.TARGET_HASH to match a dictionary word (e.g., hashlib.sha256(b"admin").hexdigest())

Or add the number 49999999 to the dictionary list.

![image alt](https://github.com/NadzmiAmsan/Parallel-Hash-Breaker-with-Performance-Visualizer/blob/2a29f1ae9f5e6943162d938bfa8373c82ac5ef64/dictionary_attack.png) 

    Figure 4:Terminal output showing dictionary attack run with "Not found" message

Why include dictionary attack?
Real‑world password cracking often starts with dictionary attacks before brute‑force – they are orders of magnitude faster when users choose weak passwords.



**E. Lightweight Difficulty Benchmark** – Runs in Seconds
This built‑in benchmark (--difficulty) is designed for quick demonstrations. It generates random passwords of increasing length/complexity and runs both sequential and parallel hashing.


Command: *python parallel_hash_breaker.py --difficulty*

Level	Passwords	Algorithm	Password Len	Sequential (s)	Parallel (s)	Speedup
very_easy	100,000	md5	4	0.48	0.19	2.53x
easy	10,000	md5	8	0.09	0.04	2.25x
intermediate	1,000	sha256	8	0.05	0.02	2.50x
hard	100	sha256	12	0.02	0.01	2.00x
very_hard	10	sha512	16	0.01	0.01	1.00x
Key Takeaways:

For large task counts (100k), parallel gives ~2.5x speedup.

For tiny tasks (10 passwords), overhead dominates and speedup disappears – demonstrating that parallelism has a cost.

This benchmark is ideal for live lectures because it finishes in seconds without needing huge datasets.

![image alt](https://github.com/NadzmiAmsan/Parallel-Hash-Breaker-with-Performance-Visualizer/blob/2a29f1ae9f5e6943162d938bfa8373c82ac5ef64/Difficulty_benchmark.png)

        Figure 5: Screenshot of the difficulty benchmark output from terminal



# 🧠 How It Works (The Logic)
The Parallel Hash Breaker implements three distinct cracking models and a difficulty benchmark, all following a MapReduce‑inspired pattern:

1. Sequential (Baseline)
Partition: None. One loop from 0 to limit.

Analyze: Single core hashes each number one by one.

Synthesize: Returns first match.

2. Threading (GIL Demonstration)
Partition: Search space divided among the threads.

Analyze: Each thread runs Python code concurrently – but the Global Interpreter Lock (GIL) allows only one thread to execute Python bytecode at a time.

Result: Minimal speedup (hashing is CPU‑bound, so threads just add overhead).

3. Parallel (Multiprocessing) – True Speedup
Partition: Search space split into N equal chunks (one per CPU core).

Analyze: Each core runs a separate Python process with its own GIL. Hashing happens in true parallel.

Early Termination: As soon as any process finds the password, it terminates the entire pool – saving time.

Synthesize: The main process collects the result.

4. Difficulty Benchmark (Lightweight & Fast)
Partition: A list of random passwords is generated per difficulty level (100k very easy … 10 very hard).

Analyze: Sequential version hashes each password one by one. Parallel version distributes the list across all cores using Pool.map().

Result: Even though each task is tiny, the overhead of multiprocessing is offset by true parallelism for medium/large counts.

# ✅ Conclusion
The Parallel Hash Breaker successfully demonstrates:

True parallelism using Python's multiprocessing module.

The limitations of threading under the GIL.

Practical speedups of 3x or more on a standard laptop.

Fast, demo‑friendly benchmarks (difficulty benchmark) that run in seconds.

Real‑world tasks like dictionary attacks and algorithm switching.

These concepts are directly transferable to other domains: log analysis, image processing, data transformation – anywhere CPU‑bound tasks can be split into independent chunks.
