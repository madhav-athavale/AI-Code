# Sample code to encode and decode jwt token. Secret Key needs to be 32 bytes as per recommendations

import jwt
from datetime import datetime, timedelta

secret = "XXXXXX"

payload = {"user_id": 123, "exp": datetime.utcnow() + timedelta(minutes=30)}

token = jwt.encode(payload, secret, algorithm="HS256")
print("JWT:", token)

decoded = jwt.decode(token, secret, algorithms=["HS256"])
print("Decoded:", decoded)