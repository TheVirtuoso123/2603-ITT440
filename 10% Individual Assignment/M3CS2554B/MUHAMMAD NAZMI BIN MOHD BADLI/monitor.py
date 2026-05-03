#!/usr/bin/env python3
"""
NETWORK TRAFFIC MONITOR - FIXED PROGRESS BARS + TXT OUTPUT
Features:
- Fixed progress bars (updates properly)
- Saves results to TXT file
- Clean output format
"""

import json
import time
import os
from collections import defaultdict, Counter
from datetime import datetime
from multiprocessing import Pool, cpu_count
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============= CONFIGURATION =============
PORT_SCAN_THRESHOLD = 10
DDoS_THRESHOLD = 20
CHUNK_SIZE = 5000

SUSPICIOUS_KEYWORDS = [
    "' OR '1'='1", "' OR 1=1", "DROP TABLE", "UNION SELECT",
    "<script>", "alert(", "document.cookie", "onerror=",
]

# ============= PROGRESS BAR FUNCTION =============

def print_progress_bar(current, total, bar_length=35, prefix=""):
    """Display a progress bar that updates properly"""
    if total == 0:
        return
    
    fraction = current / total
    arrow = '=' * int(round(fraction * bar_length))
    spaces = ' ' * (bar_length - len(arrow))
    percent = int(round(fraction * 100))
    
    # Format numbers with commas
    current_str = f"{current:,}"
    total_str = f"{total:,}"
    
    print(f"\r{prefix}[{arrow}{spaces}] {percent}% ({current_str}/{total_str})", end='', flush=True)

# ============= SYSTEM DETECTION =============

def count_packets_in_file(filepath):
    """Count packets with progress"""
    count = 0
    try:
        with open(filepath, 'r') as f:
            f.read(1)
            for line in f:
                if line.strip() == ']':
                    break
                count += 1
                if count % 100000 == 0:
                    print(f"\r   Counting: {count:,} packets...", end='', flush=True)
    except:
        pass
    print()
    return count

# ============= STREAMING JSON READER =============

def stream_json_packets(filepath, chunk_size=CHUNK_SIZE):
    """Stream JSON file in chunks"""
    try:
        with open(filepath, 'r', buffering=16*1024*1024) as f:
            f.read(1)
            chunk = []
            
            for line in f:
                line = line.strip()
                if line == ']':
                    break
                if line.endswith(','):
                    line = line[:-1]
                
                try:
                    packet = json.loads(line)
                    if isinstance(packet.get("payload"), str):
                        packet["payload"] = packet["payload"].encode()
                    chunk.append(packet)
                    
                    if len(chunk) >= chunk_size:
                        yield chunk
                        chunk = []
                except json.JSONDecodeError:
                    continue
            
            if chunk:
                yield chunk
    except Exception as e:
        print(f"   Error: {e}")

# ============= CHUNK PROCESSOR =============

def process_chunk(chunk_packets):
    """Process a chunk of packets"""
    chunk_alerts = []
    ip_ports = defaultdict(set)
    dst_counter = Counter()
    
    for packet in chunk_packets:
        src_ip = packet["src_ip"]
        dst_ip = packet["dst_ip"]
        port = packet.get("port", 0)
        
        ip_ports[src_ip].add(port)
        dst_counter[dst_ip] += 1
        
        payload = packet.get("payload", b"")
        if isinstance(payload, str):
            payload = payload.encode()
        
        is_malicious = False
        for keyword in SUSPICIOUS_KEYWORDS:
            if keyword.lower().encode() in payload.lower():
                is_malicious = True
                break
        
        if is_malicious:
            chunk_alerts.append({
                "type": "MALICIOUS_PAYLOAD",
                "src_ip": src_ip,
                "dst_ip": dst_ip,
            })
    
    return {
        "alerts": chunk_alerts,
        "ip_ports": {ip: list(ports) for ip, ports in ip_ports.items()},
        "dst_counter": dict(dst_counter),
        "packet_count": len(chunk_packets)
    }

# ============= SEQUENTIAL =============

def sequential_analysis(filepath):
    """Sequential with proper progress bar"""
    print(f"\n[SEQUENTIAL] Processing...")
    start_time = time.time()
    
    all_alerts = []
    ip_ports = defaultdict(set)
    dst_counter = Counter()
    total_packets = 0
    
    # Get total for progress bar
    total = count_packets_in_file(filepath)
    
    for chunk in stream_json_packets(filepath, chunk_size=1000):
        for packet in chunk:
            src_ip = packet["src_ip"]
            dst_ip = packet["dst_ip"]
            port = packet.get("port", 0)
            
            ip_ports[src_ip].add(port)
            dst_counter[dst_ip] += 1
            
            payload = packet.get("payload", b"")
            if isinstance(payload, str):
                payload = payload.encode()
            
            is_malicious = False
            for keyword in SUSPICIOUS_KEYWORDS:
                if keyword.lower().encode() in payload.lower():
                    is_malicious = True
                    break
            
            if is_malicious:
                all_alerts.append({"type": "MALICIOUS_PAYLOAD", "src_ip": src_ip, "dst_ip": dst_ip})
            
            total_packets += 1
            
            # Update progress every 5000 packets
            if total_packets % 5000 == 0:
                print_progress_bar(total_packets, total, prefix="   ")
    
    print_progress_bar(total, total, prefix="   ")
    print()
    
    # Detect attacks
    for ip, ports in ip_ports.items():
        if len(ports) >= PORT_SCAN_THRESHOLD:
            all_alerts.append({"type": "PORT_SCAN", "src_ip": ip, "details": f"Hit {len(ports)} ports"})
    
    for dst_ip, count in dst_counter.items():
        if count >= DDoS_THRESHOLD:
            all_alerts.append({"type": "DDoS", "dst_ip": dst_ip, "details": f"{count} packets"})
    
    elapsed = time.time() - start_time
    return all_alerts, elapsed, total_packets

# ============= CONCURRENT =============

def concurrent_analysis(filepath, num_workers):
    """Concurrent with proper progress bar"""
    print(f"\n[CONCURRENT] Using {num_workers} threads...")
    start_time = time.time()
    
    # Get total packets first
    total_packets = count_packets_in_file(filepath)
    
    # Collect chunks
    chunks = list(stream_json_packets(filepath))
    total_chunks = len(chunks)
    
    all_alerts = []
    combined_ip_ports = defaultdict(set)
    combined_dst_counter = Counter()
    processed = 0
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(process_chunk, chunk): i for i, chunk in enumerate(chunks)}
        
        for future in as_completed(futures):
            result = future.result()
            all_alerts.extend(result["alerts"])
            for ip, ports in result["ip_ports"].items():
                combined_ip_ports[ip].update(ports)
            combined_dst_counter.update(result["dst_counter"])
            processed += 1
            print_progress_bar(processed, total_chunks, prefix="   ")
    
    print()
    
    # Detect attacks
    for ip, ports in combined_ip_ports.items():
        if len(ports) >= PORT_SCAN_THRESHOLD:
            all_alerts.append({"type": "PORT_SCAN", "src_ip": ip, "details": f"Hit {len(ports)} ports"})
    
    for dst_ip, count in combined_dst_counter.items():
        if count >= DDoS_THRESHOLD:
            all_alerts.append({"type": "DDoS", "dst_ip": dst_ip, "details": f"{count} packets"})
    
    elapsed = time.time() - start_time
    return all_alerts, elapsed, total_packets

# ============= PARALLEL =============

def parallel_analysis(filepath, num_workers):
    """Parallel with proper progress bar"""
    print(f"\n[PARALLEL] Using {num_workers} processes...")
    start_time = time.time()
    
    # Get total packets first
    total_packets = count_packets_in_file(filepath)
    
    # Collect chunks
    chunks = list(stream_json_packets(filepath))
    total_chunks = len(chunks)
    
    all_alerts = []
    combined_ip_ports = defaultdict(set)
    combined_dst_counter = Counter()
    processed = 0
    
    with Pool(processes=num_workers) as pool:
        # Use imap_unordered for progress tracking
        for result in pool.imap_unordered(process_chunk, chunks):
            all_alerts.extend(result["alerts"])
            for ip, ports in result["ip_ports"].items():
                combined_ip_ports[ip].update(ports)
            combined_dst_counter.update(result["dst_counter"])
            processed += 1
            print_progress_bar(processed, total_chunks, prefix="   ")
    
    print()
    
    # Detect attacks
    for ip, ports in combined_ip_ports.items():
        if len(ports) >= PORT_SCAN_THRESHOLD:
            all_alerts.append({"type": "PORT_SCAN", "src_ip": ip, "details": f"Hit {len(ports)} ports"})
    
    for dst_ip, count in combined_dst_counter.items():
        if count >= DDoS_THRESHOLD:
            all_alerts.append({"type": "DDoS", "dst_ip": dst_ip, "details": f"{count} packets"})
    
    elapsed = time.time() - start_time
    return all_alerts, elapsed, total_packets

# ============= PRINT BAR GRAPH =============

def print_bar_graph(results, max_width=45):
    """Print visual bar graph"""
    print("\n" + "=" * 70)
    print("VISUAL BAR GRAPH")
    print("=" * 70)
    
    times = {
        'Sequential': results['sequential']['time'],
        'Concurrent': results['concurrent']['time'],
        'Parallel': results['parallel']['time']
    }
    
    max_time = max(times.values())
    
    print(f"\n{'Method':<12} {'Time(s)':<10} {'Bar Graph':<50}")
    print("-" * 72)
    
    for method, time_val in times.items():
        if max_time > 0:
            bar_length = int((time_val / max_time) * max_width)
            bar = '#' * bar_length
            spaces = ' ' * (max_width - bar_length)
            print(f"{method:<12} {time_val:<10.3f} |{bar}{spaces}|")
    
    print("-" * 72)
    print(f"{'':<12} {'Faster':>10} {'Slower':>50}")
    
    baseline = results['sequential']['time']
    speedup = baseline / results['parallel']['time']
    print(f"\nParallel is {speedup:.3f}x faster than Sequential")

# ============= SAVE TO TXT FILE =============

def save_results_to_txt(results, alerts, output_file):
    """Save results to a formatted TXT file"""
    with open(output_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("NETWORK TRAFFIC MONITOR - RESULTS\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("PERFORMANCE COMPARISON\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Method':<12} {'Time (s)':<12} {'Speedup':<10}\n")
        f.write("-" * 40 + "\n")
        
        baseline = results['sequential']['time']
        f.write(f"{'Sequential':<12} {baseline:<12.3f} {'1.000x':<10}\n")
        f.write(f"{'Concurrent':<12} {results['concurrent']['time']:<12.3f} {baseline/results['concurrent']['time']:.3f}x\n")
        f.write(f"{'Parallel':<12} {results['parallel']['time']:<12.3f} {baseline/results['parallel']['time']:.3f}x\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("THREAT DETECTION SUMMARY\n")
        f.write("-" * 40 + "\n")
        
        # Count threats by type
        malicious_count = sum(1 for a in alerts if a.get("type") == "MALICIOUS_PAYLOAD")
        portscan_count = sum(1 for a in alerts if a.get("type") == "PORT_SCAN")
        ddos_count = sum(1 for a in alerts if a.get("type") == "DDoS")
        
        f.write(f"Total threats detected: {len(alerts)}\n")
        f.write(f"  - Malicious Payloads: {malicious_count}\n")
        f.write(f"  - Port Scans: {portscan_count}\n")
        f.write(f"  - DDoS Attacks: {ddos_count}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("SYSTEM INFORMATION\n")
        f.write("-" * 40 + "\n")
        f.write(f"CPU Cores: {cpu_count()}\n")
        f.write(f"Packets Processed: {results['sequential']['packets']:,}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("END OF REPORT\n")
    
    print(f"\nResults saved to: {output_file}")

# ============= MAIN =============

def main():
    print("=" * 70)
    print("NETWORK TRAFFIC MONITOR")
    print("Sequential | Concurrent | Parallel")
    print("=" * 70)
    
    cpu_cores = cpu_count()
    print(f"\nCPU Cores: {cpu_cores}")
    
    # Find packet file
    packet_file = None
    for f in ["packets.json", "packets_1m.json"]:
        if os.path.exists(f):
            packet_file = f
            break
    
    if not packet_file:
        print("\nERROR: No packet file found!")
        print("First run: python3 packet_generator.py")
        return
    
    file_size = os.path.getsize(packet_file) / (1024**2)
    print(f"\nFile: {packet_file} ({file_size:.2f} MB)")
    
    # Use full file (no limit for simplicity)
    print(f"\nProcessing ALL packets...")
    
    print("\n" + "=" * 70)
    print("RUNNING PERFORMANCE COMPARISON")
    print("=" * 70)
    
    results = {}
    final_alerts = []
    
    # Sequential
    alerts_seq, time_seq, packets_seq = sequential_analysis(packet_file)
    results['sequential'] = {'time': time_seq, 'packets': packets_seq}
    final_alerts = alerts_seq  # Use sequential alerts as reference
    print(f"\n   Sequential: {len(alerts_seq)} threats in {time_seq:.3f}s")
    
    # Concurrent
    alerts_con, time_con, packets_con = concurrent_analysis(packet_file, min(cpu_cores * 2, 8))
    results['concurrent'] = {'time': time_con, 'packets': packets_con}
    print(f"\n   Concurrent: {len(alerts_con)} threats in {time_con:.3f}s")
    
    # Parallel
    alerts_par, time_par, packets_par = parallel_analysis(packet_file, cpu_cores)
    results['parallel'] = {'time': time_par, 'packets': packets_par}
    print(f"\n   Parallel: {len(alerts_par)} threats in {time_par:.3f}s")
    
    # Performance table
    print("\n" + "=" * 70)
    print("PERFORMANCE COMPARISON TABLE")
    print("=" * 70)
    print(f"\n{'Method':<12} {'Time (s)':<12} {'Speedup':<10}")
    print("-" * 40)
    
    baseline = results['sequential']['time']
    print(f"{'Sequential':<12} {baseline:<12.3f} {'1.000x':<10}")
    print(f"{'Concurrent':<12} {results['concurrent']['time']:<12.3f} {baseline/results['concurrent']['time']:.3f}x")
    print(f"{'Parallel':<12} {results['parallel']['time']:<12.3f} {baseline/results['parallel']['time']:.3f}x")
    
    # Bar graph
    print_bar_graph(results)
    
    # Save to TXT file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    txt_output = f"results_{timestamp}.txt"
    save_results_to_txt(results, final_alerts, txt_output)
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()