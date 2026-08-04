# 근거 원장

이 책이 서술하는 기술적 사실은 여기에 등록된 것만 쓴다. 등록되지 않은 폴더 이름, 명령, URL, 수치를 원고에 쓰지 않는다.

확인 기준일: 2026-08-04
확인 대상 저장소: `~/Dropbox/References/llm-wiki/`

변동성 등급은 이 사실이 얼마나 빨리 낡는지를 뜻한다. 상은 6개월 안에 바뀔 수 있는 것, 중은 1–2년 단위로 바뀌는 것, 하는 구조적으로 안정된 것이다. 변동성 상인 항목은 본문에 쓰지 않고 `appendix/`로 보낸다.

## 저장소 규모와 구조

| ID | 주장 | 근거 위치 | 확인일 | 변동성 | 사용 장 |
|---|---|---|---|---|---|
| E-001 | 최상위는 `papers/`, `sources/`, `wiki/`, `agenda/`, `materials/`, `logs/`, `scripts/`, `indexes/`, `interactives/`, `docs/`, `papers-supplementary/`와 `AGENTS.md`, `CLAUDE.md`, `index.md`로 구성된다 | 저장소 최상위 | 2026-08-04 | 하 | 3 |
| E-002 | 원문 PDF 16,127건이 `papers/`에 있다 | `find papers -name '*.pdf'` | 2026-08-04 | 상 | 3, 5 |
| E-003 | source note 15,995건이 `sources/`에 있다 | `find sources -name '*.md'` | 2026-08-04 | 상 | 4 |
| E-004 | wiki page 17,591건이 50개 category에 있다 | `index.md`, `find wiki -name '*.md'` | 2026-08-04 | 상 | 3, 4, 5 |
| E-005 | synthesis layer는 overviews 590건, concepts 408건, questions 550건이다 | `wiki/overviews/`, `wiki/concepts/`, `wiki/questions/` | 2026-08-04 | 상 | 4, 5 |
| E-006 | `papers/`와 `sources/`는 같은 stem을 공유한다. 예: `1000-genomes-project-2015-global-reference-for-human`의 `.pdf`와 `.md` | 두 폴더의 파일명 대조 | 2026-08-04 | 하 | 4 |
| E-007 | 파일명 stem은 `{저자}-{연도}-{제목 토큰}` 형식이다 | `papers/` 파일명 | 2026-08-04 | 하 | 4 |
| E-008 | category는 주제축과 방법축이 섞여 있다. `asd-ndd`, `glia`, `gwas` 같은 주제축과 `genomic-dl`, `single-cell-dl`, `statistics` 같은 방법축이 공존한다 | `wiki/` 하위 폴더 50개 | 2026-08-04 | 중 | 3, 4 |
| E-009 | category 크기는 균등하지 않다. `drug-resistance` 2,236건과 `biology-for-ai` 11건이 같은 층에 있다 | `index.md` category 표 | 2026-08-04 | 상 | 3, 4 |

## 운영 규칙

| ID | 주장 | 근거 위치 | 확인일 | 변동성 | 사용 장 |
|---|---|---|---|---|---|
| E-010 | 답변은 `sources/`와 `wiki/`에 있는 논문만을 근거로 한다 | `AGENTS.md` 「논문 기반 답변 원칙」 | 2026-08-04 | 하 | 3, 5 |
| E-011 | 웹 검색은 사용자가 명시적으로 요청할 때만 쓴다 | 같은 절 | 2026-08-04 | 하 | 3, 5 |
| E-012 | 위키가 불충분하면 원본 PDF를 다시 읽어 보충한다 | 같은 절 | 2026-08-04 | 하 | 3, 5 |
| E-013 | 해당 논문이 없으면 없다고 말하고 PDF를 요청한다 | 같은 절 | 2026-08-04 | 하 | 3, 5 |
| E-014 | 세션 시작마다 `AGENTS.md`와 registry를 다시 읽고 이전 세션의 기억에 의존하지 않는다 | `AGENTS.md` 「Agent Startup Checklist」 | 2026-08-04 | 중 | 2, 12 |
| E-015 | 이 저장소는 git을 쓰지 않고 Dropbox가 동기화와 버전을 담당한다. 2026-07-17에 git을 제거했다 | `AGENTS.md` 첫 절 | 2026-08-04 | 중 | 3, 15 |
| E-016 | git 제거의 계기는 2026-05-23에 `.git/index`가 Dropbox 충돌 사본으로 꼬여 정상 파일 980건이 삭제로 staged된 사고였다 | 같은 절 | 2026-08-04 | 하 | 3 |
| E-017 | git이 없으므로 `logs/{YYYY-MM-DD}-{agent}-{host}.md`가 무엇을 왜 바꿨는지에 대한 유일한 서술 기록이다 | 같은 절 | 2026-08-04 | 중 | 3, 4 |
| E-018 | 전수 요청은 표본으로 끝내지 않는다는 규칙이 있고, 그 규칙은 실제 실패 사례 이후에 생겼다 | `AGENTS.md` 「전수 요청은 전수로 끝낸다」 | 2026-08-04 | 중 | 2, 5, 15 |
| E-019 | 위키 내용의 언어는 영어이고 대화는 한국어나 영어로 한다 | `AGENTS.md` Language policy | 2026-08-04 | 중 | 3, 5 |

## 검색

| ID | 주장 | 근거 위치 | 확인일 | 변동성 | 사용 장 |
|---|---|---|---|---|---|
| E-020 | BM25 인덱스 구축 스크립트가 있다: `scripts/build_bm25s_wiki_index.py` | `scripts/` | 2026-08-04 | 상 | 5, 부록B |
| E-021 | 검색 스크립트가 있다: `scripts/search_llm_wiki.py`, `scripts/search_llm_wiki.sh` | `scripts/` | 2026-08-04 | 상 | 5, 부록B |
| E-022 | 야간 재색인 스크립트와 launchd 설치 스크립트가 있다: `run_bm25s_nightly_reindex.sh`, `install_bm25s_launchd.sh` | `scripts/` | 2026-08-04 | 상 | 5, 15, 부록B |
| E-023 | 계층 인덱스는 `scripts/build_hierarchical_index.py --all --apply`로 다시 만든다 | `index.md` | 2026-08-04 | 상 | 5, 부록B |
| E-024 | 결정적 탐색 경로는 `index.md`와 `indexes/{category}.md`이고, 의미 검색은 별도 도구가 담당한다 | `index.md` 머리말 | 2026-08-04 | 중 | 5 |
| E-025 | category별 synthesis coverage와 orphan 수를 집계하는 감사 스크립트가 있다: `scripts/audit_synthesis_coverage.py` | `index.md` | 2026-08-04 | 중 | 4, 5 |

## Deep Structure Analysis

| ID | 주장 | 근거 위치 | 확인일 | 변동성 | 사용 장 |
|---|---|---|---|---|---|
| E-030 | 개념 정본 문서가 있다: `wiki/concepts/deep-structure-analysis.md` (작성 2026-07-18) | 해당 파일 frontmatter | 2026-08-04 | 하 | 6 |
| E-031 | 기능 분류는 8축이다: motivation/inspiration, method and engineering lineage, core benchmarking, label/supervision set, dataset/material provenance, background biology, interpretation frame, tools and resources | 같은 문서 taxonomy 표 | 2026-08-04 | 하 | 6 |
| E-032 | 이 방법은 citation function analysis (Teufel, Siddharthan and Tidhar, 2006), citation context analysis, CiTO의 특수화이며, 추가하는 것은 section별 지도와 knowledge base coverage 단계다 | 같은 문서 Definition | 2026-08-04 | 하 | 6 |
| E-033 | 절차는 7단계다: 원문과 인용 해소 → load-bearing 인용의 원문 읽기 → section별 인용 지도 → 기능 분류 → 해석 → coverage 교차 점검 → 누락 확보 → synthesis page로 귀결 | 같은 문서 Procedure | 2026-08-04 | 하 | 6 |
| E-034 | `sources/` note를 cited PDF 대신 읽는 것과 abstract·TLDR·landing page로 full paper를 대체하는 것은 명시적으로 금지된다 | 같은 문서 Procedure 2 | 2026-08-04 | 하 | 6 |
| E-035 | 첫 적용 사례는 Geneformer (Theodoris et al., 2023)이고 main-text 46건과 Methods층 약 110건을 분리했으며 미보유 open-access 6건을 찾아냈다 | `wiki/overviews/geneformer-citation-structure` | 2026-08-04 | 하 | 6 |
| E-036 | 두 번째 적용은 scGPT (Cui et al., 2024)이고, Geneformer가 외부 ground truth 일치로 신뢰를 얻는 반면 scGPT는 방법 대 방법 벤치마킹으로 얻는다는 대비가 드러났다 | 같은 문서 Worked example | 2026-08-04 | 하 | 6 |
| E-037 | 세 번째 적용은 NTv3 (Boshar et al., 2025)로 main-text 64건과 Methods층 44건, Supplementary 4건을 분리했고 자기 인용이 계보를 지배했다 | 같은 문서 | 2026-08-04 | 하 | 6 |
| E-038 | 네 번째 적용은 scFoundation (Hao et al., 2024)으로 참고문헌 75건 중 68건이 main-text 역할을 하고 약 12건만 5천만 세포 corpus를 기록했다. host model이라는 새 범주가 드러났다 | 같은 문서 | 2026-08-04 | 하 | 6 |
| E-039 | 다섯 번째 적용은 AlphaGenome (Avsec et al., 2026)으로 참고문헌 67건 중 5,930 track 학습 corpus를 기록한 것이 거의 없고 Supplementary manifest로 넘겼다. 분석 과정에서 출판 논문의 인용 번호 오류를 발견했다 | 같은 문서 | 2026-08-04 | 하 | 6 |
| E-040 | 결과물 형태는 overviews층 페이지이며 mermaid flowchart로 인용 관계를 그린다 | 같은 문서 Output shape | 2026-08-04 | 하 | 6 |

## Karpathy 원형과 설치 Gist

| ID | 주장 | 근거 위치 | 확인일 | 변동성 | 사용 장 |
|---|---|---|---|---|---|
| E-050 | Karpathy의 LLM Wiki Gist 정본은 `gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`이고 `llm-wiki.md` 한 파일로 되어 있다 | 해당 Gist | 2026-08-04 | 중 | 3 |
| E-051 | 원형의 세 층은 raw sources, the wiki, the schema다 | 같은 문서 | 2026-08-04 | 하 | 3 |
| E-052 | raw sources는 LLM이 읽되 수정하지 않는 불변 자료다 | 같은 문서 | 2026-08-04 | 하 | 3 |
| E-053 | wiki 층은 LLM이 전적으로 소유한다. 원문 표현은 "The LLM owns this layer entirely. It creates pages, updates them when new sources arrive, maintains cross-references." | 같은 문서 | 2026-08-04 | 하 | 3 |
| E-054 | schema는 `CLAUDE.md` 같은 설정 문서이며 사람과 LLM이 함께 발전시킨다. 원문 표현은 "You and the LLM co-evolve this over time as you figure out what works for your domain." | 같은 문서 | 2026-08-04 | 하 | 3 |
| E-055 | 세 동작은 ingest, query, lint다. lint는 모순, 오래된 주장, 고립 페이지, 빠진 상호 참조를 점검한다 | 같은 문서 | 2026-08-04 | 하 | 3, 5 |
| E-056 | RAG와의 대비를 나타내는 원문 표현은 "The wiki is a persistent, compounding artifact." | 같은 문서 | 2026-08-04 | 하 | 3 |
| E-057 | 설치 Gist는 `gist.github.com/joonan30/cbce305684d079dbe9a3fbaefe4e3959`이고 `llm-wiki-gist.md`와 `AGENTS.md.template` 두 파일로 되어 있다 | 해당 Gist | 2026-08-04 | 상 | 3 |
| E-058 | `AGENTS.md.template`은 `CLAUDE.md`로 심볼릭 링크된다 | 같은 Gist | 2026-08-04 | 중 | 2, 3 |
| E-059 | 설치가 만드는 폴더는 `papers/`, `sources/`, `wiki/{categories}/`, `wiki/concepts/`, `wiki/overviews/`, `wiki/questions/`, `agenda/`, `materials/`, `logs/`, `scripts/`, `indexes/`다 | 같은 Gist | 2026-08-04 | 상 | 3 |
| E-060 | 설치 Gist의 운영 규칙은 아홉 개다. 웹 검색 금지, 위키 우선, PDF 복귀, 없으면 없다고 말하기, synthesis layer 연결 전에는 ingest 미완료, placeholder 금지, 분모와 분자를 밝히는 전수 보고, 비공개 자료는 `wiki/`에서 제외, PDF만 사용하고 출판사 HTML이나 브라우저 캡처는 쓰지 않기 | 같은 Gist | 2026-08-04 | 상 | 3, 4 |
| E-061 | 설치 Gist의 `AGENTS.md.template`은 Karpathy 링크로 `gist.github.com/karpathy/1dd0294ef9567971c1e4348a90d69285`을 가리킨다 | 같은 Gist | 2026-08-04 | 상 | 3 |
| E-062 | `1dd0294...`는 LLM Wiki가 아니라 "Git Commit Message AI"이며 `add_to_zshrc.sh` 한 파일로 된 커밋 메시지 생성 스크립트다 | 해당 Gist | 2026-08-04 | 하 | 3 |

E-060은 내용 설계안이 「최초 네 규칙」으로 서술한 것이 아홉 개로 늘어났음을 뜻한다. 3장은 아홉 개를 모두 나열하지 않고, 근거의 추적 가능성을 만드는 네 규칙을 본문에서 다루고 나머지는 부록으로 보낸다.

E-061과 E-062는 함께 쓴다. 3장은 정본 링크로 E-050을 쓰고, 설치 템플릿의 링크가 다른 Gist를 가리킨다는 사실을 각주 수준으로 밝힌다. 이 오류 자체가 위키의 lint가 무엇을 잡아야 하는지 보여주는 사례이므로, 숨기지 않고 쓴다.

## 미확인 항목

원고에 쓰기 전에 확인이 필요하다. 확인 전에는 본문에서 단정하지 않는다.

| ID | 확인해야 할 것 | 필요한 장 | 상태 |
|---|---|---|---|
| U-003 | Codex와 Claude Code의 현재 설치 절차와 화면 | 2, 부록A | 미확인 — 변동성 상, 부록에서만 다룸 |
| U-004 | 파트 3이 참조하는 workspace(`Meetings/`, `Grants/`, `Codex/`, `Projects/`, `Manuscript/`)의 실제 위치와 소유 범위 | 12–16 | 미확인 |
| U-005 | HWPX 처리 도구의 현재 동작과 지원 범위 | 16 | 미확인 |
| U-006 | 예약 자동화의 현재 job 목록과 handoff 형식 | 15 | 미확인 |

미확인 항목이 필요한 장은 그 부분을 절차와 판단 기준 중심으로 쓰고, 구체적인 화면·명령·경로는 쓰지 않는다.
