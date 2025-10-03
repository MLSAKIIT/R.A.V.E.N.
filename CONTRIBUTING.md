# Contributing to R.A.V.E.N

## Start

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/MLSAKIIT/R.A.V.E.N.git
   cd R.A.V.E.N
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a new branch:
   ```bash
   git checkout -b feature/your-username-script-name
   ```

## 📂 Script Categories

Choose any category to contribute to:

- **`crypto/`** - Cryptographic tools
- **`enumeration/`** - Service enumeration tools  
- **`exploitation/`** - Exploit tools and payloads
- **`osint/`** - Open Source Intelligence
- **`payloads/`** - Payload generators
- **`scanning/`** - Port scanning and service detection
- **`utils/`** - General utility scripts

## � Script Contribution Guidelines

### Project Structure

When contributing a script to any category, follow this structure:

```
scripts/
├── category_name/
│   ├── your_script.py          # Main script file
│   └── README.md               # Script-specific documentation
```

### 📝 Script Documentation Standards

#### 1. **Script Header Template**

Every script must include a comprehensive header:

```python
#!/usr/bin/env python3
"""
R.A.V.E.N - Script Name
Category: [crypto/enumeration/exploitation/osint/payloads/scanning/helpers]
Project: MLSAKIIT Community
Version: 1.0.0
Description: Brief description of what the script does

Usage:
    python3 script_name.py [arguments]
    
Example:
    python3 script_name.py --target 192.168.1.1 --port 80

Requirements:
    - Python 3.6+
    - requests
    - other dependencies

Disclaimer: 
    This tool is for educational and authorized testing purposes only.
    Users are responsible for complying with applicable laws and regulations.
"""
```

#### 2. **Help/Usage Function**

Every script must implement a `--help` argument:

```python
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Script description",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 script_name.py --target example.com
  python3 script_name.py --input file.txt --output results.txt
        """
    )
    parser.add_argument('--target', required=True, help='Target to scan/test')
    parser.add_argument('--output', help='Output file for results')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    return parser.parse_args()
```

#### 3. **Error Handling**

Implement robust error handling:

```python
import sys
import logging

def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format='[%(levelname)s] %(message)s',
        level=level
    )

def main():
    try:
        args = parse_arguments()
        setup_logging(args.verbose)
        
        # Your script logic here
        
    except KeyboardInterrupt:
        print("\n[!] Script interrupted by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Script error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 📄 Required Documentation

#### 1. **Script README.md Template**

Create a `README.md` file for your script:

```markdown
# Script Name

## Description
Detailed description of what the script does and its purpose.

## Features
- Feature 1
- Feature 2
- Feature 3

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python3 script_name.py --help
python3 script_name.py --target example.com
```

## Arguments
- `--target`: Target to scan/analyze (required)
- `--output`: Output file for results (optional)
- `--verbose`: Enable verbose output (optional)

## Examples
```bash
# Basic usage
python3 script_name.py --target 192.168.1.1

# With output file
python3 script_name.py --target example.com --output results.txt

# Verbose mode
python3 script_name.py --target example.com --verbose
```

## Output
Description of what the script outputs and format.

## Dependencies
- Python 3.6+
- requests>=2.25.0
- other-library>=1.0.0

## Legal Disclaimer
This tool is intended for educational and authorized security testing purposes only.
```

#### 2. **Code Quality Standards**

- **PEP 8 Compliance**: Follow Python style guidelines
- **Comments**: Add meaningful comments for complex logic
- **Functions**: Break code into logical, reusable functions
- **Constants**: Use constants for configuration values
- **Validation**: Validate all user inputs

#### 3. **Testing Requirements**

Before submitting:

```bash
# Test basic functionality
python3 your_script.py --help

# Test with sample data
python3 your_script.py --target test_target

# Test error conditions
python3 your_script.py --invalid-arg
```

### 🔍 Category-Specific Guidelines

#### **Crypto Scripts**
- Include cipher identification capabilities
- Support multiple encoding formats
- Provide encryption/decryption examples

#### **Enumeration Scripts**
- Implement service detection
- Support multiple target formats (IP, domain, CIDR)
- Include banner grabbing when applicable

#### **Exploitation Scripts**
- Add payload customization options
- Include target verification
- Implement safe execution modes

#### **OSINT Scripts**
- Support multiple data sources
- Include data export options
- Respect rate limiting and APIs

#### **Payload Scripts**
- Generate multiple payload formats
- Include encoding options
- Provide usage examples

#### **Scanning Scripts**
- Support port ranges and lists
- Include service detection
- Implement threading for performance

#### **Utils Scripts**
- Focus on reusability
- Include comprehensive help
- Support batch operations

### ✅ Pre-Submission Checklist

- [ ] Script follows naming convention: `descriptive_name.py`
- [ ] Header documentation is complete
- [ ] `--help` argument is implemented
- [ ] Error handling is robust
- [ ] Script README.md is created
- [ ] Dependencies are listed in requirements.txt (if any)
- [ ] Script is tested and functional
- [ ] Code follows PEP 8 standards
- [ ] Legal disclaimer is included

## �🚀 Submit Your Contribution

1. **Add your script** to the appropriate scripts category folder.
2. **Test your script** thoroughly.
3. **Update README.md**: Add your script to the "Scripts Available" Section of your script category


4. **Create a Pull Request** with:
   - Clear description of what your script does
   - Usage example
   - Any dependencies needed

## 🎯 Get Recognized

Your username will appear in the Contributors Dashboard once your PR is merged!

---

**Questions?** Open an issue or join our WhatsApp group for discussions.
