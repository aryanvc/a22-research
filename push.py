#!/usr/bin/env python3
"""Push a research bundle into A22 Research and rebuild the site.

Usage:
  python3 push.py SRC --slug ocean-datacenters --title "Ocean Datacenters" \
      --theme "Ocean Infrastructure" --verdict "one-liner" [--main page.md]

SRC is a markdown file or a directory of markdown files. The main file becomes
the dossier's index.md; every other .md in the tree comes along as a subpage
(relative paths preserved). Re-pushing a slug overwrites its files and bumps
the `updated` date; `created`, and any flag you omit, are preserved.
"""
import argparse, datetime, json, pathlib, shutil, subprocess, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
CONTENT = ROOT / "content"


def load_env():
    env = {}
    envfile = ROOT / ".env"
    if envfile.exists():
        for line in envfile.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def sync_supabase(meta, slug, page_count):
    env = load_env()
    url, key = env.get("SUPABASE_URL"), env.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        print("supabase: no credentials in .env, skipping sync")
        return
    headers = {"apikey": key, "Authorization": f"Bearer {key}",
               "Content-Type": "application/json"}
    row = {"slug": slug, "title": meta["title"], "theme": meta["theme"],
           "verdict": meta["verdict"], "status": meta["status"],
           "created": meta["created"], "updated": meta["updated"],
           "page_count": page_count,
           "synced_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    req = urllib.request.Request(
        f"{url}/rest/v1/dossiers?on_conflict=slug", method="POST",
        data=json.dumps(row).encode(),
        headers={**headers, "Prefer": "resolution=merge-duplicates"})
    urllib.request.urlopen(req)
    req = urllib.request.Request(
        f"{url}/rest/v1/push_log", method="POST",
        data=json.dumps({"slug": slug, "page_count": page_count}).encode(),
        headers=headers)
    urllib.request.urlopen(req)
    print(f"supabase: synced dossier '{slug}' + logged push")


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--title")
    ap.add_argument("--theme")
    ap.add_argument("--verdict")
    ap.add_argument("--status", default=None, help="living | archived")
    ap.add_argument("--main", default=None, help="main md file when SRC is a dir")
    args = ap.parse_args()

    src = pathlib.Path(args.src).expanduser().resolve()
    if not src.exists():
        sys.exit(f"source not found: {src}")

    dest = CONTENT / args.slug
    today = datetime.date.today().isoformat()

    # preserve prior frontmatter on re-push
    prior = {}
    idx = dest / "index.md"
    if idx.exists():
        prior, _ = parse_frontmatter(idx.read_text())

    if src.is_dir():
        mds = sorted(p for p in src.rglob("*.md"))
        if not mds:
            sys.exit("no .md files in source dir")
        if args.main:
            main_path = src / args.main
            if not main_path.exists():
                sys.exit(f"--main {args.main} not found in {src}")
        elif (src / "index.md").exists():
            main_path = src / "index.md"
        elif len(mds) == 1:
            main_path = mds[0]
        else:
            sys.exit("multiple .md files: specify --main")
    else:
        mds, main_path = [src], src

    dest.mkdir(parents=True, exist_ok=True)
    copied = []
    for p in mds:
        rel = p.relative_to(src) if src.is_dir() else pathlib.Path(p.name)
        rel = pathlib.Path("index.md") if p == main_path else rel
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, out)
        copied.append(rel)

    # main page keeps NO frontmatter from source; A22 owns the metadata
    raw = (dest / "index.md").read_text()
    _, body = parse_frontmatter(raw)
    meta = {
        "title": args.title or prior.get("title") or args.slug.replace("-", " ").title(),
        "theme": args.theme or prior.get("theme", ""),
        "verdict": args.verdict or prior.get("verdict", ""),
        "status": args.status or prior.get("status", "living"),
        "created": prior.get("created", today),
        "updated": today,
    }
    fm = "\n".join(f"{k}: {v}" for k, v in meta.items())
    (dest / "index.md").write_text(f"---\n{fm}\n---\n\n{body}")

    # rewrite main-page links that pointed at the old main filename
    if main_path.name != "index.md":
        for rel in copied:
            f = dest / rel
            f.write_text(f.read_text().replace(main_path.name, "index.md"))

    print(f"pushed {len(copied)} page(s) → content/{args.slug}/")
    subprocess.run([sys.executable, str(ROOT / "site" / "build.py")], check=True)
    sync_supabase(meta, args.slug, len(copied))
    print("reminder: research serves from the private app — run "
          "~/nexus/frontend/scripts/sync-research.sh && npx vercel --prod "
          "(from ~/nexus/frontend) to publish it there")


if __name__ == "__main__":
    main()
