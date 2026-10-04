#!/usr/bin/env python3
"""
运行邮件分类并发送报告到飞书
"""
import os
import sys
import subprocess
from datetime import datetime

# 运行邮件分类器
base_dir = os.path.dirname(os.path.abspath(__file__))
sorter_script = os.path.join(base_dir, 'gmail_sorter.py')

print("=" * 60)
print("Running Foreign Trade Email Sorter...")
print("=" * 60)

result = subprocess.run([sys.executable, sorter_script, '--max', '50'], 
                       capture_output=True, text=True, cwd=base_dir)

print(result.stdout)
if result.stderr:
    print("Errors:", result.stderr)

# 读取最新报告
reports_dir = os.path.join(base_dir, 'reports')
today = datetime.now().strftime('%Y-%m-%d')
report_file = os.path.join(reports_dir, f'inquiry-report-{today}.txt')

if os.path.exists(report_file):
    with open(report_file, 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    # 提取关键信息
    lines = report_content.split('\n')
    summary = []
    for line in lines:
        if 'Total Emails:' in line or 'Inquiries:' in line or 'HIGH PRIORITY' in line:
            summary.append(line.strip())
    
    print("\n" + "=" * 60)
    print("Report Summary:")
    print("=" * 60)
    for s in summary:
        print(s)
    print(f"\nFull report: {report_file}")
else:
    print("No report generated.")

print("\nDone!")
