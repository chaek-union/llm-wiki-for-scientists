#!/usr/bin/env python3
"""장 원고가 집필 계약을 지키는지 검사한다.

문체 게이트(G3)의 기계적으로 검사 가능한 부분만 다룬다. 과장 표현이나
문단 시작의 단조로움처럼 판단이 필요한 항목은 사람이 본다.

사용법:
    python3 scripts/check_chapters.py            # 전체 장
    python3 scripts/check_chapters.py part1/chapter1.md
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 분량 예산. 실제 글자 수 기준이다. 셸의 `wc -m`은 로케일에 따라 바이트를
# 세므로 한국어에서 세 배 가까이 부풀려진다. 기준은 파이썬의 len()이다.
# 참고: autism 10,144자 / how-to-write-paper 13,929자.
# 실물 근거를 넣은 뒤 장이 두꺼워져 상한을 22,000으로 올렸다.
MIN_CHARS = 11_000
MAX_CHARS = 22_000

# 본문에서 쓰지 않기로 한 표현. wiki/style.md가 정본이다.
BANNED = [
    "완전히 바꾸", "혁명적", "놀랍게도", "극적으로", "획기적",
    "여러분", "당신의", "당신은",
    "이제 살펴보", "다음 절에서는", "지금부터 알아보",
    "단순한 저장소가 아니라", "~가 아니라 ~다",
]

# 지시 대용. 문장 첫머리에 올 때만 잡는다.
VAGUE_REF = re.compile(r"(^|\n)\s*(이것은|이 사실은|그것은|이는 곧)\b")

# 섹션 제목은 명사구다. 마지막 어절이 서술어나 종결어미면 문장이다.
# 판정 기준은 Meetings/wiki/slides/output-gate.md와 같다.
SENTENCE_TITLE = re.compile(r"(다|는가|은가|인가|을까|ㄹ까)$|[?？]")

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
AUTHOR_MARKER = re.compile(r"<!--\s*AUTHOR:")
BOLD = re.compile(r"\*\*[^*\n]+\*\*")


def split_body(text):
    """frontmatter를 떼고 본문만 돌려준다."""
    m = FRONTMATTER.match(text)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


NON_PROSE_START = ("#", "|", "-", "*", ">", "<!--", "1.", "2.", "3.", "```")


def prose_paragraphs(body):
    """산문 문단만 돌려준다.

    각 항목은 (문단, 뒤에 표·목록·코드가 붙는가)다. 표나 목록을 여는
    도입 문단은 짧아도 되므로 문단 길이 검사에서 뺀다.
    """
    blocks = [b.strip() for b in body.split("\n\n") if b.strip()]
    out = []
    for i, block in enumerate(blocks):
        if block.startswith(NON_PROSE_START):
            continue
        nxt = blocks[i + 1] if i + 1 < len(blocks) else ""
        leads_structure = nxt.startswith(("|", "-", "*", "1.", "```"))
        out.append((block, leads_structure))
    return out


def count_sentences(paragraph):
    """한국어 종결 부호로 문장 수를 센다.

    소수점과 약어의 마침표를 문장 끝으로 세지 않도록, 마침표 앞이 숫자가
    아니고 뒤가 공백이거나 문자열 끝인 경우만 센다.
    """
    text = re.sub(r"(?<=\d)\.(?=\d)", "", paragraph)
    return len([s for s in re.split(r"[.!?]\s+|[.!?]$", text) if s.strip()])


def check(path):
    text = path.read_text(encoding="utf-8")
    fm, body = split_body(text)
    problems = []

    if fm is None:
        problems.append("frontmatter가 없다")
    else:
        for key in ("status", "part", "budget"):
            if f"{key}:" not in fm:
                problems.append(f"frontmatter에 {key}가 없다")

    n = len(text)
    if n < MIN_CHARS:
        problems.append(f"분량 부족: {n:,}자 (하한 {MIN_CHARS:,})")
    elif n > MAX_CHARS:
        problems.append(f"분량 초과: {n:,}자 (상한 {MAX_CHARS:,})")

    bolds = BOLD.findall(body)
    if bolds:
        problems.append(f"굵은 글씨 {len(bolds)}곳: {bolds[0][:30]}")

    # 제목 줄은 저자가 의도적으로 2인칭을 쓰는 자리가 있어 검사에서 뺀다.
    prose_only = "\n".join(
        ln for ln in body.split("\n") if not ln.startswith("#")
    )
    for word in BANNED:
        if word in prose_only:
            problems.append(f"금지 표현: {word}")

    vague = VAGUE_REF.findall(body)
    if vague:
        problems.append(f"문장 첫머리 지시 대용 {len(vague)}곳")

    paras = prose_paragraphs(body)
    # 표·목록·코드를 여는 도입 문단과 장을 여닫는 문단은 짧아도 된다.
    body_paras = [p for p, leads in paras[1:-1] if not leads]
    short = [p for p in body_paras if count_sentences(p) < 4]
    if len(short) > len(body_paras) * 0.2:
        problems.append(
            f"4문장 미만 본문 문단 {len(short)}개 / 본문 {len(body_paras)}개"
        )

    markers = AUTHOR_MARKER.findall(text)
    if not markers:
        problems.append("AUTHOR 마커가 없다")

    sections = re.findall(r"^# (.+)$", body, re.M)
    # T1: 장마다 같은 기능의 절을 반복해 붙이지 않는다. 제목만 바꾼 같은
    # 형식도 위반이므로 변형까지 함께 잡는다.
    for banned in ("해보기", "흔한 오해", "내 위키에 남기기", "정리",
                   "확인할 점", "이 장을 삶으로", "마무리", "요약",
                   "실습", "따라 하기", "따라하기"):
        for s in sections:
            if s.strip() == banned or s.strip().endswith(banned):
                problems.append(f"T1 위반 절: {s.strip()}")

    for s in sections:
        title = s.strip()
        if title.endswith("장") or re.match(r"^\d+장[.． ]", title):
            continue
        if SENTENCE_TITLE.search(title) or ":" in title:
            problems.append(f"문장형 절 제목: {title}")

    # 독자가 따라 할 것은 장 끝에 모으지 않고 본문 중간의 코드 블록으로 둔다.
    # 코드 블록이 하나도 없으면 따라 할 자리가 없다는 뜻이다.
    blocks = re.findall(r"^```", body, re.M)
    if len(blocks) < 2:
        problems.append("코드 블록이 없다 — 도식도 따라 할 자리도 없다")

    return {
        "chars": n,
        "sections": len(sections),
        "paragraphs": len(paras),
        "markers": len(markers),
        "problems": problems,
    }


def main():
    if len(sys.argv) > 1:
        targets = [ROOT / a for a in sys.argv[1:]]
    else:
        targets = sorted(
            ROOT.glob("part*/chapter*.md"),
            key=lambda p: int(re.search(r"(\d+)", p.stem).group(1)),
        )

    failed = 0
    total_chars = 0
    for path in targets:
        if not path.exists():
            print(f"{path.relative_to(ROOT)}: 파일 없음")
            failed += 1
            continue
        r = check(path)
        total_chars += r["chars"]
        mark = "OK  " if not r["problems"] else "확인"
        print(
            f"{mark} {path.relative_to(ROOT)!s:22} "
            f"{r['chars']:>7,}자  절 {r['sections']:>2}  "
            f"문단 {r['paragraphs']:>3}  마커 {r['markers']}"
        )
        for p in r["problems"]:
            print(f"       - {p}")
            failed += 1

    print(f"\n총 {len(targets)}장  {total_chars:,}자  지적 {failed}건")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
