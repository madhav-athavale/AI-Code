
from aws_secrets import AWSSecrets
secret = AWSSecrets()
print(secret.get_secret('TEST_API_KEY'))