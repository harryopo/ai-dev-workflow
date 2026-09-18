"""
ledger.py — 证据账本（Research Ledger）  [v6.0 新增]

所有搜索证据（claim）与来源（source）的统一持久化层，支持：
- 多子 Agent 并行追加（JSONL 追加式，O_APPEND，Windows/Linux 均安全）
- claim → source 多源关联，可审计、可溯源
- merge：合并子 Agent 产物（claims/、sources/ 子目录下的 json/jsonl）
- status：按 topic 统计覆盖率、独立来源数、冲突数（证据充分性判据来源）
- 导出 JSON / Markdown（供报告引用编号锚定：primary_index = [topic_id-source_seq]）

设计约束：
- 只做文件 IO、去重与统计，不做语义判断（判断交给子 Agent / 主 Agent）
- 所有写操作追加式，读操作按行解析并容错（并发写时可能出现的半行直接跳过）
- 与 tier.py 低耦合：add-source 若不传 tier，则用 domain_tier 自动判定
"""

from __future__ import annotations

import json
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from tier import domain_tier, tier_label
except ImportError:  # 独立运行/测试无 tier 时降级
    domain_tier = None  # type: ignore
    tier_label = lambda t: str(t)  # type: ignore

VALID_STATUS = {'pending', 'searching', 'verified', 'conflict', 'supplementing', 'completed'}


def _now() -> str:
    return datetime.now().isoformat(timespec='seconds')


def _slug(text: str) -> str:
    """文本 → 文件安全短名。"""
    s = re.sub(r'[^\w\u4e00-\u9fff-]', '_', text.strip()).strip('_')[:40]
    return s or 'untitled'


def _atomic_append(path: Path, line: str) -> None:
    """追加一行（Windows O_APPEND 原子性；单行小写安全）。"""
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line + '\n')
        f.flush()


def _iter_entries(path: Path):
    """按行读取 jsonl，容错跳过坏行。"""
    if not path.exists():
        return
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue


class ResearchLedger:
    """证据账本。session_dir 即 ledger 根目录。"""

    ENTRIES = 'ledger.jsonl'
    CLAIMS_DIR = 'claims'
    SOURCES_DIR = 'sources'

    def __init__(self, session_dir: str):
        self.root = Path(session_dir)
        self.entries_path = self.root / self.ENTRIES
        self.claims_dir = self.root / self.CLAIMS_DIR
        self.sources_dir = self.root / self.SOURCES_DIR

    # ------------------------------------------------------------------
    # 初始化
    # ------------------------------------------------------------------
    def init(self) -> 'ResearchLedger':
        """创建目录结构（幂等）。"""
        for d in (self.root, self.claims_dir, self.sources_dir):
            d.mkdir(parents=True, exist_ok=True)
        if not self.entries_path.exists():
            self.entries_path.write_text('', encoding='utf-8')
        return self

    # ------------------------------------------------------------------
    # 写入
    # ------------------------------------------------------------------
    def add_claim(self, claim: str, topic: str = 'general',
                  status: str = 'pending', perspective: str = 'general',
                  confidence: float = 0.5, claim_id: Optional[str] = None,
                  note: str = '') -> Dict[str, Any]:
        """写入一条 claim。

        status ∈ {verified, conflict, supplementing, pending, completed}
        注意：默认 pending——verified 必须由交叉验证（≥2 独立来源）显式赋予，
        未验证的搜索结果一律 pending，防止账本覆盖率虚高。
        """
        status = status if status in VALID_STATUS else 'pending'
        cid = claim_id or f'c-{uuid.uuid4().hex[:10]}'
        entry = {
            'type': 'claim', 'id': cid, 'text': str(claim).strip(),
            'topic': str(topic).strip() or 'general',
            'status': status, 'perspective': perspective,
            'confidence': float(min(max(confidence, 0.0), 1.0)),
            'note': note, 'created_at': _now(),
        }
        _atomic_append(self.entries_path, json.dumps(entry, ensure_ascii=False))
        return entry

    def add_source(self, claim_id: str, url: str, title: str = '',
                   tier: Optional[int] = None,
                   craap_score: Optional[float] = None) -> Dict[str, Any]:
        """为 claim 关联一条来源（多源）。tier 缺省时自动分级。"""
        url = str(url).strip()
        if not url:
            raise ValueError('source url 不能为空')
        t = int(tier) if tier is not None else (domain_tier(url) if domain_tier else 3)
        t = min(max(t, 1), 4)
        entry = {
            'type': 'source', 'claim_id': claim_id, 'url': url,
            'title': str(title).strip(), 'tier': t,
            'craap_score': float(craap_score) if craap_score is not None else None,
            'created_at': _now(),
        }
        _atomic_append(self.entries_path, json.dumps(entry, ensure_ascii=False))
        return entry

    # ------------------------------------------------------------------
    # 合并（子 Agent 产物）
    # ------------------------------------------------------------------
    def merge(self, src_dir: str) -> Tuple[int, int]:
        """合并 src_dir 下的全部子产物（.jsonl / .json），按 id 去重。

        返回 (新增 claim 数, 新增 source 数)。
        """
        src = Path(src_dir)
        added_c = added_s = 0
        if not src.exists():
            return added_c, added_s
        existing = self._ids()
        for f in sorted(src.rglob('*.jsonl')) + sorted(src.rglob('*.json')):
            for item in self._read_any(f):
                if not isinstance(item, dict):
                    continue
                typ = item.get('type') or ('claim' if item.get('text') is not None else 'source')
                if typ == 'claim':
                    if item.get('id') in existing:
                        continue
                    self.add_claim(
                        claim=item.get('text', ''), topic=item.get('topic', 'general'),
                        status=item.get('status', 'verified'),
                        perspective=item.get('perspective', 'general'),
                        confidence=item.get('confidence', 0.5),
                        claim_id=item.get('id'), note=item.get('note', ''),
                    )
                    added_c += 1
                else:
                    cid = str(item.get('claim_id', ''))
                    url = str(item.get('url', ''))
                    if not cid or not url:
                        continue
                    key = (cid, url)
                    if key in existing_sources(self.root):
                        continue
                    self.add_source(cid, url, item.get('title', ''),
                                    item.get('tier'), item.get('craap_score'))
                    added_s += 1
        return added_c, added_s

    def append_file(self, path: str) -> Tuple[int, int]:
        """合并单个产物文件。"""
        return self.merge(path if Path(path).is_dir() else str(Path(path).parent))

    def _ids(self) -> set:
        return {e['id'] for e in self._all() if e.get('type') == 'claim'}

    @staticmethod
    def _read_any(path: Path):
        """按扩展名读文件为 dict 列表。"""
        txt = path.read_text(encoding='utf-8', errors='ignore')
        try:
            if path.suffix.lower() == '.jsonl':
                for line in txt.splitlines():
                    line = line.strip()
                    if line:
                        try:
                            yield json.loads(line)
                        except ValueError:
                            continue
            else:  # .json：单个 dict 或列表
                data = json.loads(txt)
                if isinstance(data, list):
                    for d in data:
                        yield d
                elif isinstance(data, dict):
                    yield data
        except ValueError:
            return

    # ------------------------------------------------------------------
    # 读取 / 统计
    # ------------------------------------------------------------------
    def _all(self) -> List[Dict[str, Any]]:
        return list(_iter_entries(self.entries_path))

    def claims(self, topic: Optional[str] = None) -> List[Dict[str, Any]]:
        out = [e for e in self._all() if e.get('type') == 'claim'
               and (topic is None or e.get('topic') == topic)]
        out.sort(key=lambda e: e.get('created_at', ''))
        return out

    def sources_for_claim(self, claim_id: str) -> List[Dict[str, Any]]:
        return [e for e in self._all()
                if e.get('type') == 'source' and e.get('claim_id') == claim_id]

    def status(self, topic: Optional[str] = None) -> Dict[str, Any]:
        """按 topic 统计状态与证据充分性。"""
        topics: Dict[str, Dict[str, Any]] = {}
        for e in self._all():
            if e.get('type') != 'claim':
                continue
            if topic is not None and e.get('topic') != topic:
                continue
            t = topics.setdefault(e.get('topic', 'general'), {
                'claims': 0, 'verified': 0, 'conflict': 0, 'supplementing': 0,
                'pending': 0, 'source_urls': set(), 'topics': set(),
            })
            t['claims'] += 1
            st = e.get('status', '')
            if st in t:
                t[st] += 1
        # 补来源统计（独立 URL 集合）
        src_map: Dict[str, set] = {}
        for e in self._all():
            if e.get('type') != 'source':
                continue
            cid = e.get('claim_id', '')
            url = e.get('url', '')
            src_map.setdefault(cid, set()).add(url)
        claim_topic = {e['id']: e.get('topic', 'general')
                       for e in self._all() if e.get('type') == 'claim'}
        for cid, urls in src_map.items():
            top = claim_topic.get(cid)
            if top in topics:
                topics[top]['source_urls'].update(urls)

        result = {}
        for t, s in topics.items():
            n = max(s['claims'], 1)
            # sufficient 判据（v6.3 修正）：claim 级严格——
            # ≥1 条 verified claim 且每条 verified claim 均有 ≥2 独立来源 URL，
            # 不再用 topic 级 URL 并集（旧判据会被多条单源 claim 虚假满足）
            verified_claims = [e for e in self.claims(t)
                               if e.get('status') == 'verified']
            insufficient = [
                c['id'] for c in verified_claims
                if len(src_map.get(c['id'], set())) < 2
            ]
            result[t] = {
                'claims': s['claims'],
                'verified': s['verified'],
                'conflict': s['conflict'],
                'supplementing': s['supplementing'],
                'pending': s['pending'],
                'independent_sources': len(s['source_urls']),
                'coverage': round(s['verified'] / n, 2),
                'sufficient': (s['verified'] >= 1 and not insufficient
                               and len(s['source_urls']) >= 2),
                'insufficient_claim_ids': insufficient,
            }
        if topic is not None:
            return result.get(topic, {})
        return result

    def export_json(self, path: Optional[str] = None) -> Dict[str, Any]:
        """导出为完整 JSON（供 validate_report 与报告引用锚定使用）。

        v6.3：为每条 source 注入稳定编号 primary_index（1 起始，按写入顺序），
        报告 [N] 引用与校验门反查共用此编号，实现"引用→具体来源 URL"强契约。
        """
        all_entries = self._all()
        claims = [e for e in all_entries if e.get('type') == 'claim']
        sources = []
        for idx, e in enumerate(
                (e for e in all_entries if e.get('type') == 'source'), start=1):
            e = dict(e)
            e['primary_index'] = idx
            sources.append(e)
        data = {
            'exported_at': _now(),
            'stats': self.status(),
            'claims': claims,
            'sources': sources,
        }
        if path:
            Path(path).write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        return data

    def export_md(self, path: Optional[str] = None) -> str:
        """导出为 Markdown（按 topic 分组，claim + sources 表格）。"""
        lines = ['# 证据账本（Research Ledger）', '', f'导出时间：{_now()}', '']
        st = self.status()
        lines += ['| 子主题 | claims | verified | conflict | 独立来源 | 覆盖 | 充分 |',
                  '|--------|--------|----------|----------|----------|------|------|']
        for t, s in sorted(st.items()):
            lines.append(f"| {t} | {s['claims']} | {s['verified']} | {s['conflict']} "
                         f"| {s['independent_sources']} | {s['coverage']} | {'✅' if s['sufficient'] else '⚠️'} |")
        lines.append('')
        for topic in sorted(set(c['topic'] for c in self.claims())):
            lines += [f"## {topic}", '']
            for c in self.claims(topic):
                lines.append(f"- [{c['id']}] **{c['text']}**"
                             f"（状态:{c['status']} 视角:{c['perspective']} 置信:{c['confidence']}）")
                for s in sorted(self.sources_for_claim(c['id']), key=lambda x: x['tier']):
                    lines.append(f"  - Tier{s['tier']} [{s['title'] or s['url']}]({s['url']})"
                                 + (f" CRAAP:{s['craap_score']}" if s.get('craap_score') is not None else ''))
            lines.append('')
        md = '\n'.join(lines)
        if path:
            Path(path).write_text(md, encoding='utf-8')
        return md


def existing_sources(root: Path) -> set:
    """已存在的 (claim_id, url) 集合（供 merge 去重）。"""
    out = set()
    if (root / ResearchLedger.ENTRIES).exists():
        for e in _iter_entries(root / ResearchLedger.ENTRIES):
            if e.get('type') == 'source':
                out.add((e.get('claim_id', ''), e.get('url', '')))
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _main(argv: Optional[List[str]] = None) -> int:
    args = argv if argv is not None else sys.argv[1:]

    def _session():
        if '--session' not in args:
            print('缺少 --session <目录>', file=sys.stderr)
            sys.exit(2)
        return args[args.index('--session') + 1]

    def _opt(name: str, default: str = '') -> str:
        if name in args:
            return args[args.index(name) + 1]
        return default

    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        print('''\n用法:
  python ledger.py init --session <dir>
  python ledger.py add-claim --session <dir> --text <claim> [--topic <t>] [--status <s>]
                    [--perspective <p>] [--confidence <0-1>] [--id <id>] [--note <n>]
  python ledger.py add-source --session <dir> --claim-id <id> --url <u>
                    [--title <t>] [--tier <1-4>] [--craap <score>]
  python ledger.py status --session <dir> [--topic <t>]
  python ledger.py merge --session <dir> --dir <src_dir>
  python ledger.py export --session <dir> [--format json|md] [--out <path>]''')
        return 0

    cmd = args[0]
    session = _session()
    ledger = ResearchLedger(session)

    if cmd == 'init':
        ledger.init()
        print(f'已初始化账本: {session}')
        return 0

    if cmd == 'add-claim':
        ledger.init()
        if '--text' not in args:
            print('缺少 --text <claim>', file=sys.stderr)
            return 2
        entry = ledger.add_claim(
            claim=args[args.index('--text') + 1],
            topic=_opt('--topic', 'general'),
            status=_opt('--status', 'verified'),
            perspective=_opt('--perspective', 'general'),
            confidence=float(_opt('--confidence', '0.5')),
            claim_id=_opt('--id', '') or None,
            note=_opt('--note', ''),
        )
        print(json.dumps(entry, ensure_ascii=False))
        return 0

    if cmd == 'add-source':
        ledger.init()
        cid = _opt('--claim-id')
        url = _opt('--url')
        if not cid or not url:
            print('缺少 --claim-id / --url', file=sys.stderr)
            return 2
        entry = ledger.add_source(
            claim_id=cid, url=url, title=_opt('--title'),
            tier=int(_opt('--tier')) if _opt('--tier') else None,
            craap_score=float(_opt('--craap')) if _opt('--craap') else None,
        )
        print(json.dumps(entry, ensure_ascii=False))
        return 0

    if cmd == 'status':
        topic = _opt('--topic', '') or None
        print(json.dumps(ledger.status(topic), ensure_ascii=False, indent=2))
        return 0

    if cmd == 'merge':
        src = _opt('--dir')
        if not src:
            print('缺少 --dir <src_dir>', file=sys.stderr)
            return 2
        c, s = ledger.merge(src)
        print(f'合并完成：新增 claim {c} 条，source {s} 条')
        return 0

    if cmd == 'export':
        fmt = _opt('--format', 'json')
        out = _opt('--out', '') or None
        if fmt == 'md':
            print(ledger.export_md(out))
        else:
            data = ledger.export_json(out)
            if not out:
                print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    print(f'未知命令: {cmd}', file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(_main())