/* 동네미팅 사이트 설정 — 여기만 바꾸면 사이트 전체가 바뀝니다 */
window.DM = {
  insta: "dongnae.meet",                 // 인스타 아이디
  // 수파베이스를 연결하면 신청이 자동 저장됩니다 (비워 두면 인스타 DM 신청으로 안내)
  supabaseUrl: "",
  supabaseKey: "",                       // anon(public) 키만 넣습니다
  event: {
    id: "ev1128jangyu",
    title: "장유 첫 동네미팅 4:4",
    date: "2026-11-28T18:00:00+09:00",
    dateText: "11월 28일(토) 저녁 6시",
    place: "장유 율하 카페",
    placeNote: "신청 확정 후 정확한 장소 안내",
    ages: "89~96년생",
    birthMin: 1989, birthMax: 1996,
    seats: { M: 4, F: 4 },
    price: { M: "39,000원", F: "29,000원" }
  }
};
