import anthropic

client = anthropic.Anthropic()

skills = client.beta.skills.list(betas=["skills-2025-10-02"])
for s in skills.data:
    print(s.id, s.display_title)
    
