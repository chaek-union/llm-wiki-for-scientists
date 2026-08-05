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

# 분량은 게이트로 두지 않는다. 저자가 두 번 밝힌 방침이고, 장마다
# 다루는 것의 양이 다르므로 자릿수로 판정할 대상이 아니다. 상태 줄에
# 글자 수만 표시한다. 셸의 `wc -m`은 로케일에 따라 바이트를 세므로
# 한국어에서 세 배 가까이 부풀려진다. 기준은 파이썬의 len()이다.

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

# 빈 추상명사 착지. 문단의 마지막 문장이 여기로 끝나면 리본을 묶은 것이다.
EMPTY_LANDING = re.compile(r"(관점|방식|논리|문제|렌즈|공간|이야기|지점|차원)(이었다|였다|이다|다)\.\s*$")

# 두 문장으로 늘린 A가 아니라 B.
NEGATE_THEN_ASSERT = re.compile(
    r"[^.\n]{5,70}(필요는 없다|필요가 없다|필요하지 않다|하지 않아도 된다)\.\s+"
    r"[^.\n]{5,60}(면 된다|면 충분하다|하면 된다)\."
)

# 상투구
CLICHE = [
    "구조적 접근", "실질적 성과", "업무 맥락", "업무 흐름", "체계적 접근",
    "아무도 알려주지 않", "미래는 이미", "모두가 놓치는", "진짜 중요한 건",
    "무너지는 이유",
]

# R3. 장 첫머리의 범위 선언. "이 장은 ~를 다룬다" 류.
SCOPE_ANNOUNCE = re.compile(
    r"이 장[은는이의을를에서]{0,3}[^.]{0,45}"
    r"(다룬다|다룰 것|맡는다|정리한다|가르[칠친]|보인다|따라간다|세운다"
    r"|목표다|주제다|이야기다|할 일은|만드는 것은|마치면|다루는 것은)"
)

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
AUTHOR_MARKER = re.compile(r"<!--\s*AUTHOR:")
BOLD = re.compile(r"\*\*[^*\n]+\*\*")


def split_body(text):
    """frontmatter를 떼고 본문만 돌려준다."""
    m = FRONTMATTER.match(text)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


NON_PROSE_START = ("#", "|", "-", "*", ">", "!", "<!--", "1.", "2.", "3.", "```")


def prose_paragraphs(body):
    """산문 문단만 돌려준다.

    각 항목은 (문단, 뒤에 표·목록·코드가 붙는가)다. 표나 목록을 여는
    도입 문단은 짧아도 되므로 문단 길이 검사에서 뺀다.
    """
    # 코드 블록 안은 산문이 아니다. 블록 안에 빈 줄이 있으면 그 조각들이
    # 문단으로 세어져 문단 길이 검사가 헛돈다.
    body = re.sub(r"^```.*?^```", "", body, flags=re.S | re.M)
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
    front_matter_exempt = path.name in ("README.md", "getting-started.md")

    if fm is None and not front_matter_exempt:
        problems.append("frontmatter가 없다")
    elif fm is not None:
        for key in ("status", "part", "budget"):
            if f"{key}:" not in fm:
                problems.append(f"frontmatter에 {key}가 없다")

    n = len(text)

    bolds = [] if front_matter_exempt else BOLD.findall(body)
    if bolds:
        problems.append(f"굵은 글씨 {len(bolds)}곳: {bolds[0][:30]}")

    # 제목 줄은 저자가 의도적으로 2인칭을 쓰는 자리가 있어 검사에서 뺀다.
    prose_only = "\n".join(
        ln for ln in body.split("\n") if not ln.startswith("#")
    )
    banned = BANNED + CLICHE
    if front_matter_exempt:
        banned = [w for w in banned if w not in ("당신의", "당신은", "여러분")]
    for word in banned:
        if word in prose_only:
            problems.append(f"금지 표현: {word}")

    if NEGATE_THEN_ASSERT.search(prose_only):
        problems.append("부정으로 열고 다음 문장에서 긍정하는 전개")

    for blk in [b.strip() for b in body.split("\n\n")]:
        if not blk or blk.startswith(NON_PROSE_START):
            continue
        last = re.split(r"(?<=[.!?])\s+", blk)[-1]
        if EMPTY_LANDING.search(last):
            problems.append(f"빈 추상명사 착지: {last[-28:]}")

    vague = VAGUE_REF.findall(body)
    if vague:
        problems.append(f"문장 첫머리 지시 대용 {len(vague)}곳")

    paras = prose_paragraphs(body)

    # R3. 장의 첫 문단에서 그 장이 무엇을 할지 선언하지 않는다.
    # 뒤의 장을 가리키는 문장은 정보를 주므로 첫 문단만 본다.
    if paras:
        opener_para = paras[0][0]
        m = SCOPE_ANNOUNCE.search(opener_para)
        if m:
            problems.append(f"장 예고 문장: {m.group(0)[:34]}…")

    # K4. 장의 첫 문장을 짧은 부정으로 열지 않는다. 실질을 담은 긴
    # 부정문은 정상이므로 길이로 가른다.
    if paras:
        opener = re.split(r"(?<=[.!?])\s+", paras[0][0].strip())[0]
        if re.search(r"(않는다|않다|아니다|없다|못한다)\.?$", opener) and len(opener) < 30:
            problems.append(f"부정으로 여는 첫 문장: {opener}")

    # R4. 장의 마지막 문단은 코다가 앉는 자리다. 예전에는 이 문단을 길이
    # 검사에서 통째로 뺐고, 그 예외가 경구형 마무리를 그대로 통과시켰다.
    if paras and not front_matter_exempt:
        last = paras[-1][0]
        if count_sentences(last) < 6:
            problems.append(f"장 마무리 코다 의심: {last[:34]}…")
        tail = re.split(r"(?<=[.!?])\s+", last.strip())[-1]
        for seal in ("이 책을 덮고", "이 책의 처음이자", "말의 실제 내용이다",
                     "남길 것은", "만드는 것은", "것뿐이다"):
            if seal in tail:
                problems.append(f"장 마무리 봉합문: {seal}")
    # 표·목록·코드를 여는 도입 문단과 장을 여닫는 문단은 짧아도 된다.
    body_paras = [p for p, leads in paras[1:-1] if not leads]
    short = [p for p in body_paras if count_sentences(p) < 4]
    if len(short) > len(body_paras) * 0.2:
        problems.append(
            f"4문장 미만 본문 문단 {len(short)}개 / 본문 {len(body_paras)}개"
        )

    # 마커가 0이면 저자가 채울 자리가 남지 않았다는 뜻이므로 결함이 아니다.
    markers = AUTHOR_MARKER.findall(text)

    if front_matter_exempt:
        return {"chars": n, "sections": 0, "paragraphs": len(paras),
                "markers": len(markers), "problems": problems}

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
    if len(blocks) < 2 and "![" not in body:
        problems.append("코드 블록도 그림도 없다 — 따라 할 자리가 없다")

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
        # 서문과 들어가며도 같은 문체 규칙을 받는다. frontmatter와 분량
        # 규정은 없으므로 그 두 항목은 검사에서 뺀다.
        targets = [ROOT / "README.md", ROOT / "getting-started.md"] + targets

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
