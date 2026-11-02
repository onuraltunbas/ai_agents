import re
import sys
import json
import argparse
import math
import mmap
import os

def calculate_entropy(data_str):
    if not data_str:
        return 0
    entropy = 0
    for x in set(data_str):
        p_x = float(data_str.count(x)) / len(data_str)
        entropy += - p_x * math.log2(p_x)
    return entropy

def get_file_type(header):
    magic_dict = {
        b'PK\x03\x04': 'APK / ZIP Archive',
        b'\x7fELF': 'ELF (Linux / Android Native)',
        b'MZ': 'PE (Windows Executable)',
        b'dex\n': 'DEX (Android Dalvik Executable)',
        b'\x03\x00\x08\x00': 'AXML (Android Manifest)'
    }
    for magic, ftype in magic_dict.items():
        if header.startswith(magic):
            return ftype
    return 'Unknown Binary'

class HeuristicStringAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.results = {
            "metadata": {},
            "urls": set(),
            "ips": set(),
            "emails": set(),
            "high_entropy_secrets": set(),
            "suspicious_api_calls": set()
        }
        
    def analyze(self):
        file_size = os.path.getsize(self.file_path)
        if file_size == 0:
            print("Error: Empty file.")
            sys.exit(1)

        with open(self.file_path, 'rb') as f:
            header = f.read(16)
            self.results["metadata"]["file_type"] = get_file_type(header)
            self.results["metadata"]["size_bytes"] = file_size

            f.seek(0)
            with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as mm:
                data = mm.read()
        
        ascii_strings = re.findall(b'[ -~]{5,}', data)
        utf16_strings = re.findall(b'(?:[\x20-\x7E]\x00){5,}', data)

        all_strings = []
        for s in ascii_strings:
            try:
                all_strings.append(s.decode('utf-8'))
            except UnicodeDecodeError:
                pass
                
        for s in utf16_strings:
            try:
                all_strings.append(s.decode('utf-16le'))
            except UnicodeDecodeError:
                pass

        self._classify(all_strings)

    def _classify(self, strings):
        url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
        ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
        email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
        
        sus_apis = [
            'exec', 'system', 'Runtime.getRuntime', 
            'Cipher.getInstance', 'MessageDigest', 'DexClassLoader'
        ]

        for s in strings:
            if url_pattern.search(s):
                self.results["urls"].add(s)
            elif ip_pattern.search(s):
                self.results["ips"].add(s)
            elif email_pattern.search(s):
                self.results["emails"].add(s)
            else:
                for api in sus_apis:
                    if api in s:
                        self.results["suspicious_api_calls"].add(s)
                        
                if len(s) >= 20 and ' ' not in s:
                    ent = calculate_entropy(s)
                    if ent > 4.6: 
                        self.results["high_entropy_secrets"].add((s, round(ent, 2)))

    def get_report(self):
        return {
            "metadata": self.results["metadata"],
            "urls": list(self.results["urls"]),
            "ips": list(self.results["ips"]),
            "emails": list(self.results["emails"]),
            "suspicious_api_calls": list(self.results["suspicious_api_calls"]),
            "high_entropy_secrets": [
                {"value": item[0], "shannon_entropy": item[1]} 
                for item in self.results["high_entropy_secrets"]
            ]
        }

def main():
    parser = argparse.ArgumentParser(description="Static String Extractor & Classifier")
    parser.add_argument('-f', '--file', required=True, help="Target binary file")
    parser.add_argument('-o', '--out', default='reports/analysis.json', help="Output JSON path")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: Target file '{args.file}' not found.")
        sys.exit(1)

    analyzer = HeuristicStringAnalyzer(args.file)
    analyzer.analyze()
    
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(analyzer.get_report(), f, indent=4)
        
    print(f"[+] Heuristic analysis complete. Report generated at: {args.out}")

if __name__ == '__main__':
    main()
