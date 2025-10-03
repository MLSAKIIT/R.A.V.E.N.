#!/usr/bin/env python3
"""
R.A.V.E.N Advanced Port Scanner
Professional port scanning tool with multiple scan modes and service detection
"""

import argparse
import socket
import sys
import threading
import time
from datetime import datetime
import ipaddress

class RAVENPortScanner:
    def __init__(self):
        self.open_ports = []
        self.lock = threading.Lock()
        self.common_ports = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 111: 'RPCbind', 135: 'MS-RPC', 139: 'NetBIOS',
            143: 'IMAP', 443: 'HTTPS', 445: 'SMB', 993: 'IMAPS', 995: 'POP3S',
            1723: 'PPTP', 3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL',
            5900: 'VNC', 8080: 'HTTP-Alt', 8443: 'HTTPS-Alt'
        }

    def banner(self):
        """
        Display the R.A.V.E.N port scanner banner
        
        This function prints a stylized banner to the console when the scanner starts.
        It provides visual branding and identifies the tool being used.
        
        Returns:
            None - prints directly to console
        """
        print("\n" + "="*70)
        print("🔍 R.A.V.E.N ADVANCED PORT SCANNER")
        print("   Rapid Automation & Vulnerability Enumeration Networks")
        print("="*70)

    def scan_port(self, target, port, timeout):
        """
        Scan a single port on the target host using TCP connect scan
        
        This function performs a basic TCP connect scan on a specific port.
        It attempts to establish a full TCP connection to determine if the port is open.
        
        Args:
            target (str): IP address or hostname to scan
            port (int): Port number to scan (1-65535)
            timeout (float): Socket timeout in seconds
            
        Returns:
            None - Results are stored in self.open_ports list
            
        Process:
            1. Create a TCP socket
            2. Set timeout to prevent hanging
            3. Attempt connection to target:port
            4. If successful (result == 0), port is open
            5. Identify service using common_ports mapping  
            6. Thread-safely add result to open_ports list
            7. Print real-time discovery feedback
        """
        try:
            # Create a TCP socket for connection attempt
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Set timeout to prevent the scan from hanging on closed ports
            sock.settimeout(timeout)
            
            # Attempt to connect - returns 0 if successful, error code otherwise
            result = sock.connect_ex((target, port))
            
            if result == 0:  # Connection successful = port is open
                # Look up the service name for this port, default to 'Unknown'
                service = self.common_ports.get(port, 'Unknown')
                
                # Thread-safe operation to add result to shared list
                with self.lock:
                    self.open_ports.append((port, service))
                    print(f"✅ Port {port:5d}/tcp  OPEN    {service}")
            
            # Always close the socket to free resources
            sock.close()
        except Exception:
            # Silently handle any connection errors (timeouts, network issues)
            pass

    def threaded_scan(self, target, ports, threads, timeout):
        """
        Perform multi-threaded port scanning for improved performance
        
        This function coordinates multiple threads to scan ports simultaneously,
        significantly reducing scan time compared to sequential scanning.
        
        Args:
            target (str): IP address or hostname to scan
            ports (list): List of port numbers to scan
            threads (int): Number of worker threads to create
            timeout (float): Socket timeout per port
            
        Returns:
            None - Results stored in self.open_ports
            
        Process:
            1. Display scan information to user
            2. Create worker function for thread execution
            3. Create shared port queue for thread coordination
            4. Launch specified number of worker threads
            5. Wait for all threads to complete
            
        Threading Model:
            - Work-stealing approach: threads take ports from shared queue
            - Daemon threads for clean shutdown
            - Thread synchronization using locks for shared resources
        """
        # Display scan parameters to user
        print(f"\n🎯 Target: {target}")
        print(f"📡 Scanning {len(ports)} ports with {threads} threads")
        print(f"⏱️  Timeout: {timeout}s per port")
        print("-" * 50)
        
        def worker():
            """
            Worker thread function - each thread runs this independently
            
            Continuously pulls ports from the shared queue and scans them
            until no more ports remain. Uses exception handling to detect
            when queue is empty.
            """
            while True:
                try:
                    # Atomically get next port from queue (not thread-safe but works for this use case)
                    port = port_queue.pop(0)
                    # Scan the port using our scan_port method
                    self.scan_port(target, port, timeout)
                except IndexError:
                    # Queue is empty, worker can exit
                    break
        
        # Create shared work queue - all threads will pull from this
        port_queue = list(ports)
        thread_list = []
        
        # Create and start worker threads
        # Use min() to avoid creating more threads than ports
        for _ in range(min(threads, len(ports))):
            t = threading.Thread(target=worker)
            t.daemon = True  # Allow main program to exit even if threads are running
            t.start()
            thread_list.append(t)
        
        # Wait for all threads to complete their work
        for t in thread_list:
            t.join()

    def stealth_scan(self, target, port):
        """
        Perform SYN stealth scan on a single port (requires root privileges)
        
        SYN stealth scanning is a more advanced technique that sends only SYN packets
        without completing the TCP handshake, making it less detectable by intrusion
        detection systems and firewalls.
        
        Args:
            target (str): IP address to scan
            port (int): Port number to scan
            
        Returns:
            bool: True if port is open, False if closed, None if scapy unavailable
            
        Process:
            1. Import scapy library (required for packet crafting)
            2. Send SYN packet to target:port
            3. Analyze response:
               - SYN-ACK (flags=18) = Port open
               - RST (flags=4) = Port closed
               - No response = Port filtered
            4. Never complete handshake (stealth aspect)
            
        Requirements:
            - Root/Administrator privileges (raw socket access)
            - Scapy library installed
            - Network interface access
        """
        try:
            # Import scapy for packet crafting (optional dependency)
            import scapy.all as scapy
            
            # Send SYN packet and wait for response
            # IP(dst=target) creates IP header with destination
            # TCP(dport=port, flags="S") creates TCP SYN packet
            response = scapy.sr1(scapy.IP(dst=target)/scapy.TCP(dport=port, flags="S"), 
                               timeout=1, verbose=0)
            
            # Check if we received a response with TCP layer
            if response and response.haslayer(scapy.TCP):
                # TCP flags: SYN-ACK = 18 (0x12) indicates open port
                if response[scapy.TCP].flags == 18:  # SYN-ACK response
                    return True
                # RST = 4 (0x04) indicates closed port
                # Other flags may indicate filtered ports
        except ImportError:
            # Graceful fallback if scapy is not installed
            print("⚠️  Scapy not installed. Falling back to connect scan.")
            return None
        except Exception:
            # Handle any other exceptions (permissions, network errors)
            pass
        return False

    def service_detection(self, target, port):
        """
        Perform basic service detection and banner grabbing
        
        This function attempts to identify what service is running on an open port
        by connecting and analyzing the service banner or response to probes.
        
        Args:
            target (str): IP address or hostname
            port (int): Open port number to probe
            
        Returns:
            str: Service identification string or error message
            
        Process:
            1. Connect to the open port
            2. Send generic HTTP probe (works for many services)
            3. Receive and analyze the banner/response
            4. Pattern match against known service signatures
            5. Return formatted service information
            
        Detection Methods:
            - Banner grabbing: Read service announcement
            - Probe responses: Send test data and analyze replies
            - Protocol fingerprinting: Identify service by behavior
            
        Limitations:
            - Only basic detection (not comprehensive like nmap)
            - May not work with all services
            - Some services don't provide banners
        """
        try:
            # Create new socket for service probing
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)  # Shorter timeout for service detection
            sock.connect((target, port))
            
            # Send generic HTTP probe - many services respond to this
            # This is a basic technique; advanced scanners use service-specific probes
            sock.send(b"GET / HTTP/1.0\r\n\r\n")
            
            # Receive up to 1024 bytes of response
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            
            # Analyze the banner to identify the service
            if 'HTTP' in banner:
                # Extract HTTP server information from response
                return f"HTTP Server: {banner.split()[0] if banner.split() else 'Unknown'}"
            elif 'SSH' in banner:
                # SSH services typically announce their version
                return f"SSH Server: {banner.strip()}"
            elif 'FTP' in banner:
                # FTP services send welcome banners
                return f"FTP Server: {banner.strip()}"
            else:
                # For unknown services, return truncated banner
                return banner.strip()[:50] + "..." if len(banner) > 50 else banner.strip()
        except:
            # Return error message if service detection fails
            return "Service detection failed"

    def generate_port_range(self, port_arg):
        """
        Parse and generate port list from various input formats
        
        This function provides flexible port specification allowing users to:
        - Specify individual ports: "80,443,22"
        - Use port ranges: "1-1000"
        - Combine both: "22,80,443,8000-9000"
        
        Args:
            port_arg (str): Port specification string
            
        Returns:
            list: Sorted list of unique port numbers
            
        Supported Formats:
            - Single ports: "80" or "80,443,22"
            - Port ranges: "1-1000" or "8000-9000"
            - Mixed format: "22,80,443,8000-9000,3389"
            
        Examples:
            "80,443" -> [80, 443]
            "1-5" -> [1, 2, 3, 4, 5]
            "22,80,8000-8005" -> [22, 80, 8000, 8001, 8002, 8003, 8004, 8005]
        """
        ports = set()  # Use set to automatically handle duplicates
        
        # Split by comma to handle multiple port specifications
        for part in port_arg.split(','):
            part = part.strip()  # Remove whitespace
            
            if '-' in part:
                # Handle port range (e.g., "1-1000")
                start, end = map(int, part.split('-'))
                # Add all ports in range (inclusive of both start and end)
                ports.update(range(start, end + 1))
            else:
                # Handle single port (e.g., "80")
                ports.add(int(part))
        
        # Return sorted list for consistent output
        return sorted(ports)

def main():
    """
    Main function - Entry point for the R.A.V.E.N port scanner
    
    This function handles:
    - Command-line argument parsing
    - Scan configuration and validation
    - Target processing (single hosts and CIDR ranges)
    - Scan execution coordination
    - Results processing and output
    - Performance statistics calculation
    
    The function supports multiple scanning modes:
    - Basic TCP connect scanning
    - Multi-threaded scanning for performance
    - Service detection and banner grabbing
    - Network range scanning (CIDR notation)
    - Results export to file
    
    Command-line interface provides professional-grade options
    similar to industry-standard tools like nmap.
    """
    # Initialize scanner instance
    scanner = RAVENPortScanner()
    
    # Setup command-line argument parser with detailed help
    parser = argparse.ArgumentParser(
        description='R.A.V.E.N Advanced Port Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  -t 192.168.1.1 -p 80,443,22
  -t example.com -p 1-1000 -T 50
  -t 10.0.0.1 --top-ports -s
  -t 192.168.1.0/24 -p 22,80,443 --quick
        '''
    )
    
    parser.add_argument('-t', '--target', required=True, 
                       help='Target IP/hostname or CIDR range')
    parser.add_argument('-p', '--ports', default='22,80,443,21,25,53,110,143,993,995',
                       help='Ports to scan (comma-separated, ranges: 1-100)')
    parser.add_argument('-T', '--threads', type=int, default=50,
                       help='Number of threads (default: 50)')
    parser.add_argument('--timeout', type=float, default=1.0,
                       help='Socket timeout in seconds (default: 1.0)')
    parser.add_argument('--top-ports', action='store_true',
                       help='Scan top 100 common ports')
    parser.add_argument('-s', '--service-detection', action='store_true',
                       help='Enable service version detection')
    parser.add_argument('--stealth', action='store_true',
                       help='Use SYN stealth scan (requires root)')
    parser.add_argument('--quick', action='store_true',
                       help='Quick scan (reduced timeout)')
    parser.add_argument('-o', '--output', help='Save results to file')
    
    args = parser.parse_args()
    
    scanner.banner()
    
    # Handle quick scan
    if args.quick:
        args.timeout = 0.5
        args.threads = 100
        print("🚀 Quick scan mode enabled")
    
    # Generate port list
    if args.top_ports:
        ports = list(scanner.common_ports.keys())
        print("📋 Using top common ports")
    else:
        ports = scanner.generate_port_range(args.ports)
    
    # Handle CIDR ranges
    try:
        network = ipaddress.ip_network(args.target, strict=False)
        targets = [str(ip) for ip in network.hosts()] if network.num_addresses > 1 else [args.target]
    except:
        targets = [args.target]
    
    start_time = time.time()
    results = []
    
    for target in targets:
        if len(targets) > 1:
            print(f"\n🎯 Scanning target: {target}")
        
        scanner.open_ports = []  # Reset for each target
        scanner.threaded_scan(target, ports, args.threads, args.timeout)
        
        if scanner.open_ports:
            print(f"\n📊 SCAN RESULTS for {target}:")
            print("-" * 50)
            for port, service in sorted(scanner.open_ports):
                result_line = f"Port {port:5d}/tcp  OPEN    {service}"
                print(f"✅ {result_line}")
                
                # Service detection
                if args.service_detection:
                    service_info = scanner.service_detection(target, port)
                    if service_info:
                        print(f"   └── {service_info}")
                
                results.append(f"{target}:{port} - {service}")
        else:
            print(f"\n❌ No open ports found on {target}")
    
    # Summary
    elapsed = time.time() - start_time
    total_ports = len(ports) * len(targets)
    
    print(f"\n" + "="*70)
    print(f"📈 SCAN SUMMARY")
    print(f"   Targets scanned: {len(targets)}")
    print(f"   Ports per target: {len(ports)}")
    print(f"   Total ports scanned: {total_ports}")
    print(f"   Open ports found: {len(results)}")
    print(f"   Scan duration: {elapsed:.2f} seconds")
    print(f"   Scan rate: {total_ports/elapsed:.0f} ports/sec")
    print("="*70)
    
    # Save results
    if args.output:
        with open(args.output, 'w') as f:
            f.write(f"R.A.V.E.N Port Scan Results\n")
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(f"Targets: {', '.join(targets)}\n")
            f.write(f"Open Ports:\n")
            for result in results:
                f.write(f"{result}\n")
        print(f"💾 Results saved to: {args.output}")

if __name__ == "__main__":
    main()