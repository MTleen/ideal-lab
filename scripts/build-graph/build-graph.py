#!/usr/bin/env python3
"""Build skills-graph.json by scanning all SKILL.md files."""

import json
import os
import re
import yaml
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PLUGINS_DIR = REPO_ROOT / "plugins"

# ── YAML frontmatter parser ──────────────────────────────────────────────

def parse_frontmatter(text):
    """Extract YAML frontmatter from SKILL.md text."""
    match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}

# ── ARITY CLASSIFICATION ─────────────────────────────────────────────────

ORCHESTRATOR_KEYWORDS = [
    '编排', 'orchestrat', 'workflow.*协调', '流程编排', '阶段流转',
    '流水线编排', '工作流编排', '编排器', 'Orchestrator'
]

PHASE_KEYWORDS = [
    r'P\d{1,2}', '阶段', 'phase', 'Phase Skill'
]

UTILITY_KEYWORDS = [
    '工具', 'generator', '生成器', 'builder', '配图', '插图',
    '渲染', 'render', 'convert', '转换', '脚本'
]

def classify_arity(name, description):
    """Classify skill arity based on name and description."""
    text = f"{name} {description}".lower()

    for kw in ORCHESTRATOR_KEYWORDS:
        if re.search(kw, text):
            return 'orchestrator'

    for kw in PHASE_KEYWORDS:
        if re.search(kw, text):
            return 'phase'

    for kw in UTILITY_KEYWORDS:
        if re.search(kw, text):
            return 'utility'

    return 'standalone'

# ── NODE EXTRACTION ──────────────────────────────────────────────────────

def extract_nodes():
    """Walk plugins/ and extract node data from each SKILL.md."""
    nodes = []
    marketplace = load_marketplace()

    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        if not plugin_dir.is_dir():
            continue
        plugin_name = plugin_dir.name

        # Get category from marketplace
        category = 'unknown'
        for p in marketplace.get('plugins', []):
            if p.get('name') == plugin_name:
                category = p.get('category', 'unknown')
                break

        skills_dir = plugin_dir / 'skills'
        if not skills_dir.exists():
            continue

        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / 'SKILL.md'
            if not skill_md.exists():
                continue

            content = skill_md.read_text(encoding='utf-8')
            fm = parse_frontmatter(content)
            skill_name = fm.get('name', skill_dir.name)
            description = fm.get('description', '')

            node_id = f"{plugin_name}/{skill_name}"

            nodes.append({
                'id': node_id,
                'name': skill_name,
                'plugin': plugin_name,
                'category': category,
                'arity': classify_arity(skill_name, description),
                'description': description[:200] if description else '',
            })

    return nodes

def load_marketplace():
    """Load marketplace.json."""
    mp = REPO_ROOT / '.claude-plugin' / 'marketplace.json'
    if mp.exists():
        return json.loads(mp.read_text(encoding='utf-8'))
    return {}

# ── EDGE INFERENCE ───────────────────────────────────────────────────────

def infer_edges(nodes):
    """Infer typed edges between skills."""
    edges = []
    node_ids = {n['id'] for n in nodes}
    node_map = {n['id']: n for n in nodes}

    # ── EMBEDS: orchestrator mentions phase skill names ────────────────
    for node in nodes:
        if node['arity'] != 'orchestrator':
            continue
        orchestrator_id = node['id']
        orchestrator_name = node['name']
        skill_md = read_skill_md(node)
        if not skill_md:
            continue
        body = skill_md.lower()

        # Find phase skills in same plugin mentioned by name
        plugin_skills = [n for n in nodes
                         if n['plugin'] == node['plugin'] and n['id'] != orchestrator_id]
        for target in plugin_skills:
            if target['name'].lower() in body:
                edges.append({
                    'source': orchestrator_id,
                    'target': target['id'],
                    'relation': 'calls',
                    'confidence': 'extracted',
                    'evidence': f"{orchestrator_name} mentions {target['name']}"
                })

    # ── PREREQUISITE: intra-plugin phase ordering ──────────────────────
    for plugin_name in set(n['plugin'] for n in nodes):
        plugin_nodes = [n for n in nodes if n['plugin'] == plugin_name and n['arity'] == 'phase']
        plugin_nodes.sort(key=lambda n: n['name'])

        # Look for phase number patterns (P1→P3, P3→P5, etc.)
        phase_map = {}
        for n in plugin_nodes:
            skill_md = read_skill_md(n)
            if not skill_md:
                continue
            # Extract phase number from description or body
            p_match = re.search(r'P(\d+)', skill_md)
            if p_match:
                p_num = int(p_match.group(1))
                if p_num not in phase_map:
                    phase_map[p_num] = []
                phase_map[p_num].append(n['id'])

        # Sort phases and create prerequisite edges P(N)→P(N+2) (product-to-product)
        sorted_phases = sorted(phase_map.keys())
        for i in range(len(sorted_phases) - 1):
            for src in phase_map[sorted_phases[i]]:
                for tgt in phase_map[sorted_phases[i + 1]]:
                    edges.append({
                        'source': src,
                        'target': tgt,
                        'relation': 'prerequisite',
                        'confidence': 'extracted',
                        'evidence': f"P{sorted_phases[i]} → P{sorted_phases[i+1]} phase ordering"
                    })

    # ── ENHANCEMENT: cross-cutting skills ──────────────────────────────
    # panel-review enhances all skills that produce reviewable artifacts
    for node in nodes:
        if node['name'] == 'panel-review':
            for target in nodes:
                if target['id'] == node['id']:
                    continue
                if target['arity'] in ('phase', 'standalone'):
                    edges.append({
                        'source': node['id'],
                        'target': target['id'],
                        'relation': 'enhancement',
                        'confidence': 'extracted',
                        'evidence': 'panel-review reviews documents/code/solutions/PPTs'
                    })
            break

    # deep-research enhances analysis skills
    for node in nodes:
        if 'research' in node['name'].lower() or 'deep-research' in node['name'].lower():
            for target in nodes:
                if target['id'] == node['id']:
                    continue
                target_md = read_skill_md(target)
                if not target_md:
                    continue
                if any(kw in target_md.lower() for kw in ['research', '调研', '分析', 'solution', '方案']):
                    edges.append({
                        'source': node['id'],
                        'target': target['id'],
                        'relation': 'enhancement',
                        'confidence': 'extracted',
                        'evidence': f"{node['name']} provides research for analysis skills"
                    })

    # skill-builder enhances any skill-producing skill
    for node in nodes:
        if node['name'] == 'skill-builder':
            for target in nodes:
                if target['id'] == node['id']:
                    continue
                if target['arity'] == 'standalone':
                    edges.append({
                        'source': node['id'],
                        'target': target['id'],
                        'relation': 'enhancement',
                        'confidence': 'extracted',
                        'evidence': 'skill-builder optimizes any SKILL.md'
                    })
            break

    # baoyu-image-gen enhances ppt-image and illustration skills
    for node in nodes:
        if node['name'] == 'baoyu-image-gen':
            for target in nodes:
                if target['id'] == node['id']:
                    continue
                target_name = target['name'].lower()
                if any(kw in target_name for kw in ['image', 'illustration', '配图', 'ppt']):
                    edges.append({
                        'source': node['id'],
                        'target': target['id'],
                        'relation': 'enhancement',
                        'confidence': 'extracted',
                        'evidence': 'baoyu-image-gen provides images for illustration/PPT skills'
                    })
            break

    # ── ALTERNATIVE: duplicated skills ─────────────────────────────────
    # deep-research in both ideal-dev-workflow and ideal-deep-research
    research_nodes = [n for n in nodes if 'deep-research' in n['name'].lower()]
    for i in range(len(research_nodes)):
        for j in range(i + 1, len(research_nodes)):
            if research_nodes[i]['plugin'] != research_nodes[j]['plugin']:
                edges.append({
                    'source': research_nodes[i]['id'],
                    'target': research_nodes[j]['id'],
                    'relation': 'alternative',
                    'confidence': 'explicit',
                    'evidence': f"Duplicated deep-research skill across plugins"
                })

    # ── PRODUCES_FOR: utility → consumer ───────────────────────────────
    utility_consumer_map = {
        'illustration': 'document-writing',
        'document-render': 'ideal-document-workflow',
        'image-to-svg': 'ideal-ppt-image',
        'writing-skills': 'skill-builder',
    }

    for node in nodes:
        node_name = node['name']
        if node_name in utility_consumer_map:
            consumer_name = utility_consumer_map[node_name]
            for target in nodes:
                if target['name'] == consumer_name or target['name'] in consumer_name:
                    edges.append({
                        'source': node['id'],
                        'target': target['id'],
                        'relation': 'produces_for',
                        'confidence': 'extracted',
                        'evidence': f"{node_name} produces output consumed by {consumer_name}"
                    })

    # ── DEDUP ───────────────────────────────────────────────────────────
    seen = set()
    unique_edges = []
    for e in edges:
        key = (e['source'], e['target'], e['relation'])
        if key not in seen:
            seen.add(key)
            unique_edges.append(e)

    return unique_edges

def read_skill_md(node):
    """Read the full SKILL.md text for a node."""
    parts = node['id'].split('/', 1)
    if len(parts) != 2:
        return None
    plugin, skill_name = parts
    skill_path = PLUGINS_DIR / plugin / 'skills'
    for d in skill_path.iterdir() if skill_path.exists() else []:
        if d.is_dir():
            sm = d / 'SKILL.md'
            if sm.exists():
                fm = parse_frontmatter(sm.read_text(encoding='utf-8'))
                if fm.get('name') == node['name']:
                    return sm.read_text(encoding='utf-8')
    return None

# ── MAIN ─────────────────────────────────────────────────────────────────

def main():
    nodes = extract_nodes()
    edges = infer_edges(nodes)

    # Stats
    arity_counts = {}
    for n in nodes:
        arity_counts[n['arity']] = arity_counts.get(n['arity'], 0) + 1

    relation_counts = {}
    for e in edges:
        relation_counts[e['relation']] = relation_counts.get(e['relation'], 0) + 1

    # Find orphan skills (no edges)
    connected = set()
    for e in edges:
        connected.add(e['source'])
        connected.add(e['target'])
    orphans = [n['id'] for n in nodes if n['id'] not in connected]

    graph = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_skills': len(nodes),
            'total_edges': len(edges),
            'arity_distribution': arity_counts,
            'relation_distribution': relation_counts,
            'orphan_skills': orphans,
        },
        'nodes': nodes,
        'edges': edges,
    }

    output_path = REPO_ROOT / 'skills-graph.json'
    output_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✓ Wrote {len(nodes)} nodes, {len(edges)} edges to {output_path}")
    print(f"  Arity: {arity_counts}")
    print(f"  Relations: {relation_counts}")
    if orphans:
        print(f"  Orphans ({len(orphans)}): {orphans[:5]}...")

if __name__ == '__main__':
    main()