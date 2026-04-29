# 🚀 Adaptive Hybrid Parallel Web Health Monitoring System  

**Name:** Mastura Binti Rabaee  
**Student ID:** 2024201716  
**Class:** M3CS2554A  
**Course:** ITT440  
**Lecturer:** Shahadan Bin Saad

---

## 📌 Introduction
In today's digital environment, systems are required to handle large-scale data efficiently and reliably. Traditional sequential programming executes tasks one at a time, which can result in significant delays when processing thousands of web requests.

To overcome this limitation, concurrent and parallel programming techniques are used. These approaches allow multiple tasks to run simultaneously, improving performance, scalability, and overall system responsiveness. This project demonstrates how these techniques can be applied in a real-world web monitoring system.

---

## 📊 Project Overview
This project focuses on developing a high-performance web health monitoring system capable of checking the status of **5000 URLs** efficiently.

The system compares three execution approaches:
-  Sequential Programming  
-  Threading (Concurrent Programming)  
-  Multiprocessing (Parallel Programming)  

Additional features include:
- Dynamic resource scaling  
- Response time measurement  
- Result classification (FAST, NORMAL, SLOW, FAILED)  

---

## 🎯 Objectives
- To implement sequential, concurrent, and parallel programming techniques  
- To efficiently process a large-scale dataset  
- To compare execution performance  
- To demonstrate workload distribution  
- To analyze response time and classify results  

---

## 🏗️ System Design
The system is designed using a modular approach.

**Components:**
- URL Generator → Generates 5000 URLs  
- URL Loader → Loads URLs from file  
- URL Checker → Sends HTTP requests  
- Execution Modules:
  - Sequential  
  - Threading  
  - Multiprocessing  
- Performance Analyzer  

---
# ▶️ How to Run
**Step 1: Generate URLs python generate_urls.py**
<details>
<summary>Click to view generate_urls.py</summary>
		

```python
with open("urls.txt", "w") as f:
for i in range(1, 5001):
f.write(f"https://httpbin.org/status/{200 + (i % 5)}\n")
		

print("5000 URLs generated!")
```
</details> 
		

- This will create:

	- urls.txt
		

		

		

**Step 2: Run the Main Program**
		

<details>
<summary>Click to view main.py</summary>
		

```python
import requests
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import os
from requests.adapters import HTTPAdapter
import urllib3

# Disable SSL warnings (faster)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =========================================================
# GLOBAL SESSION (HIGH PERFORMANCE)
# =========================================================
session = requests.Session()

adapter = HTTPAdapter(
    pool_connections=200,
    pool_maxsize=200,
    max_retries=0
)

session.mount("http://", adapter)
session.mount("https://", adapter)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# =========================================================
# LOAD URLS
# =========================================================
def load_urls():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "urls.txt")

    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"❌ urls.txt not found at {file_path}")
        exit(1)

# =========================================================
# FAST URL CHECK (OPTIMIZED)
# =========================================================
def check_url(url):
    start = time.perf_counter()
    try:
        r = session.head(
            url,
            timeout=1.5,
            headers=HEADERS,
            allow_redirects=True,
            verify=False
        )
        return (url, r.status_code, round(time.perf_counter() - start, 3))
    except:
        return (url, "FAILED", 0)

# =========================================================
# CLASSIFY
# =========================================================
def classify(result):
    _, status, t = result
    if status == "FAILED":
        return "FAILED"
    elif t < 0.2:
        return "FAST"
    elif t < 1:
        return "NORMAL"
    else:
        return "SLOW"

# =========================================================
# PRINT RESULTS
# =========================================================
def print_results(results):
    print("\n--- SAMPLE RESULTS ---")
    for r in results[:20]:
        print(f"{r[0]} | {r[1]} | {r[2]}s | {classify(r)}")
    print(f"... total: {len(results)} URLs checked")

# =========================================================
# SEQUENTIAL
# =========================================================
def sequential(urls):
    print("\n[SEQUENTIAL] Running...")

    start = time.perf_counter()
    results = [check_url(url) for url in urls]
    total = time.perf_counter() - start

    print_results(results)
    print(f"[SEQUENTIAL] Time: {total:.2f}s")
    return total

# =========================================================
# THREADING (BEST FOR I/O)
# =========================================================
def threading_version(urls):
    print("\n[THREADING] Running...")

    workers = min(200, len(urls))  # balanced (too high = slower)
    print(f"Using {workers} threads")

    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(check_url, urls))

    total = time.perf_counter() - start

    print_results(results)
    print(f"[THREADING] Time: {total:.2f}s")
    return total

# =========================================================
# MULTIPROCESSING
# =========================================================
def multiprocessing_version(urls):
    print("\n[MULTIPROCESSING] Running...")

    processes = min(multiprocessing.cpu_count(), 8)
    print(f"Using {processes} processes")

    start = time.perf_counter()

    with multiprocessing.Pool(processes) as pool:
        results = list(pool.imap_unordered(check_url, urls, chunksize=50))

    total = time.perf_counter() - start

    print_results(results)
    print(f"[MULTIPROCESSING] Time: {total:.2f}s")
    return total

# =========================================================
# COMPARE
# =========================================================
def compare(seq, th, mp):
    print("\n===== PERFORMANCE =====")
    print(f"Sequential      : {seq:.2f}s")
    print(f"Threading       : {th:.2f}s")
    print(f"Multiprocessing : {mp:.2f}s")

# =========================================================
# MAIN MENU
# =========================================================
def main():
    urls = load_urls()
    print(f"✅ Loaded {len(urls)} URLs")

    while True:
        print("\n===== URL CHECKER =====")
        print("1. Sequential")
        print("2. Threading (FAST)")
        print("3. Multiprocessing")
        print("4. Run All")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            sequential(urls)

        elif choice == "2":
            threading_version(urls)

        elif choice == "3":
            multiprocessing_version(urls)

        elif choice == "4":
            seq = sequential(urls)
            th = threading_version(urls)
            mp = multiprocessing_version(urls)
            compare(seq, th, mp)

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("❌ Invalid choice")

# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
```
</details> 
		
--- 

# 🖥️ Program Menu
===== URL STATUS CHECKER ===== 
1. Sequential 
2. Threading (Dynamic) 
3. Multiprocessing (Dynamic) 
4. Run All (Compare)
5. Exit

---

# 🧪 Sample Input
The input file (urls.txt) contains 5000 URLs:

---

# 📊 Sample Output
**Sequential Output**
<img width="786" height="568" alt="Screenshot 2026-04-24 015214" src="https://github.com/user-attachments/assets/ef5e4583-ceb9-4011-9514-9318206017e1" />


		

**Treading Output**
<img width="701" height="597" alt="Screenshot 2026-04-24 015303" src="https://github.com/user-attachments/assets/20bc8b8a-e019-4d5c-b757-8a91e0e9e1e2" />

		

**Multiprocessing Output**
<img width="705" height="600" alt="Screenshot 2026-04-24 015311" src="https://github.com/user-attachments/assets/5b302a3a-cea4-431e-9ca3-7cb8a00d7945" />

**Final Output**
<img width="532" height="109" alt="Screenshot 2026-04-24 015318" src="https://github.com/user-attachments/assets/ab3afd1c-030e-401c-944c-395c6b23ffad" />

---

# ⚡ Performance Analysis
| Method           | Time (seconds) | Performance |
|----------------|---------------|------------|
| Sequential      | 1931.33       | Very Slow  |
| Threading       | 18.86         | Fast       |
| Multiprocessing | 236.86        | Moderate   |

- Sequential execution is the slowest due to its linear processing approach
- Threading achieves the best performance for I/O-bound tasks
- Multiprocessing introduces overhead, making it less efficient for network-based operations
--- 

# Bar Chart

<img width="640" height="480" alt="Figure_1" src="https://github.com/user-attachments/assets/97e58979-4de4-4d93-99b0-58a38ab72d78" />


**Observation:**
		

The results clearly show that choosing the right programming model is crucial. Since this project involves network requests (I/O-bound tasks), threading performs significantly better by allowing multiple requests to be processed concurrently.

Multiprocessing, although powerful for CPU-bound tasks, is less suitable here due to process creation overhead and communication costs.

--- 

# 🎥 Demonstration Video

https://youtu.be/Pu8BO5MWfwo?si=-dJRxc304-5XWMr5

--- 

# 🧩 Challenges Faced
- Handling large datasets efficiently
- Avoiding timeout errors
- Optimizing thread and process usage
- Ensuring fair performance comparison

--- 

# 💡 Conclusion
In conclusion, this project successfully demonstrates how concurrent and parallel programming can significantly improve system performance.

Threading is proven to be the most effective approach for I/O-bound applications such as web monitoring. Additionally, dynamic scaling enhances efficiency by adapting resource usage based on workload.

Overall, this project highlights the importance of selecting the appropriate technique to achieve optimal performance in real-world systems.
		

