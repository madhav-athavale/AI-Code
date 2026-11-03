import anthropic

client = anthropic.Anthropic()

client.beta.skills.versions.create(
    skill_id="skill_01BnQuxLoHK1zeHQKPaspKFo",
    files=[("stock-report/SKILL.md", open("/Users/madhavathavale/workspace/MacMiniM2/AI-Code/claude_code/code_that_works/stock-report/SKILL.md", "rb"))],
    betas=["skills-2025-10-02"],
)