# 🎬 Movie Recommendation Analyzer: A High-Performance Implementation Using Python

---

## 📌 Introduction
This system focuses on the performance differences between Sequential, Concurrent, and Parallel programming models using Python. By processing a large dataset of 3,000,000 movie ratings, the system shows how using multiple CPU cores can significantly reduce execution time, especially for tasks that require heavy computation.

---

## ❗ Problem Statement

Processing large datasets using sequential execution is time-consuming and inefficient, especially with modern multi-core processors.

Although concurrency using threading allows multiple tasks to run at the same time, it is limited by the Global Interpreter Lock (GIL) in Python because it cannot fully use multiple CPU cores for heavy calculations.

Therefore, this system aims to:
- Identify the performance limitations of sequential and concurrent methods  
- Measure the performance improvement when using multiprocessing  
- Determine the speedup achieved when distributing workload across multiple CPU cores  

---

## ⚙️ System Requirements

To ensure the system runs smoothly, the following requirements were met:

| Component           | Details |
|---------------------|--------|
| Software            | Python 3.14 |
| Libraries           | multiprocessing, threading, collections, statistics, time, matplotlib |
| Development Tool    | VS Code (Visual Studio Code) |
| Operating System    | Windows (Local Environment) |
| Hardware            | Multi-core processor (12 cores) |

---

## 🛠️ Installation Steps

### Step 1: Install Python
Ensure Python 3.14 is installed on your system.

### Step 2: Install Required Library
Run the following command in terminal:

```bash
python3.14 -m pip install matplotlib --break-system-packages
```
### Step 3: Setup Project Directory
Ensure all source files are placed in the same project folder, for example:

Documents/ITT440/Movie Recommendation Analyzer

## ▶️ How To Run

### Step 1: Open Project Folder
Launch VS Code and open the project directory:
`Documents/ITT440/Movie Recommendation Analyzer`

---

### Step 2: Open Terminal
Open the terminal in VS Code.  
Make sure the terminal path is the same as your project folder.

---

### Step 3: Run the Program
Enter the following command:

```bash
python3.14 source_code.py
```

### Step 4: Monitor Process Generation
Observe the terminal as the system generates **3,000,000 records** and saves them into `input.txt`.

---

### Step 5: Verify Concurrent Responsiveness
Look for the **"Ping" messages** from the concurrent UI thread.  
These messages show that the system remains responsive even while processing heavy data.

---

### Step 6: View Final Performance Results
Once the analysis is complete:
- The terminal will display the **Final Performance Benchmark results**
- The file `output.txt` will be generated
- A pop-up window will appear showing the **Benchmark Results chart**

## 📊 Sample Input / Output

### 🖥️ Terminal Output
The system displays the time taken for each mode:

<img width="1452" height="762" alt="terminal" src="https://github.com/user-attachments/assets/a02a8b6e-e82a-4056-a3dc-ea9374e275aa" />
<p align="center"><i>Figure 1.1 Terminal Output</i></p>

- Sequential: ~75.7356s  
- Concurrent: ~23.9716s  
- Parallel: ~23.1516s
- Speedup Ratio between Parallel and Sequential: ~3.27x Faster 

---

### 📄 Input File (`input.txt`)
Contains 3,000,000 generated movie rating records including:
- Movie title  
- Rating  

<img width="617" height="480" alt="input" src="https://github.com/user-attachments/assets/a7a8e040-3ac4-40f0-89fe-06e4db4b10aa" />
<p align="center"><i>Figure 1.2 input.txt</i></p>

---

### 📄 Output File (`output.txt`)
Contains:
- Top 100 ranked movies  
- Genre classification  
- Average rating scores 

<img width="618" height="481" alt="output" src="https://github.com/user-attachments/assets/3d9c64d3-026b-4b09-aae4-540b04060b07" />
<p align="center"><i>Figure 1.3 output.txt</i></p>

 
---

### 📈 Visual Output
A bar chart titled:

**"Performance Comparison: Processing 3,000,000 Records"**

Saved as `BenchmarkResults.png

<img width="1000" height="600" alt="BenchmarkResults" src="https://github.com/user-attachments/assets/ecd2d081-80f3-468c-b842-f0a8c9df5113" />
<p align="center"><i>Figure 1.4 Benchmark Results.txt</i></p>

## 💻 Source Code

The system is implemented in Python and includes:

- Data generation for large-scale dataset  
- Sequential processing  
- Concurrent threading (UI responsiveness)  
- Parallel multiprocessing (multi-core execution)  
- Data aggregation and ranking  
- Performance visualization using matplotlib  

<img width="832" height="458" alt="sc1" src="https://github.com/user-attachments/assets/0a8b00b6-39af-4c70-85cf-11d4c755a38c" />
<img width="830" height="418" alt="sc2" src="https://github.com/user-attachments/assets/ee775430-2a72-4264-8b4d-8ce60446cf23" />
<img width="833" height="403" alt="sc3" src="https://github.com/user-attachments/assets/24f2e2d4-5f66-4a9b-8ffb-dc61db7aa7a0" />
<img width="834" height="403" alt="sc4" src="https://github.com/user-attachments/assets/24d68a14-4b1c-4515-8fdb-cafd1a019832" />
<img width="837" height="405" alt="sc5" src="https://github.com/user-attachments/assets/8c707aae-7580-4474-a00f-f491e4644279" />
<img width="834" height="405" alt="sc6" src="https://github.com/user-attachments/assets/b7d81687-d79f-4507-80a6-fdea9aec6a9f" />
<img width="834" height="393" alt="sc7" src="https://github.com/user-attachments/assets/578d4afa-5257-4583-b911-795e96af44d2" />

---

## ✅ Conclusion

The results show that parallel programming is the most efficient approach for processing large datasets.

Sequential execution required over 136 seconds, while the parallel method reduced execution time to approximately 28 seconds by using all available CPU cores.

Although threading improves system responsiveness, it does not significantly improve performance for heavy calculations due to Python’s GIL. Therefore, multiprocessing is the most suitable method to achieve better performance when handling large amounts of data.



