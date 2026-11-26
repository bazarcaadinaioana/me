"""Adattamento editoriale IT -> EN dei sorgenti Markdown tramite API OpenAI (connessione già configurata).
Uso: python3 build/traduci.py [file ...]"""
import os, sys, json, glob, time, urllib.request, urllib.error, concurrent.futures as cf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYS = """You are the senior editor of a premium international non-fiction publisher. You produce the ENGLISH EDITION of an Italian book
("Guadagnare con l'Intelligenza Artificiale" -> "Make Money with Artificial Intelligence"). This is a true editorial edition in natural,
polished, clear international English (US spelling), written for complete beginners — not a literal translation.

STRICT RULES
1. Preserve the Markdown structure exactly: same headings and heading levels, same order, same lists, tables (same rows/columns),
   code blocks, fenced divs (lines like `::: {.box .tip}` and `:::` stay identical), task lists `- [ ]`, links and attributes in braces
   such as {.part} {.chapter} {.unnumbered .front} {.unnumbered .appendix} (keep them verbatim).
2. Image paths: change the suffix `-it.svg` to `-en.svg`; translate the alt text.
3. Keep EVERY fact, number, price, date, percentage, platform rule and caveat exactly. Do not add facts, statistics, examples or claims.
   Do not remove content. Same examples, same exercises, same fictional characters (keep their Italian names: they are fictional).
4. Keep amounts in euros (€) and dollars ($) exactly as in the source. Write numbers in English format (1,500 €→ €1,500; 0,20 $ → $0.20; 6,5% → 6.5%).
5. Prompts inside code blocks: translate them into natural English prompts, keeping the [bracket placeholders] (translated).
6. Box labels: "Consiglio." -> "Tip.", "Attenzione." -> "Warning.", "Esempio ipotetico" -> "Hypothetical example".
   Recap headings: "Cosa abbiamo imparato" -> "What we learned", "Errori da evitare" -> "Mistakes to avoid",
   "Esercizio pratico" / "Esercizio da svolgere" -> "Practical exercise", "Checklist di verifica" -> "Review checklist".
   The method acronym RCOFE stays RCOFE with English words: Role, Context, Objective, Format, Examples & limits.
7. Italy-specific material (Italian tax rules, INPS, regime forfettario, Garante privacy, AGCOM, Consob, UIBM, CAF, amazon.it VAT on ebooks)
   must be kept and clearly framed as "the example of Italy" / Italian context; where the Italian text says "in Italia", keep it.
   Do not invent equivalent rules for other countries; you may say readers outside Italy should check their own tax authority.
8. Use "AI". Use "you". Tone: warm, expert teacher; concise; no hype; no motivational filler.
Return ONLY the translated Markdown, nothing else."""
def call(text):
    body = json.dumps({"model": "gpt-5.5", "messages": [{"role": "system", "content": SYS}, {"role": "user", "content": text}]}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer sk-proxy"})
    for i in range(8):
        try:
            with urllib.request.urlopen(req, timeout=1800) as r:
                d = json.load(r); break
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504): time.sleep(20 * (i + 1)); continue
            raise
    else:
        raise RuntimeError("troppi tentativi")
    return d["choices"][0]["message"]["content"], d["choices"][0].get("finish_reason")
def split(md):
    # divide a livello di "# " (parti/capitoli) per tenere le richieste piccole
    parts, cur = [], []
    for line in md.splitlines(keepends=True):
        if line.startswith("# ") and cur and sum(len(x) for x in cur) > 12000:
            parts.append("".join(cur)); cur = []
        cur.append(line)
    parts.append("".join(cur)); return parts
def do(f):
    out = f.replace("/it/", "/en/")
    chunks = split(open(f, encoding="utf-8").read())
    res = []
    for c in chunks:
        t, fr = call(c)
        if fr != "stop": print("WARN", f, fr)
        res.append(t.strip() + "\n")
    open(out, "w", encoding="utf-8").write("\n".join(res))
    return os.path.basename(f), len(chunks)
files = sys.argv[1:] or [f for f in sorted(glob.glob(os.path.join(ROOT, "sorgenti/it/*.md"))) if not os.path.exists(f.replace("/it/", "/en/"))]
with cf.ThreadPoolExecutor(3) as ex:
    for r in ex.map(do, files): print("ok", r, flush=True)
