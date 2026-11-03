import pdfplumber
import pandas as pd
import re

with pdfplumber.open("/Users/madhavathavale/Downloads/medicare_claims.pdf") as pdf:
    text = "\n".join(page.extract_text() or "" for page in pdf.pages)

# Clean noise
text = re.sub(r"https?://\S+", "", text)  # remove URLs
text = re.sub(r"\d{1,2}/\d{1,2}/\d{2,4},.*", "", text)  # remove timestamps

# Split claims
claims = re.split(r"Medical claim", text)

results = []

for claim in claims:
    claim = claim.strip()
    if not claim:
        continue

    # Normalize spacing
    claim = re.sub(r"\n+", "\n", claim)

    # Extract fields (robust to line breaks)
    date_match = re.search(r"Date of service\s*\n?\s*([0-9/]+)", claim)
    provider_match = re.search(r"Provider\s*\n?\s*([A-Za-z .]+)", claim)
    amount_match = re.search(r"\$\s*([0-9]+\.[0-9]+)", claim)

    results.append({
        "Date of Service": date_match.group(1) if date_match else "",
        "Provider": provider_match.group(1).strip() if provider_match else "",
        "Amount": float(amount_match.group(1)) if amount_match else None
    })

df = pd.DataFrame(results)

# Remove empty rows (if any)
df = df[df["Date of Service"] != ""]

df.to_excel("output.xlsx", index=False)

print(df)