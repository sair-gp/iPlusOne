import requests

base_url = "http://127.0.0.1:8765/"


def request(action, **params):
    return {"action": action, "params": params, "version": 6}


def invoke(action, **params):
    try:
        payload = request(action, **params)
        response = requests.post(base_url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["result"]
    except requests.exceptions.RequestException as e:
        print("Request failed: ", e)


# result = invoke("deckNames")
# print(result)
