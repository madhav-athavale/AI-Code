import httpx

response = httpx.get(
    "https://www.googleapis.com/customsearch/v1",
    params={
        "key": "I",
        "cx":  "",
        "q":   "test",
        "num": 1
    }
)
print(response.status_code)
print(response.json())