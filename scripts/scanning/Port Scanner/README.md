# 🔍 R.A.V.E.N Port Scanner

**Professional-grade multi-threaded port scanner with advanced network reconnaissance capabilities**

## 📖 Description

The R.A.V.E.N Port Scanner is a high-performance, feature-rich port scanning tool designed for network reconnaissance and security assessment. Built with Python 3, it offers multi-threaded scanning, service detection, and flexible target specification for comprehensive network analysis.

## 🔧 Features

- **Multi-threading**: High-speed concurrent scanning (up to 1000 threads)
- **Multiple Scan Types**: TCP Connect scan with SYN scan support
- **Service Detection**: Automatic service identification on open ports
- **Banner Grabbing**: Captures service banners for fingerprinting
- **CIDR Support**: Scan entire network ranges (e.g., 192.168.1.0/24)
- **Common Ports**: Pre-configured common port lists for quick scans
- **Custom Port Ranges**: Flexible port specification (single, range, list)
- **Timeout Control**: Configurable connection timeouts
- **Output Formats**: Console display with optional file export
- **Rate Limiting**: Prevents network flooding and detection

## 🚀 Quick Start

### Using Through R.A.V.E.N CLI Interface (Recommended)

**The easiest way to use this tool:**

1. **Launch R.A.V.E.N Interface**:
   ```bash
   # From R.A.V.E.N root directory
   bash main.sh
   ```

2. **Navigate in the interface**:
   - Select `[6] Port Scanning and Service Detection`
   - Choose `[1] port_scanner.py` from the list
   - The interface will show the help information automatically
   - When prompted "Execute with custom arguments? (y/N):", type `y`
   - Enter your arguments: `--target 192.168.1.1 --top-ports`

### Direct Terminal Usage (Advanced)

**If you prefer running commands directly in terminal:**

Navigate to Tool Directory First:
```bash
# From R.A.V.E.N root directory:
cd "scripts/scanning/Port Scanner"
```

### Basic Usage
```bash
python port_scanner.py --target 192.168.1.1
```

### Show Help
```bash
python port_scanner.py --help
```

## �️ Using with R.A.V.E.N CLI Interface

### Step-by-Step CLI Workflow:

1. **Start the R.A.V.E.N interface**:
   ```bash
   bash main.sh
   ```

2. **Select the scanning category**:
   ```
   ▶ SELECT TARGET: 6
   ```

3. **Choose the Port Scanner**:
   ```
   ▶ SELECT EXPLOIT: 1
   ```

4. **Review the help information** (displayed automatically)

5. 🚨 **CRITICAL STEP - Answer the Yes/No Question**:
   ```
   Execute with custom arguments? (y/N): y
   ```
   
   **🔴 COMMON MISTAKE:**
   ```
   Execute with custom arguments? (y/N): -t 192.168.1.1 --top-ports
   ▶ Execution cancelled  ← This happens because you entered arguments instead of y/N!
   ```
   
   **✅ CORRECT WAY:**
   ```
   Execute with custom arguments? (y/N): y
   ```
   ⚠️ **Type ONLY the letter `y` - nothing else!**

6. **NOW Enter your scan parameters** (this prompt only appears if you typed `y` above):
   ```
   ▶ Enter arguments: --target 192.168.1.1 --top-ports --service-detection
   ```
   ⚠️ **Only enter arguments here - no script name!**

### 🎯 Feature-Specific Usage Through R.A.V.E.N Interface

When you reach the **"Enter arguments:"** prompt in the R.A.V.E.N interface, here's how to use each feature:

#### 🚀 Basic Scanning Features

**1. Simple Target Scan (Default Ports)**
```
▶ Enter arguments: --target 192.168.1.1
```
❌ **WRONG**: `port_scanner.py --target 192.168.1.1` (Don't include script name!)
✅ **CORRECT**: `--target 192.168.1.1` (Arguments only!)

- Scans most common ports automatically
- Uses default 50 threads
- Good for quick checks

**2. Scan Top 100 Common Ports**
```
▶ Enter arguments: --target example.com --top-ports
```
- Focuses on most likely open ports (HTTP, SSH, FTP, etc.)
- Faster than full range scans
- Best for initial reconnaissance

**3. Quick Scan Mode (Fast Results)**
```
▶ Enter arguments: --target 192.168.1.1 --top-ports --quick
```
- Reduced timeout for faster scanning
- Good for live networks
- Less thorough but much faster

#### 🔍 Advanced Scanning Features

**4. Custom Port Specification**
```
▶ Enter arguments: --target 10.0.0.1 --ports 80,443,22,8080,3389
```
- Scan only specific ports you're interested in
- Comma-separated list
- Fastest option for targeted scanning

**5. Port Range Scanning**
```
▶ Enter arguments: --target example.com --ports 1-1000
```
- Scan a continuous range of ports
- Good for comprehensive coverage
- Can specify any range (e.g., 8000-9000)

**6. High-Performance Scanning (More Threads)**
```
▶ Enter arguments: --target 192.168.1.1 --top-ports --threads 100
```
- Increases concurrent connections
- Faster scanning on powerful systems
- Use lower values (25-50) on slower systems

#### 🕵️ Service Detection Features

**7. Service Version Detection**
```
▶ Enter arguments: --target example.com --top-ports --service-detection
```
- Identifies what services are running on open ports
- Shows service banners and versions
- Essential for security assessments

**8. Stealth Scanning (Linux/Mac with sudo)**
```
▶ Enter arguments: --target 192.168.1.1 --stealth --top-ports
```
- Uses SYN stealth technique
- Harder to detect by target systems
- Requires running R.A.V.E.N with sudo/administrator privileges

#### 🌐 Network Range Features

**9. Subnet Scanning (CIDR Notation)**
```
▶ Enter arguments: --target 192.168.1.0/24 --top-ports
```
- Scans entire network range (192.168.1.1 to 192.168.1.254)
- Great for network discovery
- Can use any CIDR range (/16, /20, etc.)

**10. Multiple Target Scanning**
```
▶ Enter arguments: --target 192.168.1.1,192.168.1.5,192.168.1.10 --top-ports
```
- Scan multiple specific hosts
- Comma-separated IP addresses
- Efficient for scattered targets

#### ⚙️ Timing and Performance Features

**11. Slow/Careful Scanning**
```
▶ Enter arguments: --target example.com --top-ports --timeout 10 --threads 10
```
- Longer timeout (10 seconds vs default 1 second)
- Fewer threads to avoid detection
- Good for sensitive environments

**12. Aggressive Fast Scanning**
```
▶ Enter arguments: --target 192.168.1.1 --ports 1-65535 --threads 100 --timeout 2
```
- Full port range scan
- Maximum threads
- Faster timeout
- Use only on your own networks

#### 💾 Output and Reporting Features

**13. Save Results to File**
```
▶ Enter arguments: --target example.com --top-ports --service-detection --output scan_results.txt
```
- Saves all scan results to a text file
- File will be created in the Port Scanner directory
- Good for documentation and reporting

**14. Comprehensive Scan with All Features**
```
▶ Enter arguments: --target 192.168.1.1 --top-ports --service-detection --threads 75 --timeout 5 --output comprehensive_scan.txt
```
- Combines service detection, custom threading, timeout, and file output
- Most thorough scanning option
- Excellent for professional assessments

#### 🎯 Real-World Scenario Examples

**Web Server Assessment**
```
▶ Enter arguments: --target example.com --ports 80,443,8080,8443,3000,5000 --service-detection
```

**Network Discovery**
```
▶ Enter arguments: --target 192.168.1.0/24 --top-ports --quick --threads 100
```

**Security Audit (Comprehensive)**
```
▶ Enter arguments: --target target-server.com --ports 1-65535 --service-detection --threads 50 --output security_audit.txt
```

**Quick Health Check**
```
▶ Enter arguments: --target 10.0.0.1 --ports 22,80,443,3389 --quick
```

#### 🚨 Managing Long-Running Scans

**Small Network Discovery (Fast - 2-5 minutes)**
```
▶ Enter arguments: -t 192.168.1.0/28 --top-ports --quick
```
- Scans only 16 hosts (192.168.1.1-16)
- Uses top 100 ports with quick timeout
- Good for initial network discovery

**Large Network Discovery (Slow - 15-30 minutes)**
```
▶ Enter arguments: -t 192.168.1.0/24 -p 22,80,443 --threads 100
```
- Scans 254 hosts with 3 ports each
- **Tip**: You can stop anytime with Ctrl+C
- **Tip**: Results are shown as each host completes

**Emergency Stop Example:**
```
🎯 Scanning target: 192.168.1.50
📡 Scanning 3 ports with 100 threads
⏱️  Timeout: 0.5s per port
^C  ← Press Ctrl+C here to stop gracefully
```

## 📖 Direct Terminal Usage Examples

**Note**: The following examples are for direct terminal usage. If using the R.A.V.E.N CLI interface, only enter the arguments portion (everything after `python port_scanner.py`).

### Basic Port Scan
```bash
python port_scanner.py --target 192.168.1.1
```

### Scan Common Ports with Service Detection
```bash
python port_scanner.py --target example.com --top-ports --service-detection
```

### Custom Port Range with High Thread Count
```bash
python port_scanner.py --target 10.0.0.1 --ports 1-1000 --threads 100
```

### Network Range Scan
```bash
python port_scanner.py --target 192.168.1.0/24 --top-ports
```

### Stealth Scan with Longer Timeout
```bash
python port_scanner.py --target target.com --ports 80,443,8080 --timeout 5 --stealth
```

### Export Results to File
```bash
python port_scanner.py --target 192.168.1.1 --output results.txt
```

### Comprehensive Scan
```bash
python port_scanner.py --target example.com --ports 1-65535 --threads 100 --service-detection --output comprehensive_scan.txt
```

### Quick Scan Mode
```bash
python port_scanner.py --target 192.168.1.1 --top-ports --quick
```

## 🎯 Command Line Arguments

| Argument | Description | Default | Example |
|----------|-------------|---------|---------|
| `-t, --target` | Target IP address, hostname, or CIDR range | **Required** | `192.168.1.1` |
| `-p, --ports` | Port specification (comma-separated, ranges) | All common ports | `80,443,8080` or `1-1000` |
| `--top-ports` | Scan top 100 common service ports | Disabled | `--top-ports` |
| `-T, --threads` | Number of concurrent threads | `50` | `--threads 100` |
| `--timeout` | Connection timeout in seconds | `1.0` | `--timeout 5` |
| `-s, --service-detection` | Enable service version detection | Disabled | `--service-detection` |
| `--stealth` | Use SYN stealth scan (requires root/admin) | Disabled | `--stealth` |
| `--quick` | Quick scan mode (reduced timeout) | Disabled | `--quick` |
| `-o, --output` | Save results to specified file | Console only | `--output results.txt` |
| `-h, --help` | Display full help information | - | `--help` |

### Port Specification Formats

- **Single port**: `80`
- **Port range**: `1-1000`
- **Port list**: `80,443,8080,8443`
- **Mixed**: `22,80-90,443,8000-8080`

## 🔬 Technical Specifications

- **Language**: Python 3.6+
- **Dependencies**: Standard library only (socket, threading, argparse, ipaddress)
- **Performance**: Can scan 1000 ports in under 10 seconds with optimal threading
- **Memory Usage**: Low memory footprint with efficient thread management
- **Compatibility**: Cross-platform (Linux, Windows, macOS)
- **Scan Methods**: TCP Connect (reliable), SYN scan capability

## 📊 Performance Benchmarks

| Configuration | Speed | Use Case |
|---------------|-------|----------|
| **Quick Scan** | ~200 ports/second | Common ports with high threads |
| **Standard Scan** | ~100 ports/second | Default settings (1-1000 ports) |
| **Comprehensive** | ~50 ports/second | Full port range (1-65535) |
| **Stealth Scan** | ~10 ports/second | Low profile scanning |

### Recommended Configurations

#### Quick Scan (Common Ports)
```bash
python port_scanner.py --target [TARGET] --top-ports --quick --threads 100
```

#### Comprehensive Scan (All Ports)
```bash
python port_scanner.py --target [TARGET] --ports 1-65535 --threads 100 --timeout 2
```

#### Stealth Scan (Slow & Quiet)
```bash
python port_scanner.py --target [TARGET] --stealth --threads 10 --timeout 5
```

## 💡 Use Cases

- **Network Discovery**: Map open services on target networks
- **Security Assessment**: Identify exposed services and potential attack vectors
- **System Administration**: Monitor service availability and port status
- **Penetration Testing**: Initial reconnaissance phase scanning
- **Compliance Auditing**: Verify expected service configurations
- **Troubleshooting**: Diagnose network connectivity issues

## ⏹️ Controlling Scan Execution

### How to Stop a Running Scan

When scanning large networks (like `/24` subnets), scans can take a long time. Here's how to control them:

#### **Method 1: Keyboard Interrupt (Recommended)**
```
Press: Ctrl+C (Windows/Linux) or Cmd+C (Mac)
```
- **Safe method** - allows the scanner to clean up properly
- **Shows summary** of results found so far
- **Immediate response** - stops within 1-2 seconds

#### **Method 2: Terminal Control**
- **Close terminal window** - immediate but less graceful
- **Use Ctrl+Z** to pause (Linux/Mac), then `kill %1` to stop

### Scan Time Estimates

| Target Type | Ports | Estimated Time |
|-------------|-------|----------------|
| **Single Host** | 3 ports | 1-3 seconds |
| **Single Host** | 100 ports | 5-15 seconds |
| **Single Host** | 1000 ports | 30-60 seconds |
| **Small Network (/28)** | Common ports | 2-5 minutes |
| **Medium Network (/24)** | Common ports | 15-30 minutes |
| **Large Network (/16)** | Common ports | 4-8 hours |

### Optimizing Long Scans

#### **Reduce Scan Time:**
```
▶ Enter arguments: -t 192.168.1.0/24 -p 22,80,443 --quick --threads 100
```
- Use `--quick` for faster timeouts
- Limit to essential ports only
- Increase thread count for better performance

#### **Scan Smaller Ranges:**
```
▶ Enter arguments: -t 192.168.1.1-50 -p 22,80,443
```
- Target specific IP ranges instead of full subnets
- Focus on likely active hosts

#### **Use Top Ports Instead:**
```
▶ Enter arguments: -t 192.168.1.0/24 --top-ports --quick
```
- Scans only the most common 100 ports
- Much faster than custom port lists

## 🛡️ Security Considerations

### Rate Limiting
The scanner includes built-in rate limiting to prevent:
- Network flooding
- IDS/IPS detection
- Target system overload

### Stealth Options
- Adjustable timeout values
- Configurable thread counts
- Custom port ranges to avoid common detection patterns

## 🔧 Installation

### Prerequisites
- Python 3.6 or higher
- No external dependencies required

### Setup
1. Ensure Python 3.6+ is installed
2. **Navigate to the Port Scanner directory**:
   ```bash
   # From R.A.V.E.N root directory
   cd "scripts/scanning/Port Scanner"
   ```
3. Make executable (Linux/Mac): `chmod +x port_scanner.py`
4. Test the installation:
   ```bash
   python port_scanner.py --help    # Windows
   python3 port_scanner.py --help   # Linux/Mac
   ```

## 🐛 Troubleshooting

### R.A.V.E.N Interface Issues

**❌ "Execution cancelled" when entering arguments**
```
Execute with custom arguments? (y/N): -t 192.168.1.0/24 -p 22,80,443 --quick
▶ Execution cancelled
```
**Problem**: You entered arguments instead of answering the yes/no question!

**The interface expects TWO separate inputs:**
1. **First**: Answer `y` or `N` to the question
2. **Second**: Enter your arguments (only if you answered `y`)

**✅ Correct Solution**:
```
Execute with custom arguments? (y/N): y
▶ Enter arguments: -t 192.168.1.0/24 -p 22,80,443 --quick
```

**Key Points**:
- The question `Execute with custom arguments? (y/N):` expects ONLY `y` or `N`
- If you enter anything else (like arguments), it treats it as "N" and cancels
- Arguments are entered in a separate step that only appears if you answer `y`

**❌ Script not found or path errors**
**Problem**: R.A.V.E.N can't find the script file
**Solution**: Ensure you're running `bash main.sh` from the R.A.V.E.N root directory

### Common Issues

**Permission Errors (Linux/Mac)**
```bash
# Run with sudo for stealth scans (requires raw sockets)
sudo python port_scanner.py --target example.com --stealth
```

**Timeout Issues**
```bash
# Increase timeout for slow networks
python port_scanner.py --target example.com --timeout 10
```

**High Resource Usage**
```bash
# Reduce thread count for resource-constrained systems
python port_scanner.py --target example.com --threads 25
```

## ⚠️ Legal Notice

**This tool is designed for authorized security testing and network administration only.**

- Only scan networks and systems you own or have explicit written permission to test
- Ensure compliance with local laws and regulations
- Use responsibly and ethically
- Report discovered vulnerabilities through proper disclosure channels
- Maintain detailed logs of scanning activities for audit purposes

## 📝 Output Example

```
🔍 R.A.V.E.N ADVANCED PORT SCANNER
   Rapid Automation & Vulnerability Enumeration Networks
======================================================================

[+] Scanning target: example.com (93.184.216.34)
[+] Port range: 1-1000
[+] Threads: 100
[+] Timeout: 3 seconds

[✓] Port 22/tcp   open    SSH
[✓] Port 53/tcp   open    DNS
[✓] Port 80/tcp   open    HTTP
[✓] Port 443/tcp  open    HTTPS

[+] Scan completed in 8.34 seconds
[+] 4 open ports found out of 1000 scanned
```

---

*Part of the R.A.V.E.N Cybersecurity Toolkit*  
*Last Updated: September 30, 2025*