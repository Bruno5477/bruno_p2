from pathlib import Path
p=Path('..\main.py')
for i,l in enumerate(p.read_text().splitlines(),start=1):
    print(f"{i:03}: {l}")
