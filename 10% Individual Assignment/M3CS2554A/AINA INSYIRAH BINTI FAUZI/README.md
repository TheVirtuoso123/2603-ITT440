# Online Order Processing System

# Introduction
This project focuses on demostrating the concept of parallel programming using an online order processing system. In real-world applications, systems often need to handle multiple tasks simultaneously to improve efficiency. Therefore, this project compares sequential and parallel processing methods to analyze their performance in handling multiple orders.

# Problem Statement
Modern systems often need to handle a large number of tasks efficiently. When tasks are process sequentially, the system becomes slower and less efficient, especially under heavy workload. This creates delays and reduces overall performance. Therefore, there is a need to implement parallel processing techniques such as threading and multiprocessing to improve efficiency and reduce execution time.

# Objective
- To implement sequential processing in handling orders.
- To implement parallel processing using threading.
- To implement parallel processing using multiprocessing.
- To compare execution time between all approaches.
- To track total processes (payment, packaging, delivery)

# Methodology
The system simulates a number of customer orders. Each order goes through three main process:
- Payment 💳
- Packaging 📦
- Delivery 🚚

Different types of payment(QR, online banking, card) and delivery(COD, standard, express) are randomly assigned to each order using object-oriented programming concepts.
Each process includes a small delay using time.sleep() to simulate real-word operations such as network requests and system processing time. This makes the task I/O-bound.

Three approaches are used :
- **Sequential Processing** : Each order is processed one by one. Each order must complete before the next begins,resulting in longer execution time.
- **Parallel Processing (Threading)** : Multiple threads are used to process orders concurrently. This allows the system to handle waiting time more efficiently.
- **Parallel Processing (Multiprocessing)** : Multiple processes are used to execute tasks in parallel across CPU cores, improving performance for larger workloads.

# 💻 Code
```python 
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import random


# =========================
# PAYMENT CLASSES
# =========================
class Payment:
    def process(self):
        pass

class QRPayment(Payment):
    def process(self):
        time.sleep(0.0001)
        return 1

class OnlineBanking(Payment):
    def process(self):
        time.sleep(0.00015)
        return 1

class CardPayment(Payment):
    def process(self):
        time.sleep(0.00012)
        return 1


# =========================
# DELIVERY CLASSES
# =========================
class Delivery:
    def process(self):
        pass

class CODDelivery(Delivery):
    def process(self):
        time.sleep(0.0002)
        return 1

class StandardDelivery(Delivery):
    def process(self):
        time.sleep(0.0001)
        return 1

class ExpressDelivery(Delivery):
    def process(self):
        time.sleep(0.00008)
        return 1


# =========================
# ORDER CLASS
# =========================
class Order:
    def __init__(self, order_id):
        self.payment_type = random.choice([
            QRPayment(), OnlineBanking(), CardPayment()
        ])
        self.delivery_type = random.choice([
            CODDelivery(), StandardDelivery(), ExpressDelivery()
        ])

    def process_payment(self):
        return self.payment_type.process()

    def process_packaging(self):
        time.sleep(0.0001)
        return 1

    def process_delivery(self):
        return self.delivery_type.process()


# =========================
# PROCESS FUNCTION
# =========================
def process_order(order):
    p = order.process_payment()
    pack = order.process_packaging()
    d = order.process_delivery()

    for _ in range(100):
        x = _ * _

    return (p, pack, d)


# =========================
# SEQUENTIAL
# =========================
def sequential_orders(orders):
    start = time.time()

    payment = packaging = delivery = 0

    for order in orders:
        p, pack, d = process_order(order)
        payment += p
        packaging += pack
        delivery += d

    end = time.time()

    print("\n--- SEQUENTIAL ---")
    print("Time:", round(end - start, 4), "seconds")
    print("Payment:", payment)
    print("Packaging:", packaging)
    print("Delivery:", delivery)


# =========================
# THREADING
# =========================
def threading_orders(orders):
    start = time.time()

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_order, orders))

    payment = sum(r[0] for r in results)
    packaging = sum(r[1] for r in results)
    delivery = sum(r[2] for r in results)

    end = time.time()

    print("\n--- THREADING ---")
    print("Time:", round(end - start, 4), "seconds")
    print("Payment:", payment)
    print("Packaging:", packaging)
    print("Delivery:", delivery)


# =========================
# MULTIPROCESSING
# =========================
def multiprocessing_orders(orders):
    start = time.time()

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(process_order, orders, chunksize=200)

    payment = sum(r[0] for r in results)
    packaging = sum(r[1] for r in results)
    delivery = sum(r[2] for r in results)

    end = time.time()

    print("\n--- MULTIPROCESSING ---")
    print("Time:", round(end - start, 4), "seconds")
    print("Payment:", payment)
    print("Packaging:", packaging)
    print("Delivery:", delivery)


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    orders = [Order(i) for i in range(1, 1000001)]

    print("Processing", len(orders), "orders")

    sequential_orders(orders)
    threading_orders(orders)
    multiprocessing_orders(orders)
```
# 💻 Code Explanation
- **Payment & delivery classes** : Define different types of payment (QR, Online Banking, Card) and delivery (COD, Standard, Express) each with its own processing time.
- **Order(order_id)** : Represent a single order and randomly assign a payment method and delivery type.
- **process_order(order)** : Executes payment, packaging and delivery process for each order and return the result.
- **sequential_orders(orders)** : Process all orders one by one without parallel execution.
- **threading_orders(orders)** : Use ThreadPoolExecutor to process multiple orders concurrently using threads.
- **multiprocessing_orders(orders)** : Use multiprocessing to execute orders in parallel for better performance.
- **time.sleep()** : Simulates real-world delay such as system processing or network operations.
- **time.time()** : Use to measure execution time for comparison.

# Results & Output
| Method | Execution Time | Payment | Packaging | Delivery |
|----------|----------|----------|----------|----------|
| Sequential   |  771.4968 seconds  | 1 000 000 | 1 000 000 | 1 000 000 |
| Threading (Concurrent) | 312.69 seconds  | 1 000 000 | 1 000 000 | 1 000 000 |
| Multiprocessing (Parallel) |  177.9161 seconds | 1 000 000 | 1 000 000 | 1 000 000 |

- **Sequential Processing** :
<img width="330" height="152" alt="image" src="https://github.com/user-attachments/assets/9149053c-967d-46dc-bec7-4c8a2cdef667" />

- **Threading** :
<img width="272" height="120" alt="image" src="https://github.com/user-attachments/assets/0780481d-6b98-49ba-9fe0-577086713fdb" />

- **Multiprocessing** :
<img width="316" height="112" alt="image" src="https://github.com/user-attachments/assets/ba833b6e-2f7b-48e1-91a3-56c414199f58" />

# Conclusion
Sequential processing performed the slowest because each task is executed one by one and includes waiting time from simulated operations. This causes the total execution time to increase significantly. Threading performed better by handling multiple tasks concurrently, reducing waiting time. Multiprocessing also improved performance by executing tasks in parallel across multiple process. This shows that parallel processing is more efficient for I/O-bound tasks, and the choice of method depends on the nature of the workload.

# 🎥 Demonstration Video
https://youtu.be/u3jTQMmNQjE?feature=shared
