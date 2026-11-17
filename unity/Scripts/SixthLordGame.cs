// 여섯 번째 성주 (THE SIXTH LORD) · 유니티판 1단계
// 웹판(sixthlord.html + sixthfight.html)을 그대로 옮긴 캐슬파이트식 전투.
// 장면에 아무것도 놓지 않아도, Play를 누르면 이 스크립트가 알아서 화면을 만들어요.
using System.Collections.Generic;
using UnityEngine;

public class SixthLordGame : MonoBehaviour
{
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    static void Boot()
    {
        if (FindAnyObjectByType<SixthLordGame>() != null) return;
        new GameObject("SixthLord").AddComponent<SixthLordGame>();
    }

    // ===== 데이터 =====
    class Def { public string id, nm; public int rar, el, n; public float hp, atk, rng, spd, acd; public string sp; }
    static Def D(string id, string nm, int rar, int el, float hp, float atk, float rng, float spd, float acd, string sp, int n)
        => new Def { id = id, nm = nm, rar = rar, el = el, hp = hp, atk = atk, rng = rng, spd = spd, acd = acd, sp = sp, n = n };
    static readonly Def[] DEFS = {
        D("fox","여우 궁수",0,3,70,13,120,42,1.0f,"",2), D("wolf","늑대 사냥꾼",0,3,95,15,22,58,0.9f,"pack",2),
        D("owl","부엉이 마법사",1,5,75,20,130,38,1.6f,"splash",1), D("bear","곰 거인",1,6,480,28,24,30,1.4f,"",1),
        D("boar","멧돼지 돌격병",0,3,130,16,22,62,1.0f,"charge",1), D("rhino","코뿔소 파괴자",2,6,520,34,26,34,1.5f,"siege",1),
        D("croc","악어 투사",1,5,260,24,24,36,1.2f,"splash",1), D("turtle","거북 수호병",0,4,320,12,22,28,1.2f,"",1),
        D("snake","독사 암살자",1,3,55,12,22,55,0.8f,"poison",2), D("lion","사자왕",3,7,560,44,26,40,1.2f,"aura",1),
        D("panther","흑표범 자객",2,4,85,32,22,64,0.8f,"assassin",1), D("elephant","코끼리 전차",2,7,720,30,26,26,1.5f,"",1),
        D("hawk","매 척후병",0,2,45,9,22,80,0.6f,"",2), D("phoenix","불사조 현자",3,6,150,38,120,40,1.4f,"splash rebirth",1),
        D("dragon","용왕",3,8,640,52,130,30,1.8f,"splash",1), D("bunny","토끼 치유사",1,4,60,0,100,40,1.5f,"heal",1),
    };
    static Def Get(string id) { foreach (var d in DEFS) if (d.id == id) return d; return DEFS[0]; }
    static readonly Color[] RC = { new Color(.6f,.64f,.71f), new Color(.31f,.64f,1f), new Color(.7f,.42f,1f), new Color(1f,.69f,.24f) };

    class Lord { public string id, house, nm, motto; public string[] cards; public int idx; }
    static readonly Lord[] LORDS = {
        new Lord{id="green",house="그린홀드",nm="늑대 성주 그레이",motto="화살은 잊지 않는다",cards=new[]{"fox","wolf","owl"},idx=0},
        new Lord{id="mud",house="머드리버",nm="악어 성주 녹스",motto="기다리는 자가 살아남는다",cards=new[]{"croc","turtle","snake"},idx=1},
        new Lord{id="stone",house="스톤팡",nm="곰 성주 모쿠",motto="무너지는 것은 성벽뿐",cards=new[]{"boar","bear","rhino"},idx=2},
        new Lord{id="sun",house="썬메인",nm="사자 성주 아즈란",motto="왕좌는 빈 적이 없다",cards=new[]{"panther","elephant","lion"},idx=3},
        new Lord{id="ever",house="에버플레임",nm="용 성주 이그니스",motto="불은 꺼지지 않는다",cards=new[]{"hawk","phoenix","dragon"},idx=4},
    };
    static float Cost(string id) => 30 + Get(id).el * 18;
    static float Every(string id) => 6 + Get(id).el * 1.5f;

    // ===== 그림 =====
    readonly Dictionary<string, Texture2D> tex = new();
    readonly Dictionary<string, Sprite> spr = new();
    Sprite white; Material lineMat; Font font;
    Texture2D T(string path) { if (!tex.TryGetValue(path, out var t)) { t = Resources.Load<Texture2D>(path); tex[path] = t; } return t; }
    Sprite Round(string path, Color ring, bool square = false)
    {
        string key = path + ring + square;
        if (spr.TryGetValue(key, out var s)) return s;
        var src = T(path); const int N = 128;
        var o = new Texture2D(N, N, TextureFormat.RGBA32, false) { filterMode = FilterMode.Bilinear, wrapMode = TextureWrapMode.Clamp };
        var px = new Color[N * N]; float c = (N - 1) / 2f;
        for (int y = 0; y < N; y++) for (int x = 0; x < N; x++)
        {
            float d = square ? Mathf.Max(Mathf.Abs(x - c), Mathf.Abs(y - c)) : Mathf.Sqrt((x - c) * (x - c) + (y - c) * (y - c));
            Color col = Color.clear;
            if (d <= c - 6 && src != null) col = src.GetPixelBilinear(x / (float)N, y / (float)N);
            else if (d <= c - 6) col = new Color(.15f, .15f, .18f);
            else if (d <= c) col = ring;
            px[y * N + x] = col;
        }
        o.SetPixels(px); o.Apply();
        s = Sprite.Create(o, new Rect(0, 0, N, N), new Vector2(.5f, .5f), N);
        spr[key] = s; return s;
    }

    // ===== 상태 =====
    enum Scr { Title, Menu, Camp, Coll, Battle }
    Scr scr = Scr.Title;
    Lord foe; bool over, win; float resultT;
    const float L = 1000, W = 400;
    static Vector3 WP(float x, float y) => new Vector3((x - 500) / 50f, (200 - y) / 50f, 0);

    class Ent
    {
        public int kind, t; public string id; public float x, y, hp, mhp, atk, rng, spd, acd, cd, r, dot, dotT, fl, lunge; public string sp = "";
        public int reb, used, lv = 1, ulv = 1; public GameObject go; public SpriteRenderer sr; public Transform bar, barBg;
    }
    class Plot { public float x, y; public Ent b; }
    class Fx { public GameObject go; public Vector3 v; public float life, max; public bool ring; public float rr; }
    readonly List<Ent> units = new(); Ent[] cast = new Ent[2]; Plot[][] plots = new Plot[2][];
    readonly List<Fx> fxs = new();
    float[] gold = new float[2], inc = new float[2]; int[] kills = new int[2];
    float tm, aiT, spd = 1, shake; List<string> aiCards; List<string> myCards;
    Transform world; Camera cam;

    void Awake()
    {
        Application.targetFrameRate = 60;
        var t = new Texture2D(4, 4); var p = new Color[16]; for (int i = 0; i < 16; i++) p[i] = Color.white; t.SetPixels(p); t.Apply();
        white = Sprite.Create(t, new Rect(0, 0, 4, 4), new Vector2(.5f, .5f), 4);
        lineMat = new Material(Shader.Find("Sprites/Default"));
        cam = Camera.main; if (cam == null) { cam = new GameObject("Main Camera").AddComponent<Camera>(); cam.tag = "MainCamera"; }
        cam.orthographic = true; cam.clearFlags = CameraClearFlags.SolidColor; cam.backgroundColor = new Color(.03f, .03f, .04f);
        cam.transform.position = new Vector3(0, -0.6f, -10);
    }

    // ===== 전투 시작 =====
    void StartBattle(Lord l)
    {
        foe = l; scr = Scr.Battle; over = false; tm = 0; spd = 1;
        if (world != null) Destroy(world.gameObject);
        world = new GameObject("World").transform; units.Clear(); fxs.Clear();
        // 바닥
        var f = T("field");
        if (f != null)
        {
            var fs = new GameObject("Field").AddComponent<SpriteRenderer>(); fs.transform.SetParent(world);
            fs.sprite = Sprite.Create(f, new Rect(0, 0, f.width, f.height), new Vector2(.5f, .5f), f.width / 22f);
            fs.sortingOrder = -10; fs.color = new Color(.85f, .85f, .85f);
        }
        gold[0] = 120; gold[1] = 120 + l.idx * 25; kills[0] = kills[1] = 0;
        inc[0] = 6; inc[1] = 5 * (l.idx == 0 ? .55f : .8f + l.idx * .08f);
        for (int t = 0; t < 2; t++)
        {
            cast[t] = MakeEnt(2, t, t == 0 ? "lords/me" : "lords/" + l.id, t == 0 ? 40 : L - 40, W / 2, 3000, 34, 2.4f);
            var xs = t == 0 ? new[] { 120f, 185f } : new[] { 880f, 815f };
            var list = new List<Plot>(); foreach (var y in new[] { 120f, 200f, 280f }) foreach (var x in xs) list.Add(new Plot { x = x, y = y });
            plots[t] = list.ToArray();
        }
        aiCards = new List<string>(l.cards); if (l.idx >= 2) aiCards.AddRange(new[] { "wolf", "fox" }); if (l.idx >= 4) aiCards.AddRange(new[] { "owl", "croc" });
        myCards = new List<string> { "hawk", "fox", "boar", "wolf", "turtle", "bunny" };
        foreach (var lo in LORDS) if (PlayerPrefs.GetInt("camp_" + lo.id) == 1) foreach (var c in lo.cards) if (!myCards.Contains(c) && myCards.Count < 8) myCards.Add(c);
        aiT = 1;
    }

    Ent MakeEnt(int kind, int t, string img, float x, float y, float hp, float r, float size)
    {
        var e = new Ent { kind = kind, t = t, x = x, y = y, hp = hp, mhp = hp, r = r };
        e.go = new GameObject(img); e.go.transform.SetParent(world);
        e.sr = e.go.AddComponent<SpriteRenderer>();
        e.sr.sprite = Round(img, t == 0 ? new Color(.25f, .75f, .42f) : new Color(.88f, .35f, .29f), kind == 1);
        e.go.transform.localScale = Vector3.one * size; e.sr.sortingOrder = kind == 2 ? 2 : 5;
        var bg = new GameObject("hpbg").AddComponent<SpriteRenderer>(); bg.sprite = white; bg.color = new Color(0, 0, 0, .7f); bg.sortingOrder = 20;
        var fg = new GameObject("hp").AddComponent<SpriteRenderer>(); fg.sprite = white; fg.color = t == 0 ? new Color(.25f, .75f, .42f) : new Color(.88f, .35f, .29f); fg.sortingOrder = 21;
        bg.transform.SetParent(world); fg.transform.SetParent(world); e.barBg = bg.transform; e.bar = fg.transform;
        return e;
    }

    bool Build(int t, string id)
    {
        Plot P = null; foreach (var p in plots[t]) if (p.b == null) { P = p; break; }
        float c = Cost(id); if (P == null || gold[t] < c) return false;
        gold[t] -= c;
        var b = MakeEnt(1, t, "heroes/" + id, P.x, P.y, 380, 20, 1.15f); b.id = id; b.cd = 1.2f; b.ulv = t == 1 ? 1 + foe.idx / 2 : 1;
        P.b = b; Ring(P.x, P.y, new Color(1f, .85f, .45f), .5f, 1.6f); Burst(P.x, P.y, new Color(.8f, .7f, .55f), 10, 2.2f);
        return true;
    }
    float UpCost(Ent b) => Mathf.Round(Cost(b.id) * .9f * b.lv);
    bool Upgrade(int t, Ent b)
    {
        if (b.lv >= 3 || gold[t] < UpCost(b)) return false;
        gold[t] -= UpCost(b); b.lv++; b.mhp += 120; b.hp = b.mhp; Ring(b.x, b.y, new Color(.5f, 1f, .6f), .6f, 1.8f); return true;
    }
    void Spawn(Ent b)
    {
        var d = Get(b.id); float m = (1 + (b.ulv - 1) * .1f) * (1 + (b.lv - 1) * .25f);
        for (int i = 0; i < d.n; i++)
        {
            var u = MakeEnt(0, b.t, "heroes/" + b.id, b.x + (b.t == 1 ? -24 : 24), b.y + (i > 0 ? 14 : 0) + Random.Range(-5f, 5f), d.hp * m, d.hp > 400 ? 15 : 11, d.hp > 400 ? .8f : .6f);
            u.id = b.id; u.atk = d.atk * m; u.rng = d.rng; u.spd = d.spd * Random.Range(.95f, 1.05f); u.acd = d.acd; u.cd = .3f; u.sp = d.sp; u.reb = d.sp.Contains("rebirth") ? 1 : 0;
            units.Add(u);
        }
        Ring(b.x, b.y, b.t == 0 ? new Color(.5f, 1f, .6f) : new Color(.9f, .4f, .3f), .35f, .7f);
    }

    static float Dist(Ent a, Ent b) => Mathf.Sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y));
    IEnumerable<Ent> Foes(Ent e)
    {
        foreach (var u in units) if (u.t != e.t && u.hp > 0) yield return u;
        foreach (var p in plots[1 - e.t]) if (p.b != null) yield return p.b;
        yield return cast[1 - e.t];
    }
    void Dmg(Ent tg, float d, Ent src)
    {
        if (tg.hp <= 0) return;
        if (src != null && src.sp.Contains("siege") && tg.kind != 0) d *= 3;
        tg.hp -= d; tg.fl = .12f;
        if (d >= 1) Txt(tg.x, tg.y - tg.r, "-" + Mathf.RoundToInt(d), tg.t == 1 ? new Color(1f, .88f, .55f) : new Color(1f, .55f, .48f), d >= 40);
        if (src != null && src.sp.Contains("poison") && tg.kind == 0) { tg.dot = 6; tg.dotT = 3; }
        if (tg.kind == 2) shake = Mathf.Max(shake, tg.t == 1 ? .08f : .12f);
        if (tg.hp <= 0) Die(tg);
    }
    void Die(Ent e)
    {
        if (e.kind == 0)
        {
            if (e.reb == 1) { e.reb = 0; e.hp = e.mhp * .5f; Txt(e.x, e.y - 20, "부활", new Color(1f, .7f, .25f), true); return; }
            int k = 1 - e.t; int bonus = Mathf.RoundToInt(3 + Get(e.id).el * 1.5f); gold[k] += bonus; kills[k]++;
            if (k == 0) Txt(e.x, e.y - 20, "+" + bonus, new Color(1f, .85f, .45f), false);
            Ring(e.x, e.y, e.t == 1 ? new Color(.9f, .35f, .3f) : new Color(.25f, .75f, .42f), .3f, .9f);
            Burst(e.x, e.y, e.t == 1 ? new Color(.9f, .35f, .3f) : new Color(.25f, .75f, .42f), 10, 2.6f);
        }
        if (e.kind == 1) { foreach (var p in plots[e.t]) if (p.b == e) p.b = null; Burst(e.x, e.y, Color.white, 16, 3f); shake = .1f; }
        if (e.kind == 2)
        {
            Burst(e.x, e.y, new Color(1f, .6f, .25f), 40, 6f);
            for (int i = 0; i < 3; i++) Ring(e.x, e.y, new Color(1f, .88f, .55f), .6f + i * .25f, 2.4f + i * 1.2f);
            shake = .3f; over = true; win = e.t == 1; resultT = 1.4f; Save();
        }
        if (e.go != null && e.kind != 2) { Destroy(e.go); Destroy(e.bar.gameObject); Destroy(e.barBg.gameObject); }
    }
    void Save()
    {
        int g = win ? 40 + foe.idx * 15 : 12;
        PlayerPrefs.SetInt("gold", PlayerPrefs.GetInt("gold", 300) + g);
        if (win) { PlayerPrefs.SetInt("camp_" + foe.id, 1); PlayerPrefs.SetInt("tro", PlayerPrefs.GetInt("tro") + 20); }
        PlayerPrefs.Save();
    }

    // ===== 한 틱 =====
    void Step(float dt)
    {
        if (over) return;
        tm += dt;
        for (int t = 0; t < 2; t++) gold[t] += inc[t] * dt;
        for (int t = 0; t < 2; t++) foreach (var p in plots[t]) if (p.b != null)
        {
            p.b.cd -= dt;
            if (p.b.cd <= 0) { p.b.cd = Every(p.b.id) * Mathf.Pow(.82f, p.b.lv - 1); Spawn(p.b); }
        }
        foreach (var c in cast)
        {
            c.cd -= dt; if (c.cd > 0) continue;
            Ent tg = null; float bd = 190;
            foreach (var u in units) if (u.t != c.t && u.hp > 0) { float d = Dist(u, c); if (d < bd) { bd = d; tg = u; } }
            if (tg != null) { c.cd = .9f; Shot(c.x, c.y - 20, tg.x, tg.y, c.t == 1 ? new Color(.94f, .6f, .48f) : new Color(.75f, .9f, 1f)); Dmg(tg, 30, null); }
        }
        var lions = units.FindAll(u => u.sp == "aura" && u.hp > 0);
        foreach (var u in units.ToArray())
        {
            if (u.hp <= 0) continue;
            u.fl = Mathf.Max(0, u.fl - dt); u.lunge = Mathf.Max(0, u.lunge - dt);
            if (u.dotT > 0) { u.dotT -= dt; u.hp -= u.dot * dt; if (u.hp <= 0) { Die(u); continue; } }
            u.cd -= dt; int dir = u.t == 1 ? -1 : 1;
            if (u.sp == "heal")
            {
                Ent al = null; float best = 2;
                foreach (var a in units) if (a.t == u.t && a != u && a.hp > 0 && a.hp < a.mhp && Dist(a, u) < u.rng) { float r = a.hp / a.mhp; if (r < best) { best = r; al = a; } }
                if (al != null) { if (u.cd <= 0) { u.cd = u.acd; al.hp = Mathf.Min(al.mhp, al.hp + 14 * (u.mhp / 60)); Txt(al.x, al.y - 16, "+", new Color(.5f, 1f, .6f), false); } }
                else
                {
                    Ent lead = null; foreach (var a in units) if (a.t == u.t && a != u && a.hp > 0 && (lead == null || dir * (a.x - lead.x) > 0)) lead = a;
                    float gx = lead != null ? lead.x - dir * 40 : u.x + dir * 20; u.x += Mathf.Sign(gx - u.x) * Mathf.Min(Mathf.Abs(gx - u.x), u.spd * dt);
                }
                continue;
            }
            var F = new List<Ent>(Foes(u));
            if (u.sp == "assassin") { var rr = F.FindAll(f => f.kind == 0 && f.rng > 60 && Dist(f, u) < 220); if (rr.Count > 0) F = rr; }
            Ent tg = null; float bdist = 1e9f;
            foreach (var f in F) { float d = Dist(f, u) - (f.kind == 0 ? 0 : f.r * .6f); if (d < bdist && (d < 170 || f.kind != 0)) { bdist = d; tg = f; } }
            if (tg != null && tg.kind != 0 && bdist > 170 && bdist >= 260) tg = null;
            float reach = u.rng + (tg != null ? tg.r : 0);
            if (tg != null && Dist(tg, u) <= reach)
            {
                if (u.cd <= 0)
                {
                    float a = u.atk;
                    if (u.sp == "pack") foreach (var o in units) if (o != u && o.id == u.id && o.t == u.t && Dist(o, u) < 60) { a *= 1.3f; break; }
                    foreach (var l in lions) if (l.t == u.t && Dist(l, u) < 120) { a *= 1.15f; break; }
                    u.cd = u.acd;
                    if (u.rng > 60) Shot(u.x, u.y, tg.x, tg.y, u.sp.Contains("splash") ? new Color(.75f, .55f, 1f) : new Color(1f, .92f, .65f)); else u.lunge = .12f;
                    if (u.sp.Contains("splash")) { foreach (var f in F) if (f.kind == 0 && f != tg && Dist(f, tg) < 44) Dmg(f, a * .6f, u); Ring(tg.x, tg.y, new Color(.75f, .55f, 1f), .3f, .9f); }
                    if (u.sp == "charge" && u.used == 0) { a *= 2; u.used = 1; }
                    Dmg(tg, a, u);
                }
            }
            else
            {
                float gx = tg != null ? tg.x : u.x + dir * 50, gy = tg != null ? tg.y : u.y + (W / 2 - u.y) * .02f;
                float d = Mathf.Max(.01f, Mathf.Sqrt((gx - u.x) * (gx - u.x) + (gy - u.y) * (gy - u.y)));
                float sp = u.spd * (u.sp == "charge" && u.used == 0 ? 1.4f : 1);
                u.x += (gx - u.x) / d * sp * dt; u.y += (gy - u.y) / d * sp * dt * .8f;
            }
            u.y = Mathf.Clamp(u.y, 40, W - 40);
        }
        // 겹침 풀기
        for (int i = 0; i < units.Count; i++) for (int j = i + 1; j < units.Count; j++)
        {
            var a = units[i]; var b = units[j]; if (a.hp <= 0 || b.hp <= 0) continue;
            float d = Dist(a, b), m = a.r + b.r - 4;
            if (d < m && d > 0) { float p = (m - d) / 2, nx = (a.x - b.x) / d, ny = (a.y - b.y) / d; a.x += nx * p; a.y += ny * p; b.x -= nx * p; b.y -= ny * p; }
        }
        units.RemoveAll(u => u.hp <= 0);
        // 상대 AI
        aiT -= dt;
        if (aiT <= 0)
        {
            aiT = 1.2f; bool free = false; foreach (var p in plots[1]) if (p.b == null) free = true;
            string want = aiCards[Random.Range(0, aiCards.Count)];
            if (free && gold[1] >= Cost(want)) Build(1, want);
            else if (!free || gold[1] > 260) { Ent low = null; foreach (var p in plots[1]) if (p.b != null && p.b.lv < 3 && (low == null || p.b.lv < low.lv)) low = p.b; if (low != null) Upgrade(1, low); }
        }
    }

    // ===== 효과 =====
    void Txt(float x, float y, string s, Color c, bool big)
    {
        var go = new GameObject("txt"); go.transform.SetParent(world); go.transform.position = WP(x, y);
        var tmesh = go.AddComponent<TextMesh>(); if (font == null) font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf"); tmesh.font = font; go.GetComponent<MeshRenderer>().sharedMaterial = font.material; tmesh.text = s; tmesh.color = c; tmesh.fontSize = 48; tmesh.characterSize = big ? .09f : .07f;
        tmesh.anchor = TextAnchor.MiddleCenter; tmesh.fontStyle = FontStyle.Bold;
        go.GetComponent<MeshRenderer>().sortingOrder = 40;
        fxs.Add(new Fx { go = go, v = new Vector3(0, .6f, 0), life = .8f, max = .8f });
    }
    void Burst(float x, float y, Color c, int n, float sp)
    {
        for (int i = 0; i < n; i++)
        {
            var s = new GameObject("p").AddComponent<SpriteRenderer>(); s.sprite = white; s.color = c; s.sortingOrder = 30;
            s.transform.SetParent(world); s.transform.position = WP(x, y); s.transform.localScale = Vector3.one * .1f;
            fxs.Add(new Fx { go = s.gameObject, v = (Vector3)Random.insideUnitCircle * sp, life = .5f, max = .5f });
        }
    }
    void Ring(float x, float y, Color c, float life, float rr)
    {
        var go = new GameObject("ring"); go.transform.SetParent(world); go.transform.position = WP(x, y);
        var lr = go.AddComponent<LineRenderer>(); lr.material = lineMat; lr.loop = true; lr.positionCount = 32; lr.useWorldSpace = false;
        lr.startColor = lr.endColor = c; lr.widthMultiplier = .05f; lr.sortingOrder = 35;
        for (int i = 0; i < 32; i++) { float a = i / 32f * Mathf.PI * 2; lr.SetPosition(i, new Vector3(Mathf.Cos(a), Mathf.Sin(a)) * .1f); }
        fxs.Add(new Fx { go = go, life = life, max = life, ring = true, rr = rr });
    }
    void Shot(float x, float y, float tx, float ty, Color c)
    {
        var go = new GameObject("shot"); go.transform.SetParent(world);
        var lr = go.AddComponent<LineRenderer>(); lr.material = lineMat; lr.positionCount = 2; lr.SetPosition(0, WP(x, y)); lr.SetPosition(1, WP(tx, ty));
        lr.startColor = lr.endColor = c; lr.widthMultiplier = .04f; lr.sortingOrder = 34;
        fxs.Add(new Fx { go = go, life = .2f, max = .2f });
    }

    // ===== 매 프레임 =====
    void Update()
    {
        float asp = (float)Screen.width / Screen.height;
        cam.orthographicSize = Mathf.Max(5.4f, 11.2f / asp);
        if (scr != Scr.Battle || world == null) return;
        float dt = Mathf.Min(Time.deltaTime, .05f);
        for (int i = 0; i < (int)spd; i++) Step(dt);
        if (over) resultT -= Time.deltaTime;
        // 그리기
        foreach (var t in new[] { 0, 1 }) foreach (var p in plots[t]) if (p.b != null) Place(p.b, 1.15f);
        foreach (var u in units) Place(u, u.go.transform.localScale.x);
        foreach (var c in cast) if (c.hp > 0) Place(c, 2.4f); else if (c.go.activeSelf) { c.go.SetActive(false); c.bar.gameObject.SetActive(false); c.barBg.gameObject.SetActive(false); }
        for (int i = fxs.Count - 1; i >= 0; i--)
        {
            var f = fxs[i]; float k = over ? .4f : 1; f.life -= Time.deltaTime * k;
            if (f.life <= 0) { Destroy(f.go); fxs.RemoveAt(i); continue; }
            if (f.ring) { float s = (1 - f.life / f.max) * f.rr * 10 + 1; f.go.transform.localScale = Vector3.one * s; var lr = f.go.GetComponent<LineRenderer>(); var col = lr.startColor; col.a = f.life / f.max; lr.startColor = lr.endColor = col; }
            else
            {
                f.go.transform.position += f.v * Time.deltaTime * k;
                var sr = f.go.GetComponent<SpriteRenderer>(); if (sr != null) { var col = sr.color; col.a = f.life / f.max; sr.color = col; }
                var tmx = f.go.GetComponent<TextMesh>(); if (tmx != null) { var col = tmx.color; col.a = Mathf.Min(1, f.life / f.max * 2); tmx.color = col; }
            }
        }
        shake *= .9f;
        cam.transform.position = new Vector3(Random.Range(-shake, shake), -0.6f + Random.Range(-shake, shake), -10);
        // 막사 누르면 강화
        if (!over && Input.GetMouseButtonDown(0) && Input.mousePosition.y > Screen.height * .2f && Input.mousePosition.y < Screen.height * .88f)
        {
            var wp = cam.ScreenToWorldPoint(Input.mousePosition); Ent best = null; float bd = .8f;
            foreach (var p in plots[0]) if (p.b != null) { float d = Vector2.Distance(wp, WP(p.b.x, p.b.y)); if (d < bd) { bd = d; best = p.b; } }
            if (best != null) { if (!Upgrade(0, best)) toast = best.lv >= 3 ? "최고 단계예요 ★★★" : "강화에 금화 " + UpCost(best) + " 필요해요"; else toast = Get(best.id).nm + " ★" + best.lv + " · 더 빨리, 더 강하게!"; toastT = 1.5f; }
        }
        if (toastT > 0) toastT -= Time.deltaTime;
    }
    string toast = ""; float toastT;
    void Place(Ent e, float size)
    {
        int dir = e.t == 1 ? -1 : 1;
        var p = WP(e.x + dir * e.lunge * 60, e.y); e.go.transform.position = p;
        e.sr.color = e.fl > 0 ? new Color(1, 1, 1, 1) * 1.6f : Color.white;
        float r = size * .5f, w = size * .9f, f = Mathf.Clamp01(e.hp / e.mhp);
        bool show = e.hp < e.mhp || e.kind == 2;
        e.barBg.gameObject.SetActive(show); e.bar.gameObject.SetActive(show);
        e.barBg.position = p + new Vector3(0, r + .12f, 0); e.barBg.localScale = new Vector3(w, .08f, 1);
        e.bar.position = p + new Vector3(-w * (1 - f) / 2, r + .12f, 0); e.bar.localScale = new Vector3(w * f, .08f, 1);
        if (e.kind != 2) e.sr.sortingOrder = 5 + Mathf.RoundToInt(e.y / 10);
    }

    // ===== 화면 글자 · 버튼 =====
    GUIStyle Sty(int size, Color c, FontStyle fs = FontStyle.Bold, TextAnchor a = TextAnchor.MiddleCenter)
    { var s = new GUIStyle(GUI.skin.label) { fontSize = size, fontStyle = fs, alignment = a, wordWrap = true }; s.normal.textColor = c; return s; }
    void OnGUI()
    {
        float sc = Screen.height / 720f; float VW = Screen.width / sc;
        GUI.matrix = Matrix4x4.Scale(new Vector3(sc, sc, 1));
        var gold1 = new Color(.95f, .82f, .48f); var ink = new Color(.93f, .9f, .84f);
        if (scr == Scr.Title || scr == Scr.Menu || scr == Scr.Camp || scr == Scr.Coll)
        {
            var bg = T("menu"); if (bg != null) GUI.DrawTexture(new Rect(0, 0, VW, 720), bg, ScaleMode.ScaleAndCrop);
        }
        if (scr == Scr.Title)
        {
            GUI.Label(new Rect(0, 470, VW, 80), "여섯 번째 성주", Sty(64, new Color(.95f, .93f, .89f)));
            GUI.Label(new Rect(0, 540, VW, 36), "T H E   S I X T H   L O R D", Sty(20, new Color(.86f, .89f, .92f)));
            GUI.Label(new Rect(0, 578, VW, 30), "피의 달 · 다섯 가문", Sty(18, new Color(.85f, .54f, .5f), FontStyle.Normal));
            GUI.Label(new Rect(0, 640, VW, 30), "화면을 눌러 시작", Sty(16, new Color(.7f, .66f, .58f), FontStyle.Normal));
            if (Event.current.type == EventType.MouseDown) { scr = Scr.Menu; Event.current.Use(); }
            return;
        }
        if (scr == Scr.Menu)
        {
            GUI.Label(new Rect(16, 10, 400, 30), "여섯 번째 성주  THE SIXTH LORD", Sty(16, ink, FontStyle.Bold, TextAnchor.MiddleLeft));
            GUI.Label(new Rect(VW - 260, 10, 244, 30), "트로피 " + PlayerPrefs.GetInt("tro") + "   금화 " + PlayerPrefs.GetInt("gold", 300), Sty(15, gold1, FontStyle.Bold, TextAnchor.MiddleRight));
            float cx = VW / 2;
            if (Big(new Rect(cx - 110, 400, 220, 120), "전투", "빠른 대결", 34)) { var open = Open(); StartBattle(open[Random.Range(0, open.Count)]); }
            if (Big(new Rect(cx - 300, 450, 170, 90), "원정", "다섯 가문", 24)) scr = Scr.Camp;
            if (Big(new Rect(cx + 130, 450, 170, 90), "수집", "내 영웅", 24)) scr = Scr.Coll;
            return;
        }
        if (scr == Scr.Camp || scr == Scr.Coll)
        {
            GUI.color = new Color(0, 0, 0, .86f); GUI.DrawTexture(new Rect(0, 0, VW, 720), Texture2D.whiteTexture); GUI.color = Color.white;
            if (GUI.Button(new Rect(VW - 130, 12, 114, 36), "← 돌아가기")) scr = Scr.Menu;
            if (scr == Scr.Camp)
            {
                GUI.Label(new Rect(20, 12, 600, 36), "원정 · 다섯 가문을 차례로 꺾고 왕좌로", Sty(20, ink, FontStyle.Bold, TextAnchor.MiddleLeft));
                for (int i = 0; i < LORDS.Length; i++)
                {
                    var l = LORDS[i]; bool open = i == 0 || PlayerPrefs.GetInt("camp_" + LORDS[i - 1].id) == 1; bool beat = PlayerPrefs.GetInt("camp_" + l.id) == 1;
                    var r = new Rect(VW / 2 - 330, 70 + i * 122, 660, 110);
                    GUI.color = open ? Color.white : new Color(1, 1, 1, .35f);
                    GUI.Box(r, ""); GUI.DrawTexture(new Rect(r.x + 10, r.y + 10, 90, 90), T("lords/" + l.id));
                    GUI.Label(new Rect(r.x + 116, r.y + 12, 400, 30), (i + 1) + ". " + l.house + " · " + l.nm, Sty(20, ink, FontStyle.Bold, TextAnchor.MiddleLeft));
                    GUI.Label(new Rect(r.x + 116, r.y + 44, 400, 26), "\"" + l.motto + "\"", Sty(15, gold1, FontStyle.Italic, TextAnchor.MiddleLeft));
                    if (open && GUI.Button(new Rect(r.xMax - 130, r.y + 34, 116, 44), beat ? "다시 도전" : "⚔ 도전")) StartBattle(l);
                    if (!open) GUI.Label(new Rect(r.xMax - 130, r.y + 34, 116, 44), "잠김", Sty(16, ink));
                    GUI.color = Color.white;
                }
            }
            else
            {
                GUI.Label(new Rect(20, 12, 600, 36), "수집 · 영웅 16명", Sty(20, ink, FontStyle.Bold, TextAnchor.MiddleLeft));
                float cw = Mathf.Min(150, (VW - 60) / 8);
                for (int i = 0; i < DEFS.Length; i++)
                {
                    var d = DEFS[i]; var r = new Rect(30 + (i % 8) * cw, 80 + (i / 8) * (cw + 70), cw - 10, cw - 10);
                    GUI.color = RC[d.rar]; GUI.DrawTexture(new Rect(r.x - 3, r.y - 3, r.width + 6, r.height + 6), Texture2D.whiteTexture); GUI.color = Color.white;
                    GUI.DrawTexture(r, T("heroes/" + d.id));
                    GUI.Label(new Rect(r.x - 10, r.yMax + 4, r.width + 20, 24), d.nm, Sty(14, ink));
                    GUI.Label(new Rect(r.x - 10, r.yMax + 26, r.width + 20, 20), "금화 " + Cost(d.id) + " · " + Mathf.Round(Every(d.id)) + "초", Sty(12, gold1, FontStyle.Normal));
                }
            }
            return;
        }
        // ===== 전투 화면 =====
        GUI.color = new Color(.05f, .05f, .07f, .92f); GUI.DrawTexture(new Rect(0, 0, VW, 64), Texture2D.whiteTexture); GUI.DrawTexture(new Rect(0, 600, VW, 120), Texture2D.whiteTexture); GUI.color = Color.white;
        GUI.DrawTexture(new Rect(10, 10, 44, 44), T("lords/me")); GUI.DrawTexture(new Rect(VW - 54, 10, 44, 44), T("lords/" + foe.id));
        GUI.Label(new Rect(62, 6, 300, 24), "여섯 번째 성주", Sty(15, ink, FontStyle.Bold, TextAnchor.MiddleLeft));
        GUI.Label(new Rect(VW - 362, 6, 300, 24), foe.nm, Sty(15, ink, FontStyle.Bold, TextAnchor.MiddleRight));
        Bar(new Rect(62, 34, VW / 2 - 160, 12), cast[0].hp / cast[0].mhp, new Color(.25f, .75f, .42f));
        Bar(new Rect(VW / 2 + 98, 34, VW / 2 - 160, 12), cast[1].hp / cast[1].mhp, new Color(.88f, .35f, .29f));
        GUI.Label(new Rect(VW / 2 - 90, 4, 180, 30), "금화 " + Mathf.FloorToInt(gold[0]), Sty(22, gold1));
        if (GUI.Button(new Rect(VW / 2 - 40, 36, 80, 24), spd < 2 ? "▶ 1배" : "⏩ 2배")) spd = spd < 2 ? 2 : 1;
        if (GUI.Button(new Rect(10, 70, 90, 28), "← 성으로")) { scr = Scr.Menu; Destroy(world.gameObject); world = null; return; }
        // 카드
        float cw2 = 92, total = myCards.Count * (cw2 + 8), x0 = VW / 2 - total / 2;
        bool freeSlot = false; foreach (var p in plots[0]) if (p.b == null) freeSlot = true;
        for (int i = 0; i < myCards.Count; i++)
        {
            var id = myCards[i]; var d = Get(id); var r = new Rect(x0 + i * (cw2 + 8), 612, cw2, 100);
            bool ok = freeSlot && gold[0] >= Cost(id) && !over;
            GUI.color = ok ? RC[d.rar] : new Color(.3f, .3f, .3f); GUI.DrawTexture(r, Texture2D.whiteTexture);
            GUI.color = ok ? Color.white : new Color(.45f, .45f, .45f);
            GUI.DrawTexture(new Rect(r.x + 3, r.y + 3, r.width - 6, r.height - 6), T("heroes/" + id), ScaleMode.ScaleAndCrop); GUI.color = Color.white;
            GUI.Label(new Rect(r.x, r.y + 2, r.width, 20), "금화 " + Cost(id), Sty(13, gold1));
            GUI.Label(new Rect(r.x, r.yMax - 22, r.width, 20), d.nm, Sty(12, Color.white));
            if (GUI.Button(r, "", GUIStyle.none) && !over)
            {
                if (!freeSlot) { toast = "빈 자리가 없어요 · 막사를 눌러 강화하세요"; toastT = 1.5f; }
                else if (gold[0] < Cost(id)) { toast = "금화가 모자라요"; toastT = 1.2f; }
                else { Build(0, id); toast = d.nm + " 막사 완성! 병사가 저절로 나와요"; toastT = 1.5f; }
            }
        }
        if (toastT > 0) GUI.Label(new Rect(VW / 2 - 300, 110, 600, 34), toast, Sty(18, gold1));
        if (tm < 6 && !over) GUI.Label(new Rect(VW / 2 - 400, 150, 800, 30), "아래 카드를 누르면 막사가 지어지고, 병사가 저절로 나와 싸워요. 막사를 누르면 강화!", Sty(16, ink, FontStyle.Normal));
        if (over && resultT <= 0)
        {
            GUI.color = new Color(0, 0, 0, .8f); GUI.DrawTexture(new Rect(0, 0, VW, 720), Texture2D.whiteTexture); GUI.color = Color.white;
            GUI.DrawTexture(new Rect(VW / 2 - 60, 170, 120, 120), T("lords/" + foe.id));
            GUI.Label(new Rect(0, 300, VW, 60), win ? foe.nm + "의 성이 무너졌다!" : "성이 무너졌어요…", Sty(34, gold1));
            GUI.Label(new Rect(0, 360, VW, 30), win ? "쓰러뜨린 적 " + kills[0] + " · 금화 +" + (40 + foe.idx * 15) : "앞쪽엔 튼튼한 거북·곰, 뒤쪽엔 여우·부엉이를 섞어 보세요", Sty(18, ink, FontStyle.Normal));
            if (GUI.Button(new Rect(VW / 2 - 170, 420, 160, 50), "한 판 더")) StartBattle(foe);
            if (GUI.Button(new Rect(VW / 2 + 10, 420, 160, 50), "성으로")) { scr = Scr.Menu; Destroy(world.gameObject); world = null; }
        }
    }
    List<Lord> Open() { var o = new List<Lord>(); for (int i = 0; i < LORDS.Length; i++) if (i == 0 || PlayerPrefs.GetInt("camp_" + LORDS[i - 1].id) == 1) o.Add(LORDS[i]); return o; }
    void Bar(Rect r, float f, Color c)
    {
        GUI.color = new Color(.16f, .15f, .14f); GUI.DrawTexture(r, Texture2D.whiteTexture);
        GUI.color = c; GUI.DrawTexture(new Rect(r.x, r.y, r.width * Mathf.Clamp01(f), r.height), Texture2D.whiteTexture); GUI.color = Color.white;
    }
    bool Big(Rect r, string t, string sub, int size)
    {
        GUI.color = new Color(.85f, .9f, 1f, .28f); GUI.DrawTexture(r, Texture2D.whiteTexture);
        GUI.color = new Color(.92f, .95f, 1f, .7f); GUI.DrawTexture(new Rect(r.x, r.y, r.width, 2), Texture2D.whiteTexture); GUI.DrawTexture(new Rect(r.x, r.yMax - 2, r.width, 2), Texture2D.whiteTexture);
        GUI.color = Color.white;
        GUI.Label(new Rect(r.x, r.y + r.height * .18f, r.width, size + 10), t, Sty(size, new Color(.96f, .95f, .92f)));
        GUI.Label(new Rect(r.x, r.y + r.height * .18f + size + 8, r.width, 22), sub, Sty(13, new Color(.85f, .87f, .9f), FontStyle.Normal));
        return GUI.Button(r, "", GUIStyle.none);
    }
}
