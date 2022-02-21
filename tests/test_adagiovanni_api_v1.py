import requests

APP_API_V1_BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
s = requests.Session()


def test_place_order():
    data = {"customer_name": "Foo", "sandwich": "Ham and Cheese"}
    r = s.post(f"{APP_API_V1_BASE_URL}/order", json=data, headers=HEADERS)
    print(r.status_code, r.text)


if __name__ == "__main__":
    test_place_order()
