#!/usr/bin/env python3
"""
render_pdf.py - robust, self-terminating HTML to PDF renderer for CV Coach.

Renders an HTML file to PDF with headless Chrome in a way that can NEVER hang
the pipeline. Hand-rolled `chrome --headless --print-to-pdf` calls are fragile:
Chrome frequently writes the PDF and then fails to exit (it waits on remote web
fonts, or conflicts with the user's already-running Chrome profile), so the
shell call blocks with no output until a watchdog kills the whole run. This
helper removes every one of those failure modes:

  * a fresh throwaway --user-data-dir, so it never touches or conflicts with
    the user's running Chrome;
  * --virtual-time-budget for pages that load remote web fonts (--fancy), so
    Chrome does not wait on the network indefinitely;
  * a hard subprocess timeout that kills the whole Chrome process group. If
    Chrome already wrote the PDF before being killed (the common case), the run
    still succeeds because the file is on disk.

Usage:
    python3 render_pdf.py <input.html> <output.pdf> [--fancy] [--timeout N]

    --fancy      the page loads remote web fonts (the designed CV template);
                 adds a bounded virtual-time budget and waits for compositor
                 stages so the fonts render before the snapshot.
    --timeout N  hard cap in seconds (default 60). On timeout, if the PDF is on
                 disk and non-trivial, exit 0; otherwise exit 1.

Exit codes: 0 = PDF produced, 1 = failed (no usable PDF / no Chrome found).

Set CHROME=/path/to/chrome to override browser auto-detection.
"""
import argparse
import os
import shutil
import signal
import subprocess
import sys
import tempfile

CHROME_CANDIDATES = [
    os.environ.get("CHROME"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "microsoft-edge",
]


def find_chrome():
    for c in CHROME_CANDIDATES:
        if not c:
            continue
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c
        found = shutil.which(c)
        if found:
            return found
    return None


def main():
    ap = argparse.ArgumentParser(description="Render an HTML file to PDF (self-terminating).")
    ap.add_argument("input", help="input HTML file")
    ap.add_argument("output", help="output PDF file")
    ap.add_argument("--fancy", action="store_true",
                    help="page loads remote web fonts (the designed CV template)")
    ap.add_argument("--timeout", type=int, default=60, help="hard cap in seconds (default 60)")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print(f"render_pdf: input not found: {args.input}", file=sys.stderr)
        return 1

    chrome = find_chrome()
    if not chrome:
        print("render_pdf: no Chrome/Chromium/Edge found. Set CHROME=/path/to/chrome.",
              file=sys.stderr)
        return 1

    out = os.path.abspath(args.output)
    if os.path.exists(out):
        try:
            os.remove(out)
        except OSError:
            pass

    profile = tempfile.mkdtemp(prefix="cvcoach-chrome-")
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-first-run",
        "--no-pdf-header-footer",
        f"--user-data-dir={profile}",
        f"--print-to-pdf={out}",
    ]
    if args.fancy:
        # The designed template loads remote web fonts; bound the wait so a slow
        # or unreachable font host cannot hang the render.
        cmd += ["--virtual-time-budget=10000", "--run-all-compositor-stages-before-draw"]
    cmd.append("file://" + os.path.abspath(args.input))

    # Headless Chrome reliably WRITES the PDF within a couple of seconds but then
    # frequently fails to exit (a known quirk, even with --headless=new). So we do
    # not wait for Chrome to finish: we poll for the output file, and the instant it
    # exists and its size is stable (done writing), we kill Chrome and return. The
    # --timeout is only a hard backstop for the pathological case where no file ever
    # appears, so this can never hang the pipeline.
    import time

    def kill(proc):
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        try:
            proc.wait(timeout=10)
        except Exception:
            pass

    timed_out = False
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            start_new_session=True)
    deadline = time.time() + args.timeout
    last_size = -1
    try:
        while True:
            if os.path.isfile(out):
                size = os.path.getsize(out)
                # Two consecutive equal, non-trivial readings => finished writing.
                if size > 1000 and size == last_size:
                    break
                last_size = size
            if proc.poll() is not None:  # Chrome exited on its own
                break
            if time.time() >= deadline:
                timed_out = True
                break
            time.sleep(0.25)
    finally:
        kill(proc)
        shutil.rmtree(profile, ignore_errors=True)

    produced = os.path.isfile(out) and os.path.getsize(out) > 1000
    if produced:
        note = " (chrome was killed after the timeout, but the PDF was already written)" if timed_out else ""
        print(f"render_pdf: wrote {out} ({os.path.getsize(out)} bytes){note}")
        return 0

    print("render_pdf: FAILED to produce " + out + (" (timed out with no output)" if timed_out else ""),
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
