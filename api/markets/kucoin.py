import base64
import datetime
import hashlib
import hmac

from requests import Session, Timeout, TooManyRedirects


class KuCoin:
    def __init__(self, api_key, api_passphrase, api_secret):
        self.base_url = "https://api.kucoin.com"
        self.passphrase = api_passphrase
        self.secret = api_secret
        self.key = api_key

        self.connected = self.test_connection()

    def test_connection(self) -> bool:
        endpoint = "/api/v1/accounts"
        req = self.contact_api(endpoint, "GET")
        if req.status_code == 200:
            print("Successful authentication to KuCoin established")
            return True
        else:
            print(f"Error authenticating with KuCoin API, http status:{req.status_code} Error Contents:{req.text}")
            return False

    def contact_api(self, endpoint: str, http_operation: str, body: dict = None):
        headers = self.get_headers(endpoint, http_operation, body)

        session = Session()
        session.headers.update(headers)

        try:
            if http_operation == "POST":
                response = session.post(f"{self.base_url}{endpoint}", params=body)
            else:
                if http_operation != "GET": print(f"Unknown HTTP operation {http_operation}, assuming GET.")
                response = session.get(f"{self.base_url}{endpoint}")

            return response

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

    def get_headers(self, endpoint: str, http_operation: str, body: dict = None):
        url = f"{self.base_url}{endpoint}"
        now = int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1e3)

        str_to_sign = f"{str(now)}{http_operation}{endpoint}"

        if body:
            str_to_sign = f"{str_to_sign}{body}"

        signature = base64.b64encode(
            hmac.new(self.secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
        passphrase = base64.b64encode(
            hmac.new(self.secret.encode('utf-8'), self.passphrase.encode('utf-8'), hashlib.sha256).digest())
        headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": self.key,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2"
        }
        if http_operation == "POST":
            headers["Content-Type"] = "application/json"
        return headers
