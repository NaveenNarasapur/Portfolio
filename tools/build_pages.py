"""Generates /projects/*.html from the content below. Run: python tools/build_pages.py
Edit the CONTENT here, not the generated HTML."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://naveen-narasapur.in"
import hashlib
CSS_V = hashlib.sha1((ROOT / "assets" / "style.css").read_bytes()).hexdigest()[:8]  # cache-busting

def box(x, y, w, label, sub=""):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="54" rx="8" fill="none" stroke="currentColor" stroke-opacity=".45"/>'
    s += f'<text x="{x+w/2}" y="{y+(24 if sub else 32)}" text-anchor="middle" font-size="13" font-weight="600" fill="currentColor">{label}</text>'
    if sub:
        s += f'<text x="{x+w/2}" y="{y+42}" text-anchor="middle" font-size="11" fill="currentColor" fill-opacity=".65">{sub}</text>'
    return s

def arrow(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="currentColor" stroke-opacity=".5" marker-end="url(#a)"/>'

def pipeline(steps, caption):
    """Horizontal pipeline diagram; wraps to two rows when > 4 steps."""
    w, gap, per_row = 150, 34, 4
    rows = [steps[i:i+per_row] for i in range(0, len(steps), per_row)]
    width = per_row * w + (per_row - 1) * gap
    height = len(rows) * 54 + (len(rows) - 1) * 40 + 4
    parts = []
    for r, row in enumerate(rows):
        y = 2 + r * 94
        for i, (lab, sub) in enumerate(row):
            x = i * (w + gap)
            parts.append(box(x, y, w, lab, sub))
            if i < len(row) - 1:
                parts.append(arrow(x + w, y + 27, x + w + gap - 3, y + 27))
        if r < len(rows) - 1:
            lx = (len(row) - 1) * (w + gap) + w / 2
            parts.append(f'<path d="M{lx} {y+54} V{y+74} H{w/2} V{y+91}" fill="none" stroke="currentColor" stroke-opacity=".5" marker-end="url(#a)"/>')
    return (f'<figure><svg viewBox="-2 0 {width+4} {height}" role="img" aria-label="{caption}" style="color:var(--text);font-family:var(--sans)">'
            '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0 0L10 5L0 10z" fill="currentColor" fill-opacity=".6"/></marker></defs>'
            + "".join(parts) + f'</svg><figcaption>{caption}</figcaption></figure>')

PAGES = {
"geosnap": dict(
  title="GeoSnap: privacy-first geotagging camera PWA",
  desc="Case study: a React + TypeScript PWA that embeds and verifies GPS EXIF in camera JPEGs entirely in the browser, with lossless metadata rewriting.",
  meta=["2026", "Solo project", "React 19 · TypeScript · Vite · piexifjs · Workbox · Cloudflare Pages",
        '<a href="https://github.com/NaveenNarasapur/geosnap">Source on GitHub</a>'],
  body=f"""
<h2>Problem</h2>
<p>Field and site photos often need trustworthy location data: proof of a visit, an inspection, a delivery. Phone cameras either strip location or bury it, and most "GPS camera" apps upload photos to a server and draw coordinates onto the pixels, which is lossy and can't be read back by software. I wanted a tool that writes <em>real</em> EXIF GPS tags, never uploads the photo, and is honest about whether it worked.</p>

<h2>Architecture</h2>
{pipeline([("Camera","ImageCapture API"),("GPS fix","Geolocation API"),("EXIF writer","DMS rationals → APP1"),("Verifier","re-parse & compare"),("Export","JPEG / PNG / WebP"),("Optional lookup","Nominatim, user-triggered")],
"Capture → locate → embed → verify → export. Everything runs client-side; the only network call is an opt-in reverse-geocode.")}
<ul>
<li><b>Capture.</b> On Chromium with a rear camera, <code>ImageCapture.takePhoto()</code> returns a full-sensor JPEG; elsewhere the frame is taken from the video stream at native resolution. Camera tracks are stopped as soon as the user leaves the screen.</li>
<li><b>Lossless metadata rewrite.</b> For GPS-only and "original" exports at quality ≥ 92%, the camera's JPEG bytes are kept and only the APP1/EXIF segment is replaced, so the compressed image data stays byte-identical.</li>
<li><b>Verify, don't assume.</b> After writing, the file is parsed again and the coordinates compared with the fix. If the check fails the UI does not claim the photo is geotagged.</li>
<li><b>Offline & private.</b> A Workbox service worker precaches only the app shell. There is deliberately no runtime caching, so photos, coordinates and geocoding responses are never persisted.</li>
</ul>

<h2>Key decisions</h2>
<table>
<tr><th>Decision</th><th>Alternative</th><th>Why</th></tr>
<tr><td>Client-only processing</td><td>Upload to a backend for EXIF writing</td><td>Location + photo is sensitive data; no server means nothing to secure or leak, and zero hosting cost.</td></tr>
<tr><td>Rewrite APP1 in place</td><td>Decode → canvas → re-encode</td><td>Re-encoding loses quality and drops the camera's own metadata. In-place rewrite is lossless.</td></tr>
<tr><td>Independent read-back (exifr)</td><td>Trust the writer library</td><td>Catches writer bugs, e.g. DMS rounding at 59.99999″, that a single library would hide.</td></tr>
<tr><td>Lazy-load the editor</td><td>One bundle</td><td>Keeps first load at ~82 kB gzip; the overlay editor (~18 kB) loads on demand.</td></tr>
</table>

<h2>Limitations</h2>
<ul>
<li>PNG and WebP GPS metadata is not reliably read by common photo viewers, so those exports show coordinates only as an overlay, and the UI says so.</li>
<li>Safari and Firefox lack <code>ImageCapture</code> and torch control; those paths fall back to stream-resolution frames.</li>
<li>Real-device checks (GPS accuracy outdoors, iOS install flow) are still a manual checklist.</li>
</ul>
<h2>Next version</h2>
<ul><li>Add automated EXIF round-trip tests and run them in CI on every push.</li><li>Batch capture with a per-session GPX track export.</li><li>Optional signed hash of image + coordinates to make tampering detectable.</li></ul>
"""),

"webhook-relay": dict(
  title="Relay: reliable webhook delivery service",
  desc="Case study: a FastAPI + PostgreSQL webhook delivery service with at-least-once delivery, SKIP LOCKED workers, exponential backoff, idempotency keys and a dead-letter queue. 44 tests, ~1,000 deliveries/s.",
  meta=["2026", "Solo project", "Python · FastAPI · PostgreSQL 16 · Docker · GitHub Actions",
        '<a href="https://github.com/NaveenNarasapur/webhook-relay">Source on GitHub</a>'],
  body=f"""
<h2>Problem</h2>
<p>Every SaaS product that sends webhooks hits the same problems: receivers go down, time out, rate-limit, or return errors; producers retry and create duplicates; workers crash mid-request. Relay accepts an event once and guarantees each subscribed endpoint eventually receives it, or the delivery lands in a dead-letter queue where it can be inspected and replayed.</p>

<h2>Architecture</h2>
{pipeline([("Producer","POST /v1/events"),("API","auth · idempotency"),("PostgreSQL","event + deliveries, 1 txn"),("Workers ×N","SKIP LOCKED + lease"),("Receiver","HMAC-signed POST"),("Record","guarded UPDATE"),("Retry / DLQ","backoff · replay")],
"The event and its fan-out deliveries are written in one transaction; workers claim due rows without blocking each other; every outcome is a guarded state transition.")}
<ul>
<li><b>No lost events.</b> The event row and one delivery row per matching endpoint are inserted in one transaction (outbox pattern), so an accepted event can't exist without its deliveries.</li>
<li><b>No duplicate events.</b> <code>UNIQUE(tenant, idempotency_key)</code>; a retried POST returns the original event, and the same key with a different body returns 409. Twenty concurrent identical requests produce exactly one event.</li>
<li><b>Safe concurrency.</b> Workers claim with <code>UPDATE … WHERE id IN (SELECT … FOR UPDATE SKIP LOCKED)</code> and set a lease. A crashed worker's rows are reclaimed when its lease expires, and its late write is rejected because <code>attempts</code> no longer matches.</li>
<li><b>Polite retries.</b> Exponential backoff with full jitter, <code>Retry-After</code> honoured, permanent 4xx not retried, dead-lettered after N attempts.</li>
<li><b>Security.</b> Hashed API keys with tenant isolation, HMAC-SHA256 signatures with a replay window, and SSRF blocking of private/metadata addresses at registration and again at send time.</li>
</ul>

<h2>Key decisions</h2>
<table>
<tr><th>Decision</th><th>Alternative</th><th>Why</th></tr>
<tr><td>PostgreSQL as the queue</td><td>Kafka / RabbitMQ</td><td>Transactional with the event write, one system to run, inspectable with SQL. Measured ~1k deliveries/s on 2 CPUs; a broker becomes worth it at much higher volume or for many consumer groups.</td></tr>
<tr><td>At-least-once</td><td>Exactly-once</td><td>Impossible over HTTP (an ACK can be lost after processing). A stable <code>relay-delivery-id</code> lets receivers dedupe.</td></tr>
<tr><td>Leases</td><td>Hold a transaction during the HTTP call</td><td>Would pin a connection and row locks for up to the 10 s timeout per request.</td></tr>
<tr><td>Full jitter</td><td>Plain exponential backoff</td><td>Prevents synchronised retry storms when a receiver recovers.</td></tr>
</table>

<h2>Testing and measurements</h2>
<p>44 pytest tests run against real PostgreSQL in CI: 5xx, timeouts, connection errors, 404/410 to dead-letter, max attempts, <code>Retry-After</code>, replay, crashed worker plus stale write, four concurrent workers (60 events, zero double deliveries) and concurrent duplicate POSTs. A real-process demo (API + worker + receiver that fails twice) shows 503 → 503 → 200 on attempt 3. A benchmark of the claim → deliver → record loop measured ~800 deliveries/s with one worker and ~1,040/s with four on a 2-CPU VM. The receiver there is an in-memory mock, so this is Relay's own database overhead, not network delivery speed.</p>

<h2>Limitations and next steps</h2>
<ul><li>No per-endpoint circuit breaker or rate limit yet.</li><li>DNS-rebinding window between the SSRF check and the connection; fix by pinning the resolved IP or using an egress proxy.</li><li>No retention job for old attempts; add partitioning or pruning.</li><li>Prometheus metrics endpoint.</li></ul>
"""),

"ddos-detection": dict(
  title="DDoS flow detection: ML pipeline + inference service",
  desc="Case study: leakage-aware DDoS detection on CIC-IDS2017 (223K flows), five models compared under a temporal split, Random Forest served by an authenticated FastAPI service. F1 0.998 at 0.02% false-positive rate.",
  meta=["2025 → rebuilt 2026", "Python · scikit-learn · FastAPI", '<a href="https://github.com/NaveenNarasapur/ddos-detection">Source on GitHub</a>'],
  body=f"""
<p class="note">Defensive project: detection only, on a public offline dataset. No traffic generation.</p>
<h2>Problem</h2>
<p>Classify network flows (CICFlowMeter features) as benign or DDoS so that false alarms stay rare, because every alert costs analyst time. The project began in 2025 as unsupervised BIRCH clustering with a Proof-of-Work mitigation layer; in 2026 I rebuilt it as a reproducible, tested pipeline and kept the original approach as a baseline.</p>

<h2>Pipeline</h2>
{pipeline([("CIC-IDS2017 CSV","225,745 flows"),("Clean","drop IDs · NaN/inf · dupes"),("Temporal split","train past / test future"),("Preprocess","fitted on train only"),("5 models","LR · DT · RF · HGB · BIRCH"),("Evaluate","F1 · FPR · ROC-AUC"),("FastAPI","API key · dashboard")],
"Preprocessing is part of the serialised sklearn Pipeline, so serving applies exactly what training fitted.")}

<h2>Results (temporal split, 44,617 test flows)</h2>
<table>
<tr><th>Model</th><th>F1</th><th>Recall</th><th>False-positive rate</th></tr>
<tr><td>Logistic regression</td><td>0.9931</td><td>0.9963</td><td>0.36%</td></tr>
<tr><td>Decision tree</td><td>0.9983</td><td>0.9977</td><td>0.04%</td></tr>
<tr><td><b>Random forest (served)</b></td><td>0.9977</td><td>0.9959</td><td><b>0.02%</b> (6 / 32,767)</td></tr>
<tr><td>Hist. gradient boosting</td><td>0.9986</td><td>0.9977</td><td>0.02%</td></tr>
<tr><td>BIRCH (original unsupervised approach)</td><td>0.4216</td><td>1.0000</td><td>99.2%</td></tr>
</table>
<p><b>What the numbers do and don't say.</b> This file contains one LOIC attack and is close to linearly separable, so near-perfect supervised scores mostly reflect the dataset. The informative results are the differences:</p>
<ul>
<li>Random Forest was chosen by a rule fixed in advance: lowest false-positive rate with recall ≥ 99%.</li>
<li>Removing the <code>Init_Win_bytes_*</code> features, which partly fingerprint the attacker's TCP stack, barely changed Random Forest (6 → 7 false positives) but raised gradient boosting's from 7 to 102. That model was leaning on the fingerprint.</li>
<li>BIRCH collapsed into one dominant cluster and flagged nearly everything. A high silhouette score (the 2025 report had 0.981) doesn't mean useful detection.</li>
<li>A random split scored higher than the temporal split for every model: the leakage effect of neighbouring flows from the same burst.</li>
</ul>

<h2>Engineering</h2>
<p>Modular package (data, features, models, train, evaluate, predict, API), YAML config with CLI overrides, JSON structured logs, 29 tests (95% coverage) on Python 3.11 and 3.13 in CI. The API fails closed when no keys are configured, returns 422 naming any missing feature, and caps batch size.</p>

<h2>Limitations</h2>
<ul><li>One attack, one day: cross-dataset evaluation (CIC-DDoS2019) is the next step.</li><li>The Mininet integration is documented (a CSV → API bridge) but was not run; it needs Linux with Open vSwitch.</li></ul>
"""),

"zero-shot": dict(
  title="Zero-shot image classification on AwA2",
  desc="Case study: recognising unseen animal classes from attributes with ResNet-101 features and a learned compatibility function: 59.0% unseen-class accuracy on the standard Proposed Split, plus an audit of an earlier 90.48% claim.",
  meta=["2025 → rebuilt 2026", "Python · PyTorch · ResNet", '<a href="https://github.com/NaveenNarasapur/zero-shot-awa2">Source on GitHub</a>'],
  body=f"""
<h2>Problem</h2>
<p>A conventional classifier can only predict classes it was trained on. Zero-shot learning recognises new classes from a description: here, the 85 semantic attributes of Animals with Attributes 2 ("striped", "aquatic", "has hooves"). The model trains on 40 classes and is tested on 10 it has never seen.</p>

<h2>Approach</h2>
{pipeline([("Image","AwA2"),("ResNet-101","frozen, 2048-d"),("Learned W","2048 → 85"),("Cosine score","vs each class's attributes")],
"One learned mapping into attribute space; any class with an attribute vector can be scored without retraining.")}
<ul>
<li><b>Standard protocol.</b> Proposed Split (Xian et al., 2018), whose unseen classes are disjoint from ImageNet-1k so the pretrained backbone can't leak them. Load-time checks fail if any unseen image reaches training.</li>
<li><b>Honest model selection.</b> Hyper-parameters are chosen on 13 validation classes disjoint from the 27 training classes, imitating the test condition. The test set is touched once.</li>
<li><b>GZSL calibration.</b> Calibrated stacking subtracts γ from seen-class scores to counter the bias toward training classes; γ is tuned on validation only.</li>
</ul>

<h2>Results</h2>
<table>
<tr><th></th><th>ZSL accuracy (10 unseen, mean per class)</th><th>GZSL unseen / seen / H</th></tr>
<tr><td><b>Bilinear compatibility</b></td><td><b>59.0%</b></td><td>45.5 / 80.9 / 58.2 (calibrated) · 20.3 / 86.8 / 32.9 (raw)</td></tr>
<tr><td>ESZSL baseline</td><td>47.6%</td><td>46.5 / 61.0 / 52.8</td></tr>
<tr><td><i>Published, same features: ALE / DeViSE</i></td><td><i>62.5 / 59.7</i></td><td><i>raw H 23.9 / 27.8</i></td></tr>
</table>
<p>Errors are semantic neighbours: dolphin → blue whale (67%), seal → walrus (46%), bat → rat (40%). Their attribute signatures are nearly identical, which is the known limit of attribute-only zero-shot learning.</p>

<h2>Auditing my own earlier number</h2>
<p>My 2025 paper reported 90.48% accuracy. The original code is lost, so I tested what that number is consistent with, on the same data:</p>
<table>
<tr><th>Measurement</th><th>Result</th></tr>
<tr><td>Standard zero-shot accuracy (this project)</td><td>59.0%</td></tr>
<tr><td>Conventional 40-way classification of seen classes</td><td>92.7% per-class / 94.5% overall</td></tr>
<tr><td>Zero-shot on random, non-standard class splits</td><td>64–85%</td></tr>
<tr><td>Binary seen-vs-unseen detection</td><td>72.6% (AUROC 0.84)</td></tr>
</table>
<p>The paper used a custom split, reported binary-classification metrics and compared against out-of-distribution detectors. 90.48% matches conventional or non-standard-split accuracy, not standard zero-shot performance, so I treat it as unverified and report 59.0%.</p>

<h2>Engineering</h2>
<p>Independent modules (features, semantic, model, train, metrics, inference), YAML config, checkpoints, deterministic training enforced by a test, 14 tests and CI; runs on CPU in about a minute.</p>
"""),
}

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Naveen Narasapur</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{base}/assets/og.png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/style.css?v={CSS_V}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
  <a class="brand" href="/">Naveen Narasapur</a>
  <nav aria-label="Primary"><ul><li><a href="/#experience">Experience</a></li><li><a href="/#projects">Projects</a></li><li><a href="/resume.pdf">Resume</a></li></ul></nav>
</div></header>
<main id="main"><div class="wrap"><article>
<p class="crumb"><a href="/#projects">← All projects</a></p>
<h1>{title}</h1>
<div class="meta">{meta}</div>
{body}
<p class="crumb"><a href="/#projects">← All projects</a></p>
</article></div></main>
<footer><div class="wrap"><span>© 2026 Naveen Narasapur</span><span><a href="mailto:naveennarasapur05@gmail.com">naveennarasapur05@gmail.com</a></span></div></footer>
</body>
</html>
"""

for slug, p in PAGES.items():
    url = f"{BASE}/projects/{slug}.html"
    html = TEMPLATE.format(CSS_V=CSS_V, title=p["title"], desc=p["desc"], url=url, base=BASE,
                           meta="".join(f"<span>{m}</span>" for m in p["meta"]), body=p["body"])
    (ROOT / "projects" / f"{slug}.html").write_text(html, encoding="utf-8")
    print("wrote", slug)
