"""Validate the prebuilt production assets used by Render's static hosting."""
from pathlib import Path
import hashlib
import json
import sys

root = Path(__file__).resolve().parent
dist = root / "dist"
manifest_path = root / "build-manifest.json"
if "--refresh" in sys.argv:
    manifest = {
        str(path.relative_to(dist)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(dist.rglob("*")) if path.is_file()
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
else:
    manifest = json.loads(manifest_path.read_text())
    for relative, expected in manifest.items():
        path = dist / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit(f"Missing or changed production asset: {relative}. Rebuild before deploying.")
    if "index.html" not in manifest:
        raise SystemExit("The production build is missing index.html.")
print(f"Verified {len(manifest)} production assets. LWS Digital is ready for static hosting.")
