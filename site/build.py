#!/usr/bin/env python3
"""Build the A22 Research site from content/ dossiers. Requires pandoc."""
import html, pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
OUT = ROOT / "site" / "public"
OUT.mkdir(parents=True, exist_ok=True)

CSS = """
:root { --bg:#faf9f6; --panel:#ffffff; --ink:#1a1a1f; --muted:#6f6f78; --line:#e6e3dc;
  --accent:#8a1e2d; --accent-soft:#f6ebec; --live:#166534; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#131316; --panel:#1c1c21; --ink:#e8e6e3; --muted:#9a9aa3; --line:#2b2b33;
    --accent:#e0697a; --accent-soft:#311e22; --live:#4ade80; }
}
* { box-sizing:border-box; }
body { margin:0; font:16px/1.7 Georgia,'Times New Roman',serif; background:var(--bg); color:var(--ink); }
.wrap { max-width:840px; margin:0 auto; padding:48px 28px 96px; }
header.site { border-bottom:2px solid var(--ink); padding-bottom:18px; margin-bottom:36px; }
.brand { font:700 15px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  letter-spacing:.22em; text-transform:uppercase; }
.brand a { color:var(--ink); text-decoration:none; }
.brand .a22 { color:var(--accent); }
.tagline { font-size:13px; color:var(--muted); margin-top:6px;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
h1 { font-size:30px; line-height:1.25; margin:0 0 8px; letter-spacing:-.01em; }
h2 { font-size:21px; margin:36px 0 10px; }
h3 { font-size:17px; margin:24px 0 8px; }
a { color:var(--accent); }
em { color:var(--muted); }
code { font-size:14px; background:var(--accent-soft); padding:1px 5px; border-radius:4px; }
blockquote { margin:14px 0; padding:10px 18px; border-left:3px solid var(--accent); background:var(--panel); }
hr { border:none; border-top:1px solid var(--line); margin:28px 0; }
.tablewrap { overflow-x:auto; margin:16px 0; border:1px solid var(--line); border-radius:6px; }
table { border-collapse:collapse; width:100%; font-size:14px; background:var(--panel);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
th, td { padding:9px 12px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }
th { font-size:12px; text-transform:uppercase; letter-spacing:.05em; }
tr:last-child td { border-bottom:none; }
.meta { font:12px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  color:var(--muted); text-transform:uppercase; letter-spacing:.08em; margin-bottom:10px; }
.meta .theme { color:var(--accent); font-weight:600; }
.badge { display:inline-block; border:1px solid var(--line); border-radius:999px; padding:1px 10px; }
.badge.living { color:var(--live); border-color:var(--live); }
.card { display:block; border:1px solid var(--line); border-radius:8px; background:var(--panel);
  padding:20px 22px; margin:18px 0; text-decoration:none; color:var(--ink); }
.card:hover { border-color:var(--accent); }
.card h2 { margin:2px 0 6px; font-size:22px; }
.card .verdict { color:var(--muted); font-style:italic; margin:0; }
.subnav { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; font-size:13.5px;
  border:1px solid var(--line); border-radius:8px; background:var(--panel); padding:12px 16px; margin:22px 0; }
.subnav b { font-size:11px; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); }
.subnav a { display:inline-block; margin:3px 12px 3px 0; }
.crumb { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; font-size:13px; margin-bottom:14px; }
@media (max-width:600px){ .wrap{padding:28px 16px 64px} h1{font-size:25px} }
"""


def parse_frontmatter(text):
    meta, body = {}, text
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            for line in text[4:end].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            body = text[end + 4:].lstrip("\n")
    return meta, body


def render_md(md_text):
    h = subprocess.run(["pandoc", "-f", "gfm", "-t", "html"],
                       input=md_text, capture_output=True, text=True, check=True).stdout
    h = re.sub(r'href="((?!https?://)[^"]+)\.md"', r'href="\1.html"', h)
    return h.replace("<table>", '<div class="tablewrap"><table>').replace("</table>", "</table></div>")


def shell(title, body_html, depth=0):
    up = "../" * depth
    return f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} — A22 Research</title><style>{CSS}</style></head>
<body><div class="wrap"><header class="site">
<div class="brand"><a href="{up}index.html"><span class="a22">A22</span> RESEARCH</a></div>
<div class="tagline">A running loop of intelligence across themes.</div>
</header>{body_html}</div></body></html>"""


def page_title(md_path):
    for line in md_path.read_text().splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return md_path.stem.replace("-", " ").title()


dossiers = []
for d in sorted(CONTENT.iterdir()) if CONTENT.exists() else []:
    idx = d / "index.md"
    if not d.is_dir() or not idx.exists():
        continue
    meta, body = parse_frontmatter(idx.read_text())
    subs = sorted(p for p in d.rglob("*.md") if p != idx)
    dossiers.append((d.name, meta, body, subs))

for slug, meta, body, subs in dossiers:
    out_dir = OUT / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    status = meta.get("status", "living")
    head = (f'<div class="meta"><span class="theme">{html.escape(meta.get("theme",""))}</span> · '
            f'<span class="badge {status}">{status}</span> · '
            f'first published {meta.get("created","")} · updated {meta.get("updated","")}</div>')
    subnav = ""
    if subs:
        links = " ".join(
            f'<a href="{p.relative_to(CONTENT / slug).with_suffix(".html")}">{html.escape(page_title(p))}</a>'
            for p in subs)
        subnav = f'<div class="subnav"><b>In this dossier</b><br>{links}</div>'
    (out_dir / "index.html").write_text(shell(meta.get("title", slug), head + render_md(body) + subnav, depth=1))
    for p in subs:
        rel = p.relative_to(CONTENT / slug)
        sub_out = out_dir / rel.with_suffix(".html")
        sub_out.parent.mkdir(parents=True, exist_ok=True)
        back = "../" * (len(rel.parts) - 1)
        crumb = f'<div class="crumb"><a href="{back}index.html">← {html.escape(meta.get("title", slug))}</a></div>'
        sub_out.write_text(shell(page_title(p), crumb + render_md(p.read_text()), depth=1 + len(rel.parts) - 1))
    print(f"built {slug} ({1 + len(subs)} pages)")

cards = ""
for slug, meta, body, subs in sorted(dossiers, key=lambda x: x[1].get("updated", ""), reverse=True):
    cards += (f'<a class="card" href="{slug}/index.html">'
              f'<div class="meta"><span class="theme">{html.escape(meta.get("theme",""))}</span> · '
              f'updated {meta.get("updated","")}</div>'
              f'<h2>{html.escape(meta.get("title", slug))}</h2>'
              f'<p class="verdict">{html.escape(meta.get("verdict",""))}</p></a>')
if not cards:
    cards = "<p><em>Nothing published yet.</em></p>"
(OUT / "index.html").write_text(shell("A22 Research", f"<h1>Dossiers</h1>{cards}", depth=0))
print(f"built index ({len(dossiers)} dossiers)\nDone → {OUT}")
