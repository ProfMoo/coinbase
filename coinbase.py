import json, hmac, hashlib, time, requests
from requests.auth import AuthBase

# Before implementation, set environmental variables with the names API_KEY and API_SECRET

# Create custom authentication for Coinbase API
class CoinbaseWalletAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = timestamp + request.method + request.path_url + (request.body or '')
        signature = hmac.new(bytes(self.secret_key, 'latin-1'), bytes(message, 'latin-1'), hashlib.sha256).hexdigest()

        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
        })
        return request

api_url = 'https://api.coinbase.com/v2/'
auth = CoinbaseWalletAuth(API_KEY, API_SECRET)

# Get current user
# r = requests.get(api_url + 'user', auth=auth)

total_onramp = 0
total_cost_to_buy = 0
total_purchases = 0

query_params = ""
TYPE_OF_CRYPTO = "ETH"

quit = False
while(quit is not True):
    r = requests.get(api_url + 'accounts/d41efe25-c5bf-58e7-a7bc-4ca48f16b273/transactions' + query_params, auth=auth)

    data = json.loads(r.text)

    current_eth_amount = 0

    for transaction in data["data"]:
        if transaction["type"] == "buy" and transaction["amount"]["currency"] == TYPE_OF_CRYPTO:
            print("{} bought: {}".format(TYPE_OF_CRYPTO, transaction["amount"]["amount"]))
            total_onramp += float(transaction["amount"]["amount"])
            total_cost_to_buy += float(transaction["native_amount"]["amount"])
            total_purchases += 1


    # print("next: ", data["pagination"]["next_uri"])
    if data["pagination"]["next_uri"] is not None:
        query_params = "?starting_after=" + data["pagination"]["next_starting_after"]
    else:
        quit = True

    # json_formatted_str = json.dumps(r.json(), indent=2)
    # print(json_formatted_str)

print("=" * 50)
print("Total {} bought: {}".format(TYPE_OF_CRYPTO, total_onramp))
print("Total spent to get {}: {}".format(TYPE_OF_CRYPTO, total_cost_to_buy))
print("Total purchases of {}: {}".format(TYPE_OF_CRYPTO, total_purchases))
