
import anthropic

from dotenv import load_dotenv
import os
class Anthropic_downloads:

    def setup(self):
       

        load_dotenv()  # Loads from .env file

        ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
        client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var
        os.makedirs("outputs", exist_ok=True)
        return client

    def downloads_using_scope(self):
        files = client.beta.files.list(
        scope_id="sesn_01Q38imR7qt9i4PsfR9D3Wfv",
        betas=["managed-agents-2026-04-01"],
        )
        for file in files:
            print(file.id, file.filename)
            content = client.beta.files.download(file.id)
            local_path = os.path.join("outputs", file.filename)
            content.write_to_file(local_path)
            print(f"Downloaded: {local_path}")
                
        
    def download_single_file(self,client):
        file_id = "file_01VLcXcpiB7zLoP1rXFZPtp8"
        file_name = "revenue_summary.xlsx"
        content = client.beta.files.download(file_id)
        local_path = os.path.join("outputs",file_name)
        content.write_to_file(local_path) 

if __name__ == "__main__":
    sol = Anthropic_downloads()
    client = sol.setup()
    sol.download_single_file(client)