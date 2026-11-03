# fix_skill.py
content = open("claude_code/code_that_works/stock-report/SKILL.md", encoding="utf-8-sig").read().lstrip()
open("claude_code/code_that_works/stock-report/SKILL.md", "w", encoding="utf-8", newline="\n").write(content)