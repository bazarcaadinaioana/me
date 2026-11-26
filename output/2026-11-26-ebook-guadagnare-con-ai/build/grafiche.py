"""Genera copertine e immagini promozionali (HTML -> PNG con Chromium/Playwright).
Uso: python3 build/grafiche.py
"""
import os, asyncio, base64
def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path,"rb").read()).decode()
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.path.join(ROOT, "build", "fonts")
FONTS = f"""
@font-face{{font-family:Display;src:url({b64(FD+"/fraunces-latin-300-normal.ttf","font/ttf")});font-weight:300}}
@font-face{{font-family:Display;src:url({b64(FD+"/fraunces-latin-400-normal.ttf","font/ttf")});font-weight:400}}
@font-face{{font-family:Display;src:url({b64(FD+"/fraunces-latin-400-italic.ttf","font/ttf")});font-weight:400;font-style:italic}}
@font-face{{font-family:Display;src:url({b64(FD+"/fraunces-latin-600-normal.ttf","font/ttf")});font-weight:600}}
@font-face{{font-family:Sans;src:url({b64(FD+"/Inter-Regular.otf","font/otf")});font-weight:400}}
@font-face{{font-family:Sans;src:url({b64(FD+"/Inter-SemiBold.otf","font/otf")});font-weight:600}}
@font-face{{font-family:Sans;src:url({b64(FD+"/Inter-Bold.otf","font/otf")});font-weight:700}}
@font-face{{font-family:BkSerif;src:url({b64(FD+"/source-serif-4-latin-400-normal.ttf","font/ttf")})}}
"""
INK, GOLD, CREAM = "#141a26", "#c9a45c", "#f3eee4"

TXT = {
 "it": dict(kicker="Guida pratica · Edizione 2026", t=["Guadagnare", "con l'Intelligenza", "Artificiale"],
            sub="La guida pratica per principianti: guadagnare online con l'AI, creare prodotti digitali e avviare un business digitale anche partendo da zero",
            badges=["12 modi per guadagnare", "5 tutorial completi", "55 prompt pronti", "Piano di 30 giorni"],
            promo1="Dall'idea alla prima vendita,<br/>senza promesse irrealistiche",
            inside="Cosa trovi dentro", pages="40 capitoli · glossario · fonti ufficiali",
            stack=["PDF + EPUB", "Aggiornato a novembre 2026", "Per principianti assoluti"],
            prompts="55 prompt professionali", prompts_sub="Business · Marketing · Social · Vendita · Ebook · Copywriting · Immagini · Video · Ricerca · Prodotti digitali",
            plan="Piano operativo di 30 giorni", plan_sub="Scegliere · Costruire · Presentare · Testare",
            weeks=["Settimana 1 — Scegliere", "Settimana 2 — Costruire", "Settimana 3 — Presentare", "Settimana 4 — Testare"]),
 "en": dict(kicker="Practical guide · 2026 edition", t=["Make Money", "with Artificial", "Intelligence"],
            sub="A Practical Beginner's Guide to Making Money Online with AI, Creating Digital Products and Starting a Digital Business from Scratch",
            badges=["12 ways to earn", "5 complete tutorials", "55 ready-to-use prompts", "30-day action plan"],
            promo1="From first idea to first sale,<br/>without unrealistic promises",
            inside="What's inside", pages="40 chapters · glossary · official sources",
            stack=["PDF + EPUB", "Updated November 2026", "For complete beginners"],
            prompts="55 professional prompts", prompts_sub="Business · Marketing · Social · Sales · Ebooks · Copywriting · Images · Video · Research · Digital products",
            plan="30-day action plan", plan_sub="Choose · Build · Present · Test",
            weeks=["Week 1 — Choose", "Week 2 — Build", "Week 3 — Present", "Week 4 — Test"]),
}

def motif(w, h, opacity=1):
    """Costellazione geometrica: nodi e linee (rete neurale stilizzata)."""
    import random
    random.seed(7)
    cols = [(0.18, 4), (0.38, 6), (0.62, 6), (0.82, 3)]
    nodes = []
    for x, n in cols:
        nodes.append([(x * w, h * (0.15 + 0.7 * (i + 0.5) / n)) for i in range(n)])
    s = f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg" style="opacity:{opacity}">'
    for a, b in zip(nodes, nodes[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                o = 0.10 + random.random() * 0.25
                s += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{GOLD}" stroke-width="1.2" opacity="{o:.2f}"/>'
    for col in nodes:
        for (x, y) in col:
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{INK}" stroke="{GOLD}" stroke-width="2"/>'
    hx, hy = nodes[2][2]
    s += f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="13" fill="{GOLD}"/>'
    return s + "</svg>"

def cover_html(lang, W, H):
    t = TXT[lang]
    feats = "".join(f'<span>{x}</span>' for x in t["badges"])
    return f"""<html><head><style>{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:radial-gradient(ellipse at 70% 18%, #24304a 0%, {INK} 58%);color:{CREAM};font-family:Sans;position:relative;overflow:hidden}}
.frame{{position:absolute;inset:{W*0.04}px;border:1.5px solid rgba(201,164,92,.5)}}
.kicker{{position:absolute;top:{H*0.07}px;left:0;right:0;text-align:center;font-weight:600;font-size:{W*0.02}px;letter-spacing:.34em;text-transform:uppercase;color:{GOLD}}}
.art{{position:absolute;top:{H*0.105}px;left:{W*0.1}px}}
.title{{position:absolute;top:{H*0.39}px;left:{W*0.09}px;right:{W*0.06}px;font-family:Display;font-weight:600;font-size:{W*0.122}px;line-height:.98;letter-spacing:-.015em}}
.title .l2{{font-style:italic;color:{GOLD};font-weight:400;font-size:{W*0.098}px}}
.rule{{position:absolute;top:{H*0.665}px;left:{W*0.09}px;width:{W*0.14}px;height:4px;background:{GOLD}}}
.sub{{position:absolute;top:{H*0.685}px;left:{W*0.09}px;right:{W*0.12}px;font-family:BkSerif;font-size:{W*0.03}px;line-height:1.42;color:#dde0e7}}
.feats{{position:absolute;top:{H*0.80}px;left:{W*0.09}px;right:{W*0.09}px;display:grid;grid-template-columns:1fr 1fr;gap:{W*0.014}px}}
.feats span{{border:1.5px solid rgba(201,164,92,.75);color:{CREAM};font-weight:600;font-size:{W*0.021}px;padding:{W*0.01}px {W*0.018}px;border-radius:40px;letter-spacing:.02em;text-align:center}}
.au{{position:absolute;bottom:{H*0.065}px;left:0;right:0;text-align:center;font-family:Display;font-size:{W*0.04}px;letter-spacing:.16em;color:{GOLD}}}
</style></head><body><div class="frame"></div><div class="kicker">{t['kicker']}</div>
<div class="art">{motif(int(W*0.8), int(H*0.25), .9)}</div>
<div class="title">{t['t'][0]}<br/><span class="l2">{t['t'][1]}</span><br/>{t['t'][2]}</div>
<div class="rule"></div><div class="sub">{t['sub']}</div><div class="feats">{feats}</div><div class="au">IRINA B.</div></body></html>"""

def promo_html(lang, kind, W, H, cover_png):
    t = TXT[lang]
    base = f"""{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:{CREAM};color:{INK};font-family:Sans;position:relative;overflow:hidden}}
.k{{font-weight:700;font-size:{W*0.016}px;letter-spacing:.3em;text-transform:uppercase;color:#9a7a3a}}
h1{{font-family:Display;font-weight:400;line-height:1.05}}
.book{{box-shadow:0 30px 60px rgba(20,26,38,.35), 0 8px 16px rgba(20,26,38,.2);border-radius:2px 6px 6px 2px}}"""
    if kind == "hero":
        badges = "".join(f'<div class="b">{b}</div>' for b in t["badges"])
        return f"""<html><head><style>{base}
.book{{position:absolute;left:{W*0.07}px;top:{H*0.1}px;height:{H*0.8}px}}
.r{{position:absolute;left:{W*0.5}px;right:{W*0.06}px;top:{H*0.16}px}}
h1{{font-size:{W*0.045}px;margin:{H*0.03}px 0 {H*0.05}px}}
.b{{font-size:{W*0.022}px;font-weight:600;padding:{H*0.022}px 0;border-bottom:1.5px solid #ddd3bf}}
.b::before{{content:"";display:inline-block;width:{W*0.012}px;height:{W*0.012}px;background:#c9a45c;border-radius:50%;margin-right:{W*0.015}px}}
.s{{margin-top:{H*0.05}px;font-size:{W*0.017}px;color:#5f6470;letter-spacing:.05em}}
</style></head><body><img class="book" src="{b64(cover_png,"image/png")}"/><div class="r"><div class="k">{t['kicker']}</div><h1>{t['promo1']}</h1>{badges}<div class="s">{' · '.join(t['stack'])}</div></div></body></html>"""
    if kind == "inside":
        rows = "".join(f'<div class="w"><span>{i+1}</span>{w}</div>' for i, w in enumerate(t["weeks"]))
        return f"""<html><head><style>{base}
body{{background:{INK};color:{CREAM}}}
.c{{position:absolute;left:{W*0.08}px;right:{W*0.08}px;top:{H*0.1}px}}
.k{{color:#c9a45c}}
h1{{font-size:{W*0.05}px;margin:{H*0.03}px 0 {H*0.015}px}}
.p{{font-size:{W*0.018}px;color:#aab0bd;margin-bottom:{H*0.06}px;letter-spacing:.04em}}
.w{{font-family:Display;font-size:{W*0.033}px;padding:{H*0.03}px 0;border-top:1.5px solid rgba(201,164,92,.35);display:flex;align-items:center}}
.w span{{font-family:Sans;font-weight:700;font-size:{W*0.018}px;color:{INK};background:#c9a45c;border-radius:50%;width:{W*0.045}px;height:{W*0.045}px;display:inline-flex;align-items:center;justify-content:center;margin-right:{W*0.03}px}}
</style></head><body><div class="c"><div class="k">{t['inside']}</div><h1>{t['plan']}</h1><div class="p">{t['plan_sub']}</div>{rows}</div></body></html>"""
    if kind == "prompts":
        cats = "".join(f'<div class="g">{c.strip()}</div>' for c in t["prompts_sub"].split("·"))
        return f"""<html><head><style>{base}
.c{{position:absolute;left:{W*0.08}px;right:{W*0.08}px;top:{H*0.1}px}}
h1{{font-size:{W*0.055}px;margin:{H*0.03}px 0 {H*0.05}px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:{W*0.018}px}}
.g{{background:#fff;border:1.5px solid #e2d8c4;border-left:5px solid #c9a45c;padding:{H*0.025}px {W*0.025}px;font-size:{W*0.024}px;font-weight:600}}
.f{{position:absolute;bottom:{H*0.07}px;left:{W*0.08}px;font-size:{W*0.017}px;color:#5f6470;letter-spacing:.05em}}
</style></head><body><div class="c"><div class="k">{t['inside']}</div><h1>{t['prompts']}</h1><div class="grid">{cats}</div></div><div class="f">{t['pages']}</div></body></html>"""

async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
        async def shot(html, W, H, path):
            pg = await br.new_page(viewport={"width": W, "height": H})
            await pg.set_content(html); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=path); await pg.close()
        for lang in ("it", "en"):
            cov = os.path.join(ROOT, "copertine", f"copertina-{lang}.png")
            await shot(cover_html(lang, 1600, 2400), 1600, 2400, cov)                       # 2:3 — PDF/EPUB/Etsy
            await shot(cover_html(lang, 1600, 2560), 1600, 2560,
                       os.path.join(ROOT, "copertine", f"copertina-{lang}-kindle-1600x2560.png"))  # rapporto 1,6:1 consigliato da KDP
            for kind, (W, H) in {"hero": (2000, 1500), "inside": (2000, 1500), "prompts": (2000, 1500)}.items():
                await shot(promo_html(lang, kind, W, H, cov), W, H, os.path.join(ROOT, "promo", f"{lang}-etsy-{kind}-2000x1500.png"))
            # Amazon A+ (970x600) e post social quadrato
            await shot(promo_html(lang, "hero", 970, 600, cov), 970, 600, os.path.join(ROOT, "promo", f"{lang}-amazon-aplus-970x600.png"))
            await shot(promo_html(lang, "hero", 1080, 1080, cov).replace("left:540.0px", "left:560px"), 1080, 1080, os.path.join(ROOT, "promo", f"{lang}-social-1080x1080.png"))
        await br.close()
asyncio.run(main())
print("ok")
