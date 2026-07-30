#!/usr/bin/env python3
"""
serve.py - local companion server for a CV Coach dashboard.

A saved dashboard is a static file, and a browser cannot run local scripts from
a page opened off disk (a hard security boundary). This tiny standard-library
server serves one version folder over 127.0.0.1 and exposes a render endpoint,
so the dashboard's "generate PDF" buttons can actually run render_pdf.py for a
given CV format. No third-party dependencies.

Usage:
    python3 serve.py <version-dir> [--port N] [--no-open]

Routes:
    GET /                                  -> the dashboard HTML for this identity
    GET /<file>                            -> static files inside <version-dir>
    GET /api/status                        -> JSON: which artifacts exist
    GET /api/render?type=ats|designed|all  -> runs render_pdf.py, returns JSON

Security:
    * binds to 127.0.0.1 only (never reachable off the machine);
    * render is restricted to this folder's known CV files;
    * the `type` parameter is validated against a fixed allowlist;
    * static serving is confined to <version-dir> (SimpleHTTPRequestHandler).
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
RENDER_PDF = os.path.join(HERE, "render_pdf.py")


def identity_for(version_dir):
    """Derive the identity prefix from the '<identity>-dashboard.html' file."""
    matches = glob.glob(os.path.join(version_dir, "*-dashboard.html"))
    if not matches:
        return None
    return os.path.basename(matches[0])[: -len("-dashboard.html")]


def artifact_map(version_dir, identity):
    """Map logical names to filenames for this identity."""
    return {
        "md": f"{identity}.md",
        "ats_html": f"{identity}-ats.html",
        "designed_html": f"{identity}.html",
        "ats_pdf": f"{identity}-ats.pdf",
        "designed_pdf": f"{identity}.pdf",
        "dashboard": f"{identity}-dashboard.html",
    }


def status(version_dir, identity):
    amap = artifact_map(version_dir, identity)
    return {k: os.path.isfile(os.path.join(version_dir, v)) for k, v in amap.items()}


def render(version_dir, identity, kind):
    """Run render_pdf.py for one format. Returns (ok, detail-dict)."""
    amap = artifact_map(version_dir, identity)
    jobs = []
    if kind in ("ats", "all"):
        jobs.append(("ats", amap["ats_html"], amap["ats_pdf"], False))
    if kind in ("designed", "all"):
        jobs.append(("designed", amap["designed_html"], amap["designed_pdf"], True))
    results = {}
    for name, html, pdf, fancy in jobs:
        html_path = os.path.join(version_dir, html)
        pdf_path = os.path.join(version_dir, pdf)
        if not os.path.isfile(html_path):
            results[name] = {"ok": False, "error": f"source HTML missing: {html}"}
            continue
        cmd = [sys.executable, RENDER_PDF, html_path, pdf_path]
        if fancy:
            cmd.append("--fancy")
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            ok = proc.returncode == 0 and os.path.isfile(pdf_path)
            results[name] = {"ok": ok, "file": pdf, "detail": (proc.stdout or proc.stderr).strip()}
        except subprocess.TimeoutExpired:
            results[name] = {"ok": False, "error": "render timed out"}
    return all(r.get("ok") for r in results.values()), results


def make_handler(version_dir, identity):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=version_dir, **kw)

        def log_message(self, *a):
            pass  # quiet

        def _json(self, code, payload):
            body = json.dumps(payload).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            parsed = urlparse(self.path)
            route = parsed.path
            if route == "/api/status":
                return self._json(200, status(version_dir, identity))
            if route == "/api/render":
                qs = parse_qs(parsed.query)
                kind = (qs.get("type", [""])[0]).lower()
                if kind not in ("ats", "designed", "all"):
                    return self._json(400, {"ok": False, "error": "type must be ats, designed, or all"})
                ok, results = render(version_dir, identity, kind)
                return self._json(200 if ok else 500, {"ok": ok, "results": results,
                                                        "status": status(version_dir, identity)})
            if route == "/" or route == "":
                self.path = f"/{identity}-dashboard.html"
            return super().do_GET()

    return Handler


def main():
    ap = argparse.ArgumentParser(description="Serve a CV Coach dashboard with a live render endpoint.")
    ap.add_argument("version_dir", help="the versions/<identity> folder to serve")
    ap.add_argument("--port", type=int, default=0, help="port (default: an OS-assigned free port)")
    ap.add_argument("--no-open", action="store_true", help="do not open a browser")
    args = ap.parse_args()

    version_dir = os.path.abspath(args.version_dir)
    if not os.path.isdir(version_dir):
        print(f"serve: not a directory: {version_dir}", file=sys.stderr)
        return 1
    identity = identity_for(version_dir)
    if not identity:
        print(f"serve: no *-dashboard.html found in {version_dir}", file=sys.stderr)
        return 1

    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(version_dir, identity))
    port = httpd.server_address[1]
    url = f"http://127.0.0.1:{port}/{identity}-dashboard.html"
    # flush so a backgrounded launcher can read the URL immediately (stdout is
    # block-buffered when redirected to a file).
    print(f"serve: CV Coach dashboard for '{identity}' at {url}", flush=True)
    print("serve: press Ctrl+C to stop.", flush=True)
    if not args.no_open:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nserve: stopped.")
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
