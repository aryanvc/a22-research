#!/usr/bin/env python3
"""Generate per-company portfolio footage with Google's Veo API.

Usage:
  GEMINI_API_KEY=... python3 scripts/generate_veo.py --company micro1   # one
  GEMINI_API_KEY=... python3 scripts/generate_veo.py                    # all
  python3 scripts/generate_veo.py --model veo-2.0-generate-001          # older model

Clips land in site/assets/media/portfolio/<id>.mp4 — the build swaps them in
for that company's placeholder automatically. Rebuild after generating.
The key also reads from .env (GEMINI_API_KEY=...).

Veo bills per second of generated video — check pricing before a full run;
start with one company as a test.

Prompts are deliberately abstract motifs (no text, no logos, no factual
claims about the companies) — mood reels, not documentaries.
"""
import argparse, json, os, pathlib, sys, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
MEDIA = ROOT / "site" / "assets" / "media" / "portfolio"
API = "https://generativelanguage.googleapis.com/v1beta"

STYLE = ("cinematic, heavy 35mm film grain, dark moody color grade, slow "
         "camera movement, no text, no logos, no people, loop-friendly")

PROMPTS = {
    "micro1":          f"Macro glide across glowing circuitry in darkness, points of warm light in shallow depth of field, {STYLE}",
    "vatn-systems":    f"Deep underwater darkness, a sleek shadow gliding through blue-black water with faint shafts of light, {STYLE}",
    "ironstead":       f"Slow pan across dark forged metal surfaces, drifting ember sparks, industrial chiaroscuro lighting, {STYLE}",
    "valar-atomics":   f"Abstract radiant energy core pulsing in darkness, deep amber and blue light blooms, slow drift, {STYLE}",
    "terpli":          f"Macro botanical silhouettes in drifting mist, deep green-black palette, backlit edges, {STYLE}",
    "gelato-festival": f"Extreme slow motion of soft cream folding and swirling against black, macro studio lighting, {STYLE}",
    "drumroll":        f"Warm glaze cascading in extreme slow motion against a black background, macro studio shot, {STYLE}",
}


def api_key():
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        envfile = ROOT / ".env"
        if envfile.exists():
            for line in envfile.read_text().splitlines():
                if line.startswith(("GEMINI_API_KEY=", "GOOGLE_API_KEY=")):
                    key = line.split("=", 1)[1].strip()
    if not key:
        sys.exit("No API key. Set GEMINI_API_KEY in the environment or in .env "
                 "(get one at https://aistudio.google.com/apikey)")
    return key


def request(url, key, payload=None):
    req = urllib.request.Request(
        url, method="POST" if payload is not None else "GET",
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def find_video_uri(operation):
    """The video URI's exact location in the response has shifted across Veo
    versions — check the known paths."""
    resp = operation.get("response", {})
    for path in (
        lambda r: r["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"],
        lambda r: r["generatedVideos"][0]["video"]["uri"],
        lambda r: r["videos"][0]["uri"],
    ):
        try:
            return path(resp)
        except (KeyError, IndexError, TypeError):
            continue
    sys.exit(f"Could not locate video URI in response:\n{json.dumps(operation, indent=2)[:2000]}")


def generate(company, prompt, model, key):
    print(f"[{company}] requesting: {prompt[:70]}…")
    op = request(f"{API}/models/{model}:predictLongRunning", key, {
        "instances": [{"prompt": prompt}],
        "parameters": {"aspectRatio": "16:9"},
    })
    name = op["name"]
    while not op.get("done"):
        time.sleep(15)
        op = request(f"{API}/{name}", key)
        print(f"[{company}] …still generating")
    if "error" in op:
        sys.exit(f"[{company}] generation failed: {op['error']}")

    uri = find_video_uri(op)
    MEDIA.mkdir(parents=True, exist_ok=True)
    out = MEDIA / f"{company}.mp4"
    req = urllib.request.Request(uri, headers={"x-goog-api-key": key})
    with urllib.request.urlopen(req) as resp:
        out.write_bytes(resp.read())
    print(f"[{company}] saved {out} ({out.stat().st_size // 1024} KB)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="veo-3.0-generate-001")
    ap.add_argument("--company", choices=sorted(PROMPTS), help="generate one company's clip")
    args = ap.parse_args()

    key = api_key()
    todo = {args.company: PROMPTS[args.company]} if args.company else PROMPTS
    for company, prompt in todo.items():
        generate(company, prompt, args.model, key)
    print("Done. Rebuild to pick up new clips: python3 site/build.py")


if __name__ == "__main__":
    main()
