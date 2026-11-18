// 찰칵상세 AI 서버 (Google Apps Script) — 키는 스크립트 속성 GEMINI_KEY 에만 둔다
// 11/18: 크레딧 코드(로그인 없이) · 카카오페이 송금 주문 → 시트에서 입금확인 체크 → 코드 메일 자동 발송
const TXT = ["gemini-3.5-flash", "gemini-flash-latest", "gemini-2.5-flash", "gemini-3.1-flash-lite"];
const IMG = ["gemini-3.1-flash-image", "gemini-2.5-flash-image", "gemini-3.1-flash-lite-image"];
const PRO = ["gemini-3-pro-image", "nano-banana-pro-preview", "gemini-3-pro-image-preview", "gemini-3.1-flash-image"];
const LIMIT = { copy: 800, scene: 400, poster: 600 }; // 하루 최대 (요금 폭주 방지)
const PAGE = 50, REDO = 2, FREE_PER_DAY = 30;   // 상세페이지 1건 50크레딧 · 다시 찍기 2크레딧 · 무료 맛보기(대표 컷 1장) 하루 30명 (출시용)
const PKG = { p50: [5000, 50], p110: [10000, 110], p350: [30000, 350] }; // 원, 크레딧
const SHEET_NAME = "찰칵상세 주문";

function doGet() { return out({ ok: true, service: "chalkak-ai" }); }
function P() { return PropertiesService.getScriptProperties(); }
function jget(k) { const v = P().getProperty(k); return v ? JSON.parse(v) : null; }
function jset(k, o) { P().setProperty(k, JSON.stringify(o)); }
function lock(f) { const l = LockService.getScriptLock(); l.waitLock(8000); try { return f(); } finally { l.releaseLock(); } }
function today() { return Utilities.formatDate(new Date(), "Asia/Seoul", "yyyyMMdd"); }
function rnd(n) { const a = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"; let s = ""; for (let i = 0; i < n; i++) s += a[Math.floor(Math.random() * a.length)]; return s; }
function cc(code) { return String(code || "").toUpperCase().replace(/[^A-Z0-9-]/g, ""); }

function doPost(e) {
  let q0 = null;
  try {
    const q = JSON.parse(e.postData.contents); q0 = q;
    if (q.op === "list") {
      const k0 = P().getProperty("GEMINI_KEY");
      const lr = UrlFetchApp.fetch("https://generativelanguage.googleapis.com/v1beta/models?pageSize=200", { headers: { "x-goog-api-key": k0 }, muteHttpExceptions: true });
      const lj = JSON.parse(lr.getContentText());
      return out({ models: (lj.models || []).map(function (m) { return m.name.replace("models/", ""); }) });
    }
    /* ---- 크레딧 ---- */
    if (q.op === "bal") { const c = jget("c_" + cc(q.code)); return out(c ? { bal: c.b } : { error: "코드를 찾을 수 없어요" }); }
    if (q.op === "start" || q.op === "redo") return out(lock(function () {
      const code = cc(q.code), c = jget("c_" + code); const cost = q.op === "start" ? PAGE : REDO;
      if (!c) return { error: "코드를 찾을 수 없어요" };
      if (c.b < cost) return { error: "크레딧이 부족해요 (남은 " + c.b + ")", bal: c.b };
      c.b -= cost; jset("c_" + code, c);
      const t = rnd(16); jset("t_" + t, { code: code, cost: cost, left: q.op === "start" ? 22 : 2, used: 0, exp: Date.now() + 2 * 3600e3 });
      return { ticket: t, bal: c.b };
    }));
    if (q.op === "refund") return out(lock(function () {
      const t = jget("t_" + q.ticket); if (!t) return { error: "없음" };
      if (t.used > 0) return { error: "이미 사용됨" };
      const c = jget("c_" + t.code); c.b += t.cost; jset("c_" + t.code, c); P().deleteProperty("t_" + q.ticket); return { bal: c.b };
    }));
    if (q.op === "order") return out(lock(function () {
      const pk = PKG[q.pkg]; const em = String(q.email || "").trim();
      if (!pk || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)) return { error: "이메일과 충전 금액을 확인해 주세요" };
      const sh = sheet(); const n = Number(P().getProperty("ORDER_N") || 0) + 1; P().setProperty("ORDER_N", String(n));
      const id = String(1000 + n), rowNo = n + 1;
      const into = q.code && jget("c_" + cc(q.code)) ? cc(q.code) : ""; // 이미 코드가 있으면 그 코드에 충전 (지갑 하나)
      const claim = rnd(20); jset("o_" + claim, { order: id });
      sh.getRange(rowNo, 1, 1, 10).setValues([[new Date(), id, em, pk[0], pk[1], false, "", "", into, claim]]);
      sh.getRange(rowNo, 6).insertCheckboxes();
      return { order: id, amount: pk[0], credits: pk[1], claim: claim, into: into };
    }));
    if (q.op === "claim") { const o = jget("o_" + String(q.claim || "")); return out(o ? (o.code ? { code: o.code, credits: o.credits, bal: (jget("c_" + o.code) || {}).b } : { wait: true, order: o.order }) : { error: "주문을 찾을 수 없어요" }); }
    if (q.op === "find") return out(lock(function () { // 코드 잃어버렸을 때: 이메일로 다시 보내기 (1시간 1번)
      const em = String(q.email || "").trim().toLowerCase(); if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)) return { error: "이메일을 확인해 주세요" };
      const ok = { ok: true, msg: "충전 기록이 있으면 몇 분 안에 메일로 코드를 다시 보내 드려요" };
      const rk = "m_" + em; if (Number(P().getProperty(rk) || 0) > Date.now() - 3600e3) return ok;
      const rows = sheet().getDataRange().getValues().slice(1).filter(function (r) { return String(r[2]).trim().toLowerCase() === em && r[6]; });
      if (!rows.length) return ok;
      P().setProperty(rk, String(Date.now()));
      MailApp.sendEmail({ to: em, name: "찰칵상세", subject: "[찰칵상세] 크레딧 코드를 다시 보내 드려요",
        body: "안녕하세요, 찰칵상세예요.\n요청하신 크레딧 코드예요.\n\n" + rows.map(function (r) { const c = jget("c_" + r[6]); return "· " + r[6] + "  (주문 " + r[1] + " · 남은 " + (c ? c.b : 0) + "크레딧)"; }).join("\n") +
          "\n\nhttps://kisthestar1-boop.github.io/ttukttak/ 작업 화면 위쪽 '크레딧 코드' 칸에 넣어 주세요.\n찰칵상세 드림" });
      return ok;
    }));
    /* ---- AI 호출 ---- */
    if (q.op !== "copy" && q.op !== "scene" && q.op !== "poster") return out({ error: "잘못된 요청" });
    if (e.postData.contents.length > 6000000) return out({ error: "사진이 너무 커요" });
    if (q.op !== "copy") { const g = gate(q); if (g) return out({ error: g }); }
    const key = P().getProperty("GEMINI_KEY");
    if (!key) return out({ error: "서버에 AI 키가 아직 없어요" });
    if (!countOk(q.op)) return out({ error: "오늘 생성 한도를 다 썼어요. 내일 다시 해 주세요" });
    const models = q.op === "poster" ? PRO : q.op === "scene" ? IMG : TXT;
    let last = "모델을 찾지 못했어요";
    for (const m of models) {
      const r = UrlFetchApp.fetch("https://generativelanguage.googleapis.com/v1beta/models/" + m + ":generateContent", {
        method: "post", contentType: "application/json", payload: JSON.stringify(q.body),
        headers: { "x-goog-api-key": key }, muteHttpExceptions: true });
      const code = r.getResponseCode();
      if (code === 404) { last = "모델 없음 " + m; continue; }
      const j = JSON.parse(r.getContentText());
      if (code === 503 || code === 500 || code === 429) { last = (j.error && j.error.message) || ("오류 " + code); continue; }
      if (code >= 400) { ungate(q); return out({ error: (j.error && j.error.message) || ("오류 " + code) }); }
      return out(j);
    }
    ungate(q); return out({ error: last });
  } catch (err) { try { if (q0 && q0.op !== "copy") ungate(q0); } catch (e2) {} return out({ error: String(err) }); }
}

/* 그림 생성은 ① 크레딧 티켓 ② 무료 맛보기(브라우저당 1번, 하루 FREE_PER_DAY명) 둘 중 하나가 있어야 해요 */
function gate(q) {
  return lock(function () {
    if (q.ticket) {
      const t = jget("t_" + q.ticket);
      if (!t || t.exp < Date.now()) return "이용 시간이 지났어요. 다시 만들어 주세요";
      if (t.left <= 0) return "이번 작업에서 쓸 수 있는 사진 수를 다 썼어요";
      t.left--; t.used++; jset("t_" + q.ticket, t); return "";
    }
    if (q.taste) {
      const fk = "f_" + String(q.taste).slice(0, 40);
      if (P().getProperty(fk)) return "무료 맛보기는 한 번만 가능해요. 크레딧을 충전해 주세요";
      const dk = "free_" + today(); const n = Number(P().getProperty(dk) || 0);
      if (n >= FREE_PER_DAY) return "오늘 무료 맛보기가 모두 끝났어요. 내일 다시 오시거나 크레딧을 충전해 주세요";
      P().setProperty(dk, String(n + 1)); P().setProperty(fk, "1"); return "";
    }
    return "크레딧 코드를 넣어 주세요";
  });
}

/* AI가 실패하면 티켓 사용 1회를 돌려줘요 (실패한 사진은 돈을 안 받아요) */
function ungate(q) {
  if (q.op === "copy") return;
  lock(function () {
    if (q.ticket) { const t = jget("t_" + q.ticket); if (t) { t.left++; t.used = Math.max(0, t.used - 1); jset("t_" + q.ticket, t); } return; }
    if (q.taste) { P().deleteProperty("f_" + String(q.taste).slice(0, 40)); const dk = "free_" + today(); P().setProperty(dk, String(Math.max(0, Number(P().getProperty(dk) || 0) - 1))); }
  });
}
function countOk(op) {
  return lock(function () {
    const k = "n_" + op + "_" + today();
    const n = Number(P().getProperty(k) || 0);
    if (n >= (LIMIT[op] || 50)) return false;
    P().setProperty(k, String(n + 1)); return true;
  });
}

/* ---- 주문 시트 · 입금확인 체크 → 코드 발급 + 메일 ---- */
function sheet() {
  let id = P().getProperty("SHEET_ID"), ss = null;
  if (id) { try { ss = SpreadsheetApp.openById(id); } catch (e) { ss = null; } }
  if (!ss) {
    ss = SpreadsheetApp.create(SHEET_NAME); P().setProperty("SHEET_ID", ss.getId());
    const sh = ss.getSheets()[0]; sh.setName("주문");
    sh.appendRow(["시간", "주문번호", "이메일", "금액(원)", "크레딧", "☑ 입금확인", "크레딧 코드", "메일 발송", "기존 코드", "자동반영키"]);
    sh.setFrozenRows(1); sh.setColumnWidths(1, 10, 130);
  }
  return ss.getSheetByName("주문");
}
function mint(credits, note) {
  return lock(function () {
    let code; do { code = "CK-" + rnd(4) + "-" + rnd(4); } while (P().getProperty("c_" + code));
    jset("c_" + code, { b: credits, t: new Date().toISOString(), n: note || "" }); return code;
  });
}
function onOrderEdit(e) {
  const r = e.range, sh = r.getSheet(); if (sh.getName() !== "주문" || r.getColumn() !== 6 || r.getRow() < 2) return;
  if (r.getValue() !== true) return;
  const row = sh.getRange(r.getRow(), 1, 1, 10).getValues()[0];
  if (row[6]) return; // 이미 발급
  const add = Number(row[4]); let code = row[8] ? cc(row[8]) : "";
  if (code && jget("c_" + code)) lock(function () { const c = jget("c_" + code); c.b += add; jset("c_" + code, c); });
  else code = mint(add, "주문 " + row[1]);
  sh.getRange(r.getRow(), 7).setValue(code);
  if (row[9]) jset("o_" + row[9], { order: row[1], code: code, credits: add }); // 주문한 브라우저에 자동 반영
  MailApp.sendEmail({ to: row[2], name: "찰칵상세",
    subject: "[찰칵상세] " + add + "크레딧 충전이 완료됐어요",
    body: "안녕하세요, 찰칵상세예요.\n충전해 주셔서 감사합니다.\n주문하신 브라우저에는 크레딧이 자동으로 들어가 있어요.\n다른 기기에서 쓰실 때는 아래 코드를 넣어 주세요.\n\n크레딧 코드: " + code + "\n이번 충전: " + add + "크레딧 (지금 잔액 " + (jget("c_" + code) || {}).b + ")\n\n사용 방법\n1) https://kisthestar1-boop.github.io/ttukttak/ 접속\n2) 작업 화면 위쪽 '크레딧 코드' 칸에 코드 입력\n3) 사진 올리고 만들기 — 상세페이지 1건 50크레딧, 사진 다시 찍기 2크레딧\n\n코드는 다른 사람과 나누지 말아 주세요. 궁금한 점은 이 메일에 답장 주세요.\n찰칵상세 드림" });
  sh.getRange(r.getRow(), 8).setValue(new Date());
}
/* 처음 한 번 실행: 시트 만들기 + 체크 트리거 연결 (권한 허용 필요) */
function setup() {
  const sh = sheet();
  ScriptApp.getProjectTriggers().forEach(function (t) { if (t.getHandlerFunction() === "onOrderEdit") ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger("onOrderEdit").forSpreadsheet(sh.getParent()).onEdit().create();
  Logger.log("주문 시트: " + sh.getParent().getUrl());
}
/* 테스트·선물용 코드 (편집기에서 실행 → 실행 기록에 코드가 보여요) */
function mintTest50() { Logger.log(mint(50, "테스트")); }
function out(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
