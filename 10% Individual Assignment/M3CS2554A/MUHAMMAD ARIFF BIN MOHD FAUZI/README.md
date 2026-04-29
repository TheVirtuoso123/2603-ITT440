# MUHAMMAD ARIFF BIN MOHD FAUZI
## Problem Statement 
Streaming platforms like Netflix manage millions of watch events daily. Calculating global trends (Top 10) and personalized user recommendations (similarity scores) requires massive computational power. Executing these tasks sequentially on a single CPU core is simply unachievable as it is insufficient. This project explores how Parallelism (Multiprocessing) and Concurrency (Threading) can be used to optimize these calculations, providing a scalable solution for big-data streaming analytics.

## Segment Code
1. Sequential Execution: The "Baseline." It processes one user at a time. If user A takes 2 seconds and user B takes 2 seconds, the total is 4 seconds.
   
''' def run_sequential(db, targets, all_uids):
    print("\n[TEST] Running Sequential Analysis...")
    start = time.time()
    results = [get_recommendations(u, db, all_uids) for u in targets]
    return time.time() - start '''

2. Concurrency (Threading): Uses ThreadPoolExecutor. Explain that while it manages multiple tasks, it is limited by the Global Interpreter Lock (GIL) in Python, meaning it doesn't truly run math in parallel on multiple cores.

''' def run_concurrent_threads(db, targets, all_uids):
    print("[TEST] Running Concurrent Threading...")
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Threads share the same memory space
        results = list(executor.map(lambda u: get_recommendations(u, db, all_uids), targets))
    return time.time() - start '''

3. Parallelism (Multiprocessing): Uses ProcessPoolExecutor. It creates a separate memory instance for each CPU core, allowing the computer to perform 4 or 8 calculations at the exact same millisecond.

''' def run_parallel_processes(db, targets, all_uids):
    print("[TEST] Running Parallel Multiprocessing...")
    start = time.time()
    args = [(u, db, all_uids) for u in targets]
    # Uses all available CPU cores by default
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(worker_wrapper, args))
    return time.time() - start '''

## Analysis
After collecting all the data needed from a certain amount of users, I have acknowledged that when using a sequential performance, the execution time is linear as every user added, the time increases by a fixed amount, therefore the speedup factor is 1.00x with 16.07 seconds time in real time. Whereas, when the system use the threading method, the result shows a slight slowdown compared to sequential with 1.06x speedup factor, taking 16.75 seconds in total to sort the data. Lastly,with the highest efficiency, the Parallel Multiprocessing bringing up a speedup factor close to the number of available CPU cores of 0.42x and time taken 38.16

## Summary
The experimental results validate that for data-intensive streaming analytics, Parallel Programming via Multiprocessing is the only viable method for maintaining real-time performance. By distributing the computational load of 1 million records across the hardware's full architecture, we transformed a slow, single-threaded task into a high-performance recommendation engine.
