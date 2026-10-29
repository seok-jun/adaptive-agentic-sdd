"""Static byte/token proxies, no model calls, no runtime instrumentation.

Run: python -I -B tests/measure_sdd_reading.py
Requires the recorded base commit in this checkout. UTF-8 bytes/4 is the existing
workflow's token_proxy convention, NOT a Korean/model tokenizer estimate.
"""
import json
import math
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'ko/adaptive-sdd/workflow/'
MAPPING = json.loads((ROOT / 'tests/fixtures/sdd-section-map.json').read_text(encoding='utf-8'))
BASE = MAPPING['base']
ENTRY = ['sdd/grade.md', 'sdd/entry.md', 'sdd/issue.md']
# Cold phase snapshots, with the skill's mandatory inputs included.
SCENARIOS = {
    'Small implementation': (ENTRY, [], 'implementing-issues'),
    'Medium design and implementation': (ENTRY + ['sdd-artifacts.md', 'sdd/as-is.md', 'sdd/to-be.md', 'sdd/agent-spec.md'], [], 'implementing-issues'),
    'Large AS-IS review': (ENTRY + ['sdd-artifacts.md', 'sdd/as-is.md'], ['design-review.md'], 'implementing-issues'),
    'Large PLAN review': (ENTRY + ['sdd/to-be.md', 'sdd/agent-spec.md'], ['design-review.md'], 'implementing-issues'),
    'Implementation and verification': (ENTRY + ['sdd/agent-spec.md'], [], 'implementing-issues'),
    'Completion and handoff': (['sdd/completion.md', 'sdd/issue.md'], [], 'finishing-issues'),
    'Epic management': (['sdd/grade.md', 'sdd/epic.md', 'sdd/issue.md'], [], 'managing-issues'),
}


def read(path, before=False):
    if before:
        return subprocess.check_output(['git', 'show', f'{BASE}:{PREFIX}{path}'], cwd=ROOT).decode('utf-8')
    return (ROOT / PREFIX / path).read_text(encoding='utf-8')


def metrics(text):
    size = len(text.encode('utf-8'))
    return {'bytes': size, 'token_proxy': math.ceil(size / 4)}


def measure():
    # Cold phase snapshots. Conditional runtime sources (P, code, decisions,
    # routing, packets, observations) are excluded from BOTH sides, never waived.
    old_workflow = read('process/sdd-workflow.md', True)
    old_sections = {s.splitlines()[0][3:]: s for s in re.split(r'(?=^## )', old_workflow, flags=re.M)[1:]}
    results = {}
    for name, (selected, common, skill) in SCENARIOS.items():
        after_paths = ['process/' + p for p in selected + common]
        before_paths = ['process/sdd-workflow.md']
        if any(p in selected for p in ('sdd-artifacts.md', 'sdd/as-is.md', 'sdd/to-be.md', 'sdd/agent-spec.md')):
            before_paths.append('process/sdd-artifacts.md')
        before_paths += ['process/' + p for p in common]
        shared = [f'skills/{skill}/SKILL.md']
        if name != 'Epic management':
            shared.append('process/verification.md')
        before_paths += shared
        after_paths += shared
        before = '\n'.join(read(p, True) for p in before_paths)
        after = '\n'.join(read(p) for p in after_paths)
        # Ideal baseline: only relevant ORIGINAL workflow sections (not a claim
        # that the host can address all sections in one call). Other docs full.
        heads = [h for p in selected if p.startswith('sdd/') and p[4:-3] in MAPPING['workflow']
                 for h in MAPPING['workflow'][p[4:-3]]]
        ideal = '\n'.join(old_sections[h] for h in heads)
        ideal += '\n' + '\n'.join(read(p, True) for p in before_paths if p != 'process/sdd-workflow.md')
        results[name] = {
            'before_full': metrics(before), 'before_workflow_sections': metrics(ideal), 'after_selected': metrics(after),
            'reduction_percent_vs_full': round(100 * (1 - len(after.encode()) / len(before.encode())), 1),
            'file_reads_before_after': [len(before_paths), len(after_paths)],
            'discovery_calls_before_after': [0, 0],
            'before_paths': before_paths, 'after_paths': after_paths,
        }
    # Repeated cold reads across a Large lifecycle vs one read per unchanged
    # path in a retained context. This is a workload model, not a host trace.
    lifecycle = ['Large AS-IS review', 'Large PLAN review', 'Implementation and verification', 'Completion and handoff']
    repeated = {}
    for side in ('before', 'after'):
        paths = [p for c in lifecycle for p in results[c][side + '_paths']]
        cold = sum(len(read(p, side == 'before').encode()) for p in paths)
        unique = sum(len(read(p, side == 'before').encode()) for p in set(paths))
        repeated[side] = {'cold_bytes': cold, 'unique_bytes': unique, 'repeated_bytes': cold - unique,
                          'cold_file_reads': len(paths), 'unique_file_reads': len(set(paths))}
    sizes = {}
    for path in ['process/sdd-workflow.md', 'process/sdd-artifacts.md']:
        sizes[path] = {'before': metrics(read(path, True)), 'after': metrics(read(path))}
    sizes['new_rule_files_total'] = metrics('\n'.join(p.read_text(encoding='utf-8') for p in sorted((ROOT / PREFIX / 'process/sdd').glob('*.md'))))
    sample = json.loads((ROOT / 'tests/fixtures/sdd-artifact-sample.json').read_text(encoding='utf-8'))
    artifact_sample = {}
    for side in ('before', 'after'):
        docs = sample[side]
        human_paths = ['01-as-is.md', '02-to-be.md'] if side == 'before' else ['README.md', '02-to-be.md']
        artifact_sample[side] = {
            'files': {p: metrics(t) for p, t in docs.items()},
            'total_written_text': metrics(''.join(docs.values())),
            'human_default_read': metrics(''.join(docs[p] for p in human_paths)),
            'agent_as_is_evidence_read': metrics(docs['01-as-is.md']),
            # A human-oriented file can still contain mandatory agent inputs.
            'agent_as_is_required_views': metrics(docs['01-as-is.md'] + (docs['README.md'] if side == 'after' else '')),
            'required_file_count': len(docs),
        }
    return {'base': BASE, 'kind': 'static UTF-8 byte proxy; no model execution', 'scenarios': results,
            'large_lifecycle_repeated_reads': repeated, 'sizes': sizes,
            'synthetic_artifact_sample': artifact_sample,
            'artifact_read_limit': 'single-file evidence size is not role input savings; required views include relevant README contracts; historical detail reads and actual host behavior are unmeasured',
            'total_model_input_tokens': None, 'model_generation_tokens': None,
            'excluded_inputs': 'system/user prompts, tools, P adapters, source code, task artifacts, conditional routing/packets/observations; all remain required when applicable'}


if __name__ == '__main__':
    print(json.dumps(measure(), ensure_ascii=False, indent=2))
