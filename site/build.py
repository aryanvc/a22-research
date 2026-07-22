#!/usr/bin/env python3
"""Build the A22 site: landing page + research dossiers → site/public/.

Layout of the built site:
  /index.html                     landing (split hero + portfolio)
  /research/index.html            dossier index
  /research/<slug>/...            one dossier per content/<slug>/
  /assets/...                     css + media, copied verbatim

Inputs:
  data/portfolio.json             portfolio companies for the landing page
  content/<slug>/index.md         dossier main page (frontmatter: title, theme,
                                  verdict, status, created, updated) + subpages
  site/templates/*.html           {{TOKEN}}-style templates
  site/assets/media/*.mp4         hero loop videos (optional; placeholder used
                                  when absent — see scripts/generate_veo.py)

Requires pandoc.
"""
import datetime, html, json, pathlib, re, shutil, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
TEMPLATES = SITE / "templates"
ASSETS = SITE / "assets"
OUT = SITE / "public"
CONTENT = ROOT / "content"
DATA = ROOT / "data"


# ---------- helpers ----------

def template(name, **tokens):
    """Load a template and substitute {{TOKEN}} placeholders."""
    text = (TEMPLATES / name).read_text()
    for key, value in tokens.items():
        text = text.replace("{{" + key + "}}", value)
    return text


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


def markdown_to_html(md_text):
    h = subprocess.run(["pandoc", "-f", "gfm", "-t", "html"],
                       input=md_text, capture_output=True, text=True, check=True).stdout
    h = re.sub(r'href="((?!https?://)[^"]+)\.md"', r'href="\1.html"', h)
    return h.replace("<table>", '<div class="tablewrap"><table>').replace("</table>", "</table></div>")


def first_heading(md_path):
    for line in md_path.read_text().splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return md_path.stem.replace("-", " ").title()


def write_page(out_path, title, body_html):
    """Render a research page into the shared shell; ROOT is the relative path
    back to the site root from this page's directory."""
    depth = len(out_path.relative_to(OUT).parts) - 1
    page = template("page.html", TITLE=html.escape(title), ROOT="../" * depth, BODY=body_html)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page)


# ---------- landing ----------

def build_landing():
    """One 'scene' per portfolio company: real footage if a clip exists at
    assets/media/portfolio/<id>.mp4, otherwise a per-company animated
    placeholder keyed by its hue in portfolio.json."""
    portfolio = json.loads((DATA / "portfolio.json").read_text())
    scenes, clips = [], 0
    for i, c in enumerate(portfolio):
        file_no = f"File {i + 1:03d}"
        clip = ASSETS / "media" / "portfolio" / f"{c['id']}.mp4"
        if clip.exists():
            media = (f'<video autoplay muted loop playsinline '
                     f'src="assets/media/portfolio/{clip.name}"></video>')
            clips += 1
        else:
            media = f'<div class="ph" style="--h:{c.get("hue", 214)}"></div>'
        scenes.append(
            f'<a class="scene" href="#" data-file="{file_no}" '
            f'data-name="{html.escape(c["name"])}" data-stage="{html.escape(c["stage"])}">'
            f'{media}<div class="grain"></div>'
            f'<div class="scene-meta"><span class="file">{file_no}</span>'
            f'<span class="stage">{html.escape(c["stage"])}</span></div>'
            f'<h2 class="scene-name">{html.escape(c["name"])}</h2>'
            f'<span class="view">View file →</span></a>')

    page = template("landing.html", SCENES="\n".join(scenes),
                    FILE_COUNT=f"{len(portfolio):03d}",
                    YEAR=str(datetime.date.today().year))
    (OUT / "index.html").write_text(page)
    print(f"built landing ({len(portfolio)} files, {clips} with footage)")


# ---------- research ----------

def load_dossiers():
    dossiers = []
    if CONTENT.exists():
        for d in sorted(CONTENT.iterdir()):
            idx = d / "index.md"
            if d.is_dir() and idx.exists():
                meta, body = parse_frontmatter(idx.read_text())
                subs = sorted(p for p in d.rglob("*.md") if p != idx)
                dossiers.append((d.name, meta, body, subs))
    return dossiers


def build_dossier(slug, meta, body, subs):
    out_dir = OUT / "research" / slug
    status = meta.get("status", "living")
    head = (f'<div class="meta"><span class="theme">{html.escape(meta.get("theme", ""))}</span> · '
            f'<span class="badge {status}">{status}</span> · '
            f'first published {meta.get("created", "")} · updated {meta.get("updated", "")}</div>')
    subnav = ""
    if subs:
        links = " ".join(
            f'<a href="{p.relative_to(CONTENT / slug).with_suffix(".html")}">{html.escape(first_heading(p))}</a>'
            for p in subs)
        subnav = f'<div class="subnav"><b>In this dossier</b><br>{links}</div>'
    write_page(out_dir / "index.html", meta.get("title", slug),
               head + markdown_to_html(body) + subnav)

    for p in subs:
        rel = p.relative_to(CONTENT / slug)
        back = "../" * (len(rel.parts) - 1)
        crumb = (f'<div class="crumb"><a href="{back}index.html">'
                 f'← {html.escape(meta.get("title", slug))}</a></div>')
        write_page(out_dir / rel.with_suffix(".html"), first_heading(p),
                   crumb + markdown_to_html(p.read_text()))


def build_research_index(dossiers):
    cards = ""
    for slug, meta, _, _ in sorted(dossiers, key=lambda x: x[1].get("updated", ""), reverse=True):
        cards += (f'<a class="card" href="{slug}/index.html">'
                  f'<div class="meta"><span class="theme">{html.escape(meta.get("theme", ""))}</span> · '
                  f'updated {meta.get("updated", "")}</div>'
                  f'<h2>{html.escape(meta.get("title", slug))}</h2>'
                  f'<p class="verdict">{html.escape(meta.get("verdict", ""))}</p></a>')
    if not cards:
        cards = "<p><em>Nothing published yet.</em></p>"
    write_page(OUT / "research" / "index.html", "Research", f"<h1>Dossiers</h1>{cards}")


# ---------- main ----------

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ASSETS, OUT / "assets", dirs_exist_ok=True)
    build_landing()
    dossiers = load_dossiers()
    for slug, meta, body, subs in dossiers:
        build_dossier(slug, meta, body, subs)
        print(f"built research/{slug}")
    build_research_index(dossiers)
    print(f"Done → {OUT}")


if __name__ == "__main__":
    main()
