#!/usr/bin/env python3
"""Generate hero-loop videos for the landing page with Google's Veo API.

Usage:
  GEMINI_API_KEY=... python3 scripts/generate_veo.py            # all prompts
  GEMINI_API_KEY=... python3 scripts/generate_veo.py --only 0   # one prompt
  python3 scripts/generate_veo.py --model veo-2.0-generate-001  # older model

Output lands in site/assets/media/loop-N.mp4; the site build picks up any
.mp4 there automatically (and cycles through multiple). Re-run the build
after generating. The key also reads from .env (GEMINI_API_KEY=...).

Veo generation is billed per second of video — check current pricing before
generating many clips.
"""
import argparse, json, os, pathlib, sys, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
MEDIA = ROOT / "site" / "assets" / "media"
API = "https://generativelanguage.googleapis.com/v1beta"

# Cinematic, abstract, brand-adjacent — no text, no people, loop-friendly.
PROMPTS = [
    "Slow aerial drift over a vast dark ocean surface at dusk, deep blue-black "
    "water with faint silver light tracing the swells, heavy 35mm film grain, "
    "moody cinematic color grade, no text, no people, seamless slow movement",

    "Extreme slow motion of deep ocean water seen from below the surface, "
    "shafts of pale light falling through darkness, particles suspended in the "
    "water column, near-monochrome navy palette, cinematic film grain, no text",

    "Macro shot of ink dispersing in dark water, slow billowing clouds of "
    "deep blue and black, high contrast studio lighting, film grain, elegant "
    "and abstract, no text, no people",
]


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


def generate(prompt, index, model, key):
    print(f"[{index}] requesting: {prompt[:60]}…")
    op = request(f"{API}/models/{model}:predictLongRunning", key, {
        "instances": [{"prompt": prompt}],
        "parameters": {"aspectRatio": "9:16"},
    })
    name = op["name"]
    while not op.get("done"):
        time.sleep(15)
        op = request(f"{API}/{name}", key)
        print(f"[{index}] …still generating")
    if "error" in op:
        sys.exit(f"[{index}] generation failed: {op['error']}")

    uri = find_video_uri(op)
    out = MEDIA / f"loop-{index}.mp4"
    MEDIA.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(uri, headers={"x-goog-api-key": key})
    with urllib.request.urlopen(req) as resp:
        out.write_bytes(resp.read())
    print(f"[{index}] saved {out} ({out.stat().st_size // 1024} KB)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="veo-3.0-generate-001")
    ap.add_argument("--only", type=int, help="generate a single prompt by index")
    args = ap.parse_args()

    key = api_key()
    todo = [(i, p) for i, p in enumerate(PROMPTS) if args.only in (None, i)]
    for i, prompt in todo:
        generate(prompt, i, args.model, key)
    print("Done. Rebuild the site to pick up new clips: python3 site/build.py")


if __name__ == "__main__":
    main()
