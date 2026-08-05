#!/usr/bin/env python3
"""근거 원장에 등록된 사실이 원고에서 그대로 살아 있는지 검사한다.

윤문이나 압축 과정에서 숫자와 식별자가 사라지거나 바뀌는 것을 잡는다.
`fidelity_audit.py`는 git HEAD와 작업본을 비교하지만, 이 스크립트는
커밋 이력이 없는 장에서도 쓸 수 있다.

원장의 모든 항목을 검사하지는 않는다. 틀리면 책의 신뢰가 무너지는
값, 즉 식별자와 규모 수치만 본다.

사용법:
    python3 scripts/check_evidence.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (근거 ID, 원고에 있어야 하는 문자열, 이 값이 나와야 하는 장)
# 장 번호가 빈 목록이면 어느 장에든 한 번은 나와야 한다는 뜻이다.
FACTS = [
    ("E-002", "16,127", [4, 5]),
    ("E-003", "15,995", [4, 5]),
    ("E-004", "17,591", [4, 5]),
    ("E-005", "590", [4]),
    ("E-005", "408", [4]),
    ("E-005", "550", [4]),
    ("E-007", "theodoris-2023-transfer-learning-network-biology", [5]),
    ("E-009", "2,236", [5]),
    ("E-016", "980", [4]),
    ("E-031", "8", []),
    ("E-035", "46", [11]),
    ("E-037", "64", [11]),
    ("E-038", "75", [11]),
    ("E-039", "67", [11]),
    ("E-039", "5,930", [11]),
    ("E-050", "442a6bf555914893e9891c11519de94f", [4]),
    ("E-057", "cbce305684d079dbe9a3fbaefe4e3959", [4]),
    ("E-061", "1dd0294ef9567971c1e4348a90d69285", [4]),
]

# 관통 corpus의 서지 정보. 하나라도 어긋나면 독자가 같은 논문을 못 찾는다.
CORPUS = [
    "10.1038/s41592-024-02353-z",
    "10.1038/s41586-023-06139-9",
    "10.1038/s41592-024-02201-0",
    "10.1038/s41586-025-10014-0",
    "10.1186/s12864-025-11600-2",
]


def chapter_text(n):
    for part in (1, 2, 3):
        p = ROOT / f"part{part}" / f"chapter{n}.md"
        if p.exists():
            return p.read_text(encoding="utf-8")
    return None


def main():
    all_text = "\n".join(
        p.read_text(encoding="utf-8") for p in sorted(ROOT.glob("part*/chapter*.md"))
    )
    problems = []

    for eid, value, chapters in FACTS:
        if not chapters:
            if value not in all_text:
                problems.append(f"{eid}: '{value}'가 원고 어디에도 없다")
            continue
        for n in chapters:
            t = chapter_text(n)
            if t is None:
                problems.append(f"{eid}: {n}장 파일이 없다")
            elif value not in t:
                problems.append(f"{eid}: '{value}'가 {n}장에서 사라졌다")

    corpus = (ROOT / "wiki" / "corpus.md").read_text(encoding="utf-8")
    for doi in CORPUS:
        if doi not in corpus:
            problems.append(f"corpus.md에서 DOI {doi}가 사라졌다")

    # 근거 원장에 없는 Gist 해시가 본문에 나타나면 지어낸 값이다.
    known = {"442a6bf555914893e9891c11519de94f",
             "cbce305684d079dbe9a3fbaefe4e3959",
             "1dd0294ef9567971c1e4348a90d69285"}
    for h in set(re.findall(r"\b[0-9a-f]{32}\b", all_text)) - known:
        problems.append(f"원장에 없는 해시가 본문에 있다: {h}")

    for p in problems:
        print(f"  - {p}")
    print(f"\n검사 {len(FACTS) + len(CORPUS)}건, 지적 {len(problems)}건")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
