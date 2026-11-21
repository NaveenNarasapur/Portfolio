"""Single source of truth for all résumé variants.
Run: python resume/src/build_resume.py   → writes resume/<variant>/Naveen_Narasapur_Resume_<variant>.{pdf,docx,md}
Requires: reportlab, python-docx. Edit DATA / VARIANTS below, never the generated files."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUT = Path(__file__).resolve().parents[1]

EMAIL = "naveennarasapur05@gmail.com"
# (label shown on the page, URL behind it)
LINKS = [("naveennarasapur05@gmail.com", "mailto:naveennarasapur05@gmail.com"),
         ("Portfolio", "https://naveen-narasapur.in"),
         ("LinkedIn", "https://www.linkedin.com/in/naveen-narasapur-936226256"),
         ("GitHub", "https://github.com/NaveenNarasapur"),
         ("LeetCode", "https://leetcode.com/u/nave05/")]
CONTACT = "  |  ".join(l for l, _ in LINKS)  # plain-text form for Markdown

EDU = [("KLE Technological University, Hubli", "2022 – 2026",
        "B.E., Computer Science and Engineering (Artificial Intelligence) | CGPA: 8.90/10"),
       ("Class XII 97.17% (Vidyaniketan PU College, 2022)  |  Class X 94.08% (JSS EMS, Dharwad, 2020)", "", "")]

KPMG_FT = ("KPMG Global Services", "Analyst, Advisory (Oracle practice)", "", "Sep 2026 – Present")
KPMG_IN = ("KPMG Global Services", "Intern, Oracle practice", "", "Jan 2026 – Jul 2026")

B = {
 "ft1": "Develop and support integrations between Oracle HCM Cloud and connected enterprise systems on Oracle Integration Cloud, built from adapters, data mappings and orchestrated flows.",
 "ft2": "Write PL/SQL procedures and SQL queries that extract, validate and transform the HR data these integrations carry between systems.",
 "in1": "Built real-time integrations that move data between enterprise systems using Oracle Integration Cloud adapters, field mappings and orchestration workflows; **converted to a full-time offer** at the end of the internship.",
 "in2": "Wrote SQL and PL/SQL (multi-table joins, stored procedures) against real datasets; planned and documented work in Jira and Confluence.",
 "ftO1": "Build and support Oracle Integration Cloud (OIC) integrations for Oracle HCM Cloud on an enterprise client engagement for a US-based utility-services company: connections, adapters, lookups, mappings and orchestrated workflows.",
 "ftO2": "Work with HCM Extracts, BI Publisher and OTBI reports to source and validate HR data for downstream integrations; write SQL and PL/SQL for extraction, validation and transformation.",
 "ftD1": "Write SQL and PL/SQL to extract, validate and transform HR data for Oracle HCM integrations, working with HCM Extracts, BI Publisher and OTBI as data sources.",
 "ftD2": "Build Oracle Integration Cloud (OIC) flows that move data between Oracle HCM Cloud and connected enterprise systems using adapters, lookups and mappings.",
 # webhook relay
 "rl1": "Built a webhook delivery service with at-least-once guarantees: transactional fan-out (outbox), workers that claim jobs via FOR UPDATE SKIP LOCKED with leases, exponential backoff with full jitter, and a dead-letter queue with replay.",
 "rl2": "Enforced idempotency with a unique constraint (**20** concurrent duplicate requests produce exactly **1** event), plus HMAC-SHA256 payload signing, hashed per-tenant API keys and SSRF blocking of private and metadata IPs.",
 "rl3": "Wrote **44** pytest tests on real PostgreSQL covering timeouts, 4xx/5xx handling, crashed and concurrent workers; measured **~1,000 deliveries/s** with 4 workers on 2 CPUs and **zero double deliveries**.",
 # ddos
 "dd1": "Built a leakage-aware detection pipeline on CIC-IDS2017 (**223K** flows) with de-duplication, identifier removal and a temporal train/test split; compared five models including Random Forest, Gradient Boosting and BIRCH.",
 "dd2": "Served the Random Forest model through an API-key-secured FastAPI service with a metrics dashboard, reaching **F1 0.998** at a **0.02%** false-positive rate (6 of 32,767 benign flows) on held-out later traffic.",
 "dd3": "Showed by ablation that gradient boosting relied on TCP-window fingerprint features (false positives rose **15x** without them) while Random Forest did not; **29** tests, **95%** coverage, CI on GitHub Actions.",
 # zsl
 "zs1": "Implemented zero-shot image classification in PyTorch: frozen ResNet-101 features mapped to 85 class attributes by a learned compatibility function, with model selection on disjoint validation classes.",
 "zs2": "Reached **59.0%** unseen-class accuracy on the standard AwA2 split (published ALE baseline: 62.5%) and a **58.2** GZSL harmonic mean with calibrated stacking; deterministic runs, 14 tests.",
 "zs3": "Audited my earlier 90.48% figure, showed it matched conventional seen-class accuracy (92.7%) rather than zero-shot accuracy, and published the correction.",
 # geosnap
 "geo1": "Built an offline-capable React + TypeScript PWA that writes GPS EXIF into camera JPEGs in the browser, rewriting only the metadata segment so image bytes stay unchanged, then re-verifies the output with an independent parser.",
}

ACH = ["**CodeChef 3-star**, max rating 1632, 315 problems solved; **ACM ICPC** Asia Amritapuri Regional 2023, Honorable Mention.",
       "**GATE Data Science and AI 2026**, All India Rank 4561."]

SKILLS = {
 "backend": [("Languages", "Python, C++, SQL, PL/SQL, JavaScript, TypeScript"),
             ("Backend & Data", "FastAPI, REST API design, PostgreSQL (transactions, row locking, indexing), Oracle Integration Cloud, Oracle SQL"),
             ("Engineering", "pytest, GitHub Actions CI, Docker, Git, structured logging, Linux"),
             ("ML", "scikit-learn, PyTorch, pandas, NumPy")],
 "data": [("Languages", "Python, SQL, PL/SQL, C++"),
             ("Data", "pandas, NumPy, PostgreSQL, Oracle SQL, data cleaning & validation, BI Publisher, OTBI, HCM Extracts"),
             ("Integration & Backend", "Oracle Integration Cloud, REST APIs, FastAPI"),
             ("Engineering & ML", "pytest, GitHub Actions CI, Docker, Git, Linux; scikit-learn, PyTorch")],
 "oracle": [("Oracle Cloud", "Oracle Integration Cloud (connections, adapters, lookups, mappings, orchestration), Oracle HCM Cloud, HCM Extracts, BI Publisher, OTBI"),
             ("Languages & Data", "SQL, PL/SQL, Python, JavaScript"),
             ("Integration", "REST APIs, JSON, webhooks, retries & idempotency, error handling"),
             ("Tools", "Jira, Confluence, Git, Docker, pytest")],
 "ml": [("Languages", "Python, SQL, C++"),
             ("ML", "PyTorch, scikit-learn, pandas, NumPy, ResNet transfer learning, model evaluation & leakage control"),
             ("Serving & Backend", "FastAPI, REST APIs, PostgreSQL, Docker"),
             ("Engineering", "pytest, GitHub Actions CI, Git, Linux")],
 "general": [("Languages", "Python, C++, SQL, PL/SQL, JavaScript, TypeScript"),
             ("Backend", "FastAPI, REST APIs, PostgreSQL, Oracle Integration Cloud, Cloudflare Workers"),
             ("ML & Frontend", "PyTorch, scikit-learn, pandas, NumPy; React, PWAs"),
             ("Engineering", "pytest, GitHub Actions CI, Docker, Git, Linux; data structures & algorithms")],
}

GH = "https://github.com/NaveenNarasapur/"
PROJECTS = {
 "relay": ("Relay: Reliable Webhook Delivery Service", "Python, FastAPI, PostgreSQL, Docker", GH + "webhook-relay", ["rl1", "rl2", "rl3"]),
 "relay_g": ("Relay: Reliable Webhook Delivery Service", "Python, FastAPI, PostgreSQL, Docker", GH + "webhook-relay", ["rl1", "rl3"]),
 "ddos": ("DDoS Flow Detection Service", "Python, scikit-learn, FastAPI", GH + "ddos-detection", ["dd1", "dd2", "dd3"]),
 "ddos_b": ("DDoS Flow Detection Service", "Python, scikit-learn, FastAPI", GH + "ddos-detection", ["dd1", "dd2"]),
 "zsl": ("Zero-Shot Image Classification", "PyTorch, ResNet-101", GH + "zero-shot-awa2", ["zs1", "zs2", "zs3"]),
 "zsl_b": ("Zero-Shot Image Classification", "PyTorch, ResNet-101", GH + "zero-shot-awa2", ["zs2", "zs3"]),
 "geo": ("GeoSnap: Geotagging Camera PWA", "React, TypeScript", GH + "geosnap", ["geo1"]),
}

VARIANTS = {
 "backend": dict(skills="backend", projects=["relay", "ddos_b", "zsl_b", "geo"]),
 "data_engineer": dict(skills="data", projects=["ddos", "relay", "zsl_b"], exp=("ftD1", "ftD2")),
 "oracle_integration": dict(skills="oracle", projects=["relay", "ddos", "zsl_b"], exp=("ftO1", "ftO2")),
 "python_ml": dict(skills="ml", projects=["zsl", "ddos", "relay_g"]),
 "generalist": dict(skills="general", projects=["relay", "ddos_b", "zsl_b", "geo"]),
}

def sections(v):
    cfg = VARIANTS[v]
    ft = cfg.get("exp", ("ft1", "ft2"))
    exp = [(KPMG_FT, [B[k] for k in ft]), (KPMG_IN, [B["in1"], B["in2"]])]
    projs = [(PROJECTS[p][0], PROJECTS[p][1], PROJECTS[p][2], [B[k] for k in PROJECTS[p][3]]) for p in cfg["projects"]]
    return exp, SKILLS[cfg["skills"]], projs

# ---------- PDF ----------
import re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

FONT_DIR = Path("/usr/share/fonts/truetype/crosextra")
try:  # Carlito is metric-compatible with Calibri, so PDF and DOCX look alike
    for name, f in (("Body", "Carlito-Regular"), ("Body-Bold", "Carlito-Bold"), ("Body-Italic", "Carlito-Italic")):
        pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / f"{f}.ttf")))
    R, Bd, I = "Body", "Body-Bold", "Body-Italic"
except Exception:
    R, Bd, I = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"

INK = HexColor("#111111"); MUTE = HexColor("#444444"); LINK = HexColor("#1a4f8b"); RULE = HexColor("#9aa5b1")

def tokens(text):
    """Words as lists of (fragment, bold): '(**20** x)' -> [[('(',F),('20',T)], [('x)',F)]]"""
    words, cur, bold, buf = [], [], False, ""
    i = 0
    while i < len(text):
        if text.startswith("**", i):
            if buf: cur.append((buf, bold)); buf = ""
            bold = not bold; i += 2; continue
        ch = text[i]
        if ch == " ":
            if buf: cur.append((buf, bold)); buf = ""
            if cur: words.append(cur); cur = []
        else:
            buf += ch
        i += 1
    if buf: cur.append((buf, bold))
    if cur: words.append(cur)
    return words

def wwidth(word, size):
    return sum(stringWidth(f, Bd if b else R, size) for f, b in word)

def plain(text):
    return text.replace("**", "")

def pdf(v, path):
    exp, skills, projs = sections(v)
    W, H = A4; M = 46; c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle("Naveen Narasapur – Resume"); c.setAuthor("Naveen Narasapur"); c.setSubject("Software engineer résumé")
    S = 10.4; LH = 13.4          # body size and line height
    y = H - 50

    def link_text(x, yy, label, url, font=R, size=S, color=LINK):
        c.setFont(font, size); c.setFillColor(color); c.drawString(x, yy, label); c.setFillColor(INK)
        w = stringWidth(label, font, size)
        c.linkURL(url, (x, yy - 2, x + w, yy + size), relative=0, thickness=0)
        return w

    def rich_lines(text, width, size=S):
        lines, cur, cw = [], [], 0
        sp = stringWidth(" ", R, size)
        for w in tokens(text):
            ww = wwidth(w, size)
            if cur and cw + sp + ww > width:
                lines.append(cur); cur, cw = [], 0
            cw += (sp if cur else 0) + ww; cur.append(w)
        return lines + [cur]

    def draw_rich(line, x, yy, size=S):
        sp = stringWidth(" ", R, size)
        for w in line:
            for frag, bold in w:
                f = Bd if bold else R
                c.setFont(f, size); c.drawString(x, yy, frag); x += stringWidth(frag, f, size)
            x += sp

    def bullet(text):
        nonlocal y
        for i, ln in enumerate(rich_lines(text, W - 2*M - 13)):
            if i == 0:
                c.setFont(R, S); c.drawString(M + 3, y, "•")
            draw_rich(ln, M + 13, y); y -= LH - 0.6
        y -= 1.6

    def head(t):
        nonlocal y
        y -= 7
        c.setFont(Bd, 11.2); c.setFillColor(INK); c.drawString(M, y, t.upper())
        y -= 4.5; c.setStrokeColor(RULE); c.setLineWidth(.7); c.line(M, y, W - M, y); y -= 13.5

    def row(left, right, lf=Bd, rf=R, ls=S, rs=S, rc=MUTE):
        nonlocal y
        c.setFont(lf, ls); c.drawString(M, y, left)
        c.setFont(rf, rs); c.setFillColor(rc); c.drawRightString(W - M, y, right); c.setFillColor(INK)
        y -= LH

    # name + contact
    c.setFillColor(INK); c.setFont(Bd, 21); c.drawCentredString(W/2, y, "Naveen Nagesh Narasapur"); y -= 17
    c.setFont(R, 10.2)
    sep = "   |   "
    total = sum(stringWidth(l, R, 10.2) for l, _ in LINKS) + stringWidth(sep, R, 10.2) * (len(LINKS) - 1)
    x = (W - total) / 2
    for i, (label, url) in enumerate(LINKS):
        x += link_text(x, y, label, url, size=10.2)
        if i < len(LINKS) - 1:
            c.setFont(R, 10.2); c.setFillColor(MUTE); c.drawString(x, y, sep); c.setFillColor(INK); x += stringWidth(sep, R, 10.2)
    y -= 12

    head("Education")
    row(EDU[0][0], EDU[0][1])
    c.setFont(R, S); c.drawString(M, y, EDU[0][2]); y -= LH
    c.setFont(R, S - .4); c.setFillColor(MUTE); c.drawString(M, y, EDU[1][0]); c.setFillColor(INK); y -= LH - 2

    head("Experience")
    last_org = None
    for (org, role, loc, when), bl in exp:
        if org != last_org:
            row(org, loc); last_org = org
        row(role, when, lf=I, rf=R)
        y += 1.5
        for b in bl: bullet(b)
        y -= 3

    head("Projects")
    for name, tech, url, bl in projs:
        c.setFont(Bd, S); c.drawString(M, y, name)
        x = M + stringWidth(name, Bd, S)
        c.setFont(I, S); c.setFillColor(MUTE); t = "  |  " + tech; c.drawString(x, y, t); c.setFillColor(INK)
        lw = stringWidth("GitHub", R, S)
        link_text(W - M - lw, y, "GitHub", url)
        y -= LH - 0.5
        for b in bl: bullet(b)
        y -= 3

    head("Technical Skills")
    for k, val in skills:
        lab = k + ": "; lw = stringWidth(lab, Bd, S)
        first = True
        for ln in rich_lines(val, W - 2*M - lw):
            if first:
                c.setFont(Bd, S); c.drawString(M, y, lab)
            draw_rich(ln, M + lw, y); y -= LH - 0.6; first = False
        y -= 1

    head("Achievements")
    for a_ in ACH: bullet(a_)
    c.save()
    return y  # remaining space above the bottom edge

# ---------- DOCX ----------
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import RGBColor

def add_link(para, label, url, size=None):
    part = para.part
    r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    h = OxmlElement("w:hyperlink"); h.set(qn("r:id"), r_id)
    r = OxmlElement("w:r"); rPr = OxmlElement("w:rPr")
    col = OxmlElement("w:color"); col.set(qn("w:val"), "1A4F8B"); rPr.append(col)
    if size:
        sz = OxmlElement("w:sz"); sz.set(qn("w:val"), str(int(size * 2))); rPr.append(sz)
    r.append(rPr); t = OxmlElement("w:t"); t.text = label; r.append(t); h.append(r); para._p.append(h)

def rich(para, text):
    for i, part in enumerate(re.split(r"\*\*", text)):
        if part:
            para.add_run(part).bold = (i % 2 == 1)

def make_docx(v, path):
    exp, skills, projs = sections(v)
    d = docx.Document()
    for s in d.sections:
        s.top_margin = s.bottom_margin = Inches(.6); s.left_margin = s.right_margin = Inches(.65)
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
    st.paragraph_format.space_after = Pt(0); st.paragraph_format.space_before = Pt(0); st.paragraph_format.line_spacing = 1.05
    RIGHT = Inches(7.2)
    def p(text="", bold=False, italic=False, size=None, align=None, after=0, before=0):
        para = d.add_paragraph()
        if text:
            r = para.add_run(text); r.bold = bold; r.italic = italic
            if size: r.font.size = Pt(size)
        if align is not None: para.alignment = align
        para.paragraph_format.space_after = Pt(after); para.paragraph_format.space_before = Pt(before); return para
    def head(t):
        para = p(t.upper(), bold=True, size=11, before=9, after=4)
        pPr = para._p.get_or_add_pPr(); bdr = OxmlElement("w:pBdr"); b = OxmlElement("w:bottom")
        for k, val in (("val", "single"), ("sz", "6"), ("space", "1"), ("color", "9AA5B1")): b.set(qn("w:" + k), val)
        bdr.append(b); pPr.append(bdr)
    def bullet(t):
        para = d.add_paragraph(style="List Bullet"); rich(para, t); para.paragraph_format.space_after = Pt(1.5)
    def lr(left, rightt, italic_left=False, before=0):
        para = p(before=before); r = para.add_run(left); r.bold = not italic_left; r.italic = italic_left
        if rightt: para.add_run("\t" + rightt)
        para.paragraph_format.tab_stops.add_tab_stop(RIGHT, alignment=2); return para
    p("Naveen Nagesh Narasapur", bold=True, size=19, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    cp = p(align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    for i, (label, url) in enumerate(LINKS):
        add_link(cp, label, url, size=10)
        if i < len(LINKS) - 1:
            r = cp.add_run("   |   "); r.font.size = Pt(10); r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)
    head("Education"); lr(EDU[0][0], EDU[0][1]); p(EDU[0][2]); p(EDU[1][0], size=10)
    head("Experience")
    last = None
    for (org, role, loc, when), bl in exp:
        if org != last:
            lr(org, loc, before=0 if last is None else 4); last = org
        lr(role, when, italic_left=True); [bullet(b) for b in bl]
    head("Projects")
    for name, tech, url, bl in projs:
        para = p(before=3); para.add_run(name).bold = True
        r = para.add_run("  |  " + tech); r.italic = True
        para.add_run("\t"); add_link(para, "GitHub", url)
        para.paragraph_format.tab_stops.add_tab_stop(RIGHT, alignment=2)
        [bullet(b) for b in bl]
    head("Technical Skills")
    for k, val in skills:
        para = p(after=1.5); para.add_run(k + ": ").bold = True; rich(para, val)
    head("Achievements"); [bullet(a_) for a_ in ACH]
    d.core_properties.author = "Naveen Narasapur"; d.core_properties.title = "Naveen Narasapur – Resume"
    d.save(path)

# ---------- Markdown ----------
def md(v, path):
    exp, skills, projs = sections(v)
    L = ["# Naveen Nagesh Narasapur", " | ".join(f"[{l}]({u})" for l, u in LINKS), "", "## Education",
         f"**{EDU[0][0]}** — {EDU[0][1]}  ", EDU[0][2] + "  ", EDU[1][0], "", "## Experience"]
    for (org, role, loc, when), bl in exp:
        L += [f"**{org}**, *{role}* — {when}"] + [f"- {b}" for b in bl] + [""]
    L += ["## Projects"]
    for name, tech, url, bl in projs:
        L += [f"**{name}** | *{tech}* | [GitHub]({url})"] + [f"- {b}" for b in bl] + [""]
    L += ["## Technical Skills"] + [f"- **{k}:** {val}" for k, val in skills] + ["", "## Achievements"] + [f"- {a_}" for a_ in ACH]
    path.write_text("\n".join(L) + "\n", encoding="utf-8")

if __name__ == "__main__":
    for v in VARIANTS:
        d = OUT / v; d.mkdir(exist_ok=True)
        stem = "Naveen_Narasapur_Resume_" + "_".join(w.upper() if w in ("ml",) else w.capitalize() for w in v.split("_"))
        left = pdf(v, d / f"{stem}.pdf")
        make_docx(v, d / f"{stem}.docx"); md(v, d / f"{stem}.md")
        print(f"{v}: bottom y = {left:.0f}pt ({'OK one page' if left > 40 else 'OVERFLOW'})")
