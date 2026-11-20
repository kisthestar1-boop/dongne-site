/* 딸깍툰 재미 공식 — 우수 웹툰 학습 결과를 코드로.
   딸깍툰 엔진(planEpisode)이 이 공식으로 한 화의 비트·컷·간격·검토 기준을 자동으로 짠다.
   매일 학습이 이어지면 learned[]에 새 출처가 쌓이고 version이 올라간다. */
window.DDK_FORMULA = {
  version: "1.1",
  updated: "2026-11-20",

  /* 한 화 구성: 1화(시즌 오프너)는 우수작 공통 8비트 */
  ep1Beats: [
    { k: "cold",    name: "제목 전 한 장면",  share: 0.06, rule: "가장 인상적인 장면이나 질문 하나를 제목보다 먼저 (만화 1화 공통)", from: ["만화 1화 관행", "mangacraft"] },
    { k: "want",    name: "일상 + 소원",      share: 0.12, rule: "주인공이 무엇을 원하고 무엇이 모자란지 (의도된 결핍) — 귀엽게", from: ["Witch Hat Atelier 1화", "블루 아카이브 캐릭터 설계"] },
    { k: "event",   name: "이변",            share: 0.10, rule: "첫 3컷 안, 늦어도 10% 지점까지 사건 — 숨기지 말 것", from: ["ComixTribe", "artfolio 4비트"] },
    { k: "secret",  name: "비밀 · 정보 격차", share: 0.12, rule: "주인공(또는 독자)만 아는 금지된 것 — 미스터리 씨앗", from: ["Witch Hat Atelier 1화", "회귀물 문법"] },
    { k: "mistake", name: "실수 → 대가",      share: 0.16, rule: "호기심/선의의 실수가 소중한 것을 위험에 빠뜨림 — 감정 판돈 올리기", from: ["Witch Hat Atelier 1화"] },
    { k: "ally",    name: "동료 · 케미",      share: 0.14, rule: "티격태격 관계 하나 + 웃음 1번 이상 (웃음과 감동의 결합)", from: ["화산귀환", "유미의 세포들"] },
    { k: "win",     name: "첫 작은 승리",     share: 0.14, rule: "노력이 바로 보상받는 사이다 한 번 — 집단이 함께 자라는 느낌", from: ["화산귀환 회복의 서사"] },
    { k: "cliff",   name: "절벽",            share: 0.16, rule: "더 큰 질문으로 끝 · 마지막은 세로로 긴 컷으로 다음 장면을 가림", from: ["artfolio", "Villaire 대본법"] }
  ],

  /* 컷 예산 (LlamaGen·Villaire·WEBTOON 학습) */
  panels: { gag: [6, 12], short: [12, 20], standard: [20, 40], peak: [30, 55], opener: [40, 70], max: 55 },

  /* 세로 스크롤 연출 (WEBTOON 공식 핸드북 · Jenova · artfolio) */
  scroll: {
    width: 800, sliceMax: 1280, sliceMB: 2,
    gap: { flow: 200, quick: [50, 100], breath: [150, 300], scene: [600, 1000], reveal: 400 },
    thumbStops: [2, 3],            /* 손가락이 멈추는 꽉 찬 폭 컷 */
    restEvery: 4,                  /* 3~4컷마다 여백 한 번 */
    lowDetailPerSprint: 1,         /* 쉬는 컷(단순 배경) 한 장 */
    onScreenMax: 2                 /* 한 화면에 컷 2개까지 */
  },

  /* 글자 (WEBTOON 핸드북) */
  lettering: { bubblesPerPanel: 3, sentencesPerBubble: [1, 2], fontPx: [12, 30], inImage: false },

  /* 연재 (WEBTOON 핸드북 · Clip Studio) */
  launch: { firstDrop: 3, summaryMax: 500, thumbSquare: [1080, 1080], thumbVertical: [1080, 1920], textInThumb: false },

  /* 그림 일관성 (Gemini 파이프라인 · dev.to · LlamaGen) */
  consistency: { ref1: "캐릭터 시트", ref2: "직전 컷", reanchorEvery: 10, redoOnlyDrift: true, chat: "gemini 4ff45643e3c971ca" },

  /* 구독자 검토 기준 — 하나라도 0점이면 그 비트를 다시 */
  review: [
    { k: "hook3",   q: "첫 3컷 안에 사건이 있나?" },
    { k: "want",    q: "주인공이 원하는 것·모자란 것이 보이나?" },
    { k: "laugh",   q: "웃음 1번 이상 + 마음이 찡한 순간 1번 이상?" },
    { k: "logic",   q: "개연성: 왜 그렇게 행동했는지 납득되나?" },
    { k: "chain",   q: "인과 사슬: 모든 컷이 앞 컷 때문에 일어나나? (갑자기 등장·갑자기 해결 없음)" },
    { k: "setup",   q: "설정 일관: 정한 규칙(회색 마을·누가 컬러인지·옷)이 끝까지 지켜지나?" },
    { k: "next",    q: "마지막 컷을 보고 다음 화를 누르고 싶나?" },
    { k: "face",    q: "모든 컷에서 얼굴·옷이 같은가?" },
    { k: "text",    q: "말풍선이 컷당 3개 이하, 1~2문장인가?" },
    { k: "tone",    q: "처음 분위기와 끝 분위기가 같은 작품처럼 이어지나?" }
  ],

  /* 지키는 것 */
  rules: [
    "개연성이 가장 중요 — 만든 뒤 처음부터 끝까지 한 번 더 읽고 인과가 끊긴 컷은 다시 짠다 (민성님 원칙)",
    "AI로 그린 사실을 연재 때 밝힌다 (숨긴 AI가 가장 큰 반발)",
    "다른 작품 캐릭터를 따라 그리지 않는다 — 그림체만 참고",
    "프롬프트·수정 과정을 기록해 둔다 (저작권 대비)",
    "훅은 진짜여야 한다 — 낚시 첫 장면 금지, 처음 분위기를 끝까지"
  ],

  /* 학습 출처 (계속 늘어남) */
  learned: [
    { at: "2026-11-20", what: "Witch Hat Atelier 1화", got: "경이 → 금지된 비밀 → 실수 → 대가 → 스승 등장" },
    { at: "2026-11-20", what: "장송의 프리렌 1화", got: "여정이 끝난 뒤에서 시작 · 조용한 감정 · 시간의 무게" },
    { at: "2026-11-20", what: "화산귀환", got: "회복의 서사 · 집단 성장 · 웃음 + 한(恨)" },
    { at: "2026-11-20", what: "유미의 세포들", got: "웃음과 감동의 결합 · 공감 일상 · 긴 팬덤" },
    { at: "2026-11-20", what: "WEBTOON 크리에이터 핸드북", got: "첫 3화 동시 공개 · 컷 간격 200px · 장면 전환 600~1000px · 말풍선 3개" },
    { at: "2026-11-20", what: "Alyssa Villaire 대본법", got: "한 화 1~2장면 · 최대 55컷 · 매 화 끝 훅" },
    { at: "2026-11-20", what: "artfolio 연출 스프린트", got: "1컷 훅 · 2~4 판돈 · 5~6 뒤집기 · 마지막 절벽 · 3~4컷마다 여백" },
    { at: "2026-11-20", what: "봄을 잃은 마을 1화 재구성", got: "등장·해결마다 원인 컷을 먼저: 흘린 씨앗 → 빛 → 슬라임 → 실패 → 주인공의 선택 → 결과 → 적이 알아챔" },
    { at: "2026-11-20", what: "AI 웹툰 도구 8종", got: "캐릭터 시트 1번 참고 + 직전 컷 2번 · 10컷마다 재고정 · 글자는 따로" }
  ]
};

/* 딸깍툰 엔진: 줄거리 + 캐릭터 → 한 화 콘티 뼈대 (비트별 컷 수 · 간격 · 꽉 찬 컷 위치) */
window.planEpisode = function (opt) {
  const F = window.DDK_FORMULA;
  const kind = opt.kind || "opener";
  const [lo, hi] = F.panels[kind] || F.panels.standard;
  const total = Math.min(F.panels.max, Math.round(opt.panels || (lo + hi) / 2));
  const beats = F.ep1Beats;
  let used = 0;
  const plan = beats.map((b, i) => {
    const n = i === beats.length - 1 ? total - used : Math.max(1, Math.round(total * b.share));
    used += n;
    return { beat: b.name, rule: b.rule, panels: n };
  });
  /* 손가락 멈춤 컷: 이변 · 대가 · 절벽 비트 */
  const stopAt = ["이변", "실수 → 대가", "절벽"];
  let idx = 0;
  const panels = [];
  plan.forEach(p => {
    for (let j = 0; j < p.panels; j++) {
      idx++;
      const last = j === p.panels - 1;
      const full = stopAt.includes(p.beat) && last;
      const gap = last ? F.scroll.gap.scene[0] : (idx % F.scroll.restEvery === 0 ? F.scroll.gap.breath[1] : F.scroll.gap.flow);
      panels.push({ no: idx, beat: p.beat, width: full ? "꽉 찬 폭" : (idx % 5 === 0 ? "좁게" : "보통"), gapAfter: gap, cast: (opt.cast || []).slice(0, 2) });
    }
  });
  panels[panels.length - 1].width = "세로로 긴 컷 (다음 장면 가리기)";
  return { title: opt.title || "", premise: opt.premise || "", total, plan, panels, review: F.review.map(r => r.q) };
};
