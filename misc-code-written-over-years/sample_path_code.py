from pathlib import Path

p = Path("/Users/madhavathavale/workspace/MacMiniM2/AI-Code/my_code")
# print(p.exists())
# print(p.is_file())
# print(p.is_dir())
p = p.resolve()
print(p)
p =  p /  "sample_path_code.py"
# p = p.resolve()
# print(p.resolve())
# print(p.name)
# print(p.stem)
# print(Path.cwd())
# print(p)
print(p.read_text())
print(Path("my_code"))
print(p.is_dir())
for f in p.iterdir():
    print(f)