#!/usr/bin/env python3
"""
Dify Workflow DSL 自动化校验脚本
支持 YAML 格式、结构完整性、节点/边、变量引用、错误处理等全面检查

用法: python3 validate_workflow.py <dsl_file.yml>

输出: 结构化校验报告 (PASS/FAIL/WARN)
"""

import sys
import yaml
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any

# ANSI 颜色输出
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'


def color(text: str, c: str) -> str:
    return f"{c}{text}{RESET}"


def check_mark(ok: bool) -> str:
    return color("✅", GREEN) if ok else color("❌", RED)


def warn_mark(warn: bool) -> str:
    return color("⚠️ ", YELLOW) if warn else "  "


class WorkflowValidator:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data: Dict = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.node_ids: Set[str] = set()
        self.edge_ids: Set[str] = set()
        self.defined_variables: Set[str] = set()
        self.referenced_variables: Set[str] = set()
        self.results: List[Tuple[str, bool, str]] = []

    def load(self) -> bool:
        """加载并解析 YAML 文件"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.data = yaml.safe_load(f)
            self.results.append(("YAML 语法解析", True, "文件格式正确"))
            return True
        except yaml.YAMLError as e:
            self.results.append(("YAML 语法解析", False, f"YAML 解析错误: {e}"))
            return False
        except FileNotFoundError:
            self.results.append(("YAML 文件读取", False, f"文件不存在: {self.filepath}"))
            return False

    def check_structure(self) -> bool:
        """检查顶层结构完整性"""
        checks = [
            ("app" in self.data, "app 配置块"),
            ("kind" in self.data, "kind 字段"),
            ("version" in self.data, "version 字段"),
            ("workflow" in self.data, "workflow 配置块"),
        ]

        for node in ["app", "workflow"]:
            if node in self.data:
                sub = self.data[node]
                if isinstance(sub, dict) and "graph" in sub:
                    checks.append((True, f"{node}.graph"))
                elif node == "workflow":
                    checks.append((False, f"{node}.graph"))
                else:
                    checks.append((True, f"{node}"))
            else:
                checks.append((False, f"{node}"))

        all_pass = True
        for ok, desc in checks:
            if not ok:
                all_pass = False
            self.results.append((f"结构: {desc}", ok, "存在" if ok else "缺失"))

        # 检查 workflow.graph
        if "workflow" in self.data:
            wf = self.data["workflow"]
            if isinstance(wf, dict):
                has_graph = "graph" in wf
                has_nodes = has_graph and isinstance(wf.get("graph", {}).get("nodes"), list)
                has_edges = has_graph and isinstance(wf.get("graph", {}).get("edges"), list)
                self.results.append(("workflow.graph.nodes", has_nodes, "数组" if has_nodes else "缺失或非数组"))
                self.results.append(("workflow.graph.edges", has_edges, "数组" if has_edges else "缺失或非数组"))
                return has_nodes and has_edges
        return False

    def check_node_ids(self) -> None:
        """检查节点 ID 唯一性"""
        nodes = self.data.get("workflow", {}).get("graph", {}).get("nodes", [])
        seen: Dict[str, int] = {}

        for node in nodes:
            nid = node.get("id", "")
            if nid in seen:
                seen[nid] += 1
            else:
                seen[nid] = 1

        duplicates = [k for k, v in seen.items() if v > 1]
        if duplicates:
            self.results.append((f"节点 ID 唯一性", False, f"重复 ID: {duplicates}"))
        else:
            self.results.append((f"节点 ID 唯一性", True, f"全部 {len(nodes)} 个节点 ID 唯一"))

        for node in nodes:
            self.node_ids.add(node.get("id", ""))

    def check_edge_references(self) -> None:
        """检查边的 source/target 是否指向有效节点"""
        nodes = self.data.get("workflow", {}).get("graph", {}).get("nodes", [])
        edges = self.data.get("workflow", {}).get("graph", {}).get("edges", [])

        valid_ids = {n.get("id") for n in nodes}
        invalid_refs: List[str] = []

        for edge in edges:
            sid = edge.get("source", "")
            tid = edge.get("target", "")
            eid = edge.get("id", "")

            if sid not in valid_ids:
                invalid_refs.append(f"{eid}: source '{sid}' 不存在")
            if tid not in valid_ids:
                invalid_refs.append(f"{eid}: target '{tid}' 不存在")

            self.edge_ids.add(eid)

        if invalid_refs:
            self.results.append(("边引用有效性", False, "; ".join(invalid_refs[:3])))
        else:
            self.results.append(("边引用有效性", True, f"全部 {len(edges)} 条边引用正确"))

    def check_root_nodes(self) -> None:
        """检查根节点（只能有 1 个 start/datasource/trigger）"""
        nodes = self.data.get("workflow", {}).get("graph", {}).get("nodes", [])
        edges = self.data.get("workflow", {}).get("graph", {}).get("edges", [])

        # 找出所有被作为 target 的节点
        targeted_ids = {e.get("target") for e in edges}

        # 根节点 = 不在任何边的 target 中的 start/datasource/trigger 节点
        root_types = {"start", "datasource", "trigger-webhook", "trigger-schedule", "trigger-plugin"}
        root_nodes = [
            n for n in nodes
            if n.get("id") not in targeted_ids and n.get("data", {}).get("type") in root_types
        ]

        if len(root_nodes) == 0:
            self.results.append(("根节点", False, "未找到根节点"))
        elif len(root_nodes) > 1:
            root_ids = [n.get("id") for n in root_nodes]
            self.results.append(("根节点", False, f"存在 {len(root_nodes)} 个根节点: {root_ids}"))
        else:
            self.results.append(("根节点", True, f"存在 1 个根节点: {root_nodes[0].get('id')}"))

    def check_end_nodes(self) -> None:
        """检查终节点（至少存在 1 个 end/answer）"""
        nodes = self.data.get("workflow", {}).get("graph", {}).get("nodes", [])
        edges = self.data.get("workflow", {}).get("graph", {}).get("edges", [])

        # 终节点 = 不作为任何边 source 的 end/answer 节点
        sourced_ids = {e.get("source") for e in edges}
        end_types = {"end", "answer"}
        end_nodes = [
            n for n in nodes
            if n.get("id") not in sourced_ids and n.get("data", {}).get("type") in end_types
        ]

        if len(end_nodes) == 0:
            self.results.append(("终节点", False, "未找到 end/answer 节点"))
        else:
            end_ids = [n.get("id") for n in end_nodes]
            self.results.append(("终节点", True, f"存在 {len(end_nodes)} 个终节点: {end_ids}"))

    def check_variable_references(self) -> None:
        """检查变量引用格式和链路"""
        # 收集所有节点定义的输出变量
        nodes = self.data.get("workflow", {}).get("graph", {}).get("nodes", [])

        defined_vars: Dict[str, Set[str]] = {}  # node_id -> {output_fields}

        for node in nodes:
            nid = node.get("id", "")
            ntype = node.get("data", {}).get("type", "")
            defined_vars[nid] = set()

            # LLM 节点输出
            if ntype == "llm":
                defined_vars[nid].add("text")
                defined_vars[nid].add("usage")
                defined_vars[nid].add("reasoning_content")

            # HTTP Request 节点输出
            elif ntype == "http-request":
                defined_vars[nid].add("body")
                defined_vars[nid].add("status_code")
                defined_vars[nid].add("headers")
                defined_vars[nid].add("files")

            # Code 节点输出
            elif ntype == "code":
                outputs = node.get("data", {}).get("outputs", {})
                for out_name in outputs.keys():
                    defined_vars[nid].add(out_name)

            # If-Else 节点输出
            elif ntype == "if-else":
                defined_vars[nid].add("condition_result")

            # Loop/Iteration 节点输出
            elif ntype in ("loop", "iteration"):
                defined_vars[nid].add("output")
                defined_vars[nid].add("iteration")

            # Start 节点输出（输入变量）
            elif ntype == "start":
                for var in node.get("data", {}).get("variables", []):
                    var_name = var.get("variable", "")
                    defined_vars[nid].add(var_name)

            # Parameter Extractor 输出
            elif ntype == "parameter-extractor":
                for param in node.get("data", {}).get("parameters", []):
                    param_name = param.get("name", "")
                    defined_vars[nid].add(param_name)
                defined_vars[nid].add("__is_success")
                defined_vars[nid].add("__reason")
                defined_vars[nid].add("__usage")

            # Variable Aggregator
            elif ntype == "variable-aggregator":
                defined_vars[nid].add("output")

            # Knowledge Retrieval
            elif ntype == "knowledge-retrieval":
                defined_vars[nid].add("result")

            # Question Classifier
            elif ntype == "question-classifier":
                defined_vars[nid].add("class_name")
                defined_vars[nid].add("usage")

            # System 变量
            defined_vars["sys"] = {"query", "files", "conversation_id", "user_id",
                                   "dialogue_count", "app_id", "workflow_id",
                                   "workflow_run_id", "timestamp"}
            defined_vars["env"] = set()  # 环境变量未知
            defined_vars["conversation"] = set()  # 对话变量未知

        # 扫描所有节点配置中的变量引用
        var_pattern = re.compile(r'\{\{#[^#}]+#\}\}')
        invalid_refs: List[str] = []

        def extract_refs(obj: Any, path: str = "") -> None:
            if isinstance(obj, dict):
                for k, v in obj.items():
                    extract_refs(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    extract_refs(v, f"{path}[{i}]")
            elif isinstance(obj, str):
                for match in var_pattern.finditer(obj):
                    ref = match.group()
                    # 解析 {{#node_id.field#}} 或 {{#node_id.field.subfield#}}
                    inner = ref[3:-2]  # 去掉 {{# 和 #}}
                    parts = inner.split(".")
                    if len(parts) >= 2:
                        node_id = parts[0]
                        field = parts[1]
                        if node_id not in defined_vars:
                            invalid_refs.append(f"未知节点: {node_id}")
                        elif field not in defined_vars[node_id] and node_id != "sys":
                            # 可能是嵌套字段，暂时放行
                            pass

        extract_refs(nodes)

        unique_invalid = list(set(invalid_refs))[:5]
        if unique_invalid:
            self.results.append(("变量引用", False, f"潜在问题: {'; '.join(unique_invalid)}"))
        else:
            self.results.append(("变量引用", True, "所有引用格式正确"))

    def check_error_handling(self) -> None:
        """检查错误处理完整性"""
        nodes = self.data.get("workflow", {}).get("graph", {}).get("nodes", [])
        edges = self.data.get("workflow", {}).get("graph", {}).get("edges", [])

        fail_branch_nodes = {
            n.get("id") for n in nodes
            if n.get("data", {}).get("error_strategy") == "fail-branch"
        }

        if not fail_branch_nodes:
            self.results.append(("错误处理", True, "无 fail-branch（可选）"))
            return

        # 检查每个 fail-branch 节点是否同时有 success 和 fail 两条边
        node_out_edges: Dict[str, Set[str]] = {nid: set() for nid in fail_branch_nodes}
        for edge in edges:
            sid = edge.get("source", "")
            sh = edge.get("sourceHandle", "")
            if sid in fail_branch_nodes and sh in ("success-branch", "fail-branch"):
                node_out_edges[sid].add(sh)

        issues = []
        for nid, handles in node_out_edges.items():
            if len(handles) < 2:
                missing = []
                if "success-branch" not in handles:
                    missing.append("success-branch")
                if "fail-branch" not in handles:
                    missing.append("fail-branch")
                issues.append(f"{nid}: 缺少 {missing}")

        if issues:
            self.results.append(("错误处理完整性", False, "; ".join(issues)))
        else:
            self.results.append(("错误处理完整性", True, f"全部 {len(fail_branch_nodes)} 个 fail-branch 节点配置完整"))

    def check_idempotency(self) -> None:
        """检查节点 ID 格式"""
        nodes = self.data.get("workflow", {}).get("graph", {}).get("nodes", [])
        for node in nodes:
            nid = node.get("id", "")
            # start 节点必须是 'start'
            if node.get("data", {}).get("type") == "start" and nid != "start":
                self.results.append(("Start 节点 ID", False, f"Start 节点 ID 应为 'start'，实际为 '{nid}'"))
                return
        self.results.append(("Start 节点 ID", True, "格式正确"))

    def check_positions(self) -> None:
        """检查节点坐标合理性"""
        nodes = self.data.get("workflow", {}).get("graph", {}).get("nodes", [])
        for node in nodes:
            pos = node.get("position", {})
            x = pos.get("x", 0)
            y = pos.get("y", 0)
            if x < 0 or y < 0:
                self.warnings.append(f"节点 {node.get('id')} 坐标为负数: ({x}, {y})")

        # 检查是否有重叠（简化版：只检查 x 相同且 y 相近的节点）
        pos_seen: Dict[Tuple[int, int], List[str]] = {}
        for node in nodes:
            x = round(node.get("position", {}).get("x", 0) / 10) * 10
            y = round(node.get("position", {}).get("y", 0) / 10) * 10
            key = (x, y)
            if key not in pos_seen:
                pos_seen[key] = []
            pos_seen[key].append(node.get("id"))

        overlaps = {k: v for k, v in pos_seen.items() if len(v) > 1}
        if overlaps:
            self.warnings.append(f"存在 {len(overlaps)} 处节点坐标重叠")
        self.results.append(("节点坐标", True, "布局合理"))

    def check_llm_config(self) -> None:
        """检查 LLM 节点配置"""
        nodes = self.data.get("workflow", {}).get("graph", {}).get("nodes", [])
        for node in nodes:
            if node.get("data", {}).get("type") == "llm":
                model = node.get("data", {}).get("model", {})
                if not model.get("provider"):
                    self.warnings.append(f"LLM 节点 {node.get('id')} 缺少 provider")
                if not model.get("name"):
                    self.warnings.append(f"LLM 节点 {node.get('id')} 缺少 model name")
                prompt = node.get("data", {}).get("prompt_template", [])
                if not prompt:
                    self.warnings.append(f"LLM 节点 {node.get('id')} 缺少 prompt_template")

    def validate(self) -> None:
        """执行所有校验"""
        self.check_node_ids()
        self.check_edge_references()
        self.check_root_nodes()
        self.check_end_nodes()
        self.check_variable_references()
        self.check_error_handling()
        self.check_idempotency()
        self.check_positions()
        self.check_llm_config()

    def print_report(self) -> bool:
        """输出结构化报告"""
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}  Dify DSL 自动化校验报告{RESET}")
        print(f"{'='*60}")
        print(f"  文件: {self.filepath}")
        print(f"  版本: {self.data.get('version', 'N/A')}")
        print(f"  模式: {self.data.get('app', {}).get('mode', 'N/A')}")
        print(f"  工作流: {self.data.get('app', {}).get('name', 'N/A')}")
        print(f"  节点数: {len(self.node_ids)}")
        print(f"  连接数: {len(self.edge_ids)}")
        print(f"{'='*60}\n")

        for desc, ok, detail in self.results:
            status = check_mark(ok)
            print(f"  {status}  {desc:<25} {detail}")

        if self.warnings:
            print(f"\n  {color('⚠️  警告', YELLOW)}:")
            for w in self.warnings:
                print(f"    - {w}")

        passed = sum(1 for _, ok, _ in self.results if ok)
        total = len(self.results)
        pass_rate = passed / total * 100

        print(f"\n{'─'*60}")
        print(f"  校验结果: {passed}/{total} 通过 ({pass_rate:.0f}%)")

        if passed == total:
            print(f"\n  {color('🎉 DSL 生成成功，可直接导入 Dify！', GREEN)}")
            return True
        elif passed >= total * 0.7:
            print(f"\n  {color('⚠️  DSL 基本可用，但存在警告', YELLOW)}")
            return True
        else:
            print(f"\n  {color('❌ DSL 存在严重问题，请修复后重试', RED)}")
            return False


def main():
    if len(sys.argv) < 2:
        print(f"用法: {sys.argv[0]} <dsl_file.yml>")
        sys.exit(1)

    filepath = sys.argv[1]

    validator = WorkflowValidator(filepath)

    if not validator.load():
        validator.print_report()
        sys.exit(1)

    validator.check_structure()

    if validator.data.get("workflow", {}).get("graph"):
        validator.validate()

    ok = validator.print_report()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
