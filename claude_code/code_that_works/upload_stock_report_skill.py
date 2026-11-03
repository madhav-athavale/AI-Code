import anthropic

client = anthropic.Anthropic()

skill = client.beta.skills.create(
    display_title="Stock Report",
    files=[("stock-report/SKILL.md", open("/Users/madhavathavale/workspace/MacMiniM2/AI-Code/claude_code/code_that_works/stock-report/SKILL.md", "rb"))],
    betas=["skills-2025-10-02"],
)

print(skill.id)  # e.g. skill_01AbCdEfGhIjKlMnOpQrStUv — save this

