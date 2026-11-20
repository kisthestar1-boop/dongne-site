# 찰칵홈 학원 포트폴리오 생성기 — 업종별 내용 + 3가지 레이아웃 + 장유 지역 검색(SEO) 세팅
# 실행: python3 gen_academy.py  → web/ex/<slug>/index.html
import json, os, html
OUT = os.path.dirname(os.path.abspath(__file__))
E = html.escape

SITES = [
 dict(slug="art", name="꿈틀미술학원", en="KKUMTEUL ART", kind="미술학원", kw=["장유 미술학원", "김해 장유 미술", "율하 미술학원", "아동 미술"],
  layout="A", c1="#B5539B", c2="#F4C542", bg="#FBF4FA", hero="hero_art.jpg",
  pill="🎨 장유 · 유아·초등 미술 / 입시 기초",
  h1="그리는 즐거움이<br><em>자신감이 되는</em> 미술학원",
  sub="정답을 따라 그리지 않아요. 아이 생각을 그림으로 꺼내는 수업, 매달 작품 포트폴리오를 집으로 보내 드려요.",
  cta="무료 체험 수업", chips=["👩‍🎨 반별 최대 6명", "🖼 월간 작품 포트폴리오", "🏆 공모전 준비반"],
  progs=[("🖍","유아 감성미술","5~7세 · 색·재료 놀이로 표현력 키우기"),("✏️","초등 드로잉","관찰 드로잉 · 수채화 · 만들기"),("🏅","공모전·사고력","주제 해석부터 완성까지 1:1 코칭"),("🎓","예중·예고 기초","소묘 · 정물 · 발상 기초반")],
  sched=[("유아반","월·수·금","14:00–15:00","5명"),("초등 저학년","화·목","15:00–16:30","6명"),("초등 고학년","월·수","16:30–18:00","6명"),("토요 공모전반","토","10:00–12:00","6명")],
  why=[("🎨","재료를 아끼지 않아요","수채·아크릴·점토·판화까지 매달 새 재료로 수업해요."),("📸","작품 사진 알림","수업이 끝나면 오늘 그린 그림을 카톡으로 보내 드려요."),("🗂","포트폴리오 파일","1년 작품이 쌓이는 개인 파일을 만들어 드려요.")],
  faq=[("미술을 처음 하는 아이도 괜찮나요?","그럼요. 첫 달은 재료와 친해지는 놀이 수업부터 시작해요."),("재료비는 따로 있나요?","기본 재료는 수강료에 포함돼 있어요. 특별 재료는 미리 안내드려요."),("차량 운행을 하나요?","장유·율하 아파트 단지를 운행해요. 정확한 노선은 상담 때 안내해 드려요.")]),

 dict(slug="piano", name="도레미 피아노학원", en="DOREMI PIANO", kind="피아노학원", kw=["장유 피아노", "장유 피아노학원", "김해 피아노학원", "삼문동 피아노"],
  layout="B", c1="#2E9C83", c2="#F2A23A", bg="#F2FAF7", hero="hero_piano.jpg",
  pill="🎹 장유 삼문 · 유아~성인 피아노",
  h1="손끝에서 시작되는<br><em>작은 연주회</em>",
  sub="1:1 레슨 + 이론 + 매 학기 작은 연주회. 바이엘부터 체르니, 성인 취미반까지 개인 진도로 배워요.",
  cta="무료 체험 레슨", chips=["🎹 개인 연습실 8실", "🎼 1:1 진도 레슨", "🎤 학기별 연주회"],
  progs=[("🐣","유아 리듬반","5~7세 · 리듬 놀이 · 건반과 친해지기"),("🎹","초등 기본 과정","바이엘 → 체르니 · 이론 · 청음"),("🏆","콩쿠르·입시","콩쿠르 곡 준비 · 예중 입시 기초"),("☕","성인 취미반","원하는 곡 1곡 완성 · 직장인 저녁반")],
  sched=[("유아 리듬반","월·수","14:00–14:40","4명"),("초등 개인 레슨","월~금","14:00–19:00","1:1"),("콩쿠르반","토","10:00–13:00","1:1"),("성인 취미반","화·목","19:30–21:30","1:1")],
  why=[("🎧","방음 개인 연습실","혼자 집중해서 연습할 수 있는 연습실 8실이 있어요."),("📒","연습 일지 알림","오늘 친 곡과 다음 숙제를 매일 알림으로 보내 드려요."),("🎤","작은 연주회","학기마다 가족을 초대하는 연주회로 무대 경험을 쌓아요.")],
  faq=[("집에 피아노가 없어도 되나요?","학원 연습실에서 충분히 연습할 수 있어요. 처음엔 디지털 피아노로도 괜찮아요."),("레슨은 몇 분인가요?","개인 레슨 20분 + 연습 30분 + 이론 10분, 하루 1시간이 기본이에요."),("성인도 배울 수 있나요?","네, 직장인 저녁반이 있어요. 악보를 몰라도 시작할 수 있어요.")]),

 dict(slug="taekwondo", name="용감한 태권도", en="YONGGAM TAEKWONDO", kind="태권도장", kw=["장유 태권도", "김해 장유 태권도장", "율하 태권도", "줄넘기 태권도"],
  layout="C", c1="#D64545", c2="#1F3A68", bg="#FFF5F3", hero="hero_tkd.jpg",
  pill="🥋 장유 · 유아·초등 태권도 · 줄넘기",
  h1="몸도 마음도<br><em>씩씩하게</em> 자라요",
  sub="인사 · 예절 · 체력 · 품새를 한 번에. 매일 줄넘기와 놀이 체육으로 운동을 좋아하는 아이로 키워요.",
  cta="무료 체험 수업", chips=["🚐 안전 차량 운행", "🏅 국기원 승품 심사", "🪢 줄넘기 급수제"],
  progs=[("🐯","유아부","5~7세 · 놀이 체육 · 인사와 기본 동작"),("🥋","초등부","품새 · 겨루기 기본 · 줄넘기 급수"),("🏅","시범·대회반","시범단 · 대회 품새 · 발차기 심화"),("🎉","방학 특강","캠프 · 생존수영 연계 · 체육 놀이")],
  sched=[("유아부","월~금","14:00–14:50","12명"),("초등 저학년","월~금","15:00–15:50","15명"),("초등 고학년","월~금","16:00–16:50","15명"),("시범·대회반","화·목·토","17:00–18:00","10명")],
  why=[("🚐","등하원 안전 차량","보호 교사가 동승하고, 하차 알림을 보내 드려요."),("📷","수업 사진 알림","오늘 운동하는 모습을 사진으로 보내 드려요."),("🙇","예절 교육","인사·존댓말·정리 정돈을 매일 습관으로 만들어요.")],
  faq=[("운동을 처음 하는 아이도 괜찮나요?","유아부는 놀이 체육 위주라 처음 하는 아이도 금방 적응해요."),("차량 운행 지역은 어디인가요?","장유·율하·대청 아파트 단지를 운행해요. 상담 때 정확한 시간을 안내해 드려요."),("승품 심사는 언제 보나요?","국기원 일정에 맞춰 1년에 여러 번 볼 수 있어요.")]),

 dict(slug="coding", name="부엉이 코딩학원", en="OWL CODING", kind="코딩학원", kw=["장유 코딩학원", "김해 코딩", "초등 코딩 장유", "스크래치 파이썬"],
  layout="A", c1="#5B4FCF", c2="#1FB5A8", bg="#F4F3FF", hero="hero_coding.jpg",
  pill="💻 장유 · 초등 스크래치 → 중등 파이썬",
  h1="게임을 하던 아이가<br><em>게임을 만들어요</em>",
  sub="블록 코딩으로 시작해 파이썬·AI까지. 매달 내 손으로 만든 게임과 앱을 가족에게 보여 줘요.",
  cta="무료 체험 수업", chips=["🧩 1인 1노트북", "🎮 월 1개 작품 완성", "🏆 정보올림피아드 대비"],
  progs=[("🧩","초등 블록 코딩","스크래치·엔트리로 게임 만들기"),("🤖","로봇·피지컬","센서·모터로 움직이는 작품"),("🐍","파이썬 기초","문법 → 미니 프로젝트 → 자격증"),("🧠","AI·정보올림피아드","알고리즘 · 대회 문제 풀이")],
  sched=[("초등 블록 코딩","월·수","15:00–16:30","6명"),("로봇반","화·목","15:00–16:30","6명"),("파이썬 기초","월·수","17:00–18:30","6명"),("알고리즘반","토","10:00–12:30","6명")],
  why=[("🎮","작품 중심 수업","배운 걸 바로 게임·앱으로 만들어 보니 재미있어 해요."),("📁","온라인 포트폴리오","만든 작품을 링크로 모아 집에서도 실행해 볼 수 있어요."),("👨‍💻","현직 개발자 커리큘럼","실제로 쓰는 도구와 순서로 가르쳐요.")],
  faq=[("컴퓨터를 잘 못 다루는데 괜찮나요?","첫 달은 마우스·키보드와 블록 코딩부터 천천히 시작해요."),("노트북을 가져가야 하나요?","학원에서 1인 1노트북을 드려요."),("몇 살부터 배울 수 있나요?","초등 1학년부터 블록 코딩반에 들어올 수 있어요.")]),

 dict(slug="reading", name="고슴도치 독서논술", en="GOSUM READING", kind="독서논술학원", kw=["장유 독서논술", "장유 논술학원", "김해 독서논술", "초등 독서 장유"],
  layout="B", c1="#4E7D3A", c2="#E09A3A", bg="#FAF7EE", hero="hero_reading.jpg",
  pill="📚 장유 · 초등 독서·글쓰기 / 중등 논술",
  h1="한 권을 읽고<br><em>한 줄을 쓰는</em> 힘",
  sub="매주 한 권, 토론하고 글로 정리해요. 문해력이 모든 과목의 기초가 되도록, 아이 속도에 맞춰 함께 읽어요.",
  cta="무료 독서 진단", chips=["📖 주 1권 함께 읽기", "🗣 소그룹 토론", "📝 첨삭 노트"],
  progs=[("🌱","초등 저학년","그림책 · 짧은 동화 · 생각 그림 일기"),("🌿","초등 고학년","고전·지식책 · 토론 · 독서록"),("🌳","중등 논술","주제 글쓰기 · 서술형 · 비문학 독해"),("📰","신문·시사반","기사 읽고 내 의견 쓰기")],
  sched=[("저학년반","월·수","15:00–16:20","5명"),("고학년반","화·목","16:00–17:30","6명"),("중등 논술","월·수","18:00–19:30","6명"),("토요 시사반","토","10:00–11:30","6명")],
  why=[("✍️","1:1 첨삭","쓴 글은 선생님이 한 줄 한 줄 고쳐 돌려줘요."),("🧠","문해력 진단","학기마다 읽기·쓰기 실력을 진단해 리포트로 보내요."),("📚","학원 서재","300권 서재에서 아이가 직접 책을 골라 읽어요.")],
  faq=[("책을 싫어하는 아이도 괜찮나요?","아이가 좋아하는 주제의 짧은 책부터 골라 시작해요."),("숙제가 많나요?","주 1권 읽기와 짧은 글 한 편이 기본이에요."),("성적에도 도움이 되나요?","서술형·비문학 독해 같은 모든 과목의 기초가 돼요.")]),

 dict(slug="science", name="코알라 과학실험", en="KOALA SCIENCE", kind="과학학원", kw=["장유 과학학원", "장유 과학실험", "김해 초등 과학", "율하 과학"],
  layout="C", c1="#2F7FD0", c2="#F28C38", bg="#F2F8FE", hero="hero_science.jpg",
  pill="🔬 장유 · 초등 실험 과학 / 중등 과학 내신",
  h1="손으로 해 보면<br><em>과학이 쉬워져요</em>",
  sub="매주 직접 하는 실험으로 원리를 이해하고, 실험 보고서로 생각을 정리해요. 중등은 학교별 과학 내신까지.",
  cta="무료 실험 체험", chips=["🧪 매주 직접 실험", "📒 실험 보고서", "🏅 과학 탐구대회"],
  progs=[("🧪","초등 실험 과학","물질·생명·지구·에너지 실험"),("🔭","탐구 프로젝트","주제 정해 실험 설계부터 발표까지"),("📘","중등 과학 내신","교과서 실험 + 학교별 기출"),("🧲","방학 실험 캠프","하루 3시간 집중 실험")],
  sched=[("초등 3·4학년","월·수","15:00–16:30","8명"),("초등 5·6학년","화·목","15:30–17:00","8명"),("중등 내신반","월·수","18:00–20:00","8명"),("토요 탐구반","토","10:00–12:00","8명")],
  why=[("🥽","안전 실험실","보안경·장갑 착용, 선생님 1명당 8명까지만 실험해요."),("📷","실험 영상 알림","오늘 한 실험을 짧은 영상으로 보내 드려요."),("🧾","실험 보고서","관찰·가설·결과를 쓰며 서술형 실력도 키워요.")],
  faq=[("실험은 안전한가요?","안전 장비를 꼭 쓰고, 위험한 재료는 선생님이 먼저 다뤄요."),("초등 몇 학년부터 들을 수 있나요?","초등 3학년부터 실험반에 들어올 수 있어요."),("중학교 과학 성적에도 도움이 되나요?","교과서 실험을 직접 해 보니 서술형 문제에 강해져요.")]),

 dict(slug="dance", name="핑크판다 다이어트댄스", en="PINK PANDA DANCE", kind="다이어트댄스 학원", kw=["장유 다이어트댄스", "장유 댄스학원", "김해 다이어트 댄스", "율하 줌바"],
  layout="B", c1="#E2447A", c2="#7A4FD0", bg="#FFF3F7", hero="hero_dance.jpg",
  pill="💃 장유 · 성인 여성 다이어트댄스 · 줌바",
  h1="운동이 아니라<br><em>신나는 한 시간</em>",
  sub="음악에 맞춰 따라 하다 보면 땀이 쫙! 처음 오는 분도 맨 뒷줄에서 편하게 시작해요. 오전·저녁반 모두 있어요.",
  cta="1회 무료 체험", chips=["🎵 최신곡 · K-pop", "⏰ 오전·저녁반", "👟 초보 환영"],
  progs=[("💃","다이어트댄스","K-pop · 트로트 리믹스로 유산소"),("🔥","줌바","라틴 리듬으로 신나게 칼로리 태우기"),("🧘","스트레칭·코어","수업 전후 바른 자세와 코어"),("👯","친구랑 2인 등록","함께 다니면 수강료 할인")],
  sched=[("오전 다이어트댄스","월·수·금","10:00–10:50","20명"),("오후 줌바","화·목","14:00–14:50","20명"),("저녁 다이어트댄스","월~금","19:30–20:20","25명"),("주말 특강","토","10:00–11:00","25명")],
  why=[("🙈","초보 맨 뒷줄 자리","처음 오신 분은 편하게 뒤에서, 동작은 쉬운 버전으로 알려 드려요."),("📅","출석 챌린지","한 달 출석하면 다음 달 혜택을 드려요."),("🚿","깨끗한 탈의실","샤워실·탈의실·개인 보관함이 있어요.")],
  faq=[("몸치인데 따라갈 수 있을까요?","대부분 처음엔 몸치세요! 쉬운 동작으로 2주면 따라와요."),("어떤 옷을 입어야 하나요?","편한 운동복과 실내 운동화면 충분해요."),("아이를 데려와도 되나요?","오전반은 대기 공간이 있어요. 미리 말씀해 주세요.")]),
 dict(slug="ballet", name="루미 발레스튜디오", en="LUMI BALLET", kind="발레학원", kw=["장유 발레", "장유 발레학원", "김해 유아 발레", "율하 발레"],
  layout="A", c1="#C9628A", c2="#9C7BD1", bg="#FDF4F7", hero="hero_ballet.jpg",
  pill="🩰 장유 · 유아·초등 발레 / 성인 발레핏",
  h1="곧은 자세와<br><em>우아한 자신감</em>",
  sub="바른 자세 · 유연성 · 음악성을 함께 키워요. 아이는 즐겁게, 어른은 몸이 가벼워지는 발레 수업.",
  cta="무료 체험 수업", chips=["🩰 반별 최대 8명", "🪞 전면 거울 연습실", "🎀 연말 발표회"],
  progs=[("🎀","유아 발레","4~7세 · 음악 놀이 · 기본 자세"),("🩰","초등 발레","바 · 센터 · 작품반"),("🏅","콩쿠르·예중 준비","작품 레슨 · 개인 지도"),("🧘","성인 발레핏","자세 교정 · 유연성 · 코어")],
  sched=[("유아반","월·수","15:00–15:50","8명"),("초등반","화·목","16:00–17:00","8명"),("작품반","토","10:00–12:00","6명"),("성인 발레핏","월·수","19:30–20:30","10명")],
  why=[("🪞","안전한 연습실","충격 흡수 바닥과 전면 거울로 안전하게 연습해요."),("📷","수업 영상 알림","오늘 배운 동작을 짧은 영상으로 보내 드려요."),("🎭","연말 발표회","무대에 서는 경험으로 자신감을 키워요.")],
  faq=[("몸이 뻣뻣해도 할 수 있나요?","유연성은 수업하면서 천천히 늘어요. 처음엔 누구나 뻣뻣해요."),("발레복이 꼭 필요한가요?","첫 체험은 편한 옷이면 돼요. 등록 후 안내해 드려요."),("남자아이도 배울 수 있나요?","네, 자세와 체력에 아주 좋아요.")]),
 dict(slug="pe", name="점프업 체육교실", en="JUMP UP PE", kind="줄넘기·체육교실", kw=["장유 줄넘기", "장유 체육교실", "김해 아동 체육", "율하 줄넘기"],
  layout="C", c1="#E0A100", c2="#2D8FD6", bg="#FFFBEC", hero="hero_pe.jpg",
  pill="🪢 장유 · 줄넘기 · 놀이체육 · 학교 체육 대비",
  h1="운동을<br><em>좋아하게 되는</em> 체육교실",
  sub="줄넘기 급수제와 놀이 체육으로 체력·순발력·자신감을 키워요. 학교 체육 수행평가도 미리 준비해요.",
  cta="무료 체험 수업", chips=["🪢 줄넘기 급수제", "🏃 소근육·대근육 발달", "🏫 수행평가 대비"],
  progs=[("🐥","유아 놀이체육","균형 · 협응 · 규칙 지키기"),("🪢","줄넘기 급수반","양발 · 2단 뛰기 · 음악 줄넘기"),("⚽","구기 · 뜀틀","공 던지기 · 뜀틀 · 매트 운동"),("🏫","수행평가반","학교 체육 종목 미리 연습")],
  sched=[("유아반","월·수·금","14:00–14:50","10명"),("초등 저학년","월·수·금","15:00–15:50","12명"),("초등 고학년","화·목","16:00–17:00","12명"),("토요 수행평가반","토","10:00–11:30","10명")],
  why=[("🏅","급수 배지","단계를 통과할 때마다 배지를 받아 동기부여가 돼요."),("📊","체력 리포트","분기마다 줄넘기 기록과 체력 변화를 보내 드려요."),("🧸","운동 싫어하는 아이도","놀이로 시작해서 몸 쓰는 재미를 먼저 알려 줘요.")],
  faq=[("운동을 싫어하는 아이도 괜찮나요?","놀이 위주라 금방 재미를 붙여요."),("준비물이 있나요?","편한 운동복과 실내화, 물병이면 돼요. 줄넘기는 학원에서 드려요."),("차량 운행을 하나요?","장유 아파트 단지를 운행해요.")]),
 dict(slug="vocal", name="펭귄 실용음악학원", en="PENGUIN MUSIC", kind="실용음악학원", kw=["장유 실용음악", "장유 보컬학원", "김해 실용음악학원", "장유 기타 레슨"],
  layout="B", c1="#5A4FCF", c2="#F25F7A", bg="#F4F3FD", hero="hero_vocal.jpg",
  pill="🎤 장유 · 보컬 · 기타 · 작곡 / 입시 · 취미",
  h1="좋아하는 노래를<br><em>내 목소리로</em>",
  sub="취미부터 입시까지 1:1 레슨. 녹음실에서 내 노래를 직접 녹음해 보고, 정기 공연으로 무대에 서요.",
  cta="무료 상담 · 레벨 체크", chips=["🎙 녹음실 보유", "🎸 보컬·기타·작곡", "🎫 정기 공연"],
  progs=[("🎤","보컬","호흡 · 발성 · 음정 · 곡 완성"),("🎸","기타","통기타 · 일렉 · 코드 반주"),("🎹","작곡 · 미디","곡 만들기 · 녹음 · 편곡"),("🎓","실용음악 입시","예고 · 대학 입시 레슨")],
  sched=[("취미 보컬","월~금","15:00–21:00","1:1"),("기타","월~금","15:00–21:00","1:1"),("입시반","월~토","예약제","1:1"),("직장인 저녁반","화·목","19:30–21:30","1:1")],
  why=[("🎙","녹음실 체험","한 달에 한 번 내 노래를 녹음해 파일로 드려요."),("📹","레슨 영상","레슨 장면을 짧게 찍어 집에서 복습해요."),("🎫","정기 공연","분기마다 작은 공연으로 무대 경험을 쌓아요.")],
  faq=[("노래를 못해도 시작할 수 있나요?","처음 오시는 분 대부분이 그래요. 호흡부터 천천히 시작해요."),("레슨 시간은 어떻게 정하나요?","1:1이라 원하는 시간으로 예약해요."),("성인도 많이 배우나요?","직장인 저녁반이 따로 있을 만큼 많아요.")]),
 dict(slug="mathkids", name="곰곰 사고력수학", en="GOMGOM MATH", kind="초등 사고력수학", kw=["장유 사고력수학", "장유 초등수학", "김해 사고력 수학", "율하 수학학원"],
  layout="A", c1="#E07B2E", c2="#3F9E8C", bg="#FFF7EF", hero="hero_mathkids.jpg",
  pill="🧸 장유 · 7세~초등 사고력 · 연산",
  h1="외우는 수학 말고<br><em>생각하는 수학</em>",
  sub="교구로 만지고 그려 보며 원리를 이해해요. 연산은 짧고 꾸준하게, 사고력은 재미있게.",
  cta="무료 레벨 진단", chips=["🧩 교구 수업", "⏱ 하루 10분 연산", "📊 월간 성장 리포트"],
  progs=[("🧩","7세 수 감각","수 세기 · 모양 · 패턴 놀이"),("🧠","초등 사고력","도형 · 규칙 · 논리 퍼즐"),("➗","연산 완성","학년별 연산 속도·정확도"),("🏆","경시 준비","교내 · 외부 경시 문제 풀이")],
  sched=[("7세반","월·수","14:00–14:50","6명"),("초1·2","화·목","15:00–16:00","6명"),("초3·4","월·수","16:00–17:20","6명"),("초5·6","화·목","17:00–18:30","6명")],
  why=[("🧸","손으로 배우는 교구","블록·칠교·주사위로 개념을 손으로 익혀요."),("📝","생각 노트","답보다 풀이 과정을 말과 그림으로 써요."),("📊","성장 리포트","한 달 동안 늘어난 점을 그래프로 보내 드려요.")],
  faq=[("연산만 따로 할 수 있나요?","연산반이 따로 있어요. 상담 때 맞는 반을 추천해 드려요."),("선행도 하나요?","무리한 선행보다 지금 학년을 깊게 이해하는 걸 먼저 해요."),("숙제는 얼마나 되나요?","하루 10분 연산과 주 1회 사고력 문제가 기본이에요.")]),
 dict(slug="violin", name="삼색이 바이올린", en="SAMSAEK VIOLIN", kind="바이올린 학원", kw=["장유 바이올린", "김해 바이올린 레슨", "장유 현악기", "율하 바이올린"],
  layout="C", c1="#9C3D54", c2="#D8A04A", bg="#FBF3F4", hero="hero_violin.jpg",
  pill="🎻 장유 · 유아~성인 바이올린 · 첼로",
  h1="첫 활 긋기부터<br><em>오케스트라까지</em>",
  sub="1:1 레슨으로 바른 자세를 먼저 잡고, 앙상블 수업으로 함께 연주하는 기쁨을 느껴요.",
  cta="무료 체험 레슨", chips=["🎻 악기 대여 가능", "🎼 1:1 + 앙상블", "🎄 연말 연주회"],
  progs=[("🎵","유아 바이올린","5~7세 · 1/16 악기 · 리듬 놀이"),("🎻","초등 바이올린","스즈키 교재 · 음계 · 연습곡"),("🎶","앙상블","친구들과 합주 · 학교 오케스트라 준비"),("☕","성인 취미","원하는 곡 완성 · 평일 저녁")],
  sched=[("유아 레슨","월~금","14:00–17:00","1:1"),("초등 레슨","월~금","15:00–19:00","1:1"),("앙상블","토","10:00–11:30","8명"),("성인 레슨","화·목","19:30–21:30","1:1")],
  why=[("🎻","악기 대여","처음엔 악기를 빌려 써 보고 천천히 결정하셔도 돼요."),("🎧","연습 녹음","레슨 곡을 녹음해 드려 집에서 따라 연습해요."),("🎄","연말 연주회","가족 앞에서 연주하며 큰 성취감을 느껴요.")],
  faq=[("악기가 없어도 시작할 수 있나요?","네, 학원 악기를 대여해 드려요."),("몇 살부터 배울 수 있나요?","5세부터 작은 악기로 시작할 수 있어요."),("첼로도 배울 수 있나요?","첼로 레슨도 있어요. 상담 때 말씀해 주세요.")]),
 dict(slug="talk", name="수달 영어회화", en="SUDAL ENGLISH TALK", kind="성인 영어회화", kw=["장유 영어회화", "김해 성인 영어", "장유 영어학원 성인", "직장인 영어회화"],
  layout="B", c1="#1F6F8B", c2="#F2A541", bg="#F1F7F9", hero="hero_talk.jpg",
  pill="☕ 장유 · 직장인·주부 영어회화 소그룹",
  h1="커피 한 잔 하듯<br><em>편하게 말해요</em>",
  sub="4명 소그룹으로 매 수업 30분 이상 직접 말해요. 여행 · 업무 · 아이 영어 도와주기까지, 쓰는 영어만.",
  cta="무료 레벨 상담", chips=["👥 4명 소그룹", "🌙 오전·저녁반", "✈️ 여행·업무 영어"],
  progs=[("☕","왕초보 회화","인사 · 자기소개 · 일상 표현"),("✈️","여행 영어","공항 · 호텔 · 식당 실전 대화"),("💼","업무 영어","이메일 · 전화 · 회의 표현"),("👩‍👧","엄마표 영어","아이와 쓰는 영어 · 그림책 읽기")],
  sched=[("오전 왕초보","화·목","10:00–11:00","4명"),("오전 여행반","월·수","10:30–11:30","4명"),("저녁 업무반","월·수","19:30–20:30","4명"),("토요 프리토킹","토","10:00–11:30","6명")],
  why=[("🗣","말하는 시간 보장","한 수업에 한 사람당 15분 이상 직접 말해요."),("📱","표현 카드 알림","오늘 배운 표현을 카드로 보내 드려 출퇴근길에 복습해요."),("🙂","부담 없는 분위기","틀려도 괜찮은 작은 반이라 처음 말하기가 쉬워요.")],
  faq=[("영어를 거의 못해도 되나요?","왕초보반은 알파벳 발음부터 함께해요."),("수업 시간을 바꿀 수 있나요?","같은 레벨 반으로 옮겨서 들을 수 있어요."),("1:1 수업도 있나요?","원하시면 1:1 수업도 상담해 드려요.")])
]

LOC = "경남 김해시 장유 ○○로 ○○, 3층 (예시)"

def page(s):
    c1, c2, bg = s["c1"], s["c2"], s["bg"]
    kw = s["kw"]; title = f'{s["name"]} | {kw[0]} · 김해 장유 {s["kind"]} (찰칵홈 예시)'
    desc = f'김해 {kw[0].split()[0]} {s["name"]}(예시) — {s["sub"][:70]}'
    faqld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in s["faq"]]}
    orgld = {"@context":"https://schema.org","@type":"EducationalOrganization" if "댄스" not in s["kind"] else "ExerciseGym","name":s["name"]+"(예시)","areaServed":"김해 장유","description":s["sub"],"keywords":", ".join(kw)}
    L = s["layout"]
    hero_img = f'../heroes/{s["hero"]}'
    chips = "".join(f"<span>{E(c)}</span>" for c in s["chips"])
    btns = f'<a class="cta" href="#apply">{E(s["cta"])} →</a> <a class="cta o" href="#class">수업 · 시간표</a>'
    if L == "A":
        hero = f'''<section class="hero A"><div class="w"><div><span class="pill">{E(s["pill"])}</span><h1>{s["h1"]}</h1><p>{E(s["sub"])}</p>{btns}<div class="chips">{chips}</div></div><div class="img"><img src="{hero_img}" alt="{E(kw[0])} {E(s["name"])}"></div></div></section>'''
    elif L == "B":
        hero = f'''<section class="hero B" style="background-image:url({hero_img})"><div class="w"><div class="glass"><span class="pill">{E(s["pill"])}</span><h1>{s["h1"]}</h1><p>{E(s["sub"])}</p>{btns}<div class="chips">{chips}</div></div></div></section>'''
    else:
        hero = f'''<section class="hero C"><div class="w" style="text-align:center"><span class="pill">{E(s["pill"])}</span><h1>{s["h1"]}</h1><p style="margin-left:auto;margin-right:auto">{E(s["sub"])}</p>{btns}<div class="chips" style="justify-content:center">{chips}</div><div class="img wide"><img src="{hero_img}" alt="{E(kw[0])} {E(s["name"])}"></div></div></section>'''
    progs = "".join(f'<div class="card"><b class="ic">{p[0]}</b><h3>{E(p[1])}</h3><p>{E(p[2])}</p></div>' for p in s["progs"])
    why = "".join(f'<div class="card"><b class="ic">{p[0]}</b><h3>{E(p[1])}</h3><p>{E(p[2])}</p></div>' for p in s["why"])
    rows = "".join(f'<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td><span class="tag">{E(d)}</span></td></tr>' for a,b,c,d in s["sched"])
    fees = "".join(f'<tr><td>{E(a)}</td><td>{E(b)} · {E(c)}</td><td>○○○,000원</td><td>{E(d)}</td></tr>' for a,b,c,d in s["sched"])
    faq = "".join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in s["faq"])
    opts = "".join(f"<option>{E(p[1])}</option>" for p in s["progs"])
    J = lambda o: json.dumps(o, ensure_ascii=False).replace("<","\\u003c")
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}"><meta name="keywords" content="{E(", ".join(kw))}"><meta name="robots" content="noindex">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="{hero_img}">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap" rel="stylesheet">
<script type="application/ld+json">{J(orgld)}</script><script type="application/ld+json">{J(faqld)}</script>
<style>
:root{{--c1:{c1};--c2:{c2};--bg:{bg};--ink:#1F2430;--mu:#626B78;--ln:#E7E2EA;--card:#fff}}
*{{box-sizing:border-box}}body{{margin:0;font-family:"Noto Sans KR",system-ui,sans-serif;color:var(--ink);background:var(--bg);line-height:1.7;word-break:keep-all}}
a{{color:inherit}}.w{{max-width:1120px;margin:0 auto;padding:0 20px}}img{{max-width:100%;display:block}}
header{{position:sticky;top:0;z-index:9;background:rgba(255,255,255,.93);backdrop-filter:blur(8px);border-bottom:1px solid var(--ln)}}
header .w{{display:flex;align-items:center;gap:16px;height:70px}}.logo{{display:flex;align-items:center;gap:10px;text-decoration:none}}
.logo i{{width:40px;height:40px;border-radius:12px;background:var(--c1);color:#fff;display:grid;place-items:center;font-style:normal;font-weight:900;font-size:19px}}
.logo b{{font-size:22px;font-weight:900;letter-spacing:-.02em}}.logo small{{display:block;font-size:10.5px;color:var(--mu);font-weight:700;margin-top:-4px;letter-spacing:.06em}}
nav{{margin-left:auto;display:flex;gap:18px;font-weight:700;font-size:15px}}nav a{{text-decoration:none;color:var(--mu)}}@media(max-width:820px){{nav{{display:none}}}}
.cta{{display:inline-block;background:var(--c1);color:#fff;text-decoration:none;font-weight:900;border-radius:14px;padding:13px 20px;border:0;font:inherit;font-weight:900;cursor:pointer}}.cta.o{{background:#fff;color:var(--ink);border:1px solid var(--ln)}}
.pill{{display:inline-block;background:#fff;border:1px solid var(--ln);color:var(--c1);font-weight:900;font-size:13px;border-radius:99px;padding:6px 12px}}
h1{{font-size:clamp(34px,5.4vw,60px);line-height:1.17;letter-spacing:-.03em;margin:16px 0 14px}}h1 em{{font-style:normal;color:var(--c1)}}
.hero p{{font-size:18px;color:var(--mu);max-width:34em;margin:0 0 24px}}
.chips{{display:flex;gap:8px;flex-wrap:wrap;margin-top:20px;font-size:14px;font-weight:700}}.chips span{{background:#fff;border:1px solid var(--ln);border-radius:99px;padding:6px 12px}}
.hero.A{{padding:50px 0 60px}}.hero.A .w{{display:grid;grid-template-columns:1fr 1.05fr;gap:30px;align-items:center}}.hero.A .img img{{border-radius:28px;box-shadow:0 24px 60px rgba(0,0,0,.12)}}
@media(max-width:860px){{.hero.A .w{{grid-template-columns:1fr}}}}
.hero.B{{min-height:600px;background-size:cover;background-position:70% center;display:flex;align-items:center;padding:40px 0}}.hero.B .w{{width:100%}}
.hero.B .glass{{max-width:560px;background:rgba(255,255,255,.82);backdrop-filter:blur(10px);border-radius:28px;padding:30px 30px 26px;box-shadow:0 20px 50px rgba(0,0,0,.08)}}
@media(max-width:760px){{.hero.B{{background-position:80% top;padding-top:300px}}}}
.hero.C{{padding:56px 0 30px}}.hero.C .img.wide{{margin:34px auto 0;max-width:900px}}.hero.C .img.wide img{{border-radius:32px;box-shadow:0 24px 60px rgba(0,0,0,.12)}}
section{{padding:76px 0}}.k{{font-size:13px;font-weight:900;color:var(--c1);letter-spacing:.1em}}h2{{font-size:clamp(26px,3.4vw,38px);letter-spacing:-.02em;margin:4px 0 8px}}.lead{{color:var(--mu);margin:0 0 30px;font-size:17px}}
.alt{{background:#fff;border-top:1px solid var(--ln);border-bottom:1px solid var(--ln)}}
.grid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}.grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}@media(max-width:860px){{.grid4{{grid-template-columns:1fr 1fr}}.grid3{{grid-template-columns:1fr}}}}
.card{{background:var(--card);border:1px solid var(--ln);border-radius:20px;padding:22px}}.card .ic{{font-size:30px}}.card h3{{margin:10px 0 4px;font-size:18px}}.card p{{margin:0;color:var(--mu);font-size:15px}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--ln);border-radius:16px;overflow:hidden;font-size:15px}}th,td{{padding:14px 12px;border-bottom:1px solid var(--ln);text-align:left}}th{{background:var(--bg);font-size:13px;color:var(--mu)}}
.tag{{font-size:12px;font-weight:900;border-radius:6px;padding:2px 8px;background:var(--bg);color:var(--c1)}}
.rv{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}@media(max-width:860px){{.rv{{grid-template-columns:1fr}}}}.rv blockquote{{margin:0;background:#fff;border:1px solid var(--ln);border-radius:18px;padding:20px}}.rv cite{{display:block;margin-top:8px;color:var(--mu);font-style:normal;font-size:13px}}
details{{background:#fff;border:1px solid var(--ln);border-radius:16px;padding:16px 18px;margin-bottom:10px}}summary{{font-weight:900;cursor:pointer}}details p{{margin:8px 0 0;color:var(--mu)}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:start}}@media(max-width:860px){{.two{{grid-template-columns:1fr}}}}
form{{display:grid;gap:10px;background:#fff;border:1px solid var(--ln);border-radius:22px;padding:22px}}input,select,textarea{{font:inherit;padding:12px;border-radius:12px;border:1px solid var(--ln)}}
.gal{{background:#fff;border:1px dashed var(--ln);border-radius:18px;aspect-ratio:4/3;display:grid;place-items:center;font-size:44px;text-align:center}}.gal small{{display:block;font-size:13px;color:var(--mu);font-weight:700}}
@media(max-width:560px){{header .w>.cta{{display:none}}.logo b{{white-space:nowrap}}}}
.map{{border-radius:18px;background:repeating-linear-gradient(45deg,#fff,#fff 12px,var(--bg) 12px,var(--bg) 24px);border:1px solid var(--ln);height:180px;display:grid;place-items:center;color:var(--mu);font-weight:700;margin-top:14px}}
.notice{{background:var(--c2);color:#fff;text-align:center;font-weight:800;font-size:14px;padding:9px 12px}}
footer{{padding:28px 0 100px;color:var(--mu);font-size:13px;background:#fff;border-top:1px solid var(--ln)}}
.dock{{position:fixed;left:50%;transform:translateX(-50%);bottom:14px;z-index:20;display:flex;gap:6px;background:rgba(31,36,48,.92);padding:7px;border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,.2)}}
.dock a{{color:#fff;text-decoration:none;font-weight:900;font-size:14px;padding:10px 14px;border-radius:10px;white-space:nowrap}}.dock a.y{{background:var(--c2)}}
.badge{{position:fixed;left:12px;bottom:74px;z-index:21;background:rgba(31,36,48,.85);color:#fff;font-size:11.5px;padding:5px 10px;border-radius:99px}}.badge a{{color:#FFD45C}}
</style></head><body>
<div class="notice">📢 겨울방학 특강 접수 중 · 신규생 {E(s["cta"])} 예약 가능</div>
<header><div class="w"><a class="logo" href="#"><i>{E(s["name"][0])}</i><span><b>{E(s["name"])}</b><small>{E(s["en"])} · 김해 장유</small></span></a>
<nav><a href="#prog">수업</a><a href="#class">시간표</a><a href="#fee">교습비</a><a href="#why">특별한 점</a><a href="#faq">FAQ</a><a href="#map">오시는 길</a></nav><a class="cta" href="#apply">{E(s["cta"])}</a></div></header>
{hero}
<section id="prog" class="alt"><div class="w"><span class="k">PROGRAMS</span><h2>수업 안내</h2><p class="lead">아이(수강생)의 지금 단계에서 시작해요. 상담 후 반을 정해요.</p><div class="grid4">{progs}</div></div></section>
<section id="class"><div class="w"><span class="k">TIMETABLE</span><h2>시간표</h2><p class="lead">※ 예시 시간표예요. 정확한 시간은 상담 때 안내해 드려요.</p>
<table><tr><th>반</th><th>요일</th><th>시간</th><th>정원</th></tr>{rows}</table></div></section>
<section id="why" class="alt"><div class="w"><span class="k">WHY US</span><h2>{E(s["name"])}이 특별한 이유</h2><p class="lead">학부모(수강생)가 가장 궁금해하는 것부터 챙겼어요.</p><div class="grid3">{why}</div>
<div class="rv" style="margin-top:16px"><p style="grid-column:1/-1;margin:0;font-size:13px;color:var(--mu)">※ 실제 후기·합격 실적은 본인 동의를 받은 것만 올려요.</p><blockquote>"처음엔 걱정했는데 지금은 먼저 가자고 해요."<cite>학부모 · 예시 후기</cite></blockquote><blockquote>"매번 알림으로 오늘 한 걸 볼 수 있어서 안심돼요."<cite>학부모 · 예시 후기</cite></blockquote><blockquote>"선생님이 하나하나 챙겨 주셔서 좋아요."<cite>수강생 · 예시 후기</cite></blockquote></div></div></section>
<section id="news"><div class="w"><span class="k">NEWS</span><h2>학원 소식</h2><p class="lead">원장님이 휴대폰으로 바로 올리는 공지 자리예요.</p>
<div class="grid3"><div class="card"><small style="color:var(--c1);font-weight:900">공지 · 12/01</small><h3>겨울방학 특강 접수</h3><p>12월 첫 주부터 방학 특강 신청을 받아요. (예시)</p></div><div class="card"><small style="color:var(--c1);font-weight:900">행사 · 12/20</small><h3>연말 발표회 · 공개 수업</h3><p>가족을 초대하는 작은 발표회가 있어요. (예시)</p></div><div class="card"><small style="color:var(--c1);font-weight:900">안내 · 매월</small><h3>이달의 수업 사진</h3><p>네이버 블로그에 수업 사진을 올려요 → 블로그 연결</p></div></div></div></section>
<section class="alt"><div class="w"><span class="k">GALLERY</span><h2>교실 둘러보기</h2><p class="lead">등록 전에 가장 많이 보시는 곳 — 교실 · 대기 공간 · 화장실 · 주차장 사진 자리예요.</p>
<div class="grid4"><div class="gal">🏫<small>교실</small></div><div class="gal">🛋<small>대기 공간</small></div><div class="gal">🧼<small>화장실·세면대</small></div><div class="gal">🅿️<small>주차장·입구</small></div></div></div></section>
<section id="fee"><div class="w"><span class="k">TUITION</span><h2>교습비 안내</h2><p class="lead">교육청에 신고한 금액 그대로 게시해요. 학원법상 인터넷 광고엔 교습비·등록번호·명칭·과목 표시가 필수라, 미리 다 넣어 드려요.</p>
<table><tr><th>과정</th><th>교습 시간</th><th>월 교습비</th><th>비고</th></tr>{fees}</table>
<p style="font-size:13px;color:var(--mu);margin-top:10px">※ 예시 금액이에요. 실제 사이트에는 교육청 신고 교습비·등록번호를 그대로 넣어요. 교재비·재료비는 별도 안내.</p></div></section>
<section id="faq" class="alt"><div class="w"><span class="k">FAQ</span><h2>자주 묻는 질문</h2><div style="margin-top:18px">{faq}</div></div></section>
<section id="apply"><div class="w two"><div id="map"><span class="k">CONTACT</span><h2>{E(s["cta"])} 신청</h2><p class="lead">남겨 주시면 원장님이 오늘 안에 연락드려요.</p>
<p>📍 {LOC}<br>🕑 평일 10:00 – 21:00 · 토 10:00 – 14:00<br>📞 055-000-0000 (예시)<br>🅿️ 건물 주차 1시간 무료</p><div class="map">🗺 네이버·카카오 지도가 들어가는 자리</div><p style="margin-top:10px;font-size:14px">⭐ <a href="#">네이버 플레이스 리뷰 보기</a> · 📝 <a href="#">블로그 수업 일기</a></p></div>
<form onsubmit="event.preventDefault();this.querySelector('small').hidden=false"><input placeholder="이름" required><select>{opts}</select><input placeholder="연락처 010-" required inputmode="tel"><textarea placeholder="궁금한 점 (선택)"></textarea><label style="font-size:13px;color:var(--mu)"><input type="checkbox" required style="width:auto"> 상담 연락을 위한 이름·연락처 수집에 동의해요</label><button class="cta">{E(s["cta"])} 신청하기 →</button><small style="color:var(--mu)">📲 신청하면 원장님 휴대폰으로 바로 알림이 가요</small><small hidden>예시 사이트라 실제로 접수되지는 않아요 🙂</small></form></div></section>
<footer><div class="w"><b>{E(s["name"])}</b> (예시) · {E(" · ".join(kw[:3]))}<br>{LOC} · 학원 등록번호 제○○○호 (예시) · 교습과목 {E(s["kind"])} · 교습비 <a href="#fee">교습비 안내</a> 참고<br>© 2026 · 이 사이트는 <a href="https://kisthestar1-boop.github.io/minsung-ai/web/">찰칵홈</a>이 만든 예시예요 · 이름·숫자·후기는 가상</div></footer>
<div class="dock"><a class="y" href="#apply">{E(s["cta"])}</a><a href="#">💬 카톡 상담</a><a href="tel:0550000000">📞 전화</a></div>
<div class="badge">찰칵홈 예시 · 가상 학원 · <a href="https://kisthestar1-boop.github.io/minsung-ai/web/">만들기 문의</a></div>
</body></html>'''

if __name__ == "__main__":
    for s in SITES:
        d = os.path.join(OUT, s["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(page(s).replace("</body>", open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"kit","ux_kit.html")).read()+"\n</body>",1)); print("ok", s["slug"])
