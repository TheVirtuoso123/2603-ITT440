# 📄 Performance Report: Concurrency vs Parallelism in Document Similarity System
Name: NOR IKHWAN BIN SAMSUDDIN<br>
Student ID: 2025216128<br>
Group: M3CS2554C<br>
Lecturer Name: SIR SHAHADAN BIN SAAD<br>
# 1. Project Overview
The Parallel Document Similarity Checker is a Python-based system designed to compare multiple text documents efficiently.
It supports .txt and .md files. A key feature of this system is its adaptive execution model, where it automatically selects the most efficient processing strategy based on workload size:

* 🧭 Sequential processing for small datasets
* Concurrent processing (threading) for preprocessing larger datasets
* Parallel processing (multiprocessing) for computationally intensive similarity calculations

This design ensures optimal performance while avoiding unnecessary computational overhead.

# 🎯 2. Project Objective
The objectives of this project are:<br>

* To develop a system that accurately measures similarity between multiple documents
* To improve performance through adaptive execution strategies
* To demonstrate the practical differences between:
  * Sequential processing
  * Concurrent processing (threading)
  * Parallel processing (multiprocessing)
* To reduce execution time when handling larger datasets
* To balance efficiency vs system overhead automatically
  
# ⚙️ 3. Device Specification
The program was executed in a Linux-based environment with the following general specifications:<br>
* Operating System: Kali Linux Debian (64-bit)
* Processor: Multi-core CPU with the minimum size of 2
* RAM: Sufficient to handle multiple processes with the minimum size of 2GB<br>

Without a multi-core CPU, the multiprocessing cannot be executed properly.
# 🚀 4. Program Deployment
Go terminal run the program file by writing the program file name along with its directory path.
```bash
python3 Desktop/D/similarity_checker.py
Enter the path to a FOLDER containing the documents to compare.
Supported formats: .md, .txt  (UTF-8 encoded)
Type 'exit' at any prompt to quit.

  Folder path:
```
For this testing we create 2 folder, one with 5 .txt files and the other with 100 .txt files.<br>
Enter the folder path and the program will check all the file in the folder and check the similarity
```bash
  Folder path: /home/tiaramitsu/Desktop/D/T1

  Found 5 file(s):
    ✓ 'T1'  (83 words)
    ✓ 'T2'  (71 words)
    ✓ 'T3'  (69 words)
    ✓ 'T4'  (71 words)
    ✓ 'T5'  (75 words)

──────────────────────────────────────────────────────────────────────
  AUTO-MODE SELECTION
──────────────────────────────────────────────────────────────────────
  Documents : 5  (threshold: < 6 → sequential)
  Pairs     : 10  (threshold: < 15 → sequential)
  Preprocessing  → Sequential (for-loop)
  Similarity     → Sequential (for-loop)

──────────────────────────────────────────────────────────────────────
  STAGE 1 — Sequential Preprocessing  (small workload)
──────────────────────────────────────────────────────────────────────

[Sequential] Preprocessing 5 documents one by one …
  ✓ Finished: 'T1'  (81 tokens, 79 unique bigrams)
  ✓ Finished: 'T2'  (68 tokens, 67 unique bigrams)
  ✓ Finished: 'T3'  (67 tokens, 64 unique bigrams)
  ✓ Finished: 'T4'  (69 tokens, 68 unique bigrams)
  ✓ Finished: 'T5'  (70 tokens, 66 unique bigrams)
[Sequential] All documents preprocessed in 317.6 ms

──────────────────────────────────────────────────────────────────────
  STAGE 3 — Sequential Similarity  (small workload)
──────────────────────────────────────────────────────────────────────
[Sequential] Computing 10 pair(s) one by one …
  ✓ 'T1' ↔ 'T2'  hybrid=0.1766  (cosine=0.2717, jaccard=0.0000)  [0.037 ms]
  ✓ 'T1' ↔ 'T3'  hybrid=0.1960  (cosine=0.3015, jaccard=0.0000)  [0.023 ms]
  ✓ 'T1' ↔ 'T4'  hybrid=0.1985  (cosine=0.3016, jaccard=0.0068)  [0.02 ms]
  ✓ 'T1' ↔ 'T5'  hybrid=0.1688  (cosine=0.2596, jaccard=0.0000)  [0.016 ms]
  ✓ 'T2' ↔ 'T3'  hybrid=0.1407  (cosine=0.2123, jaccard=0.0077)  [0.023 ms]
  ✓ 'T2' ↔ 'T4'  hybrid=0.1710  (cosine=0.2509, jaccard=0.0227)  [0.017 ms]
  ✓ 'T2' ↔ 'T5'  hybrid=0.1861  (cosine=0.2781, jaccard=0.0153)  [0.015 ms]
  ✓ 'T3' ↔ 'T4'  hybrid=0.1579  (cosine=0.2429, jaccard=0.0000)  [0.016 ms]
  ✓ 'T3' ↔ 'T5'  hybrid=0.1157  (cosine=0.1780, jaccard=0.0000)  [0.014 ms]
  ✓ 'T4' ↔ 'T5'  hybrid=0.2054  (cosine=0.3036, jaccard=0.0229)  [0.016 ms]
[Sequential] All pairs done in 0.7 ms

===========================================================================
  DOCUMENT SIMILARITY REPORT  (Hybrid: 65% TF-IDF cosine + 35% Bigram Jaccard)
===========================================================================
  Pair                                      Bar                              Score
---------------------------------------------------------------------------
  T4  ↔  T5                                 █████░░░░░░░░░░░░░░░░░░░░░░░   20.5%
  T1  ↔  T4                                 █████░░░░░░░░░░░░░░░░░░░░░░░   19.8%
  T1  ↔  T3                                 █████░░░░░░░░░░░░░░░░░░░░░░░   19.6%
  T2  ↔  T5                                 █████░░░░░░░░░░░░░░░░░░░░░░░   18.6%
  T1  ↔  T2                                 ████░░░░░░░░░░░░░░░░░░░░░░░░   17.7%
  T2  ↔  T4                                 ████░░░░░░░░░░░░░░░░░░░░░░░░   17.1%
  T1  ↔  T5                                 ████░░░░░░░░░░░░░░░░░░░░░░░░   16.9%
  T3  ↔  T4                                 ████░░░░░░░░░░░░░░░░░░░░░░░░   15.8%
  T2  ↔  T3                                 ███░░░░░░░░░░░░░░░░░░░░░░░░░   14.1%
  T3  ↔  T5                                 ███░░░░░░░░░░░░░░░░░░░░░░░░░   11.6%
===========================================================================

=================================================================
  EXECUTION SUMMARY
=================================================================
  Documents processed                           5
  Pairs compared                               10

  Stage                                           Mode      Time
-----------------------------------------------------------------
  Preprocessing                             Sequential    317.6ms
  Similarity computation                    Sequential      0.7ms
-----------------------------------------------------------------
  TOTAL                                                   318.3ms
=================================================================
```
The system will give the similarity scores for all document pairs and execution time summary.

**HOW IT WORK**<br>

Stage 1: Preprocessing (Cleaning the text)<br>
In this stage, the program prepares the documents so they are easier to analyze.<br>

* Tokenization: The text is broken down into individual words.<br>
* Bigram Extraction: The program looks at pairs of consecutive words.<br>
* Stopword Handling: Common words like “the”, “is”, “and” are removed because they don’t add much meaning.<br>

This process clean up and standardize the text so comparisons are more meaningful.<br>

Stage 2: Feature Preparation (Turning text into numbers)<br>
Computers cannot directly understand words, so the text is converted into numerical form.<br>

TF-IDF Vector Preparation<br>
* Each document is transformed into a set of numbers based on how important each word is:<br>
* Words that appear often in one document → more important<br>
* Words that appear in many documents → less important<br>

This help represent each document as numbers so they can be mathematically compared.<br>

Stage 3: Similarity Computation (Comparing documents)<br>
In this stage, the program actually compares the documents using two methods:<br>

* Cosine Similarity: Measures how similar two documents are based on their word importance (TF-IDF values). Higher value = more similar content.<br>
* Jaccard Similarity (Bigram-based): Compares how many word pairs (bigrams) are shared between two documents. Hybrid Score Calculation<br>
* The final similarity score combines both:<br>
  * 65% from cosine similarity<br>
  * 35% from Jaccard similarity<br>

This help produce a more balanced and accurate similarity score between documents.

# 📊 5. Result Analytics
Based on the result, we can see that sequential provide a rather fast process execution with a total time of 318.3ms for 5 files.
<p align="center">
  <img width="512" height="243" alt="image" src="https://github.com/user-attachments/assets/dc9c4d4e-ed80-4675-ae94-a7167af42371" />
  Figure 1.1 Sequential Performance
</p>

To compare sequential with both concurrent and parallel, we run the program again but instead of writing the folder T1, we will write the folder T3 instead.
```bash
python3 Desktop/D/similarity_checker.py
Enter the path to a FOLDER containing the documents to compare.
Supported formats: .md, .txt  (UTF-8 encoded)
Type 'exit' at any prompt to quit.

  Folder path: /home/tiaramitsu/Desktop/D/T3
```

Processing 100 files in T3 utilizes both concurrent and parallel execution. While combining these methods increases overhead and resource consumption, it is significantly faster than sequential processing. For large batches of files, the performance gains justify the additional overhead.
<p align="center">
  <img width="512" height="243" alt="S2" src="https://github.com/user-attachments/assets/6c902d23-138b-4131-86f4-2a9e0be49977" />
  Figure 1.2 Concurrent (Threading) & Parallel (Multiprocessing) Performance
</p>

Comparing processing speeds, the combination of threading and multiprocessing yields a 2.45x improvement over sequential execution. Ultimately, sequential processing is more efficient for smaller workloads, whereas concurrent and parallel execution are better suited for large-scale file processing where the speed gains outweigh the overhead.
<p align="center">
  <img width="512" height="243" alt="image" src="https://github.com/user-attachments/assets/fc120888-6371-4829-93cb-e57830e772cc" />
  Figure 1.3 Sequential VS Concurrent (Threading) & Parallel (Multiprocessing)
</p>

# ✅ 6. Conclusion

The experiment shows that selecting the correct execution technique depends on the size of the dataset. Sequential execution will prove more useful in case of small-sized data sets because it will not involve unnecessary overhead. However, concurrent execution, or threading is great in speeding up unrelated tasks, such as preprocessing. Meanwhile, large and complex data sets will benefit from parallel execution, or multiprocessing since it makes use of multi-core processors. For step-by-step guide, you can click the Youtube link below:<br>

📺 https://youtu.be/r7wvEzY4oj8?si=SbnTNLaQpn8p1t8Y

# 🧾 7. Program Code
```bash
# Program Header
"""
Smart Document Similarity Checker
===================================================
Sequential technique  : plain for-loops (used automatically for small workloads)
Concurrent technique  : threading (used automatically for larger workloads, I/O-bound)
Parallel technique    : multiprocessing (used automatically for larger workloads, CPU-bound)
"""
 
# Importing Libraries and Tools
import os
import re
import math
import time
import threading
import multiprocessing
from collections import Counter
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple
 
 
# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------
 
@dataclass
class Document:
    name: str
    raw_text: str
    tokens: List[str] = field(default_factory=list)
    tf: Dict[str, float] = field(default_factory=dict)
    bigrams: Set[Tuple[str, str]] = field(default_factory=set)
 
 
@dataclass
class SimilarityResult:
    doc_a: str
    doc_b: str
    score: float          # hybrid similarity  [0, 1]
    cosine: float = 0.0   # TF-IDF cosine component
    jaccard: float = 0.0  # bigram Jaccard component
    method: str = "Hybrid (TF-IDF cosine + bigram Jaccard)"
    elapsed_ms: float = 0.0
 
 
# ---------------------------------------------------------------------------
# Thresholds — tune these to match your hardware / typical workload
# ---------------------------------------------------------------------------
 
# Below this many files  → sequential preprocessing is faster (avoids thread overhead)
SEQ_PREPROCESS_THRESHOLD = 6
 
# Below this many pairs  → sequential similarity is faster (avoids process spawn overhead)
# pairs = n*(n-1)/2, so 5 files = 10 pairs, 6 files = 15 pairs
SEQ_SIMILARITY_THRESHOLD = 15
 
 
_preprocess_lock = threading.Lock()
_progress: Dict[str, int] = {"done": 0}
 
 
# ---------------------------------------------------------------------------
# Shared preprocessing logic (used by all three modes)
# ---------------------------------------------------------------------------
 
def _preprocess_one(doc_name: str, raw_text: str, simulate_io: bool = True) -> Document:
    """
    Tokenise, compute TF, and extract bigrams for one document.
    Used by sequential, concurrent, and parallel stages alike.
    The simulate_io flag adds a small sleep to mimic real I/O latency.
    """
    if simulate_io:
        time.sleep(0.05)  # Simulate I/O latency
 
    tokens = re.findall(r"[a-z']+", raw_text.lower())
    tokens = [t for t in tokens if len(t) > 1]
 
    counts = Counter(tokens)
    total = max(len(tokens), 1)
    tf = {word: count / total for word, count in counts.items()}
 
    bigrams: Set[Tuple[str, str]] = set(zip(tokens, tokens[1:]))
 
    return Document(
        name=doc_name,
        raw_text=raw_text,
        tokens=tokens,
        tf=tf,
        bigrams=bigrams,
    )
 
 
# ---------------------------------------------------------------------------
# Stage 0 – SEQUENTIAL preprocessing (baseline)
# ---------------------------------------------------------------------------
 
def load_documents_sequentially(
    documents: Dict[str, str],
) -> Tuple[List[Document], float]:
    """
    Preprocess all documents one-by-one in a simple for-loop.
    Returns (list of Documents, elapsed_ms).
    This is the baseline: no threading, no multiprocessing.
    """
    print(f"\n[Sequential] Preprocessing {len(documents)} documents one by one …")
 
    results: List[Document] = []
    start = time.perf_counter()
 
    for name, text in documents.items():
        doc = _preprocess_one(name, text, simulate_io=True)
        results.append(doc)
        print(f"  ✓ Finished: '{doc.name}'  ({len(doc.tokens)} tokens, "
              f"{len(doc.bigrams)} unique bigrams)")
 
    elapsed = (time.perf_counter() - start) * 1000
    print(f"[Sequential] All documents preprocessed in {elapsed:.1f} ms\n")
    return results, elapsed
 
 
# ---------------------------------------------------------------------------
# Stage 1 – CONCURRENT preprocessing (threads)
# ---------------------------------------------------------------------------
 
def _load_and_preprocess(doc_name: str, raw_text: str) -> Document:
    """Tokenise, compute TF, and extract bigrams for one document (runs in a thread)."""
    doc = _preprocess_one(doc_name, raw_text, simulate_io=True)
    with _preprocess_lock:
        _progress["done"] += 1
    return doc
 
 
def load_documents_concurrently(
    documents: Dict[str, str],
    max_workers: int = None,
) -> Tuple[List[Document], float]:
    """
    Use a ThreadPoolExecutor to preprocess all documents concurrently.
    Returns (list of Documents, elapsed_ms).
    """
    max_workers = max_workers or min(len(documents), os.cpu_count() or 4)
    results: List[Document] = []
 
    print(f"[Threading] Preprocessing {len(documents)} documents "
          f"using {max_workers} threads …")
 
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="DocLoader") as pool:
        futures = {
            pool.submit(_load_and_preprocess, name, text): name
            for name, text in documents.items()
        }
        for future in as_completed(futures):
            doc = future.result()
            results.append(doc)
            print(f"  ✓ Thread finished: '{doc.name}'  ({len(doc.tokens)} tokens, "
                  f"{len(doc.bigrams)} unique bigrams)")
 
    elapsed = (time.perf_counter() - start) * 1000
    print(f"[Threading] All documents preprocessed in {elapsed:.1f} ms\n")
    return results, elapsed
 
 
# ---------------------------------------------------------------------------
# Stage 2 – IDF
# ---------------------------------------------------------------------------
 
def build_idf(documents: List[Document]) -> Dict[str, float]:
    N = len(documents)
    df: Counter = Counter()
    for doc in documents:
        df.update(set(doc.tokens))
    return {
        word: math.log((1 + N) / (1 + count)) + 1
        for word, count in df.items()
    }
 
 
def apply_tfidf(doc: Document, idf: Dict[str, float]) -> Dict[str, float]:
    return {word: tf_val * idf.get(word, 0) for word, tf_val in doc.tf.items()}
 
 
# ---------------------------------------------------------------------------
# Shared similarity computation logic
# ---------------------------------------------------------------------------
 
def _compute_hybrid(
    name_a: str,
    name_b: str,
    vec_a: Dict[str, float],
    vec_b: Dict[str, float],
    bg_a: Set[Tuple[str, str]],
    bg_b: Set[Tuple[str, str]],
) -> SimilarityResult:
    """
    Core hybrid similarity computation.
    Hybrid score = 0.65 * TF-IDF cosine  +  0.35 * bigram Jaccard
 
    The Jaccard component catches cases where a handful of words differ
    between two otherwise identical documents and cosine alone would still
    score very high (or very low for short docs).
    """
    t0 = time.perf_counter()
 
    # --- TF-IDF cosine similarity ---
    shared_keys = set(vec_a) & set(vec_b)
    dot = sum(vec_a[k] * vec_b[k] for k in shared_keys)
    mag_a = math.sqrt(sum(v * v for v in vec_a.values()))
    mag_b = math.sqrt(sum(v * v for v in vec_b.values()))
 
    if mag_a == 0 or mag_b == 0:
        cosine = 0.0
    else:
        cosine = dot / (mag_a * mag_b)
 
    # --- Bigram Jaccard similarity ---
    inter = len(bg_a & bg_b)
    union = len(bg_a | bg_b)
    jaccard = inter / union if union > 0 else 0.0
 
    # --- Hybrid ---
    hybrid = 0.65 * cosine + 0.35 * jaccard
 
    elapsed = (time.perf_counter() - t0) * 1000
    return SimilarityResult(
        doc_a=name_a,
        doc_b=name_b,
        score=round(hybrid, 6),
        cosine=round(cosine, 6),
        jaccard=round(jaccard, 6),
        elapsed_ms=round(elapsed, 3),
    )
 
 
# ---------------------------------------------------------------------------
# Stage 3a – SEQUENTIAL similarity (baseline)
# ---------------------------------------------------------------------------
 
def compute_similarities_sequentially(
    documents: List[Document],
    idf: Dict[str, float],
) -> Tuple[List[SimilarityResult], float]:
    """
    Compute hybrid similarity for every document pair one by one.
    Returns (sorted results, elapsed_ms).
    This is the baseline: no threading, no multiprocessing.
    """
    tfidf_vectors = {doc.name: apply_tfidf(doc, idf) for doc in documents}
    bigram_sets   = {doc.name: doc.bigrams for doc in documents}
 
    pairs = list(combinations(tfidf_vectors.keys(), 2))
    print(f"[Sequential] Computing {len(pairs)} pair(s) one by one …")
 
    results: List[SimilarityResult] = []
    start = time.perf_counter()
 
    for a, b in pairs:
        res = _compute_hybrid(
            a, b,
            tfidf_vectors[a], tfidf_vectors[b],
            bigram_sets[a], bigram_sets[b],
        )
        results.append(res)
        print(f"  ✓ '{res.doc_a}' ↔ '{res.doc_b}'  "
              f"hybrid={res.score:.4f}  "
              f"(cosine={res.cosine:.4f}, jaccard={res.jaccard:.4f})  "
              f"[{res.elapsed_ms} ms]")
 
    elapsed = (time.perf_counter() - start) * 1000
    print(f"[Sequential] All pairs done in {elapsed:.1f} ms\n")
 
    results.sort(key=lambda r: r.score, reverse=True)
    return results, elapsed
 
 
# ---------------------------------------------------------------------------
# Stage 3b – PARALLEL similarity (processes)
# ---------------------------------------------------------------------------
 
def _hybrid_similarity_worker(
    pair: Tuple[str, str,
                Dict[str, float], Dict[str, float],
                Set[Tuple[str, str]], Set[Tuple[str, str]]]
) -> SimilarityResult:
    """Worker function executed in a *separate process*."""
    name_a, name_b, vec_a, vec_b, bg_a, bg_b = pair
    return _compute_hybrid(name_a, name_b, vec_a, vec_b, bg_a, bg_b)
 
 
def compute_similarities_parallel(
    documents: List[Document],
    idf: Dict[str, float],
    max_workers: int = None,
) -> Tuple[List[SimilarityResult], float]:
    """
    Distribute hybrid similarity computation across multiple *processes*.
    Returns (sorted results, elapsed_ms).
    """
    max_workers = max_workers or os.cpu_count() or 2
 
    tfidf_vectors = {doc.name: apply_tfidf(doc, idf) for doc in documents}
    bigram_sets   = {doc.name: doc.bigrams for doc in documents}
 
    pairs = [
        (a, b, tfidf_vectors[a], tfidf_vectors[b], bigram_sets[a], bigram_sets[b])
        for a, b in combinations(tfidf_vectors.keys(), 2)
    ]
 
    print(f"[Multiprocessing] Computing {len(pairs)} pair(s) "
          f"across {max_workers} processes …")
 
    results: List[SimilarityResult] = []
    start = time.perf_counter()
 
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_hybrid_similarity_worker, p): p for p in pairs}
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            print(f"  ✓ '{res.doc_a}' ↔ '{res.doc_b}'  "
                  f"hybrid={res.score:.4f}  "
                  f"(cosine={res.cosine:.4f}, jaccard={res.jaccard:.4f})  "
                  f"[{res.elapsed_ms} ms]")
 
    elapsed = (time.perf_counter() - start) * 1000
    print(f"[Multiprocessing] All pairs done in {elapsed:.1f} ms\n")
 
    results.sort(key=lambda r: r.score, reverse=True)
    return results, elapsed
 
 
# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------
 
def print_similarity_report(results: List[SimilarityResult]) -> None:
    bar_width = 28
    print("=" * 75)
    print("  DOCUMENT SIMILARITY REPORT  (Hybrid: 65% TF-IDF cosine + 35% Bigram Jaccard)")
    print("=" * 75)
    print(f"  {'Pair':<40}  {'Bar':<30}  {'Score':>6}")
    print("-" * 75)
    for r in results:
        pair_label = f"{r.doc_a}  ↔  {r.doc_b}"
        bar = "█" * int(r.score * bar_width) + "░" * (bar_width - int(r.score * bar_width))
        pct = f"{r.score * 100:5.1f}%"
        print(f"  {pair_label:<40}  {bar}  {pct}")
    print("=" * 75)
    print()
 
 
def print_timing_report(
    seq_preprocess_ms: float,
    con_preprocess_ms: float,
    seq_similarity_ms: float,
    par_similarity_ms: float,
) -> None:
    """
    Print a side-by-side timing comparison across all three execution modes.
    Speedup is always relative to the sequential baseline.
    """
    total_seq = seq_preprocess_ms + seq_similarity_ms
    total_con_par = con_preprocess_ms + par_similarity_ms
 
    def speedup(baseline: float, other: float) -> str:
        if other == 0:
            return "N/A"
        return f"{baseline / other:.2f}x"
 
    print("=" * 65)
    print("  TIMING COMPARISON")
    print("=" * 65)
    print(f"  {'Stage':<35}  {'Sequential':>10}  {'Optimised':>10}")
    print("-" * 65)
    print(f"  {'Preprocessing':<35}  "
          f"{seq_preprocess_ms:>9.1f}ms  "
          f"{con_preprocess_ms:>9.1f}ms")
    print(f"  {'  └─ mode':<35}  "
          f"{'for-loop':>10}  "
          f"{'threading':>10}")
    print(f"  {'  └─ speedup':<35}  "
          f"{'(baseline)':>10}  "
          f"{speedup(seq_preprocess_ms, con_preprocess_ms):>10}")
    print()
    print(f"  {'Similarity computation':<35}  "
          f"{seq_similarity_ms:>9.1f}ms  "
          f"{par_similarity_ms:>9.1f}ms")
    print(f"  {'  └─ mode':<35}  "
          f"{'for-loop':>10}  "
          f"{'processes':>10}")
    print(f"  {'  └─ speedup':<35}  "
          f"{'(baseline)':>10}  "
          f"{speedup(seq_similarity_ms, par_similarity_ms):>10}")
    print()
    print(f"  {'TOTAL':<35}  "
          f"{total_seq:>9.1f}ms  "
          f"{total_con_par:>9.1f}ms")
    print(f"  {'  └─ overall speedup':<35}  "
          f"{'(baseline)':>10}  "
          f"{speedup(total_seq, total_con_par):>10}")
    print("=" * 65)
    print()
    print("  NOTE: Speedup gains scale with document count and size.")
    print("        For very small workloads, thread/process overhead may")
    print("        make sequential mode faster. Try with more/larger files!")
    print()
 
 
# ---------------------------------------------------------------------------
# Folder input
# ---------------------------------------------------------------------------
 
SUPPORTED_EXTENSIONS = {".txt", ".md"}
 
 
def _safe_input(prompt: str) -> str:
    """Read a line from stdin; raise SystemExit if the user types 'exit'."""
    try:
        val = input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        raise SystemExit(0)
    if val.lower() == "exit":
        print("Exiting. Goodbye!")
        raise SystemExit(0)
    return val
 
 
def collect_documents_from_folder() -> Dict[str, str]:
    """
    Ask the user for a single FOLDER path, then scan all supported files inside.
    Returns a dict of {label: text}.
    """
    print("\n" + "━" * 70)
    print("  PARALLEL DOCUMENT SIMILARITY CHECKER")
    print("  Auto-selects: Sequential (small) | Threading + Multiprocessing (large)")
    print("━" * 70)
    print("\nEnter the path to a FOLDER containing the documents to compare.")
    print(f"Supported formats: {', '.join(sorted(SUPPORTED_EXTENSIONS))}  (UTF-8 encoded)")
    print("Type 'exit' at any prompt to quit.\n")
 
    while True:
        raw = _safe_input("  Folder path: ")
        if not raw:
            continue
 
        folder = os.path.expanduser(os.path.expandvars(raw))
 
        if not os.path.isdir(folder):
            print(f"  ✗ Not a folder or does not exist: {folder}\n")
            continue
 
        # Collect all supported files (non-recursive; add os.walk for subdirs)
        file_paths = sorted(
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
            and os.path.isfile(os.path.join(folder, f))
        )
 
        if len(file_paths) < 2:
            print(f"  ✗ Found {len(file_paths)} supported file(s) in that folder. "
                  f"Need at least 2.\n")
            continue
 
        print(f"\n  Found {len(file_paths)} file(s):")
        documents: Dict[str, str] = {}
 
        for path in file_paths:
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    text = fh.read()
            except UnicodeDecodeError:
                print(f"  ⚠ Skipped (not UTF-8): {path}")
                continue
            except OSError as exc:
                print(f"  ⚠ Skipped (read error): {exc}")
                continue
 
            if not text.strip():
                print(f"  ⚠ Skipped (empty file): {path}")
                continue
 
            label = os.path.splitext(os.path.basename(path))[0]
            if label in documents:
                label = f"{label}_{len(documents) + 1}"
 
            word_count = len(text.split())
            documents[label] = text
 
            warn = ""
            if word_count < 10:
                warn = "  ⚠ very short – may affect accuracy"
            print(f"    ✓ '{label}'  ({word_count:,} words){warn}")
 
        if len(documents) < 2:
            print(f"\n  ✗ Only {len(documents)} readable file(s). Need at least 2.\n")
            continue
 
        print()
        return documents
 
 
# ---------------------------------------------------------------------------
# Pipeline — automatically selects the best execution mode
# ---------------------------------------------------------------------------
 
def print_mode_report(
    preprocess_mode: str, preprocess_ms: float,
    similarity_mode: str, similarity_ms: float,
    n_docs: int, n_pairs: int,
) -> None:
    """Print a summary of which mode was chosen and how long each stage took."""
    total_ms = preprocess_ms + similarity_ms
    print("=" * 65)
    print("  EXECUTION SUMMARY")
    print("=" * 65)
    print(f"  {'Documents processed':<35}  {n_docs:>10}")
    print(f"  {'Pairs compared':<35}  {n_pairs:>10}")
    print()
    print(f"  {'Stage':<35}  {'Mode':>15}  {'Time':>8}")
    print("-" * 65)
    print(f"  {'Preprocessing':<35}  {preprocess_mode:>15}  {preprocess_ms:>7.1f}ms")
    print(f"  {'Similarity computation':<35}  {similarity_mode:>15}  {similarity_ms:>7.1f}ms")
    print("-" * 65)
    print(f"  {'TOTAL':<35}  {'':>15}  {total_ms:>7.1f}ms")
    print("=" * 65)
    print()

 
 
def run_pipeline(documents: Dict[str, str]) -> List[SimilarityResult]:
    n_docs  = len(documents)
    n_pairs = n_docs * (n_docs - 1) // 2
 
    use_sequential_preprocess = n_docs  < SEQ_PREPROCESS_THRESHOLD
    use_sequential_similarity = n_pairs < SEQ_SIMILARITY_THRESHOLD
 
    print("─" * 70)
    print("  AUTO-MODE SELECTION")
    print("─" * 70)
    print(f"  Documents : {n_docs}  (threshold: < {SEQ_PREPROCESS_THRESHOLD} → sequential)")
    print(f"  Pairs     : {n_pairs}  (threshold: < {SEQ_SIMILARITY_THRESHOLD} → sequential)")
    print(f"  Preprocessing  → {'Sequential (for-loop)' if use_sequential_preprocess else 'Concurrent (threading)'}")
    print(f"  Similarity     → {'Sequential (for-loop)' if use_sequential_similarity  else 'Parallel (multiprocessing)'}")
    print()
 
    # ── Stage 1: Preprocessing ──────────────────────────────────────────────
    print("─" * 70)
    if use_sequential_preprocess:
        print("  STAGE 1 — Sequential Preprocessing  (small workload)")
        print("─" * 70)
        docs, preprocess_ms = load_documents_sequentially(documents)
        preprocess_mode = "Sequential"
    else:
        print("  STAGE 1 — Concurrent Preprocessing  (large workload)")
        print("─" * 70)
        docs, preprocess_ms = load_documents_concurrently(documents)
        preprocess_mode = "Concurrent"
 
    # ── Stage 2: IDF (always a single fast pass — no need to parallelise) ───
    idf = build_idf(docs)
 
    # ── Stage 3: Similarity ─────────────────────────────────────────────────
    print("─" * 70)
    if use_sequential_similarity:
        print("  STAGE 3 — Sequential Similarity  (small workload)")
        print("─" * 70)
        results, similarity_ms = compute_similarities_sequentially(docs, idf)
        similarity_mode = "Sequential"
    else:
        print("  STAGE 3 — Parallel Similarity  (large workload)")
        print("─" * 70)
        results, similarity_ms = compute_similarities_parallel(docs, idf)
        similarity_mode = "Parallel"
 
    # ── Results ──────────────────────────────────────────────────────────────
    print_similarity_report(results)
    print_mode_report(
        preprocess_mode, preprocess_ms,
        similarity_mode, similarity_ms,
        n_docs, n_pairs,
    )
 
    return results
 
 
# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
 
if __name__ == "__main__":
    multiprocessing.freeze_support()
    documents = collect_documents_from_folder()
    run_pipeline(documents)

```



