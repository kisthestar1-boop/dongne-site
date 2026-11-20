# 공룡이 우편 영업 — 학원별 편지(A4) + 방문 전단(A5) HTML 생성
import json, qrcode, os, html
D = os.path.dirname(os.path.abspath(__file__))
SUBJ = {"em": "영어·수학", "e": "영어", "m": "수학"}

def guess_subj(name):
    if "영어" in name and "수학" in name: return "em"
    if "수학" in name: return "m"
    if "영어" in name or "잉글" in name or "어학" in name: return "e"
    return "em"

def obs(a):
    n = a.get("note", "")
    if "블로그" in n: return "지금은 네이버 블로그만 보여서, 시간표·교습비·상담 신청을 한 번에 보기가 어려워요."
    if "운영 시간" in n: return "지도에 운영 시간이 비어 있고, 학원을 소개하는 홈페이지가 보이지 않아요."
    if "교습소" in n: return "교습소는 소개할 곳이 적어서, 학부모님이 수업 방식을 미리 알기 어려워요."
    return "학원 이름으로 검색했을 때 학원을 소개하는 홈페이지가 보이지 않아요."

CSS = """
@page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;font-family:Pretendard,'Noto Sans CJK KR',sans-serif;color:#1A1A2E;word-break:keep-all}
.pg{width:210mm;height:297mm;padding:16mm 16mm 12mm;position:relative;overflow:hidden;background:#fff}
.top{display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid #1A1A2E;padding-bottom:5mm}
.logo{font-weight:900;font-size:20pt;letter-spacing:-.02em}.logo b{color:#2F6BFF}
.top small{font-size:9pt;color:#666}
.to{margin:6mm 0 2mm;font-size:12pt;color:#444}
h1{font-size:21pt;line-height:1.28;margin:0 0 4mm;letter-spacing:-.02em}
h1 em{font-style:normal;background:linear-gradient(transparent 58%,#FFE45C 58%)}
.obs{background:#F3F6FF;border-left:4px solid #2F6BFF;padding:4mm 5mm;border-radius:2mm;font-size:11pt;line-height:1.6}
.obs b{color:#2F6BFF}
.phones{display:flex;gap:6mm;justify-content:center;margin:5mm 0 2mm}
.ph{width:36mm;text-align:center}.ph div{height:70mm;border:2.4mm solid #1A1A2E;border-radius:6mm;overflow:hidden;background:#eee}
.ph img{width:100%;display:block}.ph small{display:block;margin-top:2mm;font-size:8.5pt;color:#555}
.cap{text-align:center;font-size:9pt;color:#777;margin-bottom:5mm}
.offer{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm;font-size:10.5pt;margin-bottom:5mm}
.offer div:before{content:"✔ ";color:#2F6BFF;font-weight:900}
.cta{display:flex;gap:6mm;align-items:center;background:#1A1A2E;color:#fff;border-radius:4mm;padding:5mm 6mm}
.cta img.qr{width:30mm;height:30mm;background:#fff;padding:1.5mm;border-radius:2mm}
.cta b{font-size:14pt;display:block;margin-bottom:1.5mm}.cta p{margin:0;font-size:10pt;line-height:1.6;color:#DDE3FF}
.seo{display:flex;gap:5mm;align-items:center;border:1.5px solid #DCE3F5;border-radius:3mm;padding:3.5mm 5mm;margin:0 0 5mm;background:#FBFCFF}.seo .sb{flex:1.1;background:#fff;border:1px solid #DADCE0;border-radius:99px;padding:2mm 4mm;font-size:10pt;color:#202124;box-shadow:0 1px 4px rgba(0,0,0,.08)}.seo .sb span{color:#4285F4;font-weight:900;margin-right:2mm}.seo .rs{flex:1.4;font-size:8.5pt;line-height:1.45}.seo .rs b{color:#1A0DAB;font-size:10pt;display:block}.seo .rs i{font-style:normal;color:#188038}.seo .tx{flex:1.3;font-size:9.5pt;line-height:1.5}.seo .tx b{color:#2F6BFF}.dino{position:absolute;right:12mm;top:62mm;width:30mm}
.bub{position:absolute;right:40mm;top:60mm;background:#fff;border:1.5px solid #1A1A2E;border-radius:4mm;padding:2mm 3mm;font-size:9pt;font-weight:800}
.foot{position:absolute;left:16mm;right:16mm;bottom:9mm;font-size:8pt;color:#888;display:flex;justify-content:space-between}
"""

def seo(q, title):
    return f"""<div class="seo"><div class="sb"><span>G</span>{q}</div><div class="rs"><i>원장님학원.kr ›</i><b>{title}</b>시간표 · 교습비 · 상담 신청까지 한 번에</div><div class="tx"><b>구글 · 네이버 검색 노출</b><br>"동네 + 과목" 검색에 잘 나오도록 제목·지도·검색 등록까지 세팅해 드려요</div></div>"""

def phones():
    return """<div class="phones"><div class="ph"><div><img src="pf_ac_m.jpg"></div><small>영어·수학 학원</small></div><div class="ph"><div><img src="pf_bu_m.jpg"></div><small>다이어트댄스</small></div><div class="ph"><div><img src="pf_pl_m.jpg"></div><small>필라테스 스튜디오</small></div></div>
<div class="cap">찰칵홈이 만든 홈페이지 예시 — 휴대폰으로 보는 화면이에요</div>"""

def letter(a):
    subj = SUBJ.get(a.get("subj") or guess_subj(a["name"]), "영어·수학")
    q = f"qr_{a['slug']}.png"
    qrcode.make(f"https://kisthestar1-boop.github.io/minsung-ai/web/?src=mail_{a['slug']}#contact", box_size=10, border=1).save(os.path.join(D, q))
    N = html.escape(a["name"])
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="pg">
<div class="top"><div class="logo">찰칵<b>홈</b></div><small>장유 동네 학원 홈페이지 · 김해 장유</small></div>
<div class="to">{N} 원장님께</div>
<h1>학부모님이 휴대폰으로<br><em>"장유 {subj} 학원"</em>을 검색하면<br>원장님 학원이 보이시나요?</h1>
<div class="obs"><b>살펴보니</b> · {html.escape(obs(a))}<br>요즘 학부모님은 상담 전화 전에 휴대폰으로 먼저 비교해 보세요.</div>
<img class="dino" src="dino.png"><div class="bub">시안은 무료예요!</div>
{phones()}
{seo("장유 "+subj+" 학원", N+" | 장유 "+subj+" 학원")}
<div class="offer"><div>원장님 학원 사진으로 <b>무료 시안</b> 먼저</div><div>시간표 · 교습비 · 등록번호 표시까지</div><div>상담 신청 → 원장님 휴대폰으로 알림</div><div>사이트 주소 · 도메인은 원장님 소유</div><div>원장님이 직접 소식 · 사진 수정</div><div>마음에 드실 때만 제작 (부담 없어요)</div></div>
<div class="cta"><img class="qr" src="{q}"><div><b>QR을 찍으면 예시를 바로 볼 수 있어요</b><p>무료 시안 신청 · 문의: <b style="display:inline;font-size:10.5pt">kisthestar1@gmail.com</b><br>학원 사진 3장과 학원 이름만 보내 주시면, 3일 안에 시안을 보내 드릴게요.</p></div></div>
<div class="foot"><span>찰칵홈 · 김해 장유 · 동네 학원 · 가게 홈페이지</span><span>필요 없으시면 버려 주세요. 다시 보내지 않을게요.</span></div>
</div></body></html>"""

FCSS = CSS.replace("@page{size:A4;margin:0}", "@page{size:A5;margin:0}").replace(".pg{width:210mm;height:297mm;padding:16mm 16mm 12mm", ".pg{width:148mm;height:210mm;padding:10mm 10mm 8mm")
def flyer():
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{FCSS}
h1{{font-size:18pt}}.seo{{padding:2.5mm 3mm;gap:3mm;margin-bottom:3mm}}.seo .sb{{font-size:8pt;padding:1.5mm 2.5mm}}.seo .rs{{font-size:7pt}}.seo .rs b{{font-size:8pt}}.seo .tx{{font-size:7.5pt}}.ph{{width:27mm}}.ph div{{height:50mm;border-width:1.8mm}}.offer{{font-size:9pt;gap:1.5mm 4mm}}.cta img.qr{{width:24mm;height:24mm}}.cta b{{font-size:11.5pt}}.cta p{{font-size:8.5pt}}
.dino{{right:8mm;top:30mm;width:24mm}}.bub{{right:30mm;top:30mm;font-size:8pt}}.foot{{left:10mm;right:10mm;bottom:5mm;font-size:7pt}}</style></head><body><div class="pg">
<div class="top"><div class="logo">찰칵<b>홈</b></div><small>장유 학원 · 가게 홈페이지</small></div>
<h1 style="margin-top:7mm">원장님 학원,<br><em>홈페이지 무료 시안</em><br>먼저 받아 보세요</h1>
<img class="dino" src="dino.png"><div class="bub">사진 3장이면 돼요!</div>
{phones()}
{seo("장유 피아노 학원","○○피아노학원 | 장유 피아노")}
<div class="offer"><div>시간표 · 교습비 표시</div><div>상담 신청 휴대폰 알림</div><div>원장님이 직접 소식 수정</div><div>마음에 들 때만 제작</div></div>
<div class="cta"><img class="qr" src="qr_flyer.png"><div><b>QR로 예시 보기 · 시안 신청</b><p>kisthestar1@gmail.com<br>학원 사진 3장 + 이름 → 3일 안에 시안</p></div></div>
<div class="foot"><span>찰칵홈 · 김해 장유</span><span>직접 전해 드리는 안내지예요</span></div>
</div></body></html>"""

if __name__ == "__main__":
    L = json.load(open(os.path.join(D, "targets.json")))
    for a in L:
        open(os.path.join(D, f"letter_{a['slug']}.html"), "w").write(letter(a))
    open(os.path.join(D, "flyer.html"), "w").write(flyer())
    print(len(L), "letters + flyer")
