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

CONTACT = "naveennarasapur05@gmail.com | naveen-narasapur.in | linkedin.com/in/naveen-narasapur-936226256 | github.com/NaveenNarasapur"

EDU = [("KLE Technological University, Hubli", "2022 – 2026",
        "B.E., Computer Science and Engineering (Artificial Intelligence) | CGPA: 8.90/10"),
       ("Class XII 97.17% (Vidyaniketan PU College, 2022)  |  Class X 94.08% (JSS EMS, Dharwad, 2020)", "", "")]

KPMG_FT = ("KPMG Global Services, Analyst, Advisory (Oracle practice)", "Full-time  |  Sep 2026 – Present")
NOTICE = "Notice period: 60 days"
KPMG_IN = ("KPMG Global Services, Oracle Practice", "Intern  |  Jan 2026 – Jul 2026")

B = {
 "ft1": "Build and support Oracle Integration Cloud (OIC) integrations between Oracle HCM Cloud and connected enterprise systems using adapters, data mappings and orchestrated workflows.",
 "ft2": "Write SQL and PL/SQL for data extraction, validation and transformation behind HCM integration flows.",
 "in1": "Built real-time OIC integrations moving data between systems; converted to a full-time offer at the end of the internship.",
 "in2": "Wrote SQL/PL-SQL queries, joins and stored procedures against real datasets; delivered work through Jira and Confluence.",
 "ftO1": "Build and support Oracle Integration Cloud (OIC) integrations for Oracle HCM Cloud on an enterprise client engagement for a US-based utility-services company: connections, adapters, lookups, mappings and orchestrated workflows.",
 "ftO2": "Work with HCM Extracts, BI Publisher and OTBI reports to source and validate HR data for downstream integrations; write SQL and PL/SQL for extraction, validation and transformation.",
 "ftD1": "Write SQL and PL/SQL to extract, validate and transform HR data for Oracle HCM integrations, working with HCM Extracts, BI Publisher and OTBI as data sources.",
 "ftD2": "Build Oracle Integration Cloud (OIC) flows that move data between Oracle HCM Cloud and connected enterprise systems using adapters, lookups and mappings.",
 # webhook relay
 "rl1": "Built a webhook delivery service (FastAPI, PostgreSQL) with at-least-once guarantees: transactional fan-out, worker job claiming via FOR UPDATE SKIP LOCKED with leases, exponential backoff with full jitter and a dead-letter queue with replay.",
 "rl2": "Enforced idempotency keys with a unique constraint (20 concurrent duplicate requests produce exactly 1 event), HMAC-SHA256 payload signing, hashed per-tenant API keys and SSRF blocking of private/metadata IPs.",
 "rl3": "Wrote 44 pytest tests on real PostgreSQL covering timeouts, 5xx/4xx handling, crashed and concurrent workers; measured ~1,000 deliveries/s with 4 workers on a 2-CPU VM with zero double deliveries.",
 # ddos
 "dd1": "Built a leakage-aware detection pipeline on CIC-IDS2017 (223K flows): de-duplication, identifier removal, temporal train/test split; compared Logistic Regression, Decision Tree, Random Forest, Gradient Boosting and BIRCH.",
 "dd2": "Served Random Forest via an API-key-secured FastAPI service with a metrics dashboard: F1 0.998 at 0.02% false-positive rate (6 of 32,767 benign flows) on the held-out later traffic.",
 "dd3": "Showed by ablation that gradient boosting relied on TCP-window fingerprint features (FPR rose 15x when removed) while Random Forest did not; 29 tests, 95% coverage, GitHub Actions CI.",
 # zsl
 "zs1": "Implemented zero-shot image classification in PyTorch: frozen ResNet-101 features mapped to 85 class attributes by a learned compatibility function, with selection on disjoint validation classes.",
 "zs2": "Reached 59.0% unseen-class accuracy on the standard AwA2 split (published ALE: 62.5%) and 58.2 GZSL harmonic mean with calibrated stacking; deterministic, 14 tests.",
 "zs3": "Audited a previously published 90.48% result: measured that it matches conventional seen-class accuracy (92.7%), not zero-shot accuracy, and documented the correction.",
 # geosnap
 "geo1": "Built an offline-capable React + TypeScript PWA that embeds GPS EXIF in camera JPEGs client-side, rewriting only the APP1 segment (image bytes unchanged) and re-verifying output with an independent parser.",
}

ACH = ["CodeChef 3-star (max rating 1632, 315 problems solved); ACM ICPC Asia Amritapuri Regional 2023 participant (Honorable Mention).",
       "GATE Data Science & AI 2026: All India Rank 4561."]

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

PROJECTS = {
 "relay": ("Relay: Reliable Webhook Delivery Service", "Python, FastAPI, PostgreSQL | github.com/NaveenNarasapur/webhook-relay", ["rl1", "rl2", "rl3"]),
 "relay_g": ("Relay: Reliable Webhook Delivery Service", "Python, FastAPI, PostgreSQL | github.com/NaveenNarasapur/webhook-relay", ["rl1", "rl3"]),
 "ddos": ("DDoS Flow Detection Service", "Python, scikit-learn, FastAPI | github.com/NaveenNarasapur/ddos-detection", ["dd1", "dd2", "dd3"]),
 "ddos_b": ("DDoS Flow Detection Service", "Python, scikit-learn, FastAPI | github.com/NaveenNarasapur/ddos-detection", ["dd1", "dd2"]),
 "zsl": ("Zero-Shot Image Classification (AwA2)", "PyTorch, ResNet | github.com/NaveenNarasapur/zero-shot-awa2", ["zs1", "zs2", "zs3"]),
 "zsl_b": ("Zero-Shot Image Classification (AwA2)", "PyTorch, ResNet | github.com/NaveenNarasapur/zero-shot-awa2", ["zs2", "zs3"]),
 "geo": ("GeoSnap: Geotagging Camera PWA", "React, TypeScript | github.com/NaveenNarasapur/geosnap", ["geo1"]),
}

VARIANTS = {
 "backend": dict(skills="backend", projects=["relay", "ddos", "zsl_b", "geo"]),
 "data_engineer": dict(skills="data", projects=["ddos", "relay", "zsl_b"], exp=("ftD1", "ftD2")),
 "oracle_integration": dict(skills="oracle", projects=["relay", "ddos", "zsl_b"], exp=("ftO1", "ftO2")),
 "python_ml": dict(skills="ml", projects=["zsl", "ddos", "relay_g"]),
 "generalist": dict(skills="general", projects=["relay", "ddos", "zsl", "geo"]),
}

def sections(v):
    cfg = VARIANTS[v]
    ft = cfg.get("exp", ("ft1", "ft2"))
    exp = [(KPMG_FT, [B[k] for k in ft]), (KPMG_IN, [B["in1"], B["in2"]])]
    projs = [(PROJECTS[p][0], PROJECTS[p][1], [B[k] for k in PROJECTS[p][2]]) for p in cfg["projects"]]
    return exp, SKILLS[cfg["skills"]], projs

# ---------- PDF ----------
def pdf(v, path):
    exp, skills, projs = sections(v)
    W, H = A4; M = 40; c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle("Naveen Narasapur – Resume"); c.setAuthor("Naveen Narasapur")
    y = H - 44
    R, Bd, I = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"
    def line(t, f=R, s=9.6, x=M, dy=12.2):
        nonlocal y; c.setFont(f, s); c.drawString(x, y, t); y -= dy
    def right(t, f=R, s=9.6):
        c.setFont(f, s); c.drawRightString(W - M, y + 12.2, t)
    def wrap(t, f, s, width):
        words, out, cur = t.split(), [], ""
        for w in words:
            nxt = (cur + " " + w).strip()
            if stringWidth(nxt, f, s) > width: out.append(cur); cur = w
            else: cur = nxt
        return out + [cur]
    def bullet(t):
        nonlocal y
        for i, ln in enumerate(wrap(t, R, 9.6, W - 2*M - 12)):
            if i == 0: c.setFont(R, 9.6); c.drawString(M + 2, y, "•")
            line(ln, x=M + 12, dy=11.8)
    def head(t):
        nonlocal y
        y -= 4; line(t.upper(), Bd, 10.2, dy=4); c.setLineWidth(.6); c.line(M, y, W - M, y); y -= 11
    c.setFont(Bd, 17); c.drawCentredString(W/2, y, "NAVEEN NAGESH NARASAPUR"); y -= 15
    c.setFont(R, 8.3); c.drawCentredString(W/2, y, CONTACT); y -= 10
    head("Education")
    line(EDU[0][0], Bd); right(EDU[0][1]); line(EDU[0][2]); line(EDU[1][0], s=9.2)
    head("Experience")
    for (org, when), bl in exp:
        line(org, Bd); right(when, I)
        for b in bl: bullet(b)
        y -= 2
    head("Technical Skills")
    for k, val in skills:
        for i, ln in enumerate(wrap(f"{k}: {val}", R, 9.6, W - 2*M - 14)):  # bold label is wider
            if i == 0:
                c.setFont(Bd, 9.6); c.drawString(M, y, k + ":")
                c.setFont(R, 9.6); c.drawString(M + stringWidth(k + ": ", Bd, 9.6), y, ln[len(k)+2:]); y -= 12.2
            else: line(ln)
    head("Projects")
    for name, tech, bl in projs:
        c.setFont(Bd, 9.6); c.drawString(M, y, name)
        c.setFont(I, 9.2); c.drawString(M + stringWidth(name + "  ", Bd, 9.6), y, "| " + tech); y -= 12.2
        for b in bl: bullet(b)
        y -= 2
    head("Achievements")
    for a in ACH: bullet(a)
    c.save()
    return y  # remaining space (must be > bottom margin)

# ---------- DOCX ----------
def make_docx(v, path):
    exp, skills, projs = sections(v)
    d = docx.Document()
    for s in d.sections:
        s.top_margin = s.bottom_margin = Inches(.55); s.left_margin = s.right_margin = Inches(.6)
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10)
    st.paragraph_format.space_after = Pt(0); st.paragraph_format.space_before = Pt(0)
    def p(text="", bold=False, italic=False, size=None, align=None, after=0):
        para = d.add_paragraph(); r = para.add_run(text); r.bold = bold; r.italic = italic
        if size: r.font.size = Pt(size)
        if align: para.alignment = align
        para.paragraph_format.space_after = Pt(after); return para
    def head(t):
        para = p(t.upper(), bold=True, size=10.5); para.paragraph_format.space_before = Pt(6)
        pPr = para._p.get_or_add_pPr()
        from docx.oxml import OxmlElement; from docx.oxml.ns import qn
        bdr = OxmlElement("w:pBdr"); b = OxmlElement("w:bottom")
        for k, val in (("val", "single"), ("sz", "4"), ("space", "1"), ("color", "000000")): b.set(qn("w:" + k), val)
        bdr.append(b); pPr.append(bdr)
    def bullet(t):
        para = d.add_paragraph(t, style="List Bullet"); para.paragraph_format.space_after = Pt(0)
    def lr(left, rightt):
        para = p(left, bold=True); para.add_run("\t" + rightt).italic = True
        para.paragraph_format.tab_stops.add_tab_stop(Inches(7.3), alignment=2)
    p("NAVEEN NAGESH NARASAPUR", bold=True, size=16, align=WD_ALIGN_PARAGRAPH.CENTER)
    p(CONTACT, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
    head("Education"); lr(EDU[0][0], EDU[0][1]); p(EDU[0][2]); p(EDU[1][0], size=9.5)
    head("Experience")
    for (org, when), bl in exp:
        lr(org, when); [bullet(b) for b in bl]
    head("Technical Skills")
    for k, val in skills:
        para = p(k + ": ", bold=True); para.add_run(val)
    head("Projects")
    for name, tech, bl in projs:
        para = p(name, bold=True); r = para.add_run("  | " + tech); r.italic = True
        [bullet(b) for b in bl]
    head("Achievements"); [bullet(a) for a in ACH]
    d.core_properties.author = "Naveen Narasapur"; d.core_properties.title = "Naveen Narasapur – Resume"
    d.save(path)

# ---------- Markdown ----------
def md(v, path):
    exp, skills, projs = sections(v)
    L = ["# Naveen Nagesh Narasapur", CONTACT, "", "## Education",
         f"**{EDU[0][0]}** — {EDU[0][1]}  ", EDU[0][2] + "  ", EDU[1][0], "", "## Experience"]
    for (org, when), bl in exp:
        L += [f"**{org}** — *{when}*"] + [f"- {b}" for b in bl] + [""]
    L += ["## Technical Skills"] + [f"- **{k}:** {val}" for k, val in skills] + ["", "## Projects"]
    for name, tech, bl in projs:
        L += [f"**{name}** | *{tech}*"] + [f"- {b}" for b in bl] + [""]
    L += ["## Achievements"] + [f"- {a}" for a in ACH]
    path.write_text("\n".join(L) + "\n", encoding="utf-8")

if __name__ == "__main__":
    for v in VARIANTS:
        d = OUT / v; d.mkdir(exist_ok=True)
        stem = "Naveen_Narasapur_Resume_" + "_".join(w.upper() if w in ("ml",) else w.capitalize() for w in v.split("_"))
        left = pdf(v, d / f"{stem}.pdf")
        make_docx(v, d / f"{stem}.docx"); md(v, d / f"{stem}.md")
        print(f"{v}: bottom y = {left:.0f}pt ({'OK one page' if left > 36 else 'OVERFLOW'})")
