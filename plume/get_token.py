from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

# These variables are static and wont change
base_url = "https://piranha-gamma.prod.us-west-2.aws.plumenet.io/api/"
partner_id = "65f06dae3fca80000ad38331"
scope = ["partnerId:65f06dae3fca80000ad38331 role:partnerIdAdmin"]


def get_token(client_id: str, client_secret: str):
    # This sets up the parameters for getting an access token from auth server
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
    return headers
