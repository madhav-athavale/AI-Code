import anthropic

from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env file
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
        
client = anthropic.Anthropic()

skills = client.beta.skills.list(source="anthropic")
for skill in skills.data:
    print(skill.id, skill.display_title)