from requests import get

from plume.auth import auth
from plume.get_token import base_url, get_token, partner_id

client_id = auth.get("client_id")
client_secret = auth.get("client_secret")

headers = get_token(client_id, client_secret)
response = get(f"{base_url}/partners/{partner_id}/customers/count", headers=headers)
print(response)
# print("Customer count:", response.json().get("count"))
