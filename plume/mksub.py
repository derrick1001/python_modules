from requests import post

from plume.auth import auth
from plume.get_token import base_url, get_token, partner_id

# NOTE: Claim node using customerId and locationId
# /Customers/{id}/locations/{locationId}/nodes

# NOTE: Create new customer
# /Customers/register

# NOTE: Set ssid and psk for location
# /Customers/{id}/locations/{locationId}/wifiNetwork

# NOTE: AccountID, Name, Email, SN should be input data


HEADERS = get_token(auth.get("client_id"), auth.get("client_secret"))


def set_ssid(claim_wrapper):
    def ssid_wrapper():
        wifi = input("SSID: ")
        wifi_pass = input("WPA2: ")
        loc, cust_id = claim_wrapper()
        data = {
            "id": cust_id,
            "locationId": loc,
            "ssid": wifi,
            "encryptionKey": wifi_pass,
        }
        response = post(
            f"{base_url}/Customers/{cust_id}/locations/{loc}/wifiNetwork",
            headers=HEADERS,
            data=data,
        )
        return response.status_code

    return ssid_wrapper


def claim_node(create_sub):
    @set_ssid
    def claim_wrapper():
        sn = input("Serial number: ")
        loc, cust_id = create_sub()
        data = {
            "id": cust_id,
            "locationId": loc,
            "serialNumber": sn,
        }
        response = post(
            f"{base_url}/Customers/{cust_id}/locations/{loc}/nodes",
            headers=HEADERS,
            data=data,
        )
        return loc, cust_id

    return claim_wrapper


@claim_node
def create_sub():
    acct = input("Account number: ")
    name = input("Customer name: ")
    em = input("Email: ")
    data = {
        "accountId": acct,
        "name": name,
        "email": em,
        "partnerId": f"{partner_id}",
    }
    response = post(
        f"{base_url}/Customers/register",
        headers=HEADERS,
        data=data,
    )
    loc = response.json().get("locationId")
    cust_id = response.json().get("id")
    return loc, cust_id


if __name__ == "__main__":
    x = create_sub()
    if x == 200:
        print("\nCustomer created successfully!!")
