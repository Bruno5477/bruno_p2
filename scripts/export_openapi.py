import json
import sys
from pathlib import Path

# ensure project root is on sys.path so `from main import app` works
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from main import app

openapi = app.openapi()
out = ROOT / "openapi.json"
out.write_text(json.dumps(openapi, indent=2, ensure_ascii=False), encoding="utf-8")
print("Wrote", out)
