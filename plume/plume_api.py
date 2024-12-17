from oauthlib.oauth2 import BackendApplicationClient
from requests import get
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

partner_id = "65f06dae3fca80000ad38331"
base_url = "https://piranha-gamma.prod.us-west-2.aws.plumenet.io/api/"
client_id = "0oa1ecnda3copttLE358"
client_secret = "+LpoG8SumIMxgUMCrWJNaLYTsAKYmjoG"
scope = ["partnerId:65f06dae3fca80000ad38331 role:partnerIdAdmin"]

auth = HTTPBasicAuth(client_id, client_secret)
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(
    token_url="https://external.sso.plume.com/oauth2/ausc034rgdEZKz75I357/v1/token",
    scope=scope,
    auth=auth,
)

bearer = token.get("access_token")
headers = {"Authorization": f"Bearer {bearer}"}
response = get(f"{base_url}/partners/{partner_id}/customers/count", headers=headers)
print("Customer count:", response.json().get("count"))
