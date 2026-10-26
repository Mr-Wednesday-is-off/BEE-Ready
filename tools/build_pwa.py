"""Turn the Bee Ready artifact HTML into the PWA's index.html.

Usage: python3 build_pwa.py <artifact.html> <repo_dir>
"""
import re, sys, pathlib

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[2])

# 1. Wrapper line added by the artifact host: keep its safe-area style, drop the rest
m = re.match(r'<!doctype html><html><head>.*?<style>(.*?)</style></head><body>\n', src, re.S)
assert m, "wrapper not found"
wrapper_css = m.group(1)
body = src[m.end():]

# 2. Drop title + Google Fonts links (fonts are bundled for offline use)
body = body.replace("<title>Bee Ready</title>\n", "", 1)
body = re.sub(r'<link rel="preconnect"[^>]*>\n', "", body)
body = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>\n', "", body)
assert "googleapis" not in body

# 3. Move the main stylesheet into <head>
sm = re.search(r'<style>\n/\* Layout:.*?</style>\n', body, re.S)
assert sm, "main style not found"
main_css = sm.group(0)
body = body[:sm.start()] + body[sm.end():]

# 4. Strip closing tags; we add our own
body = body.rstrip()
assert body.endswith("</body></html>")
body = body[: -len("</body></html>")].rstrip()

fonts = []
for fam, w, style, f in [
    ("Baloo 2", 600, "normal", "baloo-2-latin-600-normal.woff2"),
    ("Baloo 2", 700, "normal", "baloo-2-latin-700-normal.woff2"),
    ("Baloo 2", 800, "normal", "baloo-2-latin-800-normal.woff2"),
    ("Atkinson Hyperlegible", 400, "normal", "atkinson-hyperlegible-latin-400-normal.woff2"),
    ("Atkinson Hyperlegible", 700, "normal", "atkinson-hyperlegible-latin-700-normal.woff2"),
    ("Atkinson Hyperlegible", 400, "italic", "atkinson-hyperlegible-latin-400-italic.woff2"),
]:
    fonts.append(f'@font-face{{font-family:"{fam}";font-style:{style};font-weight:{w};font-display:swap;src:url(fonts/{f}) format("woff2")}}')

head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Bee Ready</title>
<meta name="description" content="Spelling bee practice: hear the word, spell it, fill the hive. Works offline.">
<meta name="theme-color" content="#FFF7E0" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#17120A" media="(prefers-color-scheme: dark)">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Bee Ready">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<style>{wrapper_css}</style>
<style>
{chr(10).join(fonts)}
</style>
{main_css}</head>
<body>
"""

sw = """
<script>
// Offline support: cache the app so it opens with no signal
if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost")) {
  addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
}
</script>
</body>
</html>
"""

(out / "index.html").write_text(head + body + "\n" + sw, encoding="utf-8")
print("wrote", out / "index.html", len(head + body + sw), "chars")
