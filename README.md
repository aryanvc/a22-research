# A22 Research

The compiled layer. Working research happens in segment projects (`~/ocean-infrastructure`, etc.); when a piece is high-quality, it gets pushed here as a **dossier** — a living page we add to and track over time. A running loop of intelligence across themes.

## Structure

- `content/<slug>/` — one dossier per topic: `index.md` (with frontmatter) + supporting pages
- `site/build.py` — builds the static site to `site/public/`
- `push.py` — the ingest command

## Pushing research

```bash
python3 push.py <file-or-dir> --slug ocean-datacenters --main ocean-datacenters.md \
  --title "Ocean Datacenters" --theme "Ocean Infrastructure" \
  --verdict "Physics proven, business unproven."
```

Re-pushing the same slug updates the dossier in place and bumps its `updated` date. Everything about what/how we capture will evolve — frontmatter and site structure are deliberately minimal so they can change without migrations.

## Viewing

```bash
python3 site/build.py
cd site/public && python3 -m http.server 8426
```

Static output — deployable to any host (Vercel/Netlify/Pages) when this goes public.

## Infrastructure

- **Domain:** a22vc.com (GitHub Pages custom domain)
- **Deploy:** push to `main` → GitHub Actions builds (pandoc + `site/build.py`) → GitHub Pages
- **Supabase:** project `a22-research` (ref in `.env`, not committed). `push.py` upserts each dossier into `dossiers` and appends to `push_log` — the queryable index of the corpus and its history. Public read via RLS; writes via service key.
