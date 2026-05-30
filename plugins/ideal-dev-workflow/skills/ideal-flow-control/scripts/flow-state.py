#!/usr/bin/env python3
"""
流程状态管理脚本
用于 ideal-flow-control skill
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class FlowState:
    """流程状态管理类"""

    STATUS_PENDING = "pending"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_BLOCKED = "blocked"
    STATUS_REVISION = "revision"

    STATUS_ICONS = {
        STATUS_PENDING: "⏳",
        STATUS_IN_PROGRESS: "🔄",
        STATUS_COMPLETED: "✅",
        STATUS_BLOCKED: "❌",
        STATUS_REVISION: "🔙"
    }

    PHASES = {
        "P1": "需求编写",
        "P2": "需求评审",
        "P3": "技术方案",
        "P4": "方案评审",
        "P5": "计划生成",
        "P6": "计划评审",
        "P7": "测试用例",
        "P8": "用例评审",
        "P9": "开发执行",
        "P10": "代码评审",
        "P11": "测试执行",
        "P12": "测试评审",
        "P13": "维基更新",
        "P14": "维基评审",
        "P15": "成果提交"
    }

    PREREQUISITES = {
        "P3": "P2",
        "P5": "P4",
        "P7": "P6",
        "P9": "P8",
        "P11": "P10",
        "P13": "P12",
        "P15": "P14"
    }

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.frontmatter: Dict = {}
        self.content: str = ""
        self.phases: Dict[str, Dict[str, str]] = {}
        self._parse()

    def _parse(self):
        """解析流程状态文件"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"流程状态文件不存在: {self.file_path}")

        raw = self.file_path.read_text(encoding="utf-8")

        # 解析 YAML frontmatter
        if raw.startswith("---"):
            parts = raw.split("---", 2)
            if len(parts) >= 3:
                yaml_str = parts[1].strip()
                self.content = parts[2].strip()

                if HAS_YAML:
                    parsed = yaml.safe_load(yaml_str)
                    if isinstance(parsed, dict):
                        self.frontmatter = self._normalize_frontmatter(parsed)
                else:
                    self.frontmatter = self._parse_flat_yaml(yaml_str)

        # 解析阶段状态
        phase_pattern = r"\| (P\d+) ([一-龥]+) \| (.+) \| (.+) \|"
        for match in re.finditer(phase_pattern, self.content):
            phase = match.group(1)
            status_text = match.group(3).strip()
            self.phases[phase] = {
                "status": self._parse_status(status_text),
                "updated_at": match.group(4).strip()
            }

    def _normalize_frontmatter(self, parsed: dict) -> dict:
        """确保所有值都是字符串，兼容旧的 flat key: value 接口"""
        result = {}
        for k, v in parsed.items():
            if v is None:
                result[k] = ""
            elif isinstance(v, (dict, list)):
                result[k] = v  # 保留嵌套结构
            else:
                result[k] = str(v)
        return result

    def _parse_flat_yaml(self, yaml_str: str) -> Dict[str, str]:
        """降级扁平解析（无 PyYAML 时）"""
        result = {}
        for line in yaml_str.split("\n"):
            line = line.strip()
            if ":" in line and not line.startswith("#"):
                key, value = line.split(":", 1)
                result[key.strip()] = value.strip()
        return result

    def _parse_status(self, status_text: str) -> str:
        """解析状态文本"""
        if "✅" in status_text or "completed" in status_text:
            return self.STATUS_COMPLETED
        elif "🔄" in status_text or "in_progress" in status_text:
            return self.STATUS_IN_PROGRESS
        elif "❌" in status_text or "blocked" in status_text:
            return self.STATUS_BLOCKED
        elif "🔙" in status_text or "revision" in status_text:
            return self.STATUS_REVISION
        else:
            return self.STATUS_PENDING

    def get_current_phase(self) -> str:
        """获取当前阶段"""
        val = self.frontmatter.get("current_phase", "P1")
        return str(val) if not isinstance(val, (dict, list)) else "P1"

    def get_status(self) -> str:
        """获取当前状态"""
        val = self.frontmatter.get("status", self.STATUS_PENDING)
        return str(val) if not isinstance(val, (dict, list)) else self.STATUS_PENDING

    def get_phase_status(self, phase: str) -> Optional[str]:
        """获取指定阶段的状态"""
        if phase in self.phases:
            return self.phases[phase]["status"]
        return None

    def check_prerequisite(self, phase: str) -> bool:
        """检查前置条件"""
        if phase not in self.PREREQUISITES:
            return True

        prerequisite = self.PREREQUISITES[phase]
        status = self.get_phase_status(prerequisite)
        return status == self.STATUS_COMPLETED

    def update_phase(self, phase: str, status: str) -> bool:
        """更新阶段状态"""
        if phase not in self.PHASES:
            print(f"错误: 无效的阶段 {phase}")
            return False

        today = datetime.now().strftime("%Y-%m-%d")
        self.frontmatter["current_phase"] = phase
        self.frontmatter["status"] = status
        self.frontmatter["updated_at"] = today

        self.phases[phase] = {
            "status": status,
            "updated_at": today
        }

        self._generate_content()
        return True

    def _generate_content(self):
        """生成文件内容"""
        current_phase = self.get_current_phase()
        current_status = self.get_status()
        status_icon = self.STATUS_ICONS.get(current_status, "⏳")
        status_text = {
            self.STATUS_PENDING: "待执行",
            self.STATUS_IN_PROGRESS: "进行中",
            self.STATUS_COMPLETED: "已完成",
            self.STATUS_BLOCKED: "已阻塞",
            self.STATUS_REVISION: "需要修改"
        }.get(current_status, "待执行")

        # 生成 YAML frontmatter — 保留嵌套结构
        if HAS_YAML:
            flat = {}
            for k, v in self.frontmatter.items():
                if isinstance(v, (dict, list)):
                    flat[k] = v
                else:
                    flat[k] = str(v)
            yaml_content = yaml.dump(flat, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
        else:
            yaml_content = "\n".join([f"{k}: {v}" for k, v in self.frontmatter.items()])

        # 生成阶段状态表
        def generate_section(start: int, end: int) -> str:
            rows = []
            for i in range(start, end + 1):
                phase = f"P{i}"
                name = self.PHASES[phase]
                info = self.phases.get(phase, {"status": self.STATUS_PENDING, "updated_at": "-"})
                icon = self.STATUS_ICONS.get(info["status"], "⏳")
                status_str = f"{icon} {info['status']}"
                rows.append(f"| {phase} {name} | {status_str} | {info['updated_at']} |")
            return "\n".join(rows)

        content = f"""---
{yaml_content}
---

# 流程状态

## 当前阶段

**{current_phase} - {self.PHASES[current_phase]}** {status_icon} {status_text}

## 阶段状态

### 规划阶段
| 阶段 | 状态 | 更新时间 |
|------|------|----------|
{generate_section(1, 4)}

### 准备阶段
| 阶段 | 状态 | 更新时间 |
|------|------|----------|
{generate_section(5, 8)}

### 执行阶段
| 阶段 | 状态 | 更新时间 |
|------|------|----------|
{generate_section(9, 12)}

### 收尾阶段
| 阶段 | 状态 | 更新时间 |
|------|------|----------|
{generate_section(13, 15)}

---

## 状态说明

- ⏳ pending: 待执行
- 🔄 in_progress: 进行中
- ✅ completed: 已完成
- ❌ blocked: 已阻塞
- 🔙 revision: 需要修改

## 触发下一阶段

{self._get_trigger_message()}
"""

        self._content = content

    def _get_trigger_message(self) -> str:
        """获取触发消息"""
        current = self.get_current_phase()
        next_phase = f"P{int(current[1:]) + 1}" if current != "P15" else None

        if next_phase and next_phase in self.PHASES:
            return f"当前阶段: {current} - {self.PHASES[current]}\n\n将 `{next_phase} {self.PHASES[next_phase]}` 状态改为 `completed` 后，将触发下一阶段。"
        else:
            return "流程已完成。"

    def save(self):
        """保存文件"""
        self.file_path.write_text(self._content, encoding="utf-8")
        print(f"已更新流程状态: {self.file_path}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: flow-state.py <命令> [参数]")
        print("")
        print("命令:")
        print("  get-phase <file>              获取当前阶段")
        print("  get-status <file> <phase>     获取指定阶段状态")
        print("  check-prereq <file> <phase>   检查前置条件")
        print("  update <file> <phase> <status> 更新阶段状态")
        print("")
        print("示例:")
        print("  flow-state.py get-phase docs/迭代/用户登录/流程状态.md")
        print("  flow-state.py get-status docs/迭代/用户登录/流程状态.md P2")
        print("  flow-state.py check-prereq docs/迭代/用户登录/流程状态.md P3")
        print("  flow-state.py update docs/迭代/用户登录/流程状态.md P2 completed")
        sys.exit(1)

    command = sys.argv[1]

    if command == "get-phase":
        if len(sys.argv) < 3:
            print("错误: 请提供流程状态文件路径")
            sys.exit(1)
        state = FlowState(sys.argv[2])
        print(f"当前阶段: {state.get_current_phase()} - {FlowState.PHASES.get(state.get_current_phase(), '')}")

    elif command == "get-status":
        if len(sys.argv) < 4:
            print("错误: 请提供流程状态文件路径和阶段")
            sys.exit(1)
        state = FlowState(sys.argv[2])
        phase = sys.argv[3]
        status = state.get_phase_status(phase)
        print(f"{phase} 状态: {status or '未找到'}")

    elif command == "check-prereq":
        if len(sys.argv) < 4:
            print("错误: 请提供流程状态文件路径和阶段")
            sys.exit(1)
        state = FlowState(sys.argv[2])
        phase = sys.argv[3]
        if state.check_prerequisite(phase):
            print(f"✅ {phase} 前置条件满足")
        else:
            prereq = FlowState.PREREQUISITES.get(phase, "无")
            print(f"❌ {phase} 前置条件不满足: {prereq} 未完成")

    elif command == "update":
        if len(sys.argv) < 5:
            print("错误: 请提供流程状态文件路径、阶段和状态")
            sys.exit(1)
        state = FlowState(sys.argv[2])
        phase = sys.argv[3]
        status = sys.argv[4]

        if status not in FlowState.STATUS_ICONS:
            print(f"错误: 无效的状态 '{status}'")
            print(f"有效状态: {', '.join(FlowState.STATUS_ICONS.keys())}")
            sys.exit(1)

        if state.update_phase(phase, status):
            state.save()

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()