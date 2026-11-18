"""달빛툰 1화 세로 웹툰 조립: 컷(제미나이) + 말풍선·내레이션·효과음(코드) → 800px 세로 → 1280px 조각"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math

W = 800
SRC = "/home/claude/dongne-site/_stage/ep1"
OUT = "/home/claude/dongne-site/_stage/ep1_out"
os.makedirs(OUT, exist_ok=True)
SANS = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SANSB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-SemiBold.ttc"
FD = "/home/claude/dongne-site/toon_tools/fonts/"
TALK = FD + "Jua-Regular.ttf"; LOUD = FD + "BlackHanSans-Regular.ttf"; NARR = FD + "GowunBatang-Regular.ttf"; NARRB = FD + "GowunBatang-Bold.ttf"
F = lambda p, s: ImageFont.truetype(p, s, index=1) if p.endswith(".ttc") else ImageFont.truetype(p, s)  # KR
BG = (12, 14, 22)


def panel(n, width=W, crop_top=165):
    im = Image.open(f"{SRC}/p{n:02d}.jpg").convert("RGB")
    im = im.crop((0, crop_top, im.width, im.height))
    h = round(im.height * width / im.width)
    return im.resize((width, h), Image.LANCZOS)


def wrap(d, text, font, maxw):
    out = []
    for para in text.split("\n"):
        line = ""
        for ch in para:
            t = line + ch
            if d.textlength(t, font=font) > maxw and line:
                out.append(line); line = ch
            else:
                line = t
        out.append(line)
    return out


def bubble(img, text, cx, cy, size=30, tail=None, shout=False, maxw=320):
    d = ImageDraw.Draw(img)
    size = int(size * 1.12)
    f = F(LOUD if shout else TALK, size)
    text = text.replace("…", "...")
    lines = wrap(d, text, f, maxw)
    lh = size * 1.3
    tw = max(d.textlength(l, font=f) for l in lines); th = lh * len(lines)
    rx, ry = tw / 2 + size * 1.0, th / 2 + size * 0.95
    if tail:
        tx, ty = tail
        dx, dy = tx - cx, ty - cy; dist = math.hypot(dx, dy); edge = math.hypot(rx * dx / dist, ry * dy / dist)
        L = min(dist, edge + 46); tx, ty = cx + dx / dist * L, cy + dy / dist * L
        ang = math.atan2(ty - cy, tx - cx)
        b1 = (cx + rx * 0.55 * math.cos(ang + 0.35), cy + ry * 0.55 * math.sin(ang + 0.35))
        b2 = (cx + rx * 0.55 * math.cos(ang - 0.35), cy + ry * 0.55 * math.sin(ang - 0.35))
        d.polygon([b1, (tx, ty), b2], fill="white", outline=(28, 26, 30))
    if shout:
        pts = []
        for k in range(28):
            a = k / 28 * 2 * math.pi
            r = 1.18 if k % 2 == 0 else 0.98
            pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
        d.polygon(pts, fill="white", outline=(20, 20, 20), width=3)
    else:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill="white", outline=(28, 26, 30), width=2)
    if tail:  # 꼬리 이음새 덮기
        d.polygon([b1, ((b1[0] + b2[0]) / 2 + (cx - (b1[0] + b2[0]) / 2) * 0.3, (b1[1] + b2[1]) / 2 + (cy - (b1[1] + b2[1]) / 2) * 0.3), b2], fill="white")
    y = cy - th / 2
    for l in lines:
        d.text((cx - d.textlength(l, font=f) / 2, y - size * 0.08), l, font=f, fill=(32, 28, 30)); y += lh


def narration(img, text, x, y, size=26, maxw=560, dark=True):
    d = ImageDraw.Draw(img, "RGBA")
    f = F(NARR, size)
    lines = wrap(d, text, f, maxw)
    lh = size * 1.55
    tw = max(d.textlength(l, font=f) for l in lines)
    pad = 18
    box = [x, y, x + tw + pad * 2, y + lh * len(lines) + pad * 2 - (lh - size)]
    d.rectangle(box, fill=(10, 12, 24, 215) if dark else (250, 247, 240, 235), outline=(255, 255, 255, 60) if dark else (40, 30, 20, 120), width=2)
    yy = y + pad
    for l in lines:
        d.text((x + pad, yy), l, font=f, fill=(238, 236, 228) if dark else (30, 24, 20)); yy += lh


def sfx(img, text, x, y, size=90, color=(255, 255, 255), stroke=(20, 10, 10), rot=-8):
    text = text.replace("…", "...")
    f = F(LOUD, size)
    tmp = Image.new("RGBA", (int(size * len(text) * 1.2 + 40), int(size * 1.6)), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.text((20, 10), text, font=f, fill=color, stroke_width=max(4, size // 14), stroke_fill=stroke)
    tmp = tmp.rotate(rot, expand=True, resample=Image.BICUBIC)
    img.paste(tmp, (int(x), int(y)), tmp)


def card(h, bg=BG):
    return Image.new("RGB", (W, h), bg)


def center_text(img, text, y, font, fill, spacing=1.6):
    d = ImageDraw.Draw(img)
    for i, l in enumerate(text.split("\n")):
        d.text(((W - d.textlength(l, font=font)) / 2, y + i * font.size * spacing), l, font=font, fill=fill)


blocks = []  # (image, gap_after)

# 0. 오프닝: 검은 화면 · 붉은 글씨 (전독시식 첫 화면)
c = card(900)
center_text(c, "…이번이 마지막이다.", 400, F(NARRB, 44), (214, 58, 52))
blocks.append((c, 0))
c = card(520)
center_text(c, "EPISODE 1", 170, F(TALK, 22), (201, 71, 63))
center_text(c, "F급의 수첩", 220, F(NARRB, 58), (240, 238, 232))
center_text(c, "F급 사냥꾼은 99번째 인생을 기억한다", 330, F(TALK, 22), (150, 156, 175))
blocks.append((c, 120))

p = panel(1)
narration(p, "백 년째 아침이 오지 않는 세상.", 30, 30)
bubble(p, "F급 주제에\n조각을 주웠어?", 590, 190, size=30, tail=(520, 330))
sfx(p, "하하하!", 60, 470, size=60, color=(255, 236, 200), rot=6)
blocks.append((p, 60))

p = panel(2)
narration(p, "깨진 달에서 떨어지는 은빛 '달 조각'.\n부수면 산도 밀어낼 힘이 생긴다.", 30, 30)
narration(p, "대신, 기억이 하나 지워진다.", 300, p.height - 120)
blocks.append((p, 60))

p = panel(3)
bubble(p, "이건 그린홀드\n기사단이 가져가지.", 230, 110, size=30, tail=(300, 260))
narration(p, "가문 없는 여우는, 원래 그런 대우를 받았다.", 120, p.height - 100)
blocks.append((p, 280))

p = panel(4)
narration(p, "그날 밤, 그림자 숲.\n그 숲길을 아는 건, 거기서 조각을 줍던 F급뿐이었다.", 30, 30, maxw=640)
bubble(p, "길 안내해.\n조각 값은 쳐주지.", 660, 195, size=26, tail=(610, 300))
narration(p, "조각을 되찾을 수 있다면 — 레온은 따라나섰다.", 230, p.height - 100, maxw=560)
blocks.append((p, 40))

p = panel(5)
narration(p, "길잡이가 아니라 — 미끼였다.", 220, 30)
sfx(p, "그르르…", 470, 560, size=64, color=(230, 60, 60), stroke=(10, 0, 0), rot=-4)
blocks.append((p, 40))

p = panel(6)
bubble(p, "미끼 노릇이나 해라!", 230, 110, size=34, tail=(280, 230), shout=True)
bubble(p, "…!", 560, 600, size=30, tail=(470, 680))
narration(p, "달아나던 바르크의 손에서, 빼앗긴 조각이 떨어졌다.", 40, p.height - 100, maxw=700)
blocks.append((p, 0))

c = card(900)
center_text(c, "레온의 품에는 조각이 하나 더 있었다.", 250, F(NARRB, 28), (200, 205, 220))
center_text(c, "아무에게도 보여 주지 않은, 손톱만 한 조각.", 300, F(NARRB, 22), (150, 156, 175))
center_text(c, "'쓰지 마.'", 480, F(NARRB, 40), (200, 205, 220))
center_text(c, "— 머릿속에서, 내 목소리가 들렸다.", 570, F(NARRB, 22), (120, 126, 145))
blocks.append((c, 0))

p = panel(7)
sfx(p, "콰직", 470, 60, size=110, color=(255, 255, 255), stroke=(40, 40, 80), rot=10)
blocks.append((p, 200))

p = panel(8)
narration(p, "기억이 지워져야 했다.", 30, 30)
narration(p, "그런데 — 반대였다.", 430, p.height - 100)
blocks.append((p, 40))

p = panel(9)
narration(p, "수십 번. 아니, 백 번 가까이 살아 본 기억.\n짐승들이 어디로 뛸지 — 이미 본 적이 있었다.", 30, 30, maxw=640)
bubble(p, "…다음은, 왼쪽.", 600, p.height - 150, size=28, tail=(520, p.height - 260))
blocks.append((p, 40))

p = panel(10)
sfx(p, "서걱!", 470, 90, size=120, color=(255, 255, 255), stroke=(120, 20, 20), rot=-12)
blocks.append((p, 160))

p = panel(11)
bubble(p, "이건 내가 가져가지.", 560, 140, size=32, tail=(520, 300))
narration(p, "바닥에 떨어진, 원래 내 조각.", 40, p.height - 100)
blocks.append((p, 320))

p = panel(12)
narration(p, "기억을 잃을 때마다 적어 두던, 낡은 수첩.", 30, 30)
blocks.append((p, 40))

p = panel(13)
narration(p, "그런데 페이지가 늘어나 있었다.\n처음 보는 — 하지만 틀림없는 내 글씨로.", 30, 30)
blocks.append((p, 0))

c = Image.new("RGB", (W, 760), (236, 226, 204))
d = ImageDraw.Draw(c)
for yy in range(120, 700, 52):
    d.line([(70, yy + 40), (730, yy + 40)], fill=(205, 190, 165), width=1)
fh = F(NARRB, 28)
note = ["1. 사흘 뒤, 붉은 비가 온다. 지붕 아래 있어라.", "2. 동쪽 폐성으로 가라. 그곳이 네 성이다.", "3. 세나를 지켜라. 이번에는 반드시.", "4. 절대 그 여우를 믿지 마라."]
for i, l in enumerate(note):
    d.text((80, 128 + i * 104), l, font=fh, fill=(52, 40, 30))
d.text((440, 560), "— 99번째의 너가.", font=F(NARRB, 30), fill=(52, 40, 30))
blocks.append((c, 0))

p = panel(14)
sfx(p, "…이번이 마지막이다.", 120, 40, size=46, color=(220, 40, 40), stroke=(30, 0, 0), rot=-3)
blocks.append((p, 0))

c = card(560)
center_text(c, "2화 「폐성」에서 계속", 250, F(NARRB, 34), (232, 228, 220))
blocks.append((c, 0))

# 세로로 잇기 (컷 사이 여백 = 연출 속도)
H = sum(b.height + g for b, g in blocks)
strip = Image.new("RGB", (W, H), BG)
y = 0
for b, g in blocks:
    strip.paste(b, (0, y)); y += b.height + g
strip.save(f"{OUT}/ep1_full.jpg", quality=88)
# 1280px 조각
n = 0
for top in range(0, H, 1280):
    n += 1
    strip.crop((0, top, W, min(H, top + 1280))).save(f"{OUT}/ep1_{n:02d}.jpg", quality=88)
print("height", H, "slices", n)
