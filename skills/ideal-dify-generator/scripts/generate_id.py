#!/usr/bin/env python3
"""
Dify Workflow 节点 ID 生成器
生成唯一的节点 ID（基于时间戳）

用法: python3 generate_id.py [数量]
默认生成 1 个
"""

import time
import sys

def generate_id():
    """生成一个基于时间戳的节点 ID"""
    return str(int(time.time() * 1000))

def generate_ids(count):
    """生成指定数量的唯一节点 ID"""
    ids = []
    base = int(time.time() * 1000)
    for i in range(count):
        # 同一毫秒内用微秒偏移确保唯一
        ids.append(str(base + i))
    return ids

def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    if count == 1:
        nid = generate_id()
        print(nid)
    else:
        ids = generate_ids(count)
        for nid in ids:
            print(nid)

if __name__ == "__main__":
    main()
