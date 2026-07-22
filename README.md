# A22 — a22vc.com

The public home of A22: a film-studio-style landing page with the portfolio, and **A22 Research** — living dossiers compiled from working research projects. A running loop of intelligence across themes.

## Project layout

```
data/portfolio.json      portfolio companies shown on the landing page
content/<slug>/          one research dossier per topic (markdown + frontmatter)
site/build.py            the only build entry point → site/public/
site/templates/          landing.html, page.html ({{TOKEN}} substitution)
site/assets/css/         landing.css (cinematic dark), site.css (editorial reading pages)
site/assets/media/       hero loop videos (*.mp4, picked up automatically)
scripts/generate_veo.py  generates hero videos via Google's Veo API
push.py                  ingest research → content/ → rebuild → Supabase sync
supabase/                schema migrations (dossiers + push_log tables)
.github/workflows/       push to main → build with pandoc → deploy to GitHub Pages
```

## Everyday commands

```bash
# publish research (copies markdown in, rebuilds, syncs Supabase)
python3 push.py <file-or-dir> --slug X --main page.md --title "…" --theme "…" --verdict "…"

# build + preview locally
python3 site/build.py
cd site/public && python3 -m http.server 8426

# generate hero videos (needs GEMINI_API_KEY in env or .env)
python3 scripts/generate_veo.py

# deploy = git push (GitHub Actions does the rest)
git push
```

## Conventions

- **Edit sources, never `site/public/`** — it's generated and gitignored.
- Landing content (portfolio, videos) is **data**, not markup: edit `data/portfolio.json` or drop `.mp4`s in `site/assets/media/`; the build does the rest.
- Dossier metadata (title/theme/verdict/status/dates) lives in `content/<slug>/index.md` frontmatter and is owned by `push.py` — re-push to update it.
- Research URLs: `a22vc.com/research/<slug>/`.

## Infrastructure

- **Domain:** a22vc.com → GitHub Pages (HTTPS enforced), repo `aryanvc/a22-research`
- **Supabase:** project `a22-research` — `dossiers` (corpus index) + `push_log` (push history); public read via RLS, writes via service key in gitignored `.env`
