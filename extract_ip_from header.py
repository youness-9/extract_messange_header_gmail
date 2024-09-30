import subprocess
import os
import re
from collections import defaultdict

def get_ip_base(ip):
    return '.'.join(ip.split('.')[:-1])

def get_highest_ip(ip_list):
    return max(ip_list, key=lambda ip: list(map(int, ip.split('.'))))

output_dir = "ip_results"
os.makedirs(output_dir, exist_ok=True)

path = "original\\*.eml"

result = subprocess.run(["dir", path], capture_output=True, text=True, shell=True)

all_extracted_ips = set()
ip_groups = defaultdict(list)

if result.stdout:
    for line in result.stdout.splitlines():
        parts = line.split()
        if parts and (len(parts) > 0) and (parts[-1].endswith('.eml')):
            filename = parts[-1]
            full_path = os.path.join("original", filename)

            try:
                with open(full_path, "r", encoding='utf-8') as f:
                    for file_line in f:
                        if "Received-SPF" in file_line:
                            ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', file_line)
                            all_extracted_ips.update(ips)

                            for ip in ips:
                                base = get_ip_base(ip)
                                ip_groups[base].append(ip)
            except UnicodeDecodeError:
                try:
                    with open(full_path, "r", encoding='latin-1') as f:
                        for file_line in f:
                            if "Received-SPF" in file_line:
                                ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', file_line)
                                all_extracted_ips.update(ips)

                                for ip in ips:
                                    base = get_ip_base(ip)
                                    ip_groups[base].append(ip)
                except Exception as e:
                    print(f"Error reading {full_path}: {e}")

    with open(os.path.join(output_dir, "all_ips.txt"), "w") as all_ip_file:
        for ip in sorted(all_extracted_ips):
            all_ip_file.write(ip + "\n")

    with open(os.path.join(output_dir, "hit_ip.txt"), "w") as hit_ip_file:
        for base, ips in ip_groups.items():
            highest_ip = get_highest_ip(ips)
            hit_ip_file.write(highest_ip + "\n")

    print(f"Extracted all IPs saved to {output_dir}/all_ips.txt ({len(all_extracted_ips)} found).")
    print(f"Extracted hit IPs saved to {output_dir}/hit_ip.txt ({len(ip_groups)} unique ranges found).")
else:
    print("No .eml files found.")