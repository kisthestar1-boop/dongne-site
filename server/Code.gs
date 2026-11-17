// 찰칵상세 AI 서버 (Google Apps Script) — 키는 스크립트 속성 GEMINI_KEY 에만 둔다
const TXT = ["gemini-3.5-flash", "gemini-flash-latest", "gemini-2.5-flash", "gemini-3.1-flash-lite"];
const IMG = ["gemini-3.1-flash-image", "gemini-2.5-flash-image", "gemini-3.1-flash-lite-image"];
const LIMIT = { copy: 150, scene: 600 }; // 하루 최대 (요금 폭주 방지)

function doGet() { return out({ ok: true, service: "chalkak-ai" }); }

function doPost(e) {
  try {
    const q = JSON.parse(e.postData.contents);
    if (q.op === "list") {
      const k0 = PropertiesService.getScriptProperties().getProperty("GEMINI_KEY");
      const lr = UrlFetchApp.fetch("https://generativelanguage.googleapis.com/v1beta/models?pageSize=200", { headers: { "x-goog-api-key": k0 }, muteHttpExceptions: true });
      const lj = JSON.parse(lr.getContentText());
      return out({ models: (lj.models || []).map(function (m) { return m.name.replace("models/", ""); }) });
    }
    if (q.op !== "copy" && q.op !== "scene") return out({ error: "잘못된 요청" });
    if (e.postData.contents.length > 6000000) return out({ error: "사진이 너무 커요" });
    const key = PropertiesService.getScriptProperties().getProperty("GEMINI_KEY");
    if (!key) return out({ error: "서버에 AI 키가 아직 없어요" });
    if (!countOk(q.op)) return out({ error: "오늘 생성 한도를 다 썼어요. 내일 다시 해 주세요" });
    const models = q.op === "scene" ? IMG : TXT;
    let last = "모델을 찾지 못했어요";
    for (const m of models) {
      const r = UrlFetchApp.fetch("https://generativelanguage.googleapis.com/v1beta/models/" + m + ":generateContent", {
        method: "post", contentType: "application/json", payload: JSON.stringify(q.body),
        headers: { "x-goog-api-key": key }, muteHttpExceptions: true });
      const code = r.getResponseCode();
      if (code === 404) { last = "모델 없음 " + m; continue; }
      const j = JSON.parse(r.getContentText());
      if (code === 503 || code === 500) { last = (j.error && j.error.message) || ("오류 " + code); continue; }
      if (code >= 400) return out({ error: (j.error && j.error.message) || ("오류 " + code) });
      return out(j);
    }
    return out({ error: last });
  } catch (err) { return out({ error: String(err) }); }
}

function countOk(op) {
  const lock = LockService.getScriptLock(); lock.waitLock(5000);
  try {
    const p = PropertiesService.getScriptProperties();
    const k = "n_" + op + "_" + Utilities.formatDate(new Date(), "Asia/Seoul", "yyyyMMdd");
    const n = Number(p.getProperty(k) || 0);
    if (n >= LIMIT[op]) return false;
    p.setProperty(k, String(n + 1)); return true;
  } finally { lock.releaseLock(); }
}

function out(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
