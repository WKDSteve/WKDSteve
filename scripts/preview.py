"""Look at the profile assets the way GitHub shows them: SVGs in <img> on a dark page, 880px wide.

    python scripts/preview.py [port]      # then open http://127.0.0.1:8765/preview.html

A local file:// URL is often blocked (browser panes, GitHub's own camo proxy never sees it), so this
serves the repository folder over http. preview.html is git-ignored. Stop with Ctrl+C.
Animations start on load: reload to watch the intro again.
"""
import http.server, socketserver, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
ORDER = ["hero", "family", "native", "stats", "footer"]


def main():
    imgs = "".join(f'<img src="assets/{n}.svg" width="100%"><br><br>' for n in ORDER if (ROOT / "assets" / f"{n}.svg").exists())
    (ROOT / "preview.html").write_text(
        '<!doctype html><meta charset="utf-8"><title>profile preview</title>'
        '<body style="margin:0;background:#0d1117"><div style="max-width:880px;margin:0 auto;padding:16px">'
        + imgs + "</div></body>", encoding="utf-8")
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=str(ROOT), **k)
    with socketserver.TCPServer(("127.0.0.1", PORT), handler) as srv:
        print(f"http://127.0.0.1:{PORT}/preview.html")
        srv.serve_forever()


if __name__ == "__main__":
    main()
