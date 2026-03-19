#!/usr/bin/env python3
"""
Dify DSL API 导入脚本
直接通过 Dify Console API 导入 DSL 文件，避免浏览器自动化。

用法:
    python3 dify_import.py <dsl_file.yml> [--dify-url http://localhost:8080]

前提条件:
    1. Dify 运行中
    2. 导出浏览器 cookies 到 /tmp/dify_cookies.json（browser-use: bu state save /tmp/dify_cookies.json）
    3. cookies 中包含 localhost 的 access_token 和 csrf_token

Dify API 信息:
    - 导入端点: POST /console/api/apps/imports
    - 必须用 mode: yaml-content（不是 overwrite）
    - payload: {"mode": "yaml-content", "yaml_content": "<full YAML>"}
    - 返回: {"id": "...", "status": "completed", "app_id": "..."}
"""
import json
import sys
import base64
import hashlib
import argparse
import requests


def get_auth_headers():
    """从导出的 cookies 中提取认证头"""
    with open("/tmp/dify_cookies.json") as f:
        all_cookies = json.load(f)

    local_cookies = [c for c in all_cookies if c.get("domain") == "localhost"]
    cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in local_cookies)
    access_token = next(
        (c["value"] for c in local_cookies if c["name"] == "access_token"), None
    )
    csrf_token = next(
        (c["value"] for c in local_cookies if c["name"] == "csrf_token"), None
    )

    if not access_token:
        raise ValueError("未找到 access_token，请重新导出 cookies")

    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Cookie": cookie_str,
        "X-CSRF-Token": csrf_token or "",
        "Origin": "http://localhost:8080",
        "Referer": "http://localhost:8080/apps",
    }


def import_dsl(dsl_path: str, dify_url: str = "http://localhost:8080") -> dict:
    """通过 API 导入 DSL 文件"""
    with open(dsl_path, encoding="utf-8") as f:
        yaml_content = f.read()

    headers = get_auth_headers()
    url = f"{dify_url}/console/api/apps/imports"
    payload = {"mode": "yaml-content", "yaml_content": yaml_content}

    print(f"导入 DSL: {dsl_path} ({len(yaml_content)} bytes)")
    print(f"目标: {url}")

    r = requests.post(url, headers=headers, json=payload, timeout=60)
    result = r.json()

    print(f"状态: {r.status_code}")
    print(f"结果: {json.dumps(result, indent=2, ensure_ascii=False)}")

    if r.status_code == 200:
        app_id = result.get("app_id", "")
        status = result.get("status", "")
        print(f"\n✅ 导入成功!")
        print(f"   应用 ID: {app_id}")
        print(f"   状态: {status}")
        if app_id:
            print(f"   编辑地址: {dify_url}/app/{app_id}/workflow")
        return result
    else:
        error = result.get("error", result.get("message", "未知错误"))
        print(f"\n❌ 导入失败: {error}")
        return result


def main():
    parser = argparse.ArgumentParser(description="通过 Dify Console API 导入 DSL 文件")
    parser.add_argument("dsl_file", help="DSL YAML 文件路径")
    parser.add_argument(
        "--dify-url",
        default="http://localhost:8080",
        help="Dify 服务地址（默认: http://localhost:8080）",
    )
    args = parser.parse_args()

    try:
        result = import_dsl(args.dsl_file, args.dify_url)
        if result.get("status") in ("completed", "completed-with-warnings"):
            sys.exit(0)
        else:
            sys.exit(1)
    except FileNotFoundError:
        print(f"❌ 文件不存在: {args.dsl_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
